from __future__ import annotations

"""InvoiceAgent graph: invoice analytics with Gemini text-to-SQL."""

import re
from typing import Any

from a2a.types import Artifact, DataPart, Message
from agents.invoice_agent.prompts import SCHEMA_CONTEXT, SQL_SYSTEM_PROMPT, SUMMARY_SYSTEM_PROMPT
from tools.gemini_sql import generate_sql, get_client, summarize_results
from tools.sql_query import execute_safe_sql


def _extract_limit(query: str, default: int = 5, maximum: int = 50) -> int:
    patterns = (
        r"\b(?:top|first|list|show)\s+(\d{1,3})\b",
        r"\b(\d{1,3})\s+invoices?\b",
        r"(?:前|最高|最大|列出|显示)\s*(\d{1,3})\s*(?:张|个|条)?",
    )
    for pattern in patterns:
        match = re.search(pattern, query, flags=re.IGNORECASE)
        if match:
            return min(max(1, int(match.group(1))), maximum)
    return min(max(1, int(default)), maximum)


def _is_highest_invoice_amount_query(query: str) -> bool:
    q = query.lower()
    asks_for_invoices = "invoice" in q or "发票" in query
    asks_for_amount = "amount" in q or "total" in q or "金额" in query
    asks_for_highest = any(token in q for token in ("highest", "largest", "top", "biggest", "maximum"))
    return asks_for_invoices and asks_for_amount and asks_for_highest


def _format_amount(row: dict[str, Any]) -> str:
    amount = row.get("total_amount")
    currency = row.get("currency_code") or ""
    if amount is None:
        return "N/A"
    return f"{currency} {float(amount):,.2f}".strip()


def _markdown_table(rows: list[dict[str, Any]]) -> str:
    lines = [
        "| Invoice | Supplier | Buyer | Currency | Total amount | Status |",
        "|---|---|---|---|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row.get('invoice_no') or ''} | "
            f"{row.get('supplier_name') or ''} | "
            f"{row.get('buyer_name') or ''} | "
            f"{row.get('currency_code') or ''} | "
            f"{float(row['total_amount']):,.2f} | "
            f"{row.get('invoice_status') or ''} |"
        )
    return "\n".join(lines)


def _run_highest_invoice_amount_query(query_text: str) -> dict[str, Any]:
    limit = _extract_limit(query_text)
    sql = f"""
        SELECT
            i.invoice_no,
            s.company_name AS supplier_name,
            b.company_name AS buyer_name,
            i.currency_code,
            i.total_amount,
            i.invoice_status
        FROM public.invoice i
        LEFT JOIN public.supplier_information s ON s.id = i.supplier_id
        LEFT JOIN public.buyer_information b ON b.id = i.buyer_id
        WHERE i.total_amount IS NOT NULL
        ORDER BY i.total_amount DESC NULLS LAST
        LIMIT {limit}
    """
    result = execute_safe_sql(sql)
    rows = result["rows"]

    if rows:
        top = rows[0]
        summary = (
            f"Listed the top {len(rows)} invoice(s) by total amount. "
            f"The highest invoice is {top.get('invoice_no')} at {_format_amount(top)}. "
            f"In summary: These are the {len(rows)} highest-value invoices with non-null total amounts.\n"
            f"Here are the top {len(rows)} invoices by amount:\n"
            f"{_markdown_table(rows)}"
        )
    else:
        summary = "No invoices with non-null total amounts were found. In summary: There are no invoice amounts to rank."

    return {
        "query_type": "invoice_analysis",
        "query": query_text,
        "sql": sql.strip(),
        "columns": result["columns"],
        "rows": rows,
        "count": result["count"],
        "total_count": result["total_count"],
        "summary": summary,
        "deterministic": True,
    }


def run_invoice_graph(message: Message) -> Artifact:
    query_text = " ".join(
        part.text for part in message.parts if getattr(part, "type", "") == "text"
    )

    try:
        if _is_highest_invoice_amount_query(query_text):
            data = _run_highest_invoice_amount_query(query_text)
            return Artifact(name="invoice_analysis", parts=[DataPart(data=data)])

        client = get_client()
        sql = generate_sql(client, query_text, SCHEMA_CONTEXT, SQL_SYSTEM_PROMPT)
        result = execute_safe_sql(sql)
        summary = summarize_results(client, query_text, sql, result, SUMMARY_SYSTEM_PROMPT)

        data = {
            "query_type": "invoice_analysis",
            "query": query_text,
            "sql": sql,
            "columns": result["columns"],
            "rows": result["rows"],
            "count": result["count"],
            "total_count": result["total_count"],
            "summary": summary,
        }

    except Exception as exc:  # noqa: BLE001
        data = {
            "query_type": "error",
            "query": query_text,
            "error": str(exc),
            "summary": f"Could not answer the question: {exc}",
        }

    return Artifact(name="invoice_analysis", parts=[DataPart(data=data)])
