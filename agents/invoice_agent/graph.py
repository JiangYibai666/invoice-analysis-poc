from __future__ import annotations

"""InvoiceAgent graph: parses user intent then calls the appropriate invoice query tool."""

import re

from a2a.types import Artifact, DataPart, Message
from tools.invoice_query import (
    query_long_pending_invoices,
    query_supplier_amount,
    query_supplier_frequency,
)

# ---------------------------------------------------------------------------
# Intent helpers
# ---------------------------------------------------------------------------

_PENDING_KEYWORDS = {
    "pending", "overdue", "long", "waiting", "unpaid", "outstanding",
    "old", "stuck", "delayed", "unsettled", "unresolved",
}
_FREQUENCY_KEYWORDS = {
    "frequent", "frequency", "most invoice", "how many invoice", "often",
    "count", "submitted", "issued", "number of invoice", "invoice count",
}
_AMOUNT_KEYWORDS = {
    "amount", "highest", "lowest", "total", "value", "largest", "biggest",
    "smallest", "expensive", "cheap", "high", "low", "cost", "price",
    "minimum", "maximum",
}


def _detect_intent(query: str) -> str:
    q = query.lower()
    if any(kw in q for kw in _PENDING_KEYWORDS):
        return "long_pending"
    if any(kw in q for kw in _FREQUENCY_KEYWORDS):
        return "supplier_frequency"
    if any(kw in q for kw in _AMOUNT_KEYWORDS):
        return "supplier_amount"
    return "all"


def _extract_days(query: str) -> int:
    q = query.lower()
    m = re.search(r"(\d+)\s*day", q)
    if m:
        return int(m.group(1))
    m = re.search(r"(\d+)\s*week", q)
    if m:
        return int(m.group(1)) * 7
    m = re.search(r"(\d+)\s*month", q)
    if m:
        return int(m.group(1)) * 30
    return 30  # default


def _extract_top_n(query: str) -> int:
    m = re.search(r"top\s*(\d+)", query.lower())
    return int(m.group(1)) if m else 10


def _extract_order(query: str) -> str:
    q = query.lower()
    if any(w in q for w in ("lowest", "least", "smallest", "minimum", "cheapest")):
        return "asc"
    return "desc"


# ---------------------------------------------------------------------------
# Main graph entry point
# ---------------------------------------------------------------------------

def run_invoice_graph(message: Message) -> Artifact:
    query_text = " ".join(
        part.text for part in message.parts if getattr(part, "type", "") == "text"
    )

    intent = _detect_intent(query_text)

    if intent == "long_pending":
        days = _extract_days(query_text)
        result = query_long_pending_invoices(days_threshold=days)

    elif intent == "supplier_frequency":
        top_n = _extract_top_n(query_text)
        result = query_supplier_frequency(top_n=top_n)

    elif intent == "supplier_amount":
        top_n = _extract_top_n(query_text)
        order = _extract_order(query_text)
        result = query_supplier_amount(top_n=top_n, order=order)

    else:
        # "all" — run every analysis with sensible defaults and combine
        pending = query_long_pending_invoices(days_threshold=30)
        frequency = query_supplier_frequency(top_n=10)
        amount_high = query_supplier_amount(top_n=10, order="desc")
        result = {
            "query_type": "all",
            "long_pending_invoices": pending,
            "supplier_frequency": frequency,
            "supplier_amount_highest": amount_high,
            "summary": (
                "Full invoice analysis: long-pending invoices, "
                "supplier frequency and supplier amount rankings."
            ),
        }

    return Artifact(name="invoice_analysis", parts=[DataPart(data=result)])
