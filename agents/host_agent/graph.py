from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from typing import Optional

import httpx

from a2a.client import A2AClient
from a2a.types import Artifact, DataPart, Message, TaskEvent, TaskRequest, TaskState, TextPart
from agents.host_agent.router import RouteDecision, route_query
from storage.task_store import create_session, finalize_session
from tools.document_match_query import (
    extract_do_no,
    extract_invoice_no,
    extract_po_no,
    get_do_linked_refs,
    get_invoice_linked_refs,
    get_po_linked_refs,
)


def _extract_data(artifact: Optional[Artifact]) -> dict:
    if artifact is None:
        return {}
    for part in artifact.parts:
        if getattr(part, "type", "") == "data":
            return part.data
    return {}


def _build_summary(data: dict) -> str:
    """Produce a concise human-readable summary from an agent's result."""
    qtype = data.get("query_type", "unknown")

    if qtype == "multi_agent_analysis":
        return _synthesize_multi_agent_summary(data)

    return data.get("summary", "No summary available.")


_MULTI_AGENT_SYNTHESIS_PROMPT = """
You are HostAgent, reconciling findings from multiple specialist agents into ONE
unified conclusion for the user. Each agent answers from its own database, so their
statements may overlap or even contradict. Your job is to cross-check them and give a
single coherent analysis — NOT three separate summaries.

Guidelines:
- Produce one overall analysis covering Invoice, PO, and DO together.
- Explicitly reconcile any contradictions (e.g. one agent says no DO exists, another
  finds DOs). State which is correct or call out the discrepancy as a data issue.
- Highlight whether the three entities match correctly; flag mismatches or missing links.
- Linkage is defined ONLY by invoice_item UUIDs. If an invoice item has no po_uuid/do_uuid,
  there is no matched PO/DO — ignore any DOs/POs an agent found via PO numbers or po_list,
  and state that no PO/DO is linked rather than listing those unrelated records.
- Do NOT label sections by agent name. Do NOT repeat each agent's summary verbatim.
- Never display UUID values; refer to records by their global numbers instead.
- Keep it concise. End with a single sentence starting "In summary:".
""".strip()


def _synthesize_multi_agent_summary(data: dict) -> str:
    """Combine per-agent results into a single cross-agent conclusion via the LLM."""
    query = data.get("query", "")
    agent_bodies: list[str] = []
    for agent_name, agent_data in data.get("agent_results", {}).items():
        raw = agent_data.get("summary", "No summary available.")
        agent_bodies.append(f"{agent_name} findings:\n{raw}")
    if not agent_bodies:
        return "No analysis results were returned."

    combined_findings = "\n\n".join(agent_bodies)
    try:
        from tools.gemini_sql import generate_content, get_client

        client = get_client()
        prompt = (
            f"{_MULTI_AGENT_SYNTHESIS_PROMPT}\n\n"
            f"User question: {query}\n\n"
            f"Agent findings:\n{combined_findings}\n\n"
            "Write the unified analysis now."
        )
        return generate_content(client, prompt)
    except Exception:  # noqa: BLE001
        # Fallback: concatenated agent bodies if synthesis is unavailable.
        return combined_findings


