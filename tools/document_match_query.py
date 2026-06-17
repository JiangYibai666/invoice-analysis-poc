from __future__ import annotations

"""Deterministic document matching queries for Invoice <-> PO/DO checks."""

import os
import re
from datetime import datetime
from decimal import Decimal
from typing import Any

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()

_INVOICE_DB_PARAMS: dict[str, Any] = {
    "host": os.getenv("INVOICE_DB_HOST", "localhost"),
    "port": int(os.getenv("INVOICE_DB_PORT", "5432")),
    "user": os.getenv("INVOICE_DB_USER", "postgres"),
    "password": os.getenv("INVOICE_DB_PASSWORD", "postgres"),
    "dbname": os.getenv("INVOICE_DB_NAME", "invoices"),
}

_PURCHASE_DB_PARAMS: dict[str, Any] = {
    "host": os.getenv("PURCHASE_DB_HOST", os.getenv("INVOICE_DB_HOST", "localhost")),
    "port": int(os.getenv("PURCHASE_DB_PORT", os.getenv("INVOICE_DB_PORT", "5432"))),
    "user": os.getenv("PURCHASE_DB_USER", os.getenv("INVOICE_DB_USER", "postgres")),
    "password": os.getenv("PURCHASE_DB_PASSWORD", os.getenv("INVOICE_DB_PASSWORD", "postgres")),
    "dbname": os.getenv("PURCHASE_DB_NAME", "purchase"),
}

_INVOICE_NO_PATTERNS = (
    # Explicit "invoice" / "inv" keyword followed by the number
    re.compile(
        r"(?:\binvoice\b|\binv\b)\s*(?:number|no\.?)?\s*[:=#-]?\s*"
        r"([A-Za-z0-9][A-Za-z0-9._/\-]{2,})",
        re.IGNORECASE,
    ),
    # Classic format with separator: INV-000001, PO_12345, etc.
    re.compile(r"\b([A-Z]{2,}[-_/][A-Z0-9][A-Z0-9._/\-]*)\b"),
    # No-separator format: INV000103, INV00000001, etc. (letters then 4+ digits)
    re.compile(r"\b([A-Z]{2,}[0-9]{4,})\b"),
)

_BAD_INVOICE_TOKENS = {
    # common English words that appear after "invoice" in natural language
    "and", "an", "a", "the", "its", "is", "are", "was", "be",
    "for", "or", "to", "of", "in", "on", "at", "by", "from",
    "that", "this", "related", "all", "my", "their", "our",
    # domain nouns that look like tokens but are not invoice numbers
    "amount", "amounts", "number", "status", "date", "item", "items",
    "total", "details", "info", "data", "record", "records",
    "purchase", "delivery", "order", "orders", "match", "matching",
    "analysis", "check", "show", "list", "get", "find", "do", "po",
}

_TOLERANCE = Decimal("0.01")
DEFAULT_BATCH_MATCH_LIMIT = 20
MAX_BATCH_MATCH_LIMIT = 50


def extract_invoice_no(text: str) -> str | None:
    """Extract an invoice number-like token from a user question."""
    for pattern in _INVOICE_NO_PATTERNS:
        for match in pattern.finditer(text):
            candidate = match.group(1).strip(".,;:()[]{}\"'")
            if len(candidate) < 5:  # too short to be a real invoice number
                continue
            if not re.search(r"\d", candidate):  # must contain at least one digit
                continue
            if candidate.lower() not in _BAD_INVOICE_TOKENS:
                return candidate
    return None


