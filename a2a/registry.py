from __future__ import annotations

import os

AGENT_ENDPOINTS: dict[str, str] = {
    "HostAgent": os.getenv("HOST_AGENT_URL", "http://127.0.0.1:10000"),
    "InvoiceAgent": os.getenv("INVOICE_AGENT_URL", "http://127.0.0.1:10001"),
    "PurchaseOrderAgent": os.getenv("PURCHASE_ORDER_AGENT_URL", "http://127.0.0.1:10002"),
    "DeliveryOrderAgent": os.getenv("DELIVERY_ORDER_AGENT_URL", "http://127.0.0.1:10003"),
}
