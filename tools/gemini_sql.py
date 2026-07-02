from __future__ import annotations

"""Gemini helpers for text-to-SQL agents."""

import json
import os
import re
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors
from google.genai import types as genai_types

_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-1.5-flash",
]

_RETRYABLE_CODES = {404, 429, 500, 503}
_AUTHORIZATION_CODES = {401, 403}
DEFAULT_SUMMARY_PREVIEW_ROWS = 20
MAX_SUMMARY_PREVIEW_ROWS = 200

# Deterministic config: temperature 0 ensures repeated identical questions yield the
# same SQL and summaries, so the same request cannot produce divergent answers.
_DETERMINISTIC_CONFIG = genai_types.GenerateContentConfig(temperature=0.0)


def _dotenv_override() -> bool:
    raw = os.getenv("DOXA_DOTENV_OVERRIDE")
    if raw is None:
        return True
    return raw.lower() not in {"0", "false", "no", "off"}


def get_client() -> genai.Client:
    load_dotenv(override=_dotenv_override())
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


def _friendly_api_error(exc: Exception) -> RuntimeError:
    if isinstance(exc, genai_errors.APIError):
        if exc.code in _AUTHORIZATION_CODES:
            return RuntimeError(
                "Gemini API access was denied. Check GEMINI_API_KEY, the Google "
                "Cloud/AI Studio project attached to that key, API enablement, "
                f"billing/quota status, and model access. Original error: {exc}"
            )
        return RuntimeError(f"Gemini API request failed with status {exc.code}: {exc}")
    return RuntimeError(str(exc) or type(exc).__name__)


def generate_content(client: genai.Client, prompt: str) -> str:
    last_exc: Exception | None = None
    for model in _MODELS:
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=_DETERMINISTIC_CONFIG,
            )
            text = response.text
            if text is None:
                raise RuntimeError("Model returned an empty response")
            return text.strip()
        except Exception as exc:  # noqa: BLE001
            if _is_retryable(exc):
                last_exc = exc
                continue
            raise _friendly_api_error(exc) from exc
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


def _requested_preview_rows(question: str, available_rows: int) -> int:
    patterns = (
        r"\b(?:top|first|latest|last|limit|show|list)\s+(\d{1,3})\b",
        r"\b(\d{1,3})\s+(?:rows?|records?|items?|invoices?|purchase orders?|pos?|delivery orders?|dos?)\b",
    )
    for pattern in patterns:
        match = re.search(pattern, question, flags=re.IGNORECASE)
        if match:
            requested = int(match.group(1))
            return min(max(1, requested), available_rows, MAX_SUMMARY_PREVIEW_ROWS)
    return min(DEFAULT_SUMMARY_PREVIEW_ROWS, available_rows)


def summarize_results(
    client: genai.Client,
    question: str,
    sql: str,
    result: dict[str, Any],
    summary_system_prompt: str,
) -> str:
    preview_limit = _requested_preview_rows(question, len(result["rows"]))
    rows_preview = result["rows"][:preview_limit]
    shown = result["count"]
    total = result["total_count"]
    count_note = (
        f"{shown} rows shown (limited by query)"
        if total > shown
        else f"{shown} rows"
    )
    preview_note = (
        f"{len(rows_preview)} preview rows supplied to the summarizer"
        if shown > len(rows_preview)
        else "all shown rows supplied to the summarizer"
    )
    prompt = (
        f"{summary_system_prompt}\n\n"
        f"User question: {question}\n\n"
        f"SQL executed:\n{sql}\n\n"
        f"Query results ({count_note}; {preview_note}; TRUE TOTAL matching rows = {total}):\n"
        f"{json.dumps(rows_preview, indent=2, default=str)}\n\n"
        "Write a concise answer. Use the TRUE TOTAL figure when describing how many "
        "records match. Include key figures and names. "
        'End with a single sentence starting "In summary:".'
    )
    return generate_content(client, prompt)


def _is_uuid_column(name: str) -> bool:
    """True if a column name denotes a UUID (used for matching, hidden from output)."""
    lowered = name.lower()
    return lowered == "uuid" or lowered.endswith("_uuid") or lowered.endswith("uuid")


def select_display_columns(
    client: genai.Client,
    question: str,
    columns: list[str],
    max_cols: int = 7,
) -> list[str]:
    """Return the most relevant column names to display for the user's question.

    UUID columns are used for matching logic only and are always excluded from the
    displayed output. If the result already has few columns, returns them unchanged.
    Otherwise makes a small LLM call to pick the most useful subset.
    """
    # UUIDs drive matching but should never be shown to the user.
    columns = [c for c in columns if not _is_uuid_column(c)]
    if len(columns) <= max_cols:
        return columns
    prompt = (
        f"The user asked: {question}\n\n"
        f"A database query returned these columns: {json.dumps(columns)}\n\n"
        f"Select the {max_cols} column names that are most useful for answering "
        "the user's question. Return ONLY a JSON array of column name strings, "
        'e.g. ["col1", "col2"]. Do not include any explanation.'
    )
    raw = generate_content(client, prompt)
    raw = re.sub(r"^```(?:json)?\s*\n?", "", raw, flags=re.IGNORECASE)
    raw = re.sub(r"\n?```\s*$", "", raw)
    try:
        selected = json.loads(raw)
        if isinstance(selected, list):
            valid = [c for c in selected if c in columns and not _is_uuid_column(c)]
            if valid:
                return valid[:max_cols]
    except (json.JSONDecodeError, ValueError):
        pass
    return columns[:max_cols]
