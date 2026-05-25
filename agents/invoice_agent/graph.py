from __future__ import annotations

"""InvoiceAgent graph: uses Google Gemini for text-to-SQL and result summarization."""

import json
import os
import re

from google import genai
from google.genai import errors as genai_errors

from a2a.types import Artifact, DataPart, Message
from agents.invoice_agent.prompts import SCHEMA_CONTEXT, SQL_SYSTEM_PROMPT, SUMMARY_SYSTEM_PROMPT
from tools.sql_query import execute_safe_sql

# ---------------------------------------------------------------------------
# Gemini helpers
# ---------------------------------------------------------------------------

def _get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is not set. "
            "Add it to your .env file."
        )
    return genai.Client(api_key=api_key)


# Models tried in order when a transient/availability error occurs.
_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-1.5-flash",
]

# HTTP status codes that warrant trying the next model.
_RETRYABLE_CODES = {404, 429, 500, 503}


def _is_retryable(exc: Exception) -> bool:
    if isinstance(exc, genai_errors.APIError):
        return exc.code in _RETRYABLE_CODES
    msg = str(exc)
    return any(str(c) in msg for c in _RETRYABLE_CODES)


def _generate_content(client: genai.Client, prompt: str) -> str:
    """Try each model in _MODELS; return text from the first one that responds."""
    last_exc: Exception | None = None
    for model in _MODELS:
        try:
            response = client.models.generate_content(model=model, contents=prompt)
            return response.text.strip()
        except Exception as exc:  # noqa: BLE001
            if _is_retryable(exc):
                last_exc = exc
                continue
            raise
    raise RuntimeError(f"All models unavailable. Last error: {last_exc}") from last_exc


def _generate_sql(client: genai.Client, question: str) -> str:
    """Ask Gemini to produce a safe SELECT query for the given question."""
    prompt = (
        f"{SQL_SYSTEM_PROMPT}\n\n"
        f"Database schema:\n{SCHEMA_CONTEXT}\n\n"
        f"User question: {question}\n\n"
        "Return ONLY the SQL statement. No explanation, no markdown, no code fences."
    )
    sql = _generate_content(client, prompt)
    # Strip markdown code fences in case Gemini wraps the SQL anyway.
    sql = re.sub(r"^```(?:sql)?\s*\n?", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"\n?```\s*$", "", sql)
    return sql.strip()


def _summarize_results(
    client: genai.Client,
    question: str,
    sql: str,
    result: dict,
) -> str:
    """Ask Gemini to produce a plain-English answer from the query results."""
    rows_preview = result["rows"][:20]
    shown = result["count"]
    total = result["total_count"]
    count_note = (
        f"{shown} rows shown (limited by query)"
        if total > shown
        else f"{shown} rows"
    )
    prompt = (
        f"{SUMMARY_SYSTEM_PROMPT}\n\n"
        f"User question: {question}\n\n"
        f"SQL executed:\n{sql}\n\n"
        f"Query results ({count_note}; TRUE TOTAL matching rows = {total}):\n"
        f"{json.dumps(rows_preview, indent=2, default=str)}\n\n"
        "Write a concise answer. Use the TRUE TOTAL figure when describing how many "
        "records match. Include key figures and names. "
        'End with a single sentence starting "In summary:".'
    )
    return _generate_content(client, prompt)


# ---------------------------------------------------------------------------
# Main graph entry point
# ---------------------------------------------------------------------------

def run_invoice_graph(message: Message) -> Artifact:
    query_text = " ".join(
        part.text for part in message.parts if getattr(part, "type", "") == "text"
    )

    try:
        client = _get_client()

        # Step 1: natural language → SQL
        sql = _generate_sql(client, query_text)

        # Step 2: execute the SQL safely against the read-only DB
        result = execute_safe_sql(sql)

        # Step 3: SQL results → natural language answer
        summary = _summarize_results(client, query_text, sql, result)

        data = {
            "query_type": "llm_query",
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

