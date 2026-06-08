from __future__ import annotations

import json
import re

from a2a.types import Artifact, DataPart, Message, Part
from agents.purchase_order_agent.prompts import (
    PO_SCHEMA_CONTEXT,
    SQL_SYSTEM_PROMPT,
    SUMMARY_SYSTEM_PROMPT,
    TASK_CLASSIFIER_PROMPT_TEMPLATE,
)
from tools.document_match_query import extract_invoice_no, query_invoice_po_match
from tools.gemini_sql import generate_content, generate_sql, get_client, summarize_results
from tools.sql_query import execute_safe_sql, purchase_db_params


def _route_task_type(parts: list[Part]) -> str | None:
    for part in parts:
        if getattr(part, "type", "") == "data":
            task_type = part.data.get("route_task_type")
            return str(task_type) if task_type else None
    return None


def _extract_json(text: str) -> dict:
    stripped = text.strip()
    stripped = re.sub(r"^```(?:json)?\s*\n?", "", stripped, flags=re.IGNORECASE)
    stripped = re.sub(r"\n?```\s*$", "", stripped)
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", stripped, flags=re.DOTALL)
        if not match:
            raise ValueError(f"PO classifier did not return JSON: {text}") from None
        return json.loads(match.group(0))


def _classify_task(query: str) -> str:
    prompt = TASK_CLASSIFIER_PROMPT_TEMPLATE.format(query=query)
    payload = _extract_json(generate_content(get_client(), prompt))
    task_type = str(payload.get("task_type") or "")
    if task_type not in {"invoice_po_matching", "purchase_order_analysis"}:
        raise ValueError(f"Invalid PO task_type: {task_type}")
    return task_type


def run_purchase_order_graph(message: Message) -> Artifact:
    query_text = " ".join(
        part.text for part in message.parts if getattr(part, "type", "") == "text"
    )

    try:
        routed_task = _route_task_type(message.parts)
        if routed_task == "document_matching":
            task_type = "invoice_po_matching"
        elif routed_task in {"purchase_order_analysis", "purchase_and_delivery_order_analysis"}:
            task_type = "purchase_order_analysis"
        else:
            task_type = None
        task_type = task_type or _classify_task(query_text)

        if task_type == "invoice_po_matching":
            invoice_no = extract_invoice_no(query_text)
            if not invoice_no:
                raise ValueError("No invoice number found in the question.")
            data = query_invoice_po_match(invoice_no)
            data["query"] = query_text
        else:
            client = get_client()
            sql = generate_sql(client, query_text, PO_SCHEMA_CONTEXT, SQL_SYSTEM_PROMPT)
            result = execute_safe_sql(sql, purchase_db_params())
            summary = summarize_results(client, query_text, sql, result, SUMMARY_SYSTEM_PROMPT)
            data = {
                "query_type": "purchase_order_analysis",
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
            "query_type": "purchase_order_error",
            "query": query_text,
            "error": str(exc),
            "summary": f"Could not complete the purchase order request: {exc}",
        }

    return Artifact(name="purchase_order_result", parts=[DataPart(data=data)])
