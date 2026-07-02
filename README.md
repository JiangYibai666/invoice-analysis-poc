# Invoice Analysis POC

A multi-agent invoice, purchase order, delivery order, and document matching
proof of concept for querying live **PostgreSQL** data with natural-language
questions.

The current version uses Google Gemini to translate user questions into safe
read-only SQL, routes questions to specialist agents, executes analytics queries
against invoice or purchase data, and summarizes the results for business users.

## Architecture

```text
CLI
 └─► HostAgent  (port 10000)
       ├─► InvoiceAgent        (port 10001)
       │     ├─► Gemini  (natural language -> SQL, result summary)
       │     └─► INVOICE_DB  (invoice analytics, read-only)
       ├─► PurchaseOrderAgent  (port 10002)
       │     └─► INVOICE_DB + PURCHASE_DB  (PO analytics, Invoice ↔ PO matching)
       └─► DeliveryOrderAgent  (port 10003)
             └─► INVOICE_DB + PURCHASE_DB  (DO analytics, Invoice ↔ DO matching)

Task/session store
 └─► postgres database  (read-write)
```

| Component        | Role                                                                 |
| ---------------- | -------------------------------------------------------------------- |
| **CLI**          | Interactive terminal interface for user questions and rich output    |
| **HostAgent**    | Gemini route classifier and orchestrator using capability schemas     |
| **InvoiceAgent** | Invoice, supplier, buyer, amount, status, and payment analytics       |
| **PurchaseOrderAgent** | Purchase order analytics and Invoice-to-PO matching            |
| **DeliveryOrderAgent** | Delivery order analytics and Invoice-to-DO matching             |
| **SQL tool**     | Validates model-generated SQL and runs read-only PostgreSQL queries   |
| **Task store**   | Persists sessions, tasks, messages, and artifacts for traceability    |

## Prerequisites

- Python 3.11+
- PostgreSQL running on `localhost:5432` with:
  - `INVOICE_DB_NAME` database for invoice data, read-only access required
  - `PURCHASE_DB_NAME` database for PO/DO data, read-only access required
  - `TASK_DB_NAME` database for task/session storage, read-write access required
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
INVOICE_DB_NAME=invoices

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

# Local server settings used by python main.py
DOXA_BIND_HOST=127.0.0.1
HOST_AGENT_PORT=10000
INVOICE_AGENT_PORT=10001
PURCHASE_ORDER_AGENT_PORT=10002
DELIVERY_ORDER_AGENT_PORT=10003
DOXA_FRONTEND_PORT=8080
DOXA_OPEN_FRONTEND=1
DOXA_FRONTEND_MODE=live
DOXA_CORS_ORIGINS=http://127.0.0.1:8080,http://localhost:8080

# Recent-turn conversation memory
DOXA_MEMORY_TURN_LIMIT=6
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
7. Start the browser frontend on `http://127.0.0.1:8080`.
8. Open the interactive CLI.

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
2. HostAgent creates a session record and asks Gemini to build a structured route decision:
   `{target_agents, reason, required_entities, task_type}`.
3. HostAgent dispatches the request to one or more specialist agents based on
   capability schemas in `agents/capabilities.py`.
4. For analytics, the selected agent sends the question plus its curated schema
   context to Gemini.
5. Gemini returns a single PostgreSQL `SELECT` statement.
6. `tools/sql_query.py` validates the SQL before execution:
   - statement must start with `SELECT`
   - DDL/DML/admin keywords are blocked
   - the database connection is opened in read-only mode
   - a hard row cap is added when the SQL omits `LIMIT`
   - a wrapped `COUNT(*)` query is used to calculate the true total
7. The selected agent sends the SQL result preview back to Gemini for a concise
   summary.
8. For invoice document matching questions, HostAgent composes PO and/or DO
   agent results into a two-way or three-way matching report.
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
│   ├── capabilities.py            # Agent capability schema used by HostAgent
│   ├── host_agent/
│   │   ├── graph.py               # Orchestration and final report wrapping
│   │   ├── router.py              # Gemini JSON route classifier using prompts.py
│   │   ├── server.py              # FastAPI app on port 10000
│   │   ├── prompts.py             # HostAgent prompt reference
│   │   └── card.json              # Agent capability card
│   ├── invoice_agent/
│   │   ├── graph.py               # Gemini text-to-SQL and summarization flow
│   │   ├── prompts.py             # Schema context and Gemini instructions
│   │   ├── server.py              # FastAPI app on port 10001
│   │   └── card.json              # Agent capability card
│   ├── purchase_order_agent/
│   │   ├── graph.py               # PO analytics and Invoice-to-PO matching
│   │   ├── server.py              # FastAPI app on port 10002
│   │   ├── prompts.py             # POAgent prompt reference
│   │   └── card.json              # Agent capability card
│   └── delivery_order_agent/
│       ├── graph.py               # DO analytics and Invoice-to-DO matching
│       ├── server.py              # FastAPI app on port 10003
│       ├── prompts.py             # DOAgent prompt reference
│       └── card.json              # Agent capability card
│
├── tools/
│   ├── sql_query.py               # Safe SQL validation and execution
│   ├── document_match_query.py    # Deterministic Invoice ↔ PO/DO checks
│   └── gemini_sql.py              # Shared Gemini text-to-SQL helpers
│
├── storage/
│   ├── schema.sql                 # PostgreSQL DDL for task/session tables
│   └── task_store.py              # psycopg2 task/session persistence
│
└── cli/
    └── chat.py                    # Rich interactive terminal UI
```

## Database Tables Used

The specialist agents receive curated schema context for their own data source.

Invoice analytics reads from `INVOICE_DB_NAME`:

| Table                         | Purpose                                                           |
| ----------------------------- | ----------------------------------------------------------------- |
| `public.invoice`              | Core invoice records: status, amounts, dates, supplier/buyer FKs  |
| `public.invoice_item`         | Invoice line items and PO/DO reference fields                     |
| `public.supplier_information` | Supplier names, codes, UUIDs, and country metadata                |
| `public.buyer_information`    | Buyer names, codes, and UUIDs                                     |

PO/DO analytics and matching reads PO/DO reference data from
`PURCHASE_DB_NAME` and invoice line references from `INVOICE_DB_NAME`:

| Table                        | Purpose                                             |
| ---------------------------- | --------------------------------------------------- |
| `public.purchase_order`      | Purchase order headers                              |
| `public.po_item`             | Purchase order line items                           |
| `public.delivery_order`      | Delivery order headers                              |
| `public.delivery_order_item` | Delivery order line items                           |

The task/session store creates its own `invoice_poc_*` tables in the
`TASK_DB_NAME` database and does not write to the invoice or purchase data
databases. Recent-turn conversation memory is stored in the task database and
is bounded by `DOXA_MEMORY_TURN_LIMIT` (`6` turns by default).

## Safety Model

The analytics database connections are configured as read-only. In addition,
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
separate database, update `PURCHASE_DB_*` too. If the schema changes, update the
relevant prompt schema context in `agents/invoice_agent/prompts.py`,
`agents/purchase_order_agent/prompts.py`, or
`agents/delivery_order_agent/prompts.py`. If responsibilities change, also
update `agents/capabilities.py` and the HostAgent router prompt.
