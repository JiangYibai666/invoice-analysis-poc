from __future__ import annotations

from a2a.types import Artifact, DataPart, Message
from tools.document_match_query import extract_invoice_no, query_invoice_po_match


def run_purchase_order_graph(message: Message) -> Artifact:
    query_text = " ".join(
        part.text for part in message.parts if getattr(part, "type", "") == "text"
    )
    invoice_no = extract_invoice_no(query_text)

    if not invoice_no:
        data = {
            "query_type": "po_match",
            "found": False,
            "matched": False,
            "query": query_text,
            "error": "No invoice number found in the question.",
            "summary": "Please include an invoice number so PO matching can be checked.",
            "lines": [],
        }
    else:
        data = query_invoice_po_match(invoice_no)
        data["query"] = query_text

    return Artifact(name="purchase_order_match", parts=[DataPart(data=data)])