def extract_requested_limit(
    text: str,
    default: int = DEFAULT_BATCH_MATCH_LIMIT,
    maximum: int = MAX_BATCH_MATCH_LIMIT,
) -> int:
    """Extract a user-requested batch size from text, bounded for safe matching."""
    patterns = (
        r"\b(?:top|first|latest|last|limit|show|list|check)\s+(\d{1,3})\b",
        r"\b(\d{1,3})\s+(?:invoices?|records?|items?)\b",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return min(max(1, int(match.group(1))), maximum)
    return min(max(1, int(default)), maximum)


def _connect(params: dict[str, Any]) -> psycopg2.extensions.connection:
    conn = psycopg2.connect(**params)
    conn.set_session(readonly=True, autocommit=True)
    return conn


def list_invoice_numbers_for_matching(limit: int = DEFAULT_BATCH_MATCH_LIMIT) -> list[str]:
    """Return recent invoice global numbers with line items for batch PO/DO matching."""
    limit = min(max(1, int(limit)), MAX_BATCH_MATCH_LIMIT)
    sql = """
        SELECT COALESCE(NULLIF(i.invoice_global_no, ''), i.invoice_no) AS preferred_no
        FROM public.invoice i
        WHERE (i.invoice_global_no IS NOT NULL OR i.invoice_no IS NOT NULL)
          AND EXISTS (
              SELECT 1
              FROM public.invoice_item ii
              WHERE ii.invoice_id = i.id
          )
        ORDER BY i.invoice_submission_date DESC NULLS LAST, i.id DESC
        LIMIT %s
    """

    conn = _connect(_INVOICE_DB_PARAMS)
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (limit,))
            return [str(row["preferred_no"]) for row in cur.fetchall()]
    finally:
        conn.close()


