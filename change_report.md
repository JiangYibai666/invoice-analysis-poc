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
