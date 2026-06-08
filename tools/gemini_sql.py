from __future__ import annotations

"""Gemini helpers for text-to-SQL agents."""

import json
import os
import re
from typing import Any

from google import genai
from google.genai import errors as genai_errors

_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-1.5-flash",
]

_RETRYABLE_CODES = {404, 429, 500, 503}


def get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is not set. "
            "Add it to your .env file."
        )
    return genai.Client(api_key=api_key)


def _is_retryable(exc: Exception) -> bool:
    if isinstance(exc, genai_errors.APIError):
        return exc.code in _RETRYABLE_CODES
    msg = str(exc)
    return any(str(code) in msg for code in _RETRYABLE_CODES)


def generate_content(client: genai.Client, prompt: str) -> str:
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


def generate_sql(
    client: genai.Client,
    question: str,
    schema_context: str,
    sql_system_prompt: str,
) -> str:
    prompt = (
        f"{sql_system_prompt}\n\n"
        f"Database schema:\n{schema_context}\n\n"
        f"User question: {question}\n\n"
        "Return ONLY the SQL statement. No explanation, no markdown, no code fences."
    )
    sql = generate_content(client, prompt)
    sql = re.sub(r"^```(?:sql)?\s*\n?", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"\n?```\s*$", "", sql)
    return sql.strip()


def summarize_results(
    client: genai.Client,
    question: str,
    sql: str,
    result: dict[str, Any],
    summary_system_prompt: str,
) -> str:
    rows_preview = result["rows"][:20]
    shown = result["count"]
    total = result["total_count"]
    count_note = (
        f"{shown} rows shown (limited by query)"
        if total > shown
        else f"{shown} rows"
    )
    prompt = (
        f"{summary_system_prompt}\n\n"
        f"User question: {question}\n\n"
        f"SQL executed:\n{sql}\n\n"
        f"Query results ({count_note}; TRUE TOTAL matching rows = {total}):\n"
        f"{json.dumps(rows_preview, indent=2, default=str)}\n\n"
        "Write a concise answer. Use the TRUE TOTAL figure when describing how many "
        "records match. Include key figures and names. "
        'End with a single sentence starting "In summary:".'
    )
    return generate_content(client, prompt)