def _augment_query_with_refs(query: str, route: RouteDecision) -> str:
    """Resolve cross-entity links through invoice_item UUIDs and append them as context
    so the sub-agents can build accurate SQL.

    invoice_item is the single pivot for Invoice ↔ PO ↔ DO matching. Whatever entity the
    user names — an invoice, a PO, or a DO — its identifier is first resolved to a UUID,
    and the other two entities are discovered purely through invoice_item.po_uuid /
    invoice_item.do_uuid. Plain numbers and global numbers are NEVER used to establish the
    link; they only seed the initial UUID lookup. PO/DO agents have no access to the
    invoice database, so this enrichment lets them target the correct records.
    """
    agents = set(route["target_agents"])
    needs_po = "PurchaseOrderAgent" in agents
    needs_do = "DeliveryOrderAgent" in agents
    needs_inv = "InvoiceAgent" in agents
    additions: list[str] = []

    # Resolve entity precedence: a PO/DO identifier (e.g. POGLOBAL..., DOGLOBAL...) can
    # also match the invoice token pattern, so check PO/DO first and only fall back to
    # invoice-as-entry when neither is present.
    po_no = extract_po_no(query)
    do_no = extract_do_no(query)
    invoice_no = extract_invoice_no(query)

    if invoice_no and not po_no and not do_no and (needs_po or needs_do):
        # Entry = invoice → resolve linked PO/DO UUIDs via invoice_item.
        refs = get_invoice_linked_refs(invoice_no)
        if needs_po:
            if refs.get("po_uuids"):
                additions.append(
                    f"Invoice {invoice_no} links via invoice_item.po_uuid to purchase_order.uuid: "
                    f"{', '.join(refs['po_uuids'])}."
                )
            else:
                additions.append(
                    f"Invoice {invoice_no} has NO PO linked via invoice_item.po_uuid; "
                    "report that no related PO exists and do not infer one from PO numbers."
                )
        if needs_do:
            if refs.get("do_uuids"):
                additions.append(
                    f"Invoice {invoice_no} links via invoice_item.do_uuid to delivery_order.uuid: "
                    f"{', '.join(refs['do_uuids'])}."
                )
            else:
                additions.append(
                    f"Invoice {invoice_no} has NO DO linked via invoice_item.do_uuid; "
                    "report that no related DO exists and do not infer DOs from PO numbers or po_list."
                )
        if additions:
            return query + " [Context: " + " ".join(additions) + "]"

    po_no = extract_po_no(query)
    if po_no and (needs_inv or needs_do):
        # Entry = PO → resolve PO uuid, pivot through invoice_item.po_uuid.
        refs = get_po_linked_refs(po_no)
        if refs.get("po_uuids"):
            additions.append(f"PO {po_no} resolves to purchase_order.uuid {', '.join(refs['po_uuids'])}.")
        if needs_inv:
            if refs.get("invoice_numbers"):
                additions.append(
                    f"Via invoice_item.po_uuid it links to invoice(s) {', '.join(refs['invoice_numbers'])} "
                    f"(invoice.uuid: {', '.join(refs.get('invoice_uuids') or ['n/a'])}; "
                    f"invoice_item.invoice_id: {', '.join(refs.get('invoice_ids') or ['n/a'])}). "
                    "Retrieve the invoice by matching invoice.uuid or invoice.id."
                )
            else:
                additions.append("No invoice is linked via invoice_item.po_uuid; report none.")
        if needs_do:
            if refs.get("do_uuids"):
                additions.append(
                    f"Via invoice_item it links to delivery_order.uuid: {', '.join(refs['do_uuids'])}."
                )
            else:
                additions.append(
                    "No DO is linked via invoice_item.do_uuid; report no related DO and do not "
                    "infer DOs from PO numbers or po_list."
                )
        if additions:
            return query + " [Context: " + " ".join(additions) + "]"

    if do_no and (needs_inv or needs_po):
        # Entry = DO → resolve DO uuid, pivot through invoice_item.do_uuid.
        refs = get_do_linked_refs(do_no)
        if refs.get("do_uuids"):
            additions.append(f"DO {do_no} resolves to delivery_order.uuid {', '.join(refs['do_uuids'])}.")
        if needs_inv:
            if refs.get("invoice_numbers"):
                additions.append(
                    f"Via invoice_item.do_uuid it links to invoice(s) {', '.join(refs['invoice_numbers'])} "
                    f"(invoice.uuid: {', '.join(refs.get('invoice_uuids') or ['n/a'])}; "
                    f"invoice_item.invoice_id: {', '.join(refs.get('invoice_ids') or ['n/a'])}). "
                    "Retrieve the invoice by matching invoice.uuid or invoice.id."
                )
            else:
                additions.append("No invoice is linked via invoice_item.do_uuid; report none.")
        if needs_po:
            if refs.get("po_uuids"):
                additions.append(
                    f"Via invoice_item it links to purchase_order.uuid: {', '.join(refs['po_uuids'])}."
                )
            else:
                additions.append("No PO is linked via invoice_item.po_uuid; report none.")
        if additions:
            return query + " [Context: " + " ".join(additions) + "]"

    return query


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
