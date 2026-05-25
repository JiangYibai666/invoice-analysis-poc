"""Safe SQL execution for LLM-generated queries against invoices_uat."""
from __future__ import annotations

import os
import re
from datetime import datetime
from decimal import Decimal
from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor

_INVOICE_DB_PARAMS: dict[str, Any] = {
    "host": os.getenv("INVOICE_DB_HOST", "localhost"),
    "port": int(os.getenv("INVOICE_DB_PORT", "5432")),
    "user": os.getenv("INVOICE_DB_USER", "postgres"),
    "password": os.getenv("INVOICE_DB_PASSWORD", "postgres"),
    "dbname": os.getenv("INVOICE_DB_NAME", "invoices_uat"),
}

# Only SELECT is allowed at the start of the statement.
_ONLY_SELECT = re.compile(r"^\s*SELECT\b", re.IGNORECASE)

# Deny any data-modification or administrative keywords anywhere in the query.
_FORBIDDEN = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|TRUNCATE|ALTER|CREATE|REPLACE"
    r"|GRANT|REVOKE|EXECUTE|CALL|COPY|VACUUM|ANALYZE)\b",
    re.IGNORECASE,
)

_HAS_LIMIT = re.compile(r"\bLIMIT\s+\d+", re.IGNORECASE)

MAX_ROWS = 200


def validate_sql(sql: str) -> str:
    """Return the stripped SQL or raise ValueError if it is unsafe."""
    stripped = sql.strip().rstrip(";")
    if not _ONLY_SELECT.match(stripped):
        raise ValueError("Only SELECT statements are permitted.")
    if _FORBIDDEN.search(stripped):
        raise ValueError("Query contains a forbidden keyword.")
    return stripped


def execute_safe_sql(sql: str) -> dict:
    """Validate and execute a SELECT query; return columns, rows, and count."""
    sql = validate_sql(sql)

    # Enforce a hard row cap when the LLM omits LIMIT.
    if not _HAS_LIMIT.search(sql):
        sql = f"{sql} LIMIT {MAX_ROWS}"

    def _serialize(val: Any) -> Any:
        if isinstance(val, datetime):
            return val.isoformat()
        if isinstance(val, Decimal):
            return float(val)
        return val

    conn = psycopg2.connect(**_INVOICE_DB_PARAMS)
    conn.set_session(readonly=True, autocommit=True)
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description] if cur.description else []
    finally:
        conn.close()

    return {
        "columns": columns,
        "rows": [{k: _serialize(v) for k, v in row.items()} for row in rows],
        "count": len(rows),
    }
