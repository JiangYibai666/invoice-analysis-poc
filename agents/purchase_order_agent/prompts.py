PO_SCHEMA_CONTEXT = """
Database: purchase (PostgreSQL)

TABLE public.purchase_order
  id                    bigint PK
  po_global_number      varchar(255)
  po_number             varchar(50)
  po_title              varchar(255)
  status                varchar(50)
  supplier_company_uuid varchar(255)
  buyer_company_uuid    varchar(255)
  supplier_id           bigint
  buyer_id              bigint
  currency_code         varchar(20)
  total_amount          numeric(26,2)
  sub_total             numeric(26,2)
  tax_amount            numeric(26,2)
  procurement_type      varchar(20)
  requisition_type      varchar(50)
  submitted_on          timestamptz
  issued_date           timestamptz
  po_date               timestamptz
  project_code          varchar(50)
  project_title         varchar(1000)
  delivery_order_number text
  do_status             varchar(255)
  uuid                  varchar(255)

TABLE public.po_item
  id                                bigint PK
  po_id                             bigint FK -> public.purchase_order.id
  item_code                         varchar(100)
  item_name                         varchar(255)
  item_description                  text
  supplier_name                     varchar(255)
  supplier_uuid                     varchar(50)
  uom_code                          varchar(50)
  currency                          varchar(50)
  item_unit_price                   numeric(25,12)
  quantity                          numeric(25,12)
  tax_code                          varchar(50)
  tax_rate                          double precision
  tax_amount                        numeric(26,2)
  sub_total                         numeric(26,2)
  net_price                         numeric(26,2)
  quantity_received                 numeric(25,12)
  quantity_previously_delivered     double precision
  invoice_qty                       numeric(25,12)
  invoice_rejected_qty              numeric(25,12)
  invoice_pending_approval_qty      numeric(25,12)
  qty_converted                     numeric(25,12)
  qty_rejected                      numeric(25,12)
  project_forecast_trade_code       varchar(50)
  price_type                        varchar(100)
  contracted                        boolean
  contract_reference_number         varchar(500)

Common JOIN pattern:
  FROM public.purchase_order po
  JOIN public.po_item poi ON poi.po_id = po.id
""".strip()

SQL_SYSTEM_PROMPT = """
You are a PostgreSQL expert for purchase order analytics.
Given a natural-language question about purchase orders, write one valid SELECT.

Rules:
- Output ONLY the SQL statement.
- Use only SELECT.
- Always qualify table names with public.
- Use ILIKE for case-insensitive text filters.
- Use LIMIT 50 unless the user requests a specific limit.
- When aggregating amounts, group by currency_code or currency.
- Prefer readable aliases.
""".strip()

SUMMARY_SYSTEM_PROMPT = """
You are a procurement analyst assistant. Summarize purchase order query results
clearly and concisely.

Guidelines:
- Address the user's question directly.
- Highlight important PO numbers, statuses, suppliers, amounts, and quantities.
- Always use the TRUE TOTAL figure when stating how many records match.
- End with a single sentence starting "In summary:".
- Include one markdown table when multiple rows are best compared side by side.
""".strip()


TASK_CLASSIFIER_PROMPT_TEMPLATE = """
Classify this PurchaseOrderAgent request.

Return ONLY JSON:
{{"task_type": "invoice_po_matching" | "purchase_order_analysis"}}

Use invoice_po_matching when the question links an invoice number to purchase
orders, asks whether an invoice matches a PO, or asks which PO is linked to an
invoice. Otherwise use purchase_order_analysis.

Question: {query}
""".strip()
