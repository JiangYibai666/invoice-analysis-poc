from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from typing import Optional

from a2a.client import A2AClient
from a2a.types import Artifact, DataPart, Message, TaskEvent, TaskRequest, TaskState, TextPart
from agents.host_agent.router import RouteDecision, route_query
from storage.task_store import create_session, finalize_session
from tools.document_match_query import (
    extract_invoice_no,
    extract_requested_limit,
    list_invoice_numbers_for_matching,
)


def _extract_data(artifact: Optional[Artifact]) -> dict:
    if artifact is None:
        return {}
    for part in artifact.parts:
        if getattr(part, "type", "") == "data":
            return part.data
    return {}


def _build_summary(data: dict) -> str:
    """Produce a concise human-readable summary from InvoiceAgent's result."""
    qtype = data.get("query_type", "unknown")

    if qtype == "document_matching":
        invoice_numbers = data.get("invoice_numbers") or []
        invoice_no = data.get("invoice_no")
        po_match = data.get("po_match", {})
        do_match = data.get("do_match", {})
        if invoice_no:
            lines = [f"Document matching result for invoice {invoice_no}:\n"]
        elif invoice_numbers:
            lines = [f"Document matching result for {len(invoice_numbers)} invoice(s):\n"]
        else:
            lines = ["Document matching result:\n"]

        if po_match:
            lines.append(f"PO check: {po_match.get('summary', 'No PO result available.')}")
        if do_match:
            lines.append(f"DO check: {do_match.get('summary', 'No DO result available.')}")

        po_ok = po_match.get("matched") is True if po_match else None
        do_ok = do_match.get("matched") is True if do_match else None
        scope = "all checked invoices" if invoice_numbers else "this invoice"
        review_scope = "all checked invoices are" if invoice_numbers else "this invoice is"
        if po_ok is True and do_ok is True:
            conclusion = f"In summary: Two-way and three-way document matching passed for {scope}."
        elif po_ok is True and do_ok is None:
            conclusion = f"In summary: Invoice-to-PO matching passed for {scope}."
        elif do_ok is True and po_ok is None:
            conclusion = f"In summary: Invoice-to-DO matching passed for {scope}."
        elif po_ok is True:
            conclusion = "In summary: Invoice-to-PO matching passed, but Invoice-to-DO matching needs review."
        elif do_ok is True:
            conclusion = "In summary: Invoice-to-DO matching passed, but Invoice-to-PO matching needs review."
        else:
            conclusion = f"In summary: Document matching needs review before {review_scope} treated as matched."
        lines.append(f"\n{conclusion}")
        return "\n".join(lines)

    if qtype == "multi_agent_analysis":
        parts = []
        for agent_name, agent_data in data.get("agent_results", {}).items():
            summary = agent_data.get("summary", "No summary available.")
            parts.append(f"{agent_name}: {summary}")
        return "\n\n".join(parts) or "No analysis results were returned."

    return data.get("summary", "No summary available.")


def _document_matching_context(query: str, route: RouteDecision) -> dict:
    if route["task_type"] != "document_matching" or extract_invoice_no(query):
        return {}

    limit = extract_requested_limit(query)
    invoice_numbers = list_invoice_numbers_for_matching(limit)
    return {
        "route_missing_invoice_no": True,
        "route_batch_limit": limit,
        "route_invoice_numbers": invoice_numbers,
    }


async def _send_to_agent(
    client: A2AClient,
    session_id: str,
    query: str,
    target_agent: str,
    route: RouteDecision,
    extra_context: dict | None = None,
) -> dict:
    route_data = {
        "route_task_type": route["task_type"],
        "route_target_agents": route["target_agents"],
        "route_reason": route["reason"],
    }
    if extra_context:
        route_data.update(extra_context)

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
    extra_context = _document_matching_context(query, route)
    results = await asyncio.gather(
        *(
            _send_to_agent(client, session_id, query, agent_name, route, extra_context)
            for agent_name in target_agents
        )
    )
    by_agent = dict(zip(target_agents, results))

    if route["task_type"] == "document_matching":
        invoice_numbers = extra_context.get("route_invoice_numbers", [])
        return {
            "query_type": "document_matching",
            "query": query,
            "invoice_no": (
                by_agent.get("PurchaseOrderAgent", {}).get("invoice_no")
                or by_agent.get("DeliveryOrderAgent", {}).get("invoice_no")
                or extract_invoice_no(query)
            ),
            "invoice_numbers": invoice_numbers,
            "missing_invoice_no": bool(extra_context.get("route_missing_invoice_no")),
            "po_match": by_agent.get("PurchaseOrderAgent", {}),
            "do_match": by_agent.get("DeliveryOrderAgent", {}),
            "route": route,
        }

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

    client = A2AClient(timeout=30.0)
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
