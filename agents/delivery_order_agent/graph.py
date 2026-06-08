from __future__ import annotations

from a2a.types import Artifact, DataPart, Message
from tools.document_match_query import extract_invoice_no, query_invoice_do_match


def run_delivery_order_graph(message: Message) -> Artifact:
    query_text = " ".join(
        part.text for part in message.parts if getattr(part, "type", "") == "text"
    )
    invoice_no = extract_invoice_no(query_text)

    if not invoice_no:
        data = {
            "query_type": "do_match",
            "found": False,
            "matched": False,
            "query": query_text,
            "error": "No invoice number found in the question.",
            "summary": "Please include an invoice number so DO matching can be checked.",
            "lines": [],
        }
    else:
        data = query_invoice_do_match(invoice_no)
        data["query"] = query_text

    return Artifact(name="delivery_order_match", parts=[DataPart(data=data)])
