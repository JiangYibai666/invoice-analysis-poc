from __future__ import annotations

"""Invoice query tools that read directly from the invoices_uat PostgreSQL database.

Three query families are supported:

1. long_pending_invoices  — invoices that have been in a non-terminal state
                            for longer than a given threshold (days).
2. supplier_frequency     — which suppliers submitted the most invoices.
3. supplier_amount        — which suppliers have the highest/lowest total
                            invoice amounts.
"""

import os
from datetime import datetime, timezone
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

# Invoice statuses that are considered "terminal" (resolved) and should be
# excluded from the long-pending query.
_TERMINAL_STATUSES = (
    "PAID",
    "COMPLETED",
    "REJECTED",
    "CANCELLED",
    "VOID",
    "FAILED",
)


def _connect() -> psycopg2.extensions.connection:
    conn = psycopg2.connect(**_INVOICE_DB_PARAMS)
    conn.set_session(readonly=True, autocommit=True)
    return conn


def _row_to_dict(row: Any) -> dict:
    """Convert a RealDictRow to a plain dict with JSON-serialisable values."""
    result: dict = {}
    for key, value in row.items():
        if isinstance(value, datetime):
            result[key] = value.isoformat()
        elif value is None:
            result[key] = None
        else:
            result[key] = value
    return result


# ---------------------------------------------------------------------------
# Query 1: Long-pending invoices
# ---------------------------------------------------------------------------

def query_long_pending_invoices(days_threshold: int = 30, limit: int = 50) -> dict:
    """Return invoices that have been pending for more than *days_threshold* days.

    Joins supplier_information and buyer_information so callers get readable names.
    Ordered oldest-first so the most urgent items appear at the top.
    """
    days_threshold = max(1, int(days_threshold))
    limit = min(max(1, int(limit)), 200)

    sql = """
        SELECT
            i.invoice_no,
            i.invoice_status,
            i.payment_status,
            i.total_amount,
            i.currency_code,
            i.invoice_submission_date,
            i.invoice_due_date,
            EXTRACT(DAY FROM (NOW() - i.invoice_submission_date))::int AS days_pending,
            si.company_name  AS supplier_name,
            si.supplier_code,
            bi.company_name  AS buyer_name
        FROM public.invoice i
        LEFT JOIN public.supplier_information si ON si.id = i.supplier_id
        LEFT JOIN public.buyer_information    bi ON bi.id = i.buyer_id
        WHERE i.invoice_status NOT IN %s
          AND i.invoice_submission_date IS NOT NULL
          AND i.invoice_submission_date < NOW() - (INTERVAL '1 day' * %s)
        ORDER BY i.invoice_submission_date ASC
        LIMIT %s
    """

    count_sql = """
        SELECT COUNT(*) AS total
        FROM public.invoice i
        WHERE i.invoice_status NOT IN %s
          AND i.invoice_submission_date IS NOT NULL
          AND i.invoice_submission_date < NOW() - (INTERVAL '1 day' * %s)
    """

    conn = _connect()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(count_sql, (_TERMINAL_STATUSES, days_threshold))
            total_count = cur.fetchone()["total"]
            cur.execute(sql, (_TERMINAL_STATUSES, days_threshold, limit))
            rows = cur.fetchall()
    finally:
        conn.close()

    invoices = [_row_to_dict(r) for r in rows]
    return {
        "query_type": "long_pending_invoices",
        "threshold_days": days_threshold,
        "count": total_count,
        "shown": len(invoices),
        "invoices": invoices,
        "summary": (
            f"Found {total_count} invoice(s) that have been pending for more than "
            f"{days_threshold} day(s)."
        ),
    }


# ---------------------------------------------------------------------------
# Query 2: Supplier invoicing frequency
# ---------------------------------------------------------------------------

def query_supplier_frequency(top_n: int = 10) -> dict:
    """Return the suppliers that have submitted the most invoices, ranked descending."""
    top_n = min(max(1, int(top_n)), 100)

    sql = """
        SELECT
            si.company_name  AS supplier_name,
            si.supplier_code,
            COUNT(i.id)      AS invoice_count,
            MIN(i.invoice_submission_date) AS first_invoice_date,
            MAX(i.invoice_submission_date) AS last_invoice_date
        FROM public.invoice i
        JOIN public.supplier_information si ON si.id = i.supplier_id
        WHERE si.company_name IS NOT NULL
        GROUP BY si.id, si.company_name, si.supplier_code
        ORDER BY invoice_count DESC
        LIMIT %s
    """

    conn = _connect()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (top_n,))
            rows = cur.fetchall()
    finally:
        conn.close()

    suppliers = [_row_to_dict(r) for r in rows]
    return {
        "query_type": "supplier_frequency",
        "top_n": top_n,
        "count": len(suppliers),
        "suppliers": suppliers,
        "summary": (
            f"Top {len(suppliers)} supplier(s) by invoice submission count."
        ),
    }


# ---------------------------------------------------------------------------
# Query 3: Supplier invoicing amount
# ---------------------------------------------------------------------------

def query_supplier_amount(top_n: int = 10, order: str = "desc") -> dict:
    """Return suppliers ranked by their total invoiced amount.

    Parameters
    ----------
    top_n:
        How many suppliers to return.
    order:
        ``"desc"`` → highest total first (default).
        ``"asc"``  → lowest total first.
    """
    top_n = min(max(1, int(top_n)), 100)
    # Whitelist the sort direction to prevent SQL injection.
    direction = "DESC" if order.lower() != "asc" else "ASC"

    sql = f"""
        SELECT
            si.company_name        AS supplier_name,
            si.supplier_code,
            COUNT(i.id)            AS invoice_count,
            SUM(i.total_amount)    AS total_amount,
            AVG(i.total_amount)    AS avg_amount,
            MIN(i.total_amount)    AS min_amount,
            MAX(i.total_amount)    AS max_amount,
            i.currency_code        AS currency
        FROM public.invoice i
        JOIN public.supplier_information si ON si.id = i.supplier_id
        WHERE i.total_amount IS NOT NULL
          AND si.company_name IS NOT NULL
        GROUP BY si.id, si.company_name, si.supplier_code, i.currency_code
        ORDER BY total_amount {direction} NULLS LAST
        LIMIT %s
    """

    conn = _connect()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (top_n,))
            rows = cur.fetchall()
    finally:
        conn.close()

    suppliers = [_row_to_dict(r) for r in rows]
    order_label = "highest" if direction == "DESC" else "lowest"
    return {
        "query_type": "supplier_amount",
        "top_n": top_n,
        "order": order_label,
        "count": len(suppliers),
        "suppliers": suppliers,
        "summary": (
            f"Top {len(suppliers)} supplier(s) by {order_label} total invoice amount."
        ),
    }
