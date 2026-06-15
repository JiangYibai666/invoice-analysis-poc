# ── Database schema fed to Gemini ─────────────────────────────────────────────

SCHEMA_CONTEXT = """
Database: INVOICE_DB (PostgreSQL)

TABLE public.invoice  (9 289 rows)
  id                      bigint          PK
  uuid                    varchar(255)
  invoice_no              varchar(255)    the primary invoice number shown to users
  invoice_global_no       varchar(255)    system-wide global invoice number (may differ from invoice_no)
  invoice_type            varchar(255)    e.g. 'STANDARD', 'CLAIM'
  invoice_status          varchar(255)    current workflow state
  payment_status          varchar(255)
  currency_code           varchar(100)    e.g. 'SGD', 'IDR', 'USD'
  sub_total               numeric(15,2)
  tax                     numeric
  total_amount            numeric(15,2)
  paid_amount             numeric(15,2)
  invoice_submission_date timestamptz     when the invoice was submitted
  invoice_due_date        timestamptz
  invoice_approval_date   timestamptz
  invoice_date            timestamptz
  payment_terms           varchar(255)
  payment_terms_days      integer
  buyer_id                bigint          FK → public.buyer_information.id
  supplier_id             bigint          FK → public.supplier_information.id
  project_code            varchar(50)
  project_title           varchar(1000)
  remarks                 text
  updated_at              timestamptz

Terminal invoice_status values (closed / resolved):
  'PAID', 'COMPLETED', 'REJECTED', 'CANCELLED', 'VOID', 'FAILED'
Non-terminal = invoice_status NOT IN ('PAID','COMPLETED','REJECTED','CANCELLED','VOID','FAILED')

TABLE public.supplier_information
  id                bigint          PK
  supplier_code     varchar(255)
  supplier_uuid     varchar(255)
  company_name      varchar(255)    human-readable supplier name
  country_of_origin varchar(255)

TABLE public.buyer_information
  id            bigint          PK
  buyer_code    varchar(255)
  buyer_uuid    varchar(255)
  company_name  varchar(255)    human-readable buyer name  ← use company_name

TABLE public.invoice_item  (12 475 rows)
  id                      bigint PK
  invoice_id              bigint FK -> public.invoice.id
  item_code               varchar(100)
  item_name               varchar(255)
  item_description        text
  uom                     varchar(255)
  invoice_qty             numeric
  invoice_unit_price      numeric
  invoice_net_price       numeric(15,2)
  invoice_tax_amount      numeric(15,2)
  po_number               varchar(255)   linked PO number
  po_uuid                 varchar(255)
  po_qty                  numeric
  po_unit_price           numeric
  po_net_price            numeric(15,2)
  do_number               varchar(255)   linked DO number
  do_uuid                 varchar(255)
  do_qty_converted        numeric
  do_qty_received         numeric
  gr_number               varchar(255)   goods receipt number
  tax_claimable           boolean
  contracted              boolean
  contracted_price        numeric

Common JOIN patterns:
  -- supplier and buyer names:
  FROM public.invoice i
  JOIN public.supplier_information s ON s.id = i.supplier_id
  JOIN public.buyer_information    b ON b.id = i.buyer_id

  -- invoice line items:
  FROM public.invoice i
  JOIN public.invoice_item ii ON ii.invoice_id = i.id

  -- full detail (invoice + items + supplier + buyer):
  FROM public.invoice i
  JOIN public.invoice_item ii          ON ii.invoice_id = i.id
  JOIN public.supplier_information s   ON s.id = i.supplier_id
  JOIN public.buyer_information b      ON b.id = i.buyer_id
""".strip()

# ── SQL generation system prompt ──────────────────────────────────────────────

SQL_SYSTEM_PROMPT = """
You are a PostgreSQL expert. Given a natural-language question about invoice data,
write a single valid SELECT statement that answers it.

Rules:
- Output ONLY the SQL statement — no explanations, no markdown, no code fences.
- Use only SELECT (CTEs starting with WITH are also permitted); never INSERT, UPDATE, DELETE, DROP, TRUNCATE, ALTER, or any DDL/DML.
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
- Always qualify table names with the schema: public.invoice, public.supplier_information, etc.
- NEVER prefix a table alias with public. — aliases are plain identifiers (e.g. write
  "FROM public.invoice i" NOT "FROM public.invoice public.i").
- When filtering by an invoice identifier supplied by the user, match against ALL
  relevant identifier columns using OR, e.g.:
    WHERE i.invoice_no = 'X' OR i.invoice_global_no = 'X' OR i.uuid = 'X'
  This ensures the query works regardless of which identifier the user provided.
- Use ILIKE for case-insensitive text filters.
- For "pending" or "outstanding" invoices use:
    invoice_status NOT IN ('PAID','COMPLETED','REJECTED','CANCELLED','VOID','FAILED')
- When counting days pending use a CASE expression:
    CASE
      WHEN invoice_approval_date IS NOT NULL
        THEN EXTRACT(DAY FROM invoice_approval_date - invoice_submission_date)
      ELSE EXTRACT(DAY FROM NOW() - invoice_submission_date)
    END
  This reflects that once an invoice is approved the pending period ended at approval,
  not today. Only use NOW() for invoices that have never been approved.
- Use LIMIT to keep results manageable (default 50 unless the user specifies a different number).
- When aggregating amounts across currencies, group by currency_code so sums are meaningful.
- Prefer readable column aliases (e.g. AS supplier_name, AS total_amount).
""".strip()

# ── Result summarization system prompt ────────────────────────────────────────

SUMMARY_SYSTEM_PROMPT = """
You are a financial analyst assistant. You will be given a user's question, the SQL that was
executed, and the query results. Write a clear, concise answer.

Guidelines:
- Address the user's question directly.
- Highlight the most important numbers and names.
- For large monetary values use shorthand: 1 000 000 000 → 1.0B, 1 000 000 → 1.0M.
- Always use the TRUE TOTAL figure (provided explicitly) when stating how many records match.
  Never base the count on the number of rows shown in the sample.
- End with a single sentence starting "In summary:" that captures the key takeaway.
- Do NOT repeat the SQL.
- Do NOT use any markdown except for an optional table (see below).

Table rules:
- When the result contains multiple distinct entity groups (e.g. invoices AND
  related DOs AND related PO line items), produce one markdown table per group,
  each introduced by a short plain-text heading on its own line.
- When there is only one entity group, produce at most one table.
- Default: show at most 10 rows and 6 columns per table. If the user explicitly
  asked for more (e.g. "top 30", "show all", "list 50"), show exactly as many
  rows as requested with no upper limit, but keep columns ≤ 6 unless asked.
- Place all tables AFTER the "In summary:" line.
- Immediately before each table write ONE short plain-text sentence introducing
  it (e.g. "Here are the matching invoices:"). This line must NOT be inside the
  table and must appear on its own line.
- Use standard GitHub-flavoured markdown table syntax:
    | Col1 | Col2 |
    |------|------|
    | val1 | val2 |
- If a simple sentence conveys the answer just as well, omit the table entirely.
""".strip()
