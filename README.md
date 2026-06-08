# Invoice Analysis POC

A multi-agent invoice analytics proof of concept for querying a live
**PostgreSQL** database (`invoices_uat`) with natural-language questions.

The current version uses Google Gemini to translate user questions into safe
read-only SQL, executes the query against invoice data, and summarizes the
results for business users.

## Architecture

```text
CLI
 └─► HostAgent  (port 10000)
       ├─► InvoiceAgent        (port 10001)
       │     ├─► Gemini  (natural language -> SQL, result summary)
       │     └─► invoices_uat  (PostgreSQL, read-only)
       ├─► PurchaseOrderAgent  (port 10002)
       │     └─► invoices_uat  (Invoice ↔ PO matching)
       └─► DeliveryOrderAgent  (port 10003)
             └─► invoices_uat  (Invoice ↔ DO matching)

Task/session store
 └─► postgres database  (read-write)
```

| Component        | Role                                                                 |
| ---------------- | -------------------------------------------------------------------- |
| **CLI**          | Interactive terminal interface for user questions and rich output    |
| **HostAgent**    | Receives user queries, delegates to InvoiceAgent, stores final report |
| **InvoiceAgent** | Generates SQL with Gemini, executes safe SQL, summarizes results      |
| **PurchaseOrderAgent** | Checks whether invoice lines match linked PO lines             |
| **DeliveryOrderAgent** | Checks whether invoice quantities are covered by linked DO lines |
| **SQL tool**     | Validates model-generated SQL and runs read-only PostgreSQL queries   |
| **Task store**   | Persists sessions, tasks, messages, and artifacts for traceability    |

## Prerequisites

- Python 3.11+
- PostgreSQL running on `localhost:5432` with:
  - `invoices_uat` database for invoice data, read-only access required
  - `postgres` database for task/session storage, read-write access required
  - User `postgres` / password `postgres`, or matching values in `.env`
- Google Gemini API key in `GEMINI_API_KEY`

## Setup

### 1. Open the project

```bash
cd /path/to/invoice-analysis-poc
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Copy `.env.example` to `.env` and edit as needed:

```ini
# Invoice data source
INVOICE_DB_HOST=localhost
INVOICE_DB_PORT=5432
INVOICE_DB_USER=postgres
INVOICE_DB_PASSWORD=postgres
INVOICE_DB_NAME=invoices_uat

# Purchase/PO/DO data source
PURCHASE_DB_HOST=localhost
PURCHASE_DB_PORT=5432
PURCHASE_DB_USER=postgres
PURCHASE_DB_PASSWORD=postgres
PURCHASE_DB_NAME=purchase

# Task/session store
TASK_DB_HOST=localhost
TASK_DB_PORT=5432
TASK_DB_USER=postgres
TASK_DB_PASSWORD=postgres
TASK_DB_NAME=postgres

# Required for LLM-powered SQL generation and summarization
GEMINI_API_KEY=your-gemini-api-key-here

# Agent URLs
HOST_AGENT_URL=http://127.0.0.1:10000
INVOICE_AGENT_URL=http://127.0.0.1:10001
PURCHASE_ORDER_AGENT_URL=http://127.0.0.1:10002
DELIVERY_ORDER_AGENT_URL=http://127.0.0.1:10003
```

### 4. Run

```bash
python main.py
```

On startup the application will:

1. Load `.env`.
2. Initialise the task/session tables in the `postgres` database.
3. Start **HostAgent** on `http://127.0.0.1:10000`.
4. Start **InvoiceAgent** on `http://127.0.0.1:10001`.
5. Start **PurchaseOrderAgent** on `http://127.0.0.1:10002`.
6. Start **DeliveryOrderAgent** on `http://127.0.0.1:10003`.
7. Open the interactive CLI.

## Using the CLI

Type a natural-language question at the `>` prompt.

Examples:

```text
> Which invoices have been pending for more than 60 days?
> Show me the top 10 suppliers by invoice count
> Which suppliers have the highest invoice amounts?
> Which suppliers have the lowest total invoice amounts?
> Give me a full invoice analysis
> Which buyers have the most unpaid invoices?
> Show overdue invoices by currency
> Does invoice INV-001 match its PO and DO?
> Check three-way matching for invoice INV-001
```

CLI commands:

| Input                 | Action                        |
| --------------------- | ----------------------------- |
| `help`                | Show query examples           |
| `exit` / `quit` / `q` | Exit the application          |

## Current Query Flow

1. The CLI sends the user question to HostAgent through the local A2A HTTP API.
2. HostAgent creates a session record and forwards the query to InvoiceAgent.
3. For normal analytics, InvoiceAgent sends the question plus curated schema
   context to Gemini.
4. Gemini returns a single PostgreSQL `SELECT` statement.
5. `tools/sql_query.py` validates the SQL before execution:
   - statement must start with `SELECT`
   - DDL/DML/admin keywords are blocked
   - the database connection is opened in read-only mode
   - a hard row cap is added when the SQL omits `LIMIT`
   - a wrapped `COUNT(*)` query is used to calculate the true total
6. InvoiceAgent sends the SQL result preview back to Gemini for a concise summary.
7. HostAgent wraps the structured data and summary into a final report.
8. For invoice document matching questions, HostAgent calls PurchaseOrderAgent
   and DeliveryOrderAgent instead of the generic text-to-SQL path.
