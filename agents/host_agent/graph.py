from __future__ import annotations

import asyncio
import re
from collections.abc import AsyncIterator
from typing import Optional

import httpx

from a2a.client import A2AClient
from a2a.types import Artifact, DataPart, Message, TaskEvent, TaskRequest, TaskState, TextPart
from agents.host_agent.router import RouteDecision, route_query
from storage.task_store import create_session, finalize_session
from tools.document_match_query import extract_invoice_no, get_invoice_linked_refs


def _extract_data(artifact: Optional[Artifact]) -> dict:
    if artifact is None:
        return {}
    for part in artifact.parts:
        if getattr(part, "type", "") == "data":
            return part.data
    return {}


def _split_at_summary(text: str) -> tuple[str, str]:
    """Split an agent summary into (body, summary_sentence).

    'body'  — descriptive text before 'In summary:'.
    'summary_sentence' — the 'In summary: …' sentence (first line only).

    Everything after the summary sentence (table-heading lines, markdown tables)
    is discarded because the CLI now renders raw DB tables instead.
    """
    match = re.search(r"\bIn summary:[^\n]*", text)
    if match:
        body = text[:match.start()].strip()
        summary_sentence = match.group(0).strip()
        return body, summary_sentence
    return text.strip(), ""

def _build_summary(data: dict) -> str:
    """Produce a concise human-readable summary from an agent's result."""
    qtype = data.get("query_type", "unknown")

    if qtype == "multi_agent_analysis":
        sections: list[str] = []
        bullets: list[str] = []
        for agent_name, agent_data in data.get("agent_results", {}).items():
            raw = agent_data.get("summary", "No summary available.")
            body, sentence = _split_at_summary(raw)
            if body:
                sections.append(f"{agent_name}:\n{body}")
            if sentence:
                content = re.sub(r"^In summary:\s*", "", sentence)
                bullets.append(f"- {agent_name}: {content}")
        combined = "\n\n".join(sections)
        if bullets:
            combined += "\n\nIn summary:\n" + "\n".join(bullets)
        return combined or "No analysis results were returned."

    return data.get("summary", "No summary available.")


def _augment_query_with_refs(query: str, route: RouteDecision) -> str:
    """When the query contains an invoice number and routes to PO/DO agents,
    resolve the invoice's linked PO and DO numbers from the invoice DB and
    append them as context so the sub-agents can build accurate SQL.

    PO/DO agents have no access to the invoice database, so without this they
    cannot resolve an invoice number to a matching PO or DO record.
    """
    invoice_no = extract_invoice_no(query)
    if not invoice_no:
        return query
    agents = set(route["target_agents"])
    needs_po = "PurchaseOrderAgent" in agents
    needs_do = "DeliveryOrderAgent" in agents
    if not (needs_po or needs_do):
        return query
    refs = get_invoice_linked_refs(invoice_no)
    additions: list[str] = []
    if needs_po and refs["po_numbers"]:
        additions.append(
            f"Invoice {invoice_no} is linked to PO number(s): {', '.join(refs['po_numbers'])}."
        )
    if needs_do and refs["do_numbers"]:
        additions.append(
            f"Invoice {invoice_no} is linked to DO number(s): {', '.join(refs['do_numbers'])}."
        )
    if not additions:
        return query
    return query + " [Context: " + " ".join(additions) + "]"


async def _send_to_agent(
    client: A2AClient,
    session_id: str,
    query: str,
    target_agent: str,
    route: RouteDecision,
) -> dict:
    route_data = {
        "route_task_type": route["task_type"],
        "route_target_agents": route["target_agents"],
        "route_reason": route["reason"],
    }

    req = TaskRequest(
        session_id=session_id,
        source_agent="HostAgent",
        target_agent=target_agent,
        message=Message(
            role="user",
            parts=[
                TextPart(text=query),
                DataPart(data=route_data),
            ],
        ),
    )
    resp = await client.send(req)
    return _extract_data(resp.artifact)


async def _dispatch_route(client: A2AClient, session_id: str, query: str, route: RouteDecision) -> dict:
    target_agents = route["target_agents"]
    augmented_query = _augment_query_with_refs(query, route)
    results = await asyncio.gather(
        *(
            _send_to_agent(client, session_id, augmented_query, agent_name, route)
            for agent_name in target_agents
        )
    )
    by_agent = dict(zip(target_agents, results))

    if len(target_agents) == 1:
        data = results[0]
        data["route"] = route
        return data

    return {
        "query_type": "multi_agent_analysis",
        "query": query,
        "agent_results": by_agent,
        "route": route,
    }


async def run_host_graph(task_request: TaskRequest) -> AsyncIterator[TaskEvent]:
    query = " ".join(
        part.text for part in task_request.message.parts
        if getattr(part, "type", "") == "text"
    )
    create_session(task_request.session_id, query)

    yield TaskEvent(
        task_id=task_request.task_id,
        state=TaskState.WORKING,
        message="HostAgent: routing request",
    )

    # Each sub-agent makes 2 LLM calls (~10-20 s each) plus a DB query.
    # Use a fast connect timeout but no read cutoff so parallel multi-agent
    # queries don't get killed mid-flight.
    _sub_agent_timeout = httpx.Timeout(connect=10.0, read=None, write=30.0, pool=10.0)
    client = A2AClient(timeout=_sub_agent_timeout)
    try:
        route = route_query(query)
        yield TaskEvent(
            task_id=task_request.task_id,
            state=TaskState.WORKING,
            message=(
                "HostAgent: route="
                f"{route['task_type']} targets={','.join(route['target_agents'])}"
            ),
        )
        invoice_data = await _dispatch_route(client, task_request.session_id, query, route)

        yield TaskEvent(
            task_id=task_request.task_id,
            state=TaskState.WORKING,
            message="HostAgent: received invoice analysis, composing report",
        )

        summary = _build_summary(invoice_data)
        report = {
            "query": query,
            "query_type": invoice_data.get("query_type"),
            "summary": summary,
            "raw_data": invoice_data,
        }

        finalize_session(task_request.session_id, report)

        from a2a.types import Artifact, DataPart
        artifact = Artifact(
            name="invoice_report",
            parts=[DataPart(data=report)],
        )

        yield TaskEvent(
            task_id=task_request.task_id,
            state=TaskState.COMPLETED,
            message="HostAgent: completed",
            artifact=artifact,
        )

    except Exception as exc:
        err_msg = str(exc) or type(exc).__name__
        yield TaskEvent(
            task_id=task_request.task_id,
            state=TaskState.FAILED,
            message=f"HostAgent error: {err_msg}",
        )
    finally:
        await client.close()
