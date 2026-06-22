DO_SCHEMA_CONTEXT = """
Database: purchase (PostgreSQL)

TABLE public.delivery_order
  id                    bigint PK
  delivery_order_number varchar(50)    local DO number (may repeat across buyers/suppliers)
  global_do_number      varchar(50)    preferred unique system-wide DO identifier; fewer duplicates
  status                varchar(255)   DO workflow status
  delivery_date         timestamptz
  created_date          timestamptz
  issued_date           timestamptz
  po_list               varchar(255)   linked PO number(s)
  procurement_type      varchar(50)
  company_uuid          varchar(255)
  supplier_id           bigint FK -> public.suppliers.id
  buyer_id              bigint FK -> public.buyer_information.id
  currency_code         varchar(50)
  buyer_company_uuid    varchar(255)
  project_code          varchar(50)
  project_title         varchar(1000)
  do_type               varchar(10)
  uuid                  varchar(255)

TABLE public.delivery_order_item
  id                           bigint PK
  delivery_order_id            bigint FK -> public.delivery_order.id
  purchase_order_number        varchar(255)   text reference to PO
  purchase_order_uuid          varchar(255)
  po_item_id                   bigint         FK to po_item (no hard FK constraint)
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
  price_type                   varchar(100)
  contracted                   boolean
  contract_reference_number    varchar(500)
  over_purchased_qty           boolean

TABLE public.purchase_order
  id                    bigint PK
  po_global_number      varchar(255)   preferred unique system-wide PO identifier
  po_number             varchar(50)    local PO number; often used by DO-side reference fields
  uuid                  varchar(255)
  delivery_order_number text           denormalized linked DO number(s) from the PO record
  do_status             varchar(255)   denormalized delivery status summary from the PO record

TABLE public.po_item
  id             bigint PK
  po_id          bigint FK -> public.purchase_order.id
  item_code      varchar(100)
  item_name      varchar(255)
  quantity       numeric(25,12)
  net_price      numeric(26,2)

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
  -- items:
  FROM public.delivery_order doo
  JOIN public.delivery_order_item doi ON doi.delivery_order_id = doo.id

  -- supplier name:
  FROM public.delivery_order doo
  JOIN public.suppliers s ON s.id = doo.supplier_id

  -- buyer name:
  FROM public.delivery_order doo
  JOIN public.buyer_information b ON b.id = doo.buyer_id

  -- cross-reference to PO items:
  JOIN public.po_item poi ON poi.id = doi.po_item_id

  -- delivery orders related to a PO identifier (local PO no, global PO no, or PO uuid):
  FROM public.delivery_order doo
  JOIN public.delivery_order_item doi ON doi.delivery_order_id = doo.id
  LEFT JOIN public.po_item poi ON poi.id = doi.po_item_id
  LEFT JOIN public.purchase_order po ON po.id = poi.po_id
  WHERE po.po_global_number = 'X'
     OR po.po_number = 'X'
     OR po.uuid = 'X'
     OR doi.purchase_order_number = 'X'
     OR doi.purchase_order_number = po.po_number
     OR doo.po_list ILIKE '%' || po.po_number || '%'

  -- PO record's denormalized DO reference/status summary:
  FROM public.purchase_order po
  WHERE po.po_global_number = 'X' OR po.po_number = 'X' OR po.uuid = 'X'
""".strip()

