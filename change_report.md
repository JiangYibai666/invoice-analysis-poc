# Change Report

## Prompt/output format fixes

Date: 2026-06-17

### 1. Render all markdown tables returned by summaries

- File changed: `cli/chat.py`
- Problem: `_render_summary()` only searched for the first markdown table block, so later tables allowed by the summary prompts were not displayed.
- Change: Reworked `_render_summary()` to iterate over every markdown table block and render text/table segments in their original order.
- Impact: Multi-table summaries from InvoiceAgent, PurchaseOrderAgent, and DeliveryOrderAgent are no longer silently truncated by the CLI.

### 2. Make JSON prompt examples valid JSON

- Files changed:
  - `agents/host_agent/prompts.py`
  - `agents/purchase_order_agent/prompts.py`
  - `agents/delivery_order_agent/prompts.py`
- Problem: Several prompts asked for JSON but showed pseudo-JSON examples using inline union syntax such as `"A" | "B"`, which is not valid JSON.
- Change: Replaced pseudo-JSON examples with valid JSON objects and moved allowed enum values into separate bullet lists.
- Impact: The router and task classifiers receive clearer instructions and are less likely to return invalid JSON.

### 3. Dynamically size summary preview rows

- File changed: `tools/gemini_sql.py`
- Problem: `summarize_results()` always sent only the first 20 rows to the model, even when the user explicitly requested more rows such as `top 50`.
- Change: Added `_requested_preview_rows()` to extract requested row counts from the user question and use that count for the summary preview, capped by available rows and the hard query result cap.
- Impact: When users request a specific larger result count, the summarizer can now see and summarize the requested rows instead of being limited to 20 by default.

### 4. Remove forced InvoiceAgent routing for document matching

- File changed: `agents/host_agent/prompts.py`
- Problem: The routing prompt required `InvoiceAgent` to be included for document matching, but the two-way and three-way matching flow is handled by PurchaseOrderAgent and DeliveryOrderAgent, and HostAgent does not consume an InvoiceAgent result in that matching branch.
- Change: Removed the instruction that always included InvoiceAgent alongside PurchaseOrderAgent or DeliveryOrderAgent for document matching.
- Impact: The router prompt now better matches the current implementation: invoice-to-PO matching can route to PurchaseOrderAgent, invoice-to-DO matching can route to DeliveryOrderAgent, and three-way matching can route to both matching agents without an unused InvoiceAgent call.

### 5. Clarify combined PO/DO matching summary wording

- File changed: `agents/host_agent/graph.py`
- Problem: When both PO and DO checks passed, HostAgent said "Two-way and three-way document matching passed" even though the current deterministic checks are separate Invoice-to-PO and Invoice-to-DO checks, not an additional direct PO-vs-DO consistency check.
- Change: Updated the combined conclusion to say "Invoice-to-PO and Invoice-to-DO checks passed" and stripped nested sub-agent `In summary:` sentences before HostAgent adds its final summary.
- Impact: Results for questions such as `Check INV00020608 and its related do and po` now describe exactly what was checked while still showing both PO and DO detail tables.

### 6. Teach LLM agents how to resolve PO-to-DO cross-domain lookups

- Files changed:
  - `agents/delivery_order_agent/prompts.py`
  - `agents/purchase_order_agent/prompts.py`
- Problem: For questions such as `Check POGLOBAL00008981 and its related invoice and DO`, PurchaseOrderAgent could describe a DO reference from `public.purchase_order.delivery_order_number`, while DeliveryOrderAgent could fail to find DO records because it was not explicitly told how to resolve a PO global number into DO-side records.
- Change: Expanded DeliveryOrderAgent's schema context with minimal `public.purchase_order` and `public.po_item` fields, plus join patterns for resolving local/global PO identifiers through `delivery_order_item`, `po_item`, `purchase_order`, and `delivery_order.po_list`. Added SQL prompt guidance to treat `POGLOBAL...`, `PO-...`, and PO UUID values as PO identifiers when the user asks for related DOs. Updated PurchaseOrderAgent's summary guidance to label `delivery_order_number` and `do_status` from `public.purchase_order` as PO-record references/status summaries rather than independently verified DO facts.
- Impact: Cross-domain PO questions remain LLM-generated SQL flows, but the LLM now has the schema and relationship rules needed to find related DOs from a PO global number and to avoid contradictory source wording.

## Frontend hosting and runtime configuration

Date: 2026-06-28

### 1. Start the browser frontend from `python main.py`

- Files changed:
  - `main.py`
  - `frontend_app.py`
  - `README.md`
- Problem: The frontend files existed in the project, but `python main.py` only started the agent backends and CLI. Users had to serve the frontend separately, and opening the original `.dc.html` page could produce a blank page if its external runtime dependencies were unavailable.
- Change: Added a FastAPI frontend app and included it in the `main.py` process list. Startup now launches HostAgent, InvoiceAgent, PurchaseOrderAgent, DeliveryOrderAgent, and the browser frontend together. The frontend URL is printed and opened automatically unless `DOXA_OPEN_FRONTEND=0` is set.
- Impact: Running `python main.py` now provides both the CLI and browser UI. The frontend is available by default at `http://127.0.0.1:8080/`.

### 2. Add a self-contained browser UI entrypoint

- Files changed:
  - `doxa-agent-frontend/index.html`
  - `frontend_app.py`
- Problem: The original generated frontend page depended on the bundled DC runtime loading React from a CDN. When the browser could not fetch that dependency, the raw template was hidden and the user saw a blank page.
- Change: Added `doxa-agent-frontend/index.html`, a self-contained HTML/CSS/JavaScript frontend that talks to the existing HostAgent `POST /tasks/sendSubscribe` SSE endpoint. `frontend_app.py` serves this file at `/` and keeps the original `DoxaApp.dc.html` available for compatibility.
- Impact: The default frontend no longer depends on CDN-loaded React and avoids the blank-page failure mode while preserving the existing backend protocol.

### 3. Make frontend/backend ports and origins configurable

- Files changed:
  - `main.py`
  - `frontend_app.py`
  - `agents/host_agent/server.py`
  - `doxa-agent-frontend/index.html`
  - `.env.example`
  - `README.md`
- Problem: The initial integration hardcoded local addresses and ports in multiple places, and HostAgent used permissive wildcard CORS. This made non-default local setups harder and left connection policy implicit.
- Change: Added environment-driven runtime settings:
  - `DOXA_BIND_HOST`
  - `HOST_AGENT_PORT`
  - `INVOICE_AGENT_PORT`
  - `PURCHASE_ORDER_AGENT_PORT`
  - `DELIVERY_ORDER_AGENT_PORT`
  - `DOXA_FRONTEND_PORT`
  - `DOXA_OPEN_FRONTEND`
  - `DOXA_FRONTEND_MODE`
  - `DOXA_CORS_ORIGINS`
  The frontend now loads `/config.js` to discover the HostAgent URL instead of hardcoding it in the page. HostAgent CORS now defaults to the local frontend origins and can be widened explicitly through `DOXA_CORS_ORIGINS`.
- Impact: Defaults still support the existing one-command local POC, but ports, bind host, frontend mode, automatic browser opening, and CORS policy can now be changed without code edits.
