from __future__ import annotations

"""InvoiceAgent graph: invoice analytics with Gemini text-to-SQL."""

from a2a.types import Artifact, DataPart, Message
from agents.invoice_agent.prompts import SCHEMA_CONTEXT, SQL_SYSTEM_PROMPT, SUMMARY_SYSTEM_PROMPT
from tools.gemini_sql import generate_sql, get_client, summarize_results
from tools.sql_query import execute_safe_sql

def run_invoice_graph(message: Message) -> Artifact:
    query_text = " ".join(
        part.text for part in message.parts if getattr(part, "type", "") == "text"
    )

    try:
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
