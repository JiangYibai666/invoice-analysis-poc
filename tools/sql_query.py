"""Safe SQL execution for LLM-generated read-only PostgreSQL queries."""
from __future__ import annotations

import os
import re
from datetime import datetime
from decimal import Decimal
from typing import Any

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()

# Only SELECT (or a CTE starting with WITH) is allowed at the start.
_ONLY_SELECT = re.compile(r"^\s*(SELECT|WITH)\b", re.IGNORECASE)

# Deny any data-modification or administrative keywords anywhere in the query.
_FORBIDDEN = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|TRUNCATE|ALTER|CREATE|REPLACE"
    r"|GRANT|REVOKE|EXECUTE|CALL|COPY|VACUUM|ANALYZE)\b",
    re.IGNORECASE,
)

# Match only the OUTERMOST/trailing LIMIT (with optional OFFSET) at the very end of
# the statement. LIMITs inside CTEs or subqueries (e.g. "... ORDER BY x LIMIT 1)" that
# selects a single top row) are semantically essential and must be preserved when
# building the COUNT(*) wrapper, otherwise the true-total count is grossly inflated.
_TRAILING_LIMIT = re.compile(
    r"\s+LIMIT\s+\d+(?:\s+OFFSET\s+\d+)?\s*;?\s*$",
    re.IGNORECASE,
)

MAX_ROWS = 200


def invoice_db_params() -> dict[str, Any]:
    return {
        "host": os.getenv("INVOICE_DB_HOST", "localhost"),
        "port": int(os.getenv("INVOICE_DB_PORT", "5432")),
        "user": os.getenv("INVOICE_DB_USER", "postgres"),
        "password": os.getenv("INVOICE_DB_PASSWORD", "postgres"),
        "dbname": os.getenv("INVOICE_DB_NAME", "invoices"),
    }


def purchase_db_params() -> dict[str, Any]:
    return {
        "host": os.getenv("PURCHASE_DB_HOST", os.getenv("INVOICE_DB_HOST", "localhost")),
        "port": int(os.getenv("PURCHASE_DB_PORT", os.getenv("INVOICE_DB_PORT", "5432"))),
        "user": os.getenv("PURCHASE_DB_USER", os.getenv("INVOICE_DB_USER", "postgres")),
        "password": os.getenv("PURCHASE_DB_PASSWORD", os.getenv("INVOICE_DB_PASSWORD", "postgres")),
        "dbname": os.getenv("PURCHASE_DB_NAME", "purchase"),
    }


def validate_sql(sql: str) -> str:
    """Return the stripped SQL or raise ValueError if it is unsafe."""
    stripped = sql.strip().rstrip(";")
    if not _ONLY_SELECT.match(stripped):
        raise ValueError("Only SELECT statements (or CTEs starting with WITH) are permitted.")
    if _FORBIDDEN.search(stripped):
        raise ValueError("Query contains a forbidden keyword.")
    return stripped


def execute_safe_sql(sql: str, db_params: dict[str, Any] | None = None) -> dict:
    """Validate and execute a SELECT query; return columns, rows, count, and total_count."""
    sql = validate_sql(sql)

    # Enforce a hard row cap when the LLM omits an outer LIMIT. Only a trailing LIMIT
    # counts as the display cap; a LIMIT inside a CTE/subquery does not bound the
    # final result set, so the cap must still be appended in that case.
    if not _TRAILING_LIMIT.search(sql):
        sql = f"{sql} LIMIT {MAX_ROWS}"

    # Build a COUNT(*) wrapper to get the true total regardless of the display LIMIT.
    # Strip ONLY the trailing LIMIT so LIMITs inside CTEs/subqueries stay intact.
    sql_no_limit = _TRAILING_LIMIT.sub("", sql).strip().rstrip(";")
    count_sql = f"SELECT COUNT(*) AS total FROM ({sql_no_limit}) AS _count_subq"

    def _serialize(val: Any) -> Any:
        if isinstance(val, datetime):
            return val.isoformat()
        if isinstance(val, Decimal):
            return float(val)
        return val

    conn = psycopg2.connect(**(db_params or invoice_db_params()))
    conn.set_session(readonly=True, autocommit=True)
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(count_sql)
            total_count: int = cur.fetchone()["total"]

            cur.execute(sql)
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description] if cur.description else []
    finally:
        conn.close()

    return {
        "columns": columns,
        "rows": [{k: _serialize(v) for k, v in row.items()} for row in rows],
        "count": len(rows),
        "total_count": total_count,
    }
