PO_SCHEMA_CONTEXT = """
Database: purchase (PostgreSQL)

TABLE public.purchase_order
  id                      bigint PK
  po_global_number        varchar(255)
  po_number               varchar(50)
  pr_number               varchar(50)        purchase requisition number
  po_title                varchar(255)
  status                  varchar(50)        PO workflow status
  supplier_id             bigint FK -> public.suppliers.id
  buyer_id                bigint FK -> public.buyer_information.id
  supplier_company_uuid   varchar(255)
  buyer_company_uuid      varchar(255)
  currency_code           varchar(20)
  total_amount            numeric(26,2)
  sub_total               numeric(26,2)
  tax_amount              numeric(26,2)
  procurement_type        varchar(20)
  requisition_type        varchar(50)
  submitted_on            timestamptz
  issued_date             timestamptz
  po_date                 timestamptz
  project_code            varchar(50)
  project_title           varchar(1000)
  delivery_order_number   text               linked DO number(s)
  do_status               varchar(255)       delivery status summary
  has_fully_received      boolean
  requester_name          varchar(255)
  purchaser_name          varchar(255)
  payment_terms           varchar(255)
  contract_reference_number varchar(500)
  uuid                    varchar(255)

TABLE public.po_item
  id                            bigint PK
  po_id                         bigint FK -> public.purchase_order.id
  item_code                     varchar(100)
  item_name                     varchar(255)
  item_description              text
  supplier_name                 varchar(255)  denormalized — use directly
  supplier_uuid                 varchar(50)
  uom_code                      varchar(50)
  currency                      varchar(50)
  item_unit_price               numeric(25,12)
  quantity                      numeric(25,12)
  tax_code                      varchar(50)
  tax_rate                      double precision
  tax_amount                    numeric(26,2)
  sub_total                     numeric(26,2)
  net_price                     numeric(26,2)
  quantity_received             numeric(25,12)
  quantity_previously_delivered double precision
  invoice_qty                   numeric(25,12)
  invoice_rejected_qty          numeric(25,12)
  invoice_pending_approval_qty  numeric(25,12)
  qty_converted                 numeric(25,12)
  qty_rejected                  numeric(25,12)
  price_type                    varchar(100)
  contracted                    boolean
  contract_reference_number     varchar(500)

TABLE public.suppliers
  id                   bigint PK
  uuid                 varchar(255)
  code                 varchar(255)   supplier code
  company_name         varchar(255)   human-readable supplier name
  contact_person_name  varchar(255)
  contact_person_email varchar(255)
  country_of_origin    varchar(255)

TABLE public.buyer_information
  id              bigint PK
  buyer_code      varchar(50)
  buyer_name      varchar(150)   human-readable buyer name  ← use buyer_name (NOT company_name)
  country         varchar(50)
  company_reg_no  varchar(150)
  uuid            varchar(255)

Common JOIN patterns:
  -- items with supplier name from denormalized column:
  FROM public.purchase_order po
  JOIN public.po_item poi ON poi.po_id = po.id

  -- supplier name from lookup table:
  FROM public.purchase_order po
  JOIN public.suppliers s ON s.id = po.supplier_id

  -- buyer name:
  FROM public.purchase_order po
  JOIN public.buyer_information b ON b.id = po.buyer_id
""".strip()

SQL_SYSTEM_PROMPT = """
You are a PostgreSQL expert for purchase order analytics.
Given a natural-language question about purchase orders, write one valid SELECT.

Rules:
- Output ONLY the SQL statement.
- Use only SELECT. CTEs (WITH clauses) are permitted and preferred for complex queries.
- Always qualify table names with public.
- Use ILIKE for case-insensitive text filters.
- Use LIMIT 50 unless the user requests a specific limit.
- When aggregating amounts, group by currency_code or currency.
- Never use UNION or UNION ALL; use a single query or CTE instead.
- Focus only on purchase order data. Do not attempt to answer questions about delivery orders.
- Supplier names: use poi.supplier_name (denormalized in po_item) for item-level queries, or JOIN public.suppliers s ON s.id = po.supplier_id and use s.company_name for PO-level supplier queries.
- Buyer names: JOIN public.buyer_information b ON b.id = po.buyer_id and use b.buyer_name (NOT b.company_name).
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
