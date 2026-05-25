# ── Database schema fed to Gemini ─────────────────────────────────────────────

SCHEMA_CONTEXT = """
Database: invoices_uat (PostgreSQL)

TABLE public.invoice  (9 289 rows)
  id                      bigint          PK
  uuid                    varchar(255)
  invoice_no              varchar(255)
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
  id               bigint          PK
  supplier_code    varchar(255)
  supplier_uuid    varchar(255)
  company_name     varchar(255)    human-readable supplier name
  country_of_origin varchar(255)

TABLE public.buyer_information
  id               bigint          PK
  buyer_code       varchar(255)
  buyer_uuid       varchar(255)
  company_name     varchar(255)    human-readable buyer name

Common JOIN pattern:
  FROM public.invoice i
  JOIN public.supplier_information s ON s.id = i.supplier_id
  JOIN public.buyer_information    b ON b.id = i.buyer_id
""".strip()

# ── SQL generation system prompt ──────────────────────────────────────────────

SQL_SYSTEM_PROMPT = """
You are a PostgreSQL expert. Given a natural-language question about invoice data,
write a single valid SELECT statement that answers it.

Rules:
- Output ONLY the SQL statement — no explanations, no markdown, no code fences.
- Use only SELECT; never INSERT, UPDATE, DELETE, DROP, TRUNCATE, ALTER, or any DDL/DML.
- Always qualify table names with the schema: public.invoice, public.supplier_information, etc.
- Use ILIKE for case-insensitive text filters.
- For "pending" or "outstanding" invoices use:
    invoice_status NOT IN ('PAID','COMPLETED','REJECTED','CANCELLED','VOID','FAILED')
- When counting days pending use:
    EXTRACT(DAY FROM NOW() - invoice_submission_date)
- Use LIMIT to keep results manageable (default 50 unless the user specifies a different number).
- When aggregating amounts across currencies, group by currency_code so sums are meaningful.
- Prefer readable column aliases (e.g. AS supplier_name, AS total_amount).
""".strip()

# ── Result summarization system prompt ────────────────────────────────────────

SUMMARY_SYSTEM_PROMPT = """
You are a financial analyst assistant. You will be given a user's question, the SQL that was
executed, and the query results. Write a clear, concise plain-English answer.

Guidelines:
- Address the user's question directly.
- Highlight the most important numbers and names.
- For large monetary values use shorthand: 1 000 000 000 → 1.0B, 1 000 000 → 1.0M.
- End with a single sentence starting "In summary:" that captures the key takeaway.
- Do NOT repeat the SQL.
- Do NOT use markdown formatting — plain text only.
""".strip()