9. The CLI renders the summary and any markdown table returned by the model or
   deterministic matching tables returned by the matching agents.

## Project Structure

```text
invoice-analysis-poc/
├── main.py                        # Entry point: starts agents and CLI
├── .env.example                   # Template for environment variables
├── requirements.txt
├── pyproject.toml
├── database_structure.md          # Full database schema reference
├── Report.md                      # Project brief and current limitations
│
├── a2a/                           # Lightweight A2A protocol layer
│   ├── types.py                   # Pydantic models
│   ├── client.py                  # HTTP client for agent-to-agent calls
│   ├── server.py                  # FastAPI router factory
│   └── registry.py                # Agent endpoint map
│
├── agents/
│   ├── host_agent/
│   │   ├── graph.py               # Orchestration and final report wrapping
│   │   ├── server.py              # FastAPI app on port 10000
│   │   ├── prompts.py             # HostAgent prompt reference
│   │   └── card.json              # Agent capability card
│   ├── invoice_agent/
│   │   ├── graph.py               # Gemini text-to-SQL and summarization flow
│   │   ├── prompts.py             # Schema context and Gemini instructions
│   │   ├── server.py              # FastAPI app on port 10001
│   │   └── card.json              # Agent capability card
│   ├── purchase_order_agent/
│   │   ├── graph.py               # Invoice-to-PO matching flow
│   │   ├── server.py              # FastAPI app on port 10002
│   │   ├── prompts.py             # POAgent prompt reference
│   │   └── card.json              # Agent capability card
│   └── delivery_order_agent/
│       ├── graph.py               # Invoice-to-DO matching flow
│       ├── server.py              # FastAPI app on port 10003
│       ├── prompts.py             # DOAgent prompt reference
│       └── card.json              # Agent capability card
│
├── tools/
│   ├── sql_query.py               # Safe SQL validation and execution
│   ├── document_match_query.py    # Deterministic Invoice ↔ PO/DO checks
│   └── invoice_query.py           # Legacy deterministic query helpers
│
├── storage/
│   ├── schema.sql                 # PostgreSQL DDL for task/session tables
│   └── task_store.py              # psycopg2 task/session persistence
│
└── cli/
    └── chat.py                    # Rich interactive terminal UI
```

## Database Tables Used

The LLM is given curated schema context for these `invoices_uat.public` tables:

| Table                         | Purpose                                                           |
| ----------------------------- | ----------------------------------------------------------------- |
| `public.invoice`              | Core invoice records: status, amounts, dates, supplier/buyer FKs  |
| `public.invoice_item`         | Invoice line items and PO/DO reference fields                     |
| `public.supplier_information` | Supplier names, codes, UUIDs, and country metadata                |
| `public.buyer_information`    | Buyer names, codes, and UUIDs                                     |
| `public.purchase_order`       | Purchase order headers, read from `PURCHASE_DB_NAME`              |
| `public.po_item`              | Purchase order line items, read from `PURCHASE_DB_NAME`           |
| `public.delivery_order`       | Delivery order headers, read from `PURCHASE_DB_NAME`              |
| `public.delivery_order_item`  | Delivery order line items, read from `PURCHASE_DB_NAME`           |

The task/session store creates its own `invoice_poc_*` tables in the
**`postgres`** database and does not write to `invoices_uat`.

## Safety Model

The invoice database connection is configured as read-only. In addition,
model-generated SQL is checked before execution:

- only `SELECT` statements are accepted
- dangerous keywords such as `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`,
  `CREATE`, `TRUNCATE`, `COPY`, and `VACUUM` are rejected
- result size is capped at `MAX_ROWS = 200` when no explicit `LIMIT` is present
- decimal and timestamp values are converted into JSON-serialisable values

This is a POC-level guardrail, not a full SQL parser or production policy engine.
Complex SQL can still expose edge cases in regex-based validation and limit
rewriting.

## Current Limitations

- SQL quality depends on the schema context and Gemini's interpretation of the
  business question.
- Ambiguous business terms or internal abbreviations may produce executable but
  semantically incorrect SQL unless the schema context is expanded.
- The README examples are representative; the active query surface is broader
  because the system uses text-to-SQL rather than a fixed intent list.
- PO/DO matching is deterministic and currently starts from an invoice number.
  PO matching checks line quantity, unit price, and line amount. DO matching is
  quantity-based because delivery order records do not carry invoice amounts in
  the current schema.
- `tools/invoice_query.py` contains older deterministic helpers. The current
  InvoiceAgent path uses `tools/sql_query.py` instead.

## Extending the Project

### Improve query accuracy

1. Add clearer business definitions to `agents/invoice_agent/prompts.py`.
2. Add table or column context from `database_structure.md` only when it is
   needed for the target question family.
3. Add deterministic tests around generated SQL validation and result rendering.

### Add stricter SQL safety

1. Replace regex-only SQL validation with a PostgreSQL-aware parser.
2. Enforce an allowlist of schemas and tables.
3. Add statement timeout and row/byte limits at the database level.
4. Log generated SQL and validation decisions for review.

### Point to a different database

Update the `INVOICE_DB_*` variables in `.env`. If PO/DO tables live in a
separate database, update `PURCHASE_DB_*` too. If the schema changes, update
`SCHEMA_CONTEXT` in `agents/invoice_agent/prompts.py` as well.
