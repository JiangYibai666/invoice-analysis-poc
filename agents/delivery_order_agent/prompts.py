DO_SCHEMA_CONTEXT = """
Database: purchase (PostgreSQL)

TABLE public.delivery_order
  id                    bigint PK
  delivery_order_number varchar(50)
  global_do_number      varchar(50)
  status                varchar(255)
  delivery_date         timestamptz
  created_date          timestamptz
  issued_date           timestamptz
  po_list               varchar(255)
  procurement_type      varchar(50)
  company_uuid          varchar(255)
  buyer_id              bigint
  supplier_id           bigint
  currency_code         varchar(50)
  buyer_company_uuid    varchar(255)
  project_code          varchar(50)
  project_title         varchar(1000)
  do_type               varchar(10)
  uuid                  varchar(255)

TABLE public.delivery_order_item
  id                           bigint PK
  delivery_order_id            bigint FK -> public.delivery_order.id
  purchase_order_number        varchar(255)
  purchase_order_uuid          varchar(255)
  item_code                    varchar(100)
  item_name                    varchar(255)
  item_description             text
  uom_code                     varchar(50)
  po_quantity                  numeric(25,12)
  qty_converted                numeric(25,12)
  qty_received                 numeric(25,12)
  qty_rejected                 numeric(25,12)
  qty_to_convert               numeric(25,12)
  invoice_qty                  numeric(25,12)
  invoice_rejected_qty         numeric(25,12)
  invoice_pending_approval_qty numeric(25,12)
  po_item_id                   bigint
  price_type                   varchar(100)
  contracted                   boolean
  contract_reference_number    varchar(500)
  over_purchased_qty           boolean

Common JOIN pattern:
  FROM public.delivery_order doo
  JOIN public.delivery_order_item doi ON doi.delivery_order_id = doo.id
""".strip()

SQL_SYSTEM_PROMPT = """
You are a PostgreSQL expert for delivery order analytics.
Given a natural-language question about delivery orders, write one valid SELECT.

Rules:
- Output ONLY the SQL statement.
- Use only SELECT.
- Always qualify table names with public.
- Use ILIKE for case-insensitive text filters.
- Use LIMIT 50 unless the user requests a specific limit.
- Delivery order facts are quantity/status/date based; do not invent amounts.
- Prefer readable aliases.
""".strip()

SUMMARY_SYSTEM_PROMPT = """
You are a delivery and receiving analyst assistant. Summarize delivery order
query results clearly and concisely.

Guidelines:
- Address the user's question directly.
- Highlight DO numbers, statuses, delivery dates, PO numbers, quantities, and exceptions.
- Always use the TRUE TOTAL figure when stating how many records match.
- End with a single sentence starting "In summary:".
- Include one markdown table when multiple rows are best compared side by side.
""".strip()


TASK_CLASSIFIER_PROMPT_TEMPLATE = """
Classify this DeliveryOrderAgent request.

Return ONLY JSON:
{{"task_type": "invoice_do_matching" | "delivery_order_analysis"}}

Use invoice_do_matching when the question links an invoice number to delivery
orders, asks whether an invoice matches a DO, or asks which DO is linked to an
invoice. Otherwise use delivery_order_analysis.

Question: {query}
""".strip()