SQL_SYSTEM_PROMPT = """
You are a PostgreSQL expert for delivery order analytics.
Given a natural-language question about delivery orders, write one valid SELECT.

Rules:
- Output ONLY the SQL statement.
- Use only SELECT. CTEs (WITH clauses) are permitted and preferred for complex queries.
- Always qualify table names with public. (e.g. public.delivery_order).
- NEVER prefix a table alias with public. — aliases are plain identifiers anywhere in
  the query (FROM, SELECT, WHERE, JOIN ON). Write `doo.global_do_number` NOT
  `public.doo.global_do_number`; write `FROM public.delivery_order doo` NOT
  `FROM public.delivery_order public.doo`.
- When filtering by a DO identifier supplied by the user, match against ALL
  relevant identifier columns using OR, e.g.:
    WHERE doo.delivery_order_number = 'X' OR doo.global_do_number = 'X' OR doo.uuid = 'X'
  This ensures the query works regardless of which identifier the user provided.
- When displaying DO identifiers in results, always include `global_do_number` as the
  first/primary identifier column. `delivery_order_number` may repeat across different
  buyers or suppliers; `global_do_number` is unique system-wide and avoids confusion.
  Include `delivery_order_number` as a secondary column only when it adds useful context.
- Use ILIKE for case-insensitive text filters.
- Use LIMIT 50 unless the user requests a specific limit.
- Delivery order facts are quantity/status/date based; do not invent amounts.
- Never use UNION or UNION ALL; use a single query or CTE instead.
- CTE discipline: every column you reference from a CTE must be explicitly listed in
  that CTE's SELECT clause. Never reference a column in a later CTE or the final SELECT
  that was not computed/aliased in the CTE that produced it.
- Avoid deep multi-level CTE chains. Prefer a single JOIN query or at most two CTE steps.
- NEVER use set-returning functions (e.g. unnest(), generate_series()) inside FILTER
  clauses or inside aggregate functions. If you need to expand an array/text, do it in
  a subquery or lateral join before aggregating.
- NEVER use COUNT(DISTINCT ...) OVER(...) or any DISTINCT inside a window function;
  PostgreSQL does not support it. Use a subquery or CTE to deduplicate first.
- delivery_order.po_list is a plain text field (may contain one PO number or a
  comma-separated list). Do NOT unnest or split it in aggregates; treat it as an
  opaque text value or use ILIKE/= for matching.
- If the user provides a PO identifier (for example POGLOBAL..., PO-..., or a
  PO uuid) and asks for related delivery orders, treat it as a PO identifier,
  not a DO identifier. Resolve related DOs by joining delivery_order_item ->
  po_item -> purchase_order, matching against po.po_global_number, po.po_number,
  po.uuid, doi.purchase_order_number, and doo.po_list when useful.
- Focus on delivery order data. Use purchase_order and po_item only to resolve
  PO-to-DO relationships, not to perform general purchase order analytics.
- Supplier names: JOIN public.suppliers s ON s.id = doo.supplier_id, use s.company_name.
- Buyer names: JOIN public.buyer_information b ON b.id = doo.buyer_id, use b.buyer_name (NOT b.company_name).
- Prefer readable aliases.
""".strip()

SUMMARY_SYSTEM_PROMPT = """
You are a delivery and receiving analyst assistant. Summarize delivery order
query results clearly and concisely.

Guidelines:
- Address the user's question directly.
- Highlight DO numbers, statuses, delivery dates, PO numbers, quantities, and exceptions.
- When referring to a DO by its number, always use `global_do_number` as the primary
  identifier. Only fall back to `delivery_order_number` if `global_do_number` is not
  present in the result set.
- Always use the TRUE TOTAL figure when stating how many records match.
- End with a single sentence starting "In summary:".
- Do NOT repeat the SQL.

Table rules:
- When the result contains multiple distinct entity groups (e.g. DOs AND their
  line items AND related POs), produce one markdown table per group, each
  introduced by a short plain-text heading on its own line.
- When there is only one entity group, produce at most one table.
- Show at most 20 rows per table and at most 7 columns.
- Use standard GitHub-flavoured markdown table syntax:
    | Col1 | Col2 |
    |------|------|
    | val1 | val2 |
- Place all tables AFTER the "In summary:" line.
- If a simple sentence answers the question equally well, omit the table.
""".strip()


TASK_CLASSIFIER_PROMPT_TEMPLATE = """
Classify this DeliveryOrderAgent request.

Return ONLY JSON:
{{"task_type": "delivery_order_analysis"}}

Allowed task_type values:
- invoice_do_matching
- delivery_order_analysis

Use invoice_do_matching when the question links an invoice number to delivery
orders, asks whether an invoice matches a DO, or asks which DO is linked to an
invoice. Otherwise use delivery_order_analysis.

Question: {query}
""".strip()
