# Invoice Analysis POC

A multi-agent invoice analysis system built on the A2A (Agent-to-Agent) protocol,
querying a live **PostgreSQL** database (`invoices_uat`) to answer questions about
supplier invoicing behaviour.

## Architecture

```
CLI
 └─► HostAgent  (port 10000)
       └─► InvoiceAgent  (port 10001)
             └─► invoices_uat  (PostgreSQL, read-only)
```

| Component        | Role                                                                                    |
| ---------------- | --------------------------------------------------------------------------------------- |
| **HostAgent**    | Receives user queries, delegates to InvoiceAgent, formats the final report              |
| **InvoiceAgent** | Detects query intent, executes SQL against `invoices_uat`, returns structured data      |
| **Task store**   | Session & task tracking written to the `postgres` database (separate from invoice data) |

---

## Prerequisites

- Python 3.11+
- PostgreSQL running on `localhost:5432` with:
  - `invoices_uat` database (invoice data, read-only access required)
  - `postgres` database (task/session store, read-write access required)
  - User `postgres` / password `postgres` (or update `.env`)

---

## Setup

### 1. Clone / open the project

```bash
cd C:\Workspace\GitHub\invoice-analysis-poc
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Copy `.env.example` to `.env` (already done if you ran the setup) and edit as needed:

```ini
# Invoice data source
INVOICE_DB_HOST=localhost
INVOICE_DB_PORT=5432
INVOICE_DB_USER=postgres
INVOICE_DB_PASSWORD=postgres
INVOICE_DB_NAME=invoices_uat

# Task/session store
TASK_DB_HOST=localhost
TASK_DB_PORT=5432
TASK_DB_USER=postgres
TASK_DB_PASSWORD=postgres
TASK_DB_NAME=postgres
```

### 4. Run

```bash
python main.py
```

On startup the application will:
1. Initialise the task/session tables in the `postgres` database (safe to run multiple times — uses `CREATE TABLE IF NOT EXISTS`).
2. Start **HostAgent** on `http://localhost:10000`.
3. Start **InvoiceAgent** on `http://localhost:10001`.
4. Open the interactive CLI.

---

## Using the CLI

Type a natural-language question at the `>` prompt.

### Supported query types

#### Long-pending invoices
Find invoices that have been in a non-terminal status (not paid, not rejected, not cancelled) for longer than a given number of days.

```
> Which invoices have been pending for more than 60 days?
> Show me all outstanding invoices older than 90 days
> List overdue invoices pending for more than 2 months
```

Default threshold: **30 days** when no number is specified.

#### Supplier invoicing frequency
Rank suppliers by how many invoices they have submitted.

```
> Which suppliers issue the most invoices?
> Show the top 10 suppliers by invoice count
> Which supplier submits invoices most frequently?
```

Default ranking: **top 10** suppliers.

#### Supplier invoicing amount
Rank suppliers by their total (or average / min / max) invoice amounts.

```
> Which suppliers have the highest invoice amounts?
> Show me the top 5 suppliers by total invoice value
> Which suppliers have the lowest invoice amounts?
```

Use words like **"lowest"**, **"least"**, or **"minimum"** to reverse the sort order.
Default ranking: **top 10** suppliers, highest first.

#### Full analysis
When the query does not match a specific type, all three analyses run together.

```
> Give me a full invoice analysis
> Invoice summary
```

### CLI commands

| Input                 | Action                        |
| --------------------- | ----------------------------- |
| `help`                | Show available query examples |
| `exit` / `quit` / `q` | Exit the application          |

---

## Project structure

```
invoice-analysis-poc/
├── main.py                        # Entry point — starts agents and CLI
├── .env                           # Local environment variables (not committed)
├── .env.example                   # Template for environment variables
├── requirements.txt
├── pyproject.toml
│
├── a2a/                           # A2A protocol layer
│   ├── types.py                   # Pydantic models (TaskRequest, Artifact, …)
│   ├── client.py                  # HTTP client for agent-to-agent calls
│   ├── server.py                  # FastAPI router factory
│   └── registry.py                # Agent endpoint map (reads from .env)
│
├── agents/
│   ├── host_agent/
│   │   ├── graph.py               # Orchestration logic & report formatting
│   │   ├── server.py              # FastAPI app (port 10000)
│   │   ├── prompts.py             # System prompt
│   │   └── card.json              # Agent capability card
│   └── invoice_agent/
│       ├── graph.py               # Intent detection + tool dispatch
│       ├── server.py              # FastAPI app (port 10001)
│       ├── prompts.py             # System prompt
│       └── card.json              # Agent capability card
│
├── tools/
│   └── invoice_query.py           # Three SQL query functions against invoices_uat
│
├── storage/
│   ├── schema.sql                 # PostgreSQL DDL for task/session tables
│   └── task_store.py              # psycopg2-based task/session persistence
│
└── cli/
    └── chat.py                    # Rich interactive terminal UI
```

---

## Database tables used

All queries target the **`invoices_uat`** database, **`public`** schema.

| Table                         | Purpose                                                           |
| ----------------------------- | ----------------------------------------------------------------- |
| `public.invoice`              | Core invoice records — status, amounts, dates, supplier/buyer FKs |
| `public.supplier_information` | Supplier names and codes                                          |
| `public.buyer_information`    | Buyer company names                                               |

The task/session store creates its own tables (prefixed `invoice_poc_`) in the
**`postgres`** database and does not touch `invoices_uat`.

---

## Extending the project

### Add a new query type

1. Add a query function to `tools/invoice_query.py`.
2. Register a new intent keyword set in `agents/invoice_agent/graph.py` (`_detect_intent`).
3. Call the function in `run_invoice_graph` and return the result as a `DataPart`.
4. Add a rendering block to `cli/chat.py` (`_render_report`).

### Point to a different database

Update the `INVOICE_DB_*` variables in `.env`. No code changes are required.
