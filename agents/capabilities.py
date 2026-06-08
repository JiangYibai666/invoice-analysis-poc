from __future__ import annotations

from typing import Literal, TypedDict


AgentName = Literal["InvoiceAgent", "PurchaseOrderAgent", "DeliveryOrderAgent"]


class AgentCapability(TypedDict):
    agent_name: AgentName
    domain: str
    entities: list[str]
    task_types: list[str]
    data_sources: list[str]
    example_queries: list[str]


AGENT_CAPABILITIES: dict[AgentName, AgentCapability] = {
    "InvoiceAgent": {
        "agent_name": "InvoiceAgent",
        "domain": "Invoice analytics",
        "entities": ["invoice", "supplier", "buyer", "payment status"],
        "task_types": ["invoice_analysis", "supplier_analysis", "buyer_analysis", "payment_status_analysis"],
        "data_sources": ["INVOICE_DB.public.invoice", "INVOICE_DB.public.supplier_information", "INVOICE_DB.public.buyer_information"],
        "example_queries": [
            "Which invoices are pending for more than 60 days?",
            "Which suppliers submit the most invoices?",
            "Show unpaid invoice totals by buyer.",
        ],
    },
    "PurchaseOrderAgent": {
        "agent_name": "PurchaseOrderAgent",
        "domain": "Purchase order analytics and Invoice-to-PO matching",
        "entities": ["purchase order", "po", "po item", "invoice-to-po match"],
        "task_types": ["purchase_order_analysis", "invoice_po_matching"],
        "data_sources": ["PURCHASE_DB.public.purchase_order", "PURCHASE_DB.public.po_item", "INVOICE_DB.public.invoice_item"],
        "example_queries": [
            "Which purchase orders have the highest value?",
            "Show open POs by status.",
            "Does invoice INV-00000001 match its PO?",
        ],
    },
    "DeliveryOrderAgent": {
        "agent_name": "DeliveryOrderAgent",
        "domain": "Delivery order analytics and Invoice-to-DO matching",
        "entities": ["delivery order", "do", "delivery order item", "invoice-to-do match"],
        "task_types": ["delivery_order_analysis", "invoice_do_matching"],
        "data_sources": ["PURCHASE_DB.public.delivery_order", "PURCHASE_DB.public.delivery_order_item", "INVOICE_DB.public.invoice_item"],
        "example_queries": [
            "Which delivery orders are pending?",
            "Show delivered quantities by PO.",
            "Does invoice INV-00000001 match its DO?",
        ],
    },
}
