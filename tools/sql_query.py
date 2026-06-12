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

_HAS_LIMIT = re.compile(r"\bLIMIT\s+\d+", re.IGNORECASE)
_TRAILING_LIMIT = re.compile(r"\s+LIMIT\s+\d+\s*$", re.IGNORECASE)
_SEMICOLON = re.compile(r";")

MAX_ROWS = 200
DEFAULT_STATEMENT_TIMEOUT_MS = 15_000


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
    if _SEMICOLON.search(stripped):
        raise ValueError("Only one SQL statement is permitted.")
    if not _ONLY_SELECT.match(stripped):
        raise ValueError("Only SELECT statements (or CTEs starting with WITH) are permitted.")
    if _FORBIDDEN.search(stripped):
        raise ValueError("Query contains a forbidden keyword.")
    return stripped


def _find_top_level_order_by(sql: str) -> int | None:
    depth = 0
    in_single_quote = False
    in_double_quote = False
    i = 0
    while i < len(sql):
        char = sql[i]
        if char == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
            i += 1
            continue
        if char == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
            i += 1
            continue
        if in_single_quote or in_double_quote:
            i += 1
            continue
        if char == "(":
            depth += 1
        elif char == ")" and depth:
            depth -= 1
        elif depth == 0 and sql[i : i + 5].lower() == "order":
            match = re.match(r"order\s+by\b", sql[i:], flags=re.IGNORECASE)
            if match:
                return i
        i += 1
    return None


def _count_sql_for(sql: str) -> str:
    sql_no_limit = _TRAILING_LIMIT.sub("", sql).strip().rstrip(";")
    order_by_index = _find_top_level_order_by(sql_no_limit)
    if order_by_index is not None:
        sql_no_limit = sql_no_limit[:order_by_index].strip()
    return f"SELECT COUNT(*) AS total FROM ({sql_no_limit}) AS _count_subq"


def execute_safe_sql(sql: str, db_params: dict[str, Any] | None = None) -> dict:
    """Validate and execute a SELECT query; return columns, rows, count, and total_count."""
    sql = validate_sql(sql)

    # Enforce a hard row cap when the LLM omits LIMIT.
    if not _HAS_LIMIT.search(sql):
        sql = f"{sql} LIMIT {MAX_ROWS}"

    # Build a COUNT(*) wrapper to get the true total regardless of LIMIT.
    # A trailing ORDER BY is not needed for counting and can make top-N queries
    # much slower, so remove it from the count wrapper.
    count_sql = _count_sql_for(sql)

    def _serialize(val: Any) -> Any:
        if isinstance(val, datetime):
            return val.isoformat()
        if isinstance(val, Decimal):
            return float(val)
        return val

    params = dict(db_params or invoice_db_params())
    params.setdefault("connect_timeout", int(os.getenv("SQL_CONNECT_TIMEOUT_SECONDS", "5")))
    statement_timeout_ms = int(os.getenv("SQL_STATEMENT_TIMEOUT_MS", str(DEFAULT_STATEMENT_TIMEOUT_MS)))

    conn = psycopg2.connect(**params)
    conn.set_session(readonly=True, autocommit=True)
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SET statement_timeout = %s", (statement_timeout_ms,))
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
