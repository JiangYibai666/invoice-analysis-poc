from __future__ import annotations

from a2a.types import DataPart, Message, TextPart
from agents.delivery_order_agent import graph as do_graph
from agents.purchase_order_agent import graph as po_graph
from tools import document_match_query as match_query


def test_extract_invoice_no_and_requested_limit() -> None:
    assert match_query.extract_invoice_no("Check invoice INV-00000001 matching") == "INV-00000001"
    assert match_query.extract_invoice_no("检查发票 INV-00000002 的三方匹配") == "INV-00000002"
    assert match_query.extract_requested_limit("检查最近 5 张发票的三方匹配") == 5
    assert match_query.extract_requested_limit("Check latest 999 invoices") == match_query.MAX_BATCH_MATCH_LIMIT


def test_po_batch_match_deduplicates_and_omits_line_details(monkeypatch) -> None:
    def fake_po_match(invoice_no: str) -> dict:
        return {
            "query_type": "po_match",
            "invoice_no": invoice_no,
            "found": True,
            "matched": invoice_no == "INV-1",
            "summary": f"{invoice_no} summary",
            "lines": [{"invoice_item_id": 1}],
        }

    monkeypatch.setattr(match_query, "query_invoice_po_match", fake_po_match)

    result = match_query.query_invoice_po_batch_match(["INV-1", "INV-2", "INV-1"])

    assert result["query_type"] == "po_batch_match"
    assert result["invoice_numbers"] == ["INV-1", "INV-2"]
    assert result["checked_count"] == 2
    assert result["matched_count"] == 1
    assert result["needs_review_count"] == 1
    assert result["matched"] is False
    assert all("lines" not in item for item in result["results"])


def test_do_batch_match_handles_empty_candidates() -> None:
    result = match_query.query_invoice_do_batch_match([])

    assert result["query_type"] == "do_batch_match"
    assert result["found"] is False
    assert result["matched"] is False
    assert result["checked_count"] == 0
    assert result["results"] == []


def test_purchase_order_agent_batches_when_matching_lacks_invoice_no(monkeypatch) -> None:
    monkeypatch.setattr(
        po_graph,
        "query_invoice_po_batch_match",
        lambda invoice_numbers: {
            "query_type": "po_batch_match",
            "invoice_numbers": invoice_numbers,
            "matched": True,
            "summary": "batch po ok",
        },
    )

    message = Message(
        role="user",
        parts=[
            TextPart(text="Check three-way matching"),
            DataPart(data={"route_task_type": "document_matching", "route_invoice_numbers": ["INV-1", "INV-2"]}),
        ],
    )

    data = po_graph.run_purchase_order_graph(message).parts[0].data

    assert data["query_type"] == "po_batch_match"
    assert data["invoice_numbers"] == ["INV-1", "INV-2"]
    assert data["query"] == "Check three-way matching"


def test_delivery_order_agent_batches_when_matching_lacks_invoice_no(monkeypatch) -> None:
    monkeypatch.setattr(
        do_graph,
        "query_invoice_do_batch_match",
        lambda invoice_numbers: {
            "query_type": "do_batch_match",
            "invoice_numbers": invoice_numbers,
            "matched": False,
            "summary": "batch do review",
        },
    )

    message = Message(
        role="user",
        parts=[
            TextPart(text="Check three-way matching"),
            DataPart(data={"route_task_type": "document_matching", "route_invoice_numbers": ["INV-1", "INV-2"]}),
        ],
    )

    data = do_graph.run_delivery_order_graph(message).parts[0].data

    assert data["query_type"] == "do_batch_match"
    assert data["invoice_numbers"] == ["INV-1", "INV-2"]
    assert data["query"] == "Check three-way matching"
