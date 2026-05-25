from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Optional

from a2a.client import A2AClient
from a2a.types import Artifact, DataPart, Message, TaskEvent, TaskRequest, TaskState, TextPart
from storage.task_store import create_session, finalize_session


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

    if qtype == "long_pending_invoices":
        count = data.get("count", 0)
        shown = data.get("shown", count)
        threshold = data.get("threshold_days", "?")
        lines = [
            f"Found {count} invoice(s) pending for more than {threshold} days.\n"
        ]
        for inv in data.get("invoices", [])[:10]:
            supplier = inv.get("supplier_name") or "Unknown supplier"
            days = inv.get("days_pending", "?")
            status = inv.get("invoice_status", "?")
            amount = inv.get("total_amount")
            currency = inv.get("currency_code", "")
            amt_str = f"{currency} {float(amount):,.2f}" if amount else "N/A"
            lines.append(
                f"  • {inv.get('invoice_no', 'N/A')} | {supplier} | "
                f"{days} days | {status} | {amt_str}"
            )
        remaining = count - 10
        if remaining > 0:
            lines.append(f"  ... and {remaining} more.")
        if count == 0:
            conclusion = f"\nIn summary: No invoices have been pending for more than {threshold} days."
        else:
            conclusion = f"\nIn summary: There are {count} invoice(s) overdue by more than {threshold} days that require attention."
        lines.append(conclusion)
        return "\n".join(lines)

    if qtype == "supplier_frequency":
        top_n = data.get("top_n", "?")
        suppliers = data.get("suppliers", [])
        lines = [f"Top {top_n} suppliers by invoice count:\n"]
        for i, s in enumerate(suppliers, 1):
            name = s.get("supplier_name", "Unknown")
            cnt = s.get("invoice_count", 0)
            lines.append(f"  {i:2}. {name} — {cnt} invoice(s)")
        if suppliers:
            top = suppliers[0]
            conclusion = (
                f"\nIn summary: {top.get('supplier_name', 'Unknown')} is the most frequent submitter "
                f"with {top.get('invoice_count', 0)} invoice(s)."
            )
            lines.append(conclusion)
        return "\n".join(lines)

    if qtype == "supplier_amount":
        order = data.get("order", "highest")
        top_n = data.get("top_n", "?")
        suppliers = data.get("suppliers", [])
        lines = [f"Top {top_n} suppliers by {order} total invoice amount:\n"]
        for i, s in enumerate(suppliers, 1):
            name = s.get("supplier_name", "Unknown")
            total = s.get("total_amount")
            avg = s.get("avg_amount")
            currency = s.get("currency", "")
            total_str = f"{currency} {float(total):,.2f}" if total else "N/A"
            avg_str = f"{currency} {float(avg):,.2f}" if avg else "N/A"
            lines.append(
                f"  {i:2}. {name} — total: {total_str}, avg: {avg_str}"
            )
        # Natural-language summary sentence
        if suppliers:
            def _fmt_short(s: dict) -> str:
                total = s.get("total_amount")
                currency = s.get("currency", "")
                if total is None:
                    return s.get("supplier_name", "Unknown")
                val = float(total)
                if val >= 1_000_000_000:
                    short = f"{val / 1_000_000_000:.1f}B"
                elif val >= 1_000_000:
                    short = f"{val / 1_000_000:.1f}M"
                else:
                    short = f"{val:,.0f}"
                return f"{s.get('supplier_name', 'Unknown')} ({currency} {short})"
            named = [_fmt_short(s) for s in suppliers[:3]]
            if len(named) == 1:
                conclusion = f"In summary: {named[0]} has the {order} invoice amount."
            elif len(named) == 2:
                conclusion = f"In summary: {named[0]} leads, followed by {named[1]}."
            else:
                conclusion = (
                    f"In summary: {named[0]} leads, followed by "
                    + ", ".join(named[1:-1])
                    + f", and {named[-1]}."
                )
            lines.append(f"\n{conclusion}")
        return "\n".join(lines)

    if qtype == "all":
        parts = []
        if "long_pending_invoices" in data:
            parts.append(_build_summary(data["long_pending_invoices"]))
        if "supplier_frequency" in data:
            parts.append(_build_summary(data["supplier_frequency"]))
        if "supplier_amount_highest" in data:
            parts.append(_build_summary(data["supplier_amount_highest"]))
        return "\n\n".join(parts)

    return data.get("summary", "No summary available.")


async def run_host_graph(task_request: TaskRequest) -> AsyncIterator[TaskEvent]:
    query = " ".join(
        part.text for part in task_request.message.parts
        if getattr(part, "type", "") == "text"
    )
    create_session(task_request.session_id, query)

    yield TaskEvent(
        task_id=task_request.task_id,
        state=TaskState.WORKING,
        message="HostAgent: dispatching to InvoiceAgent",
    )

    client = A2AClient()
    try:
        inv_req = TaskRequest(
            session_id=task_request.session_id,
            source_agent="HostAgent",
            target_agent="InvoiceAgent",
            message=Message(role="user", parts=[TextPart(text=query)]),
        )
        inv_resp = await client.send(inv_req)
        invoice_data = _extract_data(inv_resp.artifact)

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
        yield TaskEvent(
            task_id=task_request.task_id,
            state=TaskState.FAILED,
            message=f"HostAgent error: {exc}",
        )
    finally:
        await client.close()