def _serialize(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    return value


def _row_to_dict(row: Any) -> dict[str, Any]:
    return {key: _serialize(value) for key, value in row.items()}


def _decimal(value: Any) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def _sum_decimal(rows: list[dict[str, Any]], key: str) -> Decimal | None:
    values = [_decimal(row.get(key)) for row in rows if row.get(key) is not None]
    if not values:
        return None
    return sum(values, Decimal("0"))


def _abs_lte(value: Decimal | None, tolerance: Decimal = _TOLERANCE) -> bool | None:
    if value is None:
        return None
    return abs(value) <= tolerance


def _variance(left: Any, right: Any) -> Decimal | None:
    left_dec = _decimal(left)
    right_dec = _decimal(right)
    if left_dec is None or right_dec is None:
        return None
    return left_dec - right_dec


def _format_money(value: Decimal | None) -> float | None:
    return float(value) if value is not None else None


def _fetch_invoice_lines(invoice_no: str, limit: int) -> list[dict[str, Any]]:
    sql = """
        SELECT
            i.invoice_no,
            i.invoice_global_no,
            i.invoice_status,
            i.currency_code,
            i.total_amount AS invoice_total_amount,
            i.invoice_submission_date,
            ii.id AS invoice_item_id,
            ii.item_code,
            ii.item_name,
            ii.invoice_qty,
            ii.invoice_unit_price,
            ii.invoice_net_price,
            ii.po_number AS invoice_item_po_number,
            ii.po_uuid AS invoice_item_po_uuid,
            ii.po_qty AS invoice_item_po_qty,
            ii.po_unit_price AS invoice_item_po_unit_price,
            ii.po_net_price AS invoice_item_po_net_price,
            ii.po_item_id,
            ii.do_number AS invoice_item_do_number,
            ii.do_uuid AS invoice_item_do_uuid,
            ii.do_qty_converted AS invoice_item_do_qty_converted,
            ii.do_qty_received AS invoice_item_do_qty_received,
            ii.do_qty_rejected AS invoice_item_do_qty_rejected,
            ii.do_item_id
        FROM public.invoice i
        LEFT JOIN public.invoice_item ii ON ii.invoice_id = i.id
        WHERE (i.invoice_no = %s OR i.invoice_global_no = %s)
        ORDER BY ii.id
        LIMIT %s
    """

    conn = _connect(_INVOICE_DB_PARAMS)
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (invoice_no, invoice_no, limit))
            return [_row_to_dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


def _fetch_po_refs(lines: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    po_item_ids = sorted({int(line["po_item_id"]) for line in lines if line.get("po_item_id") is not None})
    if not po_item_ids:
        return {}

    sql = """
        SELECT
            poi.id AS po_item_id,
            poi.quantity AS po_quantity,
            poi.item_unit_price AS po_unit_price,
            poi.net_price AS po_net_price,
            po.po_number,
            po.po_global_number,
            po.status AS po_status,
            po.currency_code AS po_currency_code,
            po.total_amount AS po_total_amount
        FROM public.po_item poi
        LEFT JOIN public.purchase_order po ON po.id = poi.po_id
        WHERE poi.id = ANY(%s)
    """
    conn = _connect(_PURCHASE_DB_PARAMS)
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (po_item_ids,))
            return {int(row["po_item_id"]): _row_to_dict(row) for row in cur.fetchall()}
    finally:
        conn.close()


def _fetch_do_refs(lines: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    do_item_ids = sorted({int(line["do_item_id"]) for line in lines if line.get("do_item_id") is not None})
    if not do_item_ids:
        return {}

    sql = """
        SELECT
            doi.id AS do_item_id,
            doi.qty_converted AS do_qty_converted,
            doi.qty_received AS do_qty_received,
            doi.qty_rejected AS do_qty_rejected,
            doi.purchase_order_number AS do_purchase_order_number,
            d.delivery_order_number,
            d.global_do_number,
            d.status AS do_status,
            d.delivery_date
        FROM public.delivery_order_item doi
        LEFT JOIN public.delivery_order d ON d.id = doi.delivery_order_id
        WHERE doi.id = ANY(%s)
    """
    conn = _connect(_PURCHASE_DB_PARAMS)
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (do_item_ids,))
            return {int(row["do_item_id"]): _row_to_dict(row) for row in cur.fetchall()}
    finally:
        conn.close()


def query_invoice_po_match(invoice_no: str, limit: int = 100) -> dict[str, Any]:
    """Check whether an invoice's line values match its linked PO lines."""
    limit = min(max(1, int(limit)), 200)
    rows = _fetch_invoice_lines(invoice_no, limit)

    if not rows:
        return {
            "query_type": "po_match",
            "invoice_no": invoice_no,
            "found": False,
            "matched": False,
            "summary": f"No invoice was found for invoice number {invoice_no}.",
            "lines": [],
        }

    lines = [row for row in rows if row.get("invoice_item_id") is not None]
    po_refs = _fetch_po_refs(lines)
    for line in lines:
        po_ref = po_refs.get(int(line["po_item_id"])) if line.get("po_item_id") is not None else None
        if po_ref:
            line.update(po_ref)
        po_qty = line.get("po_quantity") if line.get("po_quantity") is not None else line.get("invoice_item_po_qty")
        po_unit_price = (
            line.get("po_unit_price")
            if line.get("po_unit_price") is not None
            else line.get("invoice_item_po_unit_price")
        )
        po_net_price = (
            line.get("po_net_price")
            if line.get("po_net_price") is not None
            else line.get("invoice_item_po_net_price")
        )
        qty_variance = _variance(line.get("invoice_qty"), po_qty)
        unit_price_variance = _variance(line.get("invoice_unit_price"), po_unit_price)
        net_amount_variance = _variance(line.get("invoice_net_price"), po_net_price)
        line["matched_po_quantity"] = _serialize(po_qty)
        line["matched_po_unit_price"] = _serialize(po_unit_price)
        line["matched_po_net_price"] = _serialize(po_net_price)
        line["quantity_variance"] = _format_money(qty_variance)
        line["unit_price_variance"] = _format_money(unit_price_variance)
        line["net_amount_variance"] = _format_money(net_amount_variance)
        line["quantity_match"] = _abs_lte(qty_variance, Decimal("0.000001"))
        line["unit_price_match"] = _abs_lte(unit_price_variance)
        line["net_amount_match"] = _abs_lte(net_amount_variance)
        line["has_po_reference"] = bool(
            line.get("po_number")
            or line.get("invoice_item_po_number")
            or line.get("invoice_item_po_uuid")
            or line.get("po_item_id")
        )

    invoice_line_total = _sum_decimal(lines, "invoice_net_price")
    po_line_total = _sum_decimal(lines, "matched_po_net_price")
    amount_variance = _variance(invoice_line_total, po_line_total)
    missing_po_lines = sum(1 for line in lines if not line.get("has_po_reference"))
    mismatched_lines = sum(
        1
        for line in lines
        if line.get("net_amount_match") is False
        or line.get("unit_price_match") is False
        or line.get("quantity_match") is False
    )
    amount_match = bool(lines) and missing_po_lines == 0 and _abs_lte(amount_variance) is True
    matched = amount_match and mismatched_lines == 0

    display_no = rows[0].get("invoice_global_no") or invoice_no
    summary = (
        f"Invoice {display_no} has {len(lines)} line item(s). "
        f"{missing_po_lines} line item(s) have no PO reference. "
        f"Invoice line total is {rows[0].get('currency_code') or ''} "
        f"{_format_money(invoice_line_total) if invoice_line_total is not None else 'N/A'}, "
        f"matched PO line total is "
        f"{_format_money(po_line_total) if po_line_total is not None else 'N/A'}. "
        f"In summary: Invoice-to-PO matching {'passed' if matched else 'needs review'}."
    )

    return {
        "query_type": "po_match",
        "invoice_no": invoice_no,
        "invoice_global_no": rows[0].get("invoice_global_no") or invoice_no,
        "found": True,
        "matched": matched,
        "amount_match": amount_match,
        "line_count": len(lines),
        "missing_po_lines": missing_po_lines,
        "mismatched_lines": mismatched_lines,
        "currency_code": rows[0].get("currency_code"),
        "invoice_total_amount": rows[0].get("invoice_total_amount"),
        "invoice_line_total": _format_money(invoice_line_total),
        "po_line_total": _format_money(po_line_total),
        "amount_variance": _format_money(amount_variance),
        "summary": summary,
        "lines": lines,
    }


def query_invoice_do_match(invoice_no: str, limit: int = 100) -> dict[str, Any]:
    """Check whether an invoice's quantities are covered by linked DO lines."""
    limit = min(max(1, int(limit)), 200)
    rows = _fetch_invoice_lines(invoice_no, limit)

    if not rows:
        return {
            "query_type": "do_match",
            "invoice_no": invoice_no,
            "found": False,
            "matched": False,
            "summary": f"No invoice was found for invoice number {invoice_no}.",
            "lines": [],
        }

    lines = [row for row in rows if row.get("invoice_item_id") is not None]
    do_refs = _fetch_do_refs(lines)
    for line in lines:
        do_ref = do_refs.get(int(line["do_item_id"])) if line.get("do_item_id") is not None else None
        if do_ref:
            line.update(do_ref)
        received_qty = (
            line.get("do_qty_received")
            if line.get("do_qty_received") is not None
            else line.get("invoice_item_do_qty_received")
        )
        if received_qty is None:
            received_qty = (
                line.get("do_qty_converted")
                if line.get("do_qty_converted") is not None
                else line.get("invoice_item_do_qty_converted")
            )
        qty_variance = _variance(line.get("invoice_qty"), received_qty)
        line["matched_do_quantity"] = _serialize(received_qty)
        line["quantity_variance"] = _format_money(qty_variance)
        line["quantity_covered"] = (
            None
            if qty_variance is None
            else qty_variance <= Decimal("0.000001")
        )
        line["has_do_reference"] = bool(
            line.get("delivery_order_number")
            or line.get("invoice_item_do_number")
            or line.get("invoice_item_do_uuid")
            or line.get("do_item_id")
        )

    missing_do_lines = sum(1 for line in lines if not line.get("has_do_reference"))
    uncovered_lines = sum(1 for line in lines if line.get("quantity_covered") is False)
    unknown_lines = sum(1 for line in lines if line.get("quantity_covered") is None)
    matched = bool(lines) and missing_do_lines == 0 and uncovered_lines == 0 and unknown_lines == 0

    display_no = rows[0].get("invoice_global_no") or invoice_no
    summary = (
        f"Invoice {display_no} has {len(lines)} line item(s). "
        f"{missing_do_lines} line item(s) have no DO reference and "
        f"{uncovered_lines} line item(s) exceed matched DO quantity. "
        "DO records do not carry invoice amounts in the current schema, so this check is quantity-based. "
        f"In summary: Invoice-to-DO matching {'passed' if matched else 'needs review'}."
    )

    return {
        "query_type": "do_match",
        "invoice_no": invoice_no,
        "invoice_global_no": rows[0].get("invoice_global_no") or invoice_no,
        "found": True,
        "matched": matched,
        "line_count": len(lines),
        "missing_do_lines": missing_do_lines,
        "uncovered_lines": uncovered_lines,
        "unknown_quantity_lines": unknown_lines,
        "summary": summary,
        "lines": lines,
    }


def _without_lines(result: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in result.items() if key != "lines"}


def _batch_summary(
    label: str,
    invoice_numbers: list[str],
    results: list[dict[str, Any]],
) -> str:
    checked_count = len(invoice_numbers)
    found_count = sum(1 for result in results if result.get("found") is True)
    matched_count = sum(1 for result in results if result.get("matched") is True)
    needs_review_count = sum(
        1
        for result in results
        if result.get("found") is True and result.get("matched") is not True
    )
    not_found_count = checked_count - found_count
    not_found_note = f", and {not_found_count} were not found" if not_found_count else ""
    outcome = "passed for all checked invoices" if checked_count and matched_count == checked_count else "needs review"

    return (
        f"No invoice number was provided, so {label} checked {checked_count} recent invoice(s). "
        f"{matched_count} passed, {needs_review_count} need review"
        f"{not_found_note}. "
        f"In summary: Batch {label} matching {outcome}."
    )


def query_invoice_po_batch_match(invoice_numbers: list[str]) -> dict[str, Any]:
    """Run Invoice-to-PO matching for a shared batch of invoice numbers."""
    invoice_numbers = list(dict.fromkeys(str(value) for value in invoice_numbers if value))
    if not invoice_numbers:
        return {
            "query_type": "po_batch_match",
            "found": False,
            "matched": False,
            "invoice_numbers": [],
            "checked_count": 0,
            "matched_count": 0,
            "needs_review_count": 0,
            "summary": "No invoice number was provided and no candidate invoices were found for PO matching.",
            "results": [],
        }

    results = [query_invoice_po_match(invoice_no) for invoice_no in invoice_numbers]
    matched_count = sum(1 for result in results if result.get("matched") is True)
    needs_review_count = sum(
        1
        for result in results
        if result.get("found") is True and result.get("matched") is not True
    )
    not_found_count = sum(1 for result in results if result.get("found") is not True)

    return {
        "query_type": "po_batch_match",
        "found": any(result.get("found") is True for result in results),
        "matched": bool(results) and matched_count == len(results),
        "invoice_numbers": invoice_numbers,
        "checked_count": len(results),
        "matched_count": matched_count,
        "needs_review_count": needs_review_count,
        "not_found_count": not_found_count,
        "summary": _batch_summary("Invoice-to-PO", invoice_numbers, results),
        "results": [_without_lines(result) for result in results],
    }


def query_invoice_do_batch_match(invoice_numbers: list[str]) -> dict[str, Any]:
    """Run Invoice-to-DO matching for a shared batch of invoice numbers."""
    invoice_numbers = list(dict.fromkeys(str(value) for value in invoice_numbers if value))
    if not invoice_numbers:
        return {
            "query_type": "do_batch_match",
            "found": False,
            "matched": False,
            "invoice_numbers": [],
            "checked_count": 0,
            "matched_count": 0,
            "needs_review_count": 0,
            "summary": "No invoice number was provided and no candidate invoices were found for DO matching.",
            "results": [],
        }

    results = [query_invoice_do_match(invoice_no) for invoice_no in invoice_numbers]
    matched_count = sum(1 for result in results if result.get("matched") is True)
    needs_review_count = sum(
        1
        for result in results
        if result.get("found") is True and result.get("matched") is not True
    )
    not_found_count = sum(1 for result in results if result.get("found") is not True)

    return {
        "query_type": "do_batch_match",
        "found": any(result.get("found") is True for result in results),
        "matched": bool(results) and matched_count == len(results),
        "invoice_numbers": invoice_numbers,
        "checked_count": len(results),
        "matched_count": matched_count,
        "needs_review_count": needs_review_count,
        "not_found_count": not_found_count,
        "summary": _batch_summary("Invoice-to-DO", invoice_numbers, results),
        "results": [_without_lines(result) for result in results],
    }
