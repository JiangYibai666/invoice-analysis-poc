# Change Report

Date: 2026-07-02

## Recent-turn Conversation Memory MVP

### Summary

Implemented a recent N-turn context memory MVP without adding a vector database.
The system now keeps a stable `conversation_id` across multiple user turns, stores
completed conversation turns in PostgreSQL, and lets HostAgent inject recent
conversation context through a resolved follow-up query before routing and
specialist-agent dispatch.

### Files changed

- `a2a/types.py`
- `agents/host_agent/graph.py`
- `main.py`
- `cli/chat.py`
- `doxa-agent-frontend/index.html`
- `doxa-agent-frontend/DoxaApp.dc.html`
- `.env.example`
- `README.md`
- `storage/schema.sql`
- `storage/task_store.py`
- `storage/memory_store.py`
- `agents/host_agent/router.py`
- `tools/gemini_sql.py`
- `change_report.md`

### Key changes

1. Added optional `conversation_id` to `TaskRequest` so one conversation can span
   multiple request-level `session_id` values.
2. Added PostgreSQL tables and columns for conversation memory:
   - `invoice_poc_conversations`
   - `invoice_poc_conversation_turns`
   - `invoice_poc_sessions.conversation_id`
   - `invoice_poc_sessions.turn_index`
3. Added `storage/memory_store.py` with helpers to:
   - create/update conversations
   - reserve the next turn index inside a database transaction
   - load only completed recent turns
   - save each completed turn with original query, rewritten query, summary, and final report
4. Updated HostAgent to:
   - resolve the active conversation
   - reserve each conversation turn before routing
   - rewrite short follow-up questions into a single resolved query when recent
     context is needed
   - send recent memory as structured `DataPart` metadata instead of appending
     the full history to the user question
   - keep the original user query in the final report
   - save the completed turn after finalization
5. Updated CLI to reuse one `conversation_id` for the lifetime of the interactive
   CLI process.
6. Updated the browser frontend to keep one `conversation_id` in `sessionStorage`
   and generate a new one when the user clicks New chat.
7. Documented `DOXA_MEMORY_TURN_LIMIT` in `.env.example`, `README.md`, and this
   change report.
8. Added Gemini access-error hardening:
   - HostAgent router still falls back to keyword routing when the model returns
     malformed routing JSON.
   - Gemini runtime/configuration failures, including missing API keys and 401/403
     authorization errors, are no longer silently downgraded to keyword routing.
   - Gemini API authorization failures are formatted as actionable configuration
     errors that mention `GEMINI_API_KEY`, project access, API enablement, billing,
     quota, and model access.
9. Fixed the conversation turn race:
   - `start_conversation_turn()` locks the conversation row with `FOR UPDATE`,
     calculates the next index, and inserts a placeholder turn in one transaction.
   - Concurrent requests for the same conversation now receive distinct indexes.
10. Fixed stale environment variable handling:
    - `python main.py` now loads `.env` with override enabled by default.
    - Gemini client creation refreshes `.env` before reading `GEMINI_API_KEY`.
    - Task-store connections read database settings at connection time instead of
      freezing them at import time.
    - `DOXA_DOTENV_OVERRIDE=0` can be used when deployment environment variables
      should take precedence over `.env`.

### Configuration

Recent context length is controlled by `DOXA_MEMORY_TURN_LIMIT`.

- Default: `6`
- Minimum effective value: `0`
- Maximum effective value: `20`

Setting `DOXA_MEMORY_TURN_LIMIT=0` disables recent-turn context injection while
leaving turn persistence enabled.

`DOXA_DOTENV_OVERRIDE=1` is the default local behavior. It prevents stale shell
values such as an old `GEMINI_API_KEY` from overriding the project `.env`.

### Behavior

Example:

1. User asks: `Check three-way matching for invoice INV-00000001`
2. User asks next: `What about its PO?`
3. HostAgent rewrites the second question to a single resolved question referring
   to `INV-00000001`, while also passing structured memory metadata to the
   specialist agents.

The MVP intentionally avoids long-term semantic/vector memory. It only uses
bounded recent-turn context from the same conversation.

### Runtime note

If Gemini returns an error such as `403 PERMISSION_DENIED` or `Lightning dunning
decision is deny`, HostAgent now reports an actionable Gemini configuration or
authorization error instead of silently falling back to keyword routing. LLM-powered
SQL generation and summarization remain unavailable until the Gemini API key,
Google project billing/quota, API enablement, and model access are fixed.

### Verification

- Python compilation passed for A2A types, storage, HostAgent, router, Gemini
  helpers, CLI, and specialist agent graphs.
- `init_db()` successfully applied the schema to the local PostgreSQL task store.
- A threaded local PostgreSQL test started 8 turns for the same conversation and
  received `[1, 2, 3, 4, 5, 6, 7, 8]` with no duplicates.
- Router tests confirmed malformed Gemini routing JSON still falls back to keyword
  routing, while missing `GEMINI_API_KEY` raises a clear runtime error.
- HostGraph failure-path testing confirmed missing `GEMINI_API_KEY` returns a
  failed task event with an actionable message instead of silently falling back.
- Query rewrite tests confirmed follow-up questions with references are resolved,
  while unrelated questions and questions with explicit invoice numbers are not
  rewritten.
- Startup verification confirmed `python main.py` reaches the CLI and starts all
  local agents/frontend after stale processes are stopped.
- Environment verification confirmed that even with a bad shell-level
  `GEMINI_API_KEY`, Gemini routing uses the current `.env` key when
  `DOXA_DOTENV_OVERRIDE=1`.

---

Date: 2026-07-03

## Conversation Memory Hardening and Frontend History

### Summary

Extended the recent-turn memory MVP into a user-visible conversation history
feature. The task store now records turn lifecycle status, failed turns are
auditable, HostAgent avoids over-broad follow-up rewrites, and the browser
frontend can list, open, and delete saved conversations from the left History
panel.

### Files changed

- `agents/host_agent/graph.py`
- `agents/host_agent/server.py`
- `cli/chat.py`
- `doxa-agent-frontend/index.html`
- `README.md`
- `storage/schema.sql`
- `storage/memory_store.py`
- `change_report.md`

### Key changes

1. Hardened conversation turn persistence:
   - Added `status`, `error_message`, `completed_at`, and `updated_at` to
     `invoice_poc_conversation_turns`.
   - Backfilled existing turns with `final_report IS NOT NULL` to
     `status='completed'`.
   - Memory context now only reads completed turns with a saved final report.
   - Failed HostAgent requests are saved as `status='failed'` with the error
     message when a turn has already been reserved.
2. Improved follow-up query rewriting:
   - HostAgent now selects only the relevant recent entity for a follow-up
     question instead of appending every recent invoice/PO/DO reference.
   - PO-specific follow-ups such as `What about its PO?` resolve only the recent
     PO.
   - Generic collection queries such as `Which POs are linked to invoices?` are
     not rewritten just because they contain `linked` or `related`.
   - Final reports include `latest_refs` and `selected_refs` in memory metadata
     for debugging.
3. Added memory inspection helpers:
   - `load_conversation_debug_turns()` returns stored turns with lifecycle
     status, original query, rewritten query, summary/error, and final report.
   - CLI now supports `memory` and `memory <conversation_id>` to inspect stored
     conversation turns from the terminal.
4. Added HostAgent history APIs:
   - `GET /conversations` returns recent saved conversations for the History
     sidebar.
   - `GET /conversations/{conversation_id}/turns` returns turns for a selected
     conversation.
   - `DELETE /conversations/{conversation_id}` deletes a conversation from the
     task-store memory tables.
   - CORS now allows `GET` and `DELETE` in addition to the existing streaming
     `POST` endpoints.
5. Added browser frontend History sidebar:
   - The left sidebar lists recent saved conversations.
   - The active conversation is highlighted.
   - Clicking a history item loads the saved user/assistant turns into the chat
     transcript.
   - Refreshing the page restores the current conversation when it still exists.
   - Completing a new request refreshes the History list.
   - Each history item has a delete button with a confirmation prompt.
   - Deleting the active conversation resets the UI to a new empty conversation.
6. Updated documentation:
   - README now documents memory lifecycle status, frontend History, CLI memory
     inspection, and deleting a saved conversation from the History panel.

### Behavior

Example:

1. User asks a business question in the browser.
2. The turn is stored under the current `conversation_id`.
3. The left History panel refreshes and shows the conversation title, turn count,
   and updated time.
4. User can click the history item later to reload its stored transcript.
5. User can click the `×` button on the history item, confirm deletion, and remove
   that conversation from the memory tables.

Deleting a conversation removes memory records from `invoice_poc_conversation_turns`
and `invoice_poc_conversations`. It does not delete invoice, purchase order, or
delivery order source data.

### Verification

- Python compilation passed for `storage/memory_store.py`,
  `agents/host_agent/graph.py`, `agents/host_agent/server.py`, and `cli/chat.py`.
- `init_db()` successfully applied the new memory lifecycle schema to the local
  PostgreSQL task store.
- HostAgent route registration confirmed:
  - `GET /conversations`
  - `GET /conversations/{conversation_id}/turns`
  - `DELETE /conversations/{conversation_id}`
  - `POST /tasks/send`
  - `POST /tasks/sendSubscribe`
- Local PostgreSQL verification confirmed `list_conversations(3)` returns saved
  conversations with `conversation_id`, title/query, turn count, status, and
  timestamps.
- Frontend inline JavaScript syntax validation passed using Node `vm.Script`.
- Query rewrite checks confirmed:
  - `What about its PO?` resolves only to the latest PO.
  - `What is its status?` resolves to the latest primary entity.
  - `Which POs are linked to invoices?` is not rewritten from memory.
  - `Show top 10 purchase orders by value` is not rewritten.

---

Date: 2026-07-06

## Cross-conversation Long-term Memory

### Summary

Implemented a scoped long-term memory layer on top of the existing recent-turn
conversation memory. The system now accepts a stable `memory_scope_id`, stores
cross-conversation business memories, retrieves relevant memories before HostAgent
routing, and keeps frontend conversation history scoped to the current local user.

### Files changed

- `.env.example`
- `README.md`
- `a2a/types.py`
- `agents/host_agent/graph.py`
- `agents/host_agent/long_term_memory.py`
- `agents/host_agent/server.py`
- `cli/chat.py`
- `doxa-agent-frontend/index.html`
- `storage/schema.sql`
- `storage/task_store.py`
- `storage/memory_store.py`
- `tools/gemini_sql.py`
- `change_report.md`

### Key changes

1. Added `memory_scope_id` to `TaskRequest`:
   - Browser frontend stores a stable `doxa.memoryScopeId` in `localStorage`.
   - CLI uses `DOXA_MEMORY_SCOPE_ID`, defaulting to `local-user`.
   - Conversation history and long-term memories are filtered by scope.
2. Added long-term memory storage:
   - New `invoice_poc_long_term_memories` table stores memory type, entity type,
     entity value, content, source conversation/turn, embedding JSON, importance,
     status, and timestamps.
   - `invoice_poc_conversations.memory_scope_id` isolates conversation history.
   - `init_db()` attempts to enable pgvector and create an optional
     `embedding_vector vector(768)` column/index.
   - If pgvector is unavailable, the app continues with JSONB embeddings,
     entity matching, and text fallback retrieval.
3. Added long-term memory generation:
   - Completed business turns are distilled into entity and summary memories.
   - Off-topic and failed turns are not written to long-term memory.
   - Duplicate entity memories are upserted by scope/type/entity.
   - Gemini `text-embedding-004` embeddings are generated best-effort and never
     block normal answers.
4. Added long-term memory retrieval:
   - HostAgent retrieves long-term memories before recent-turn rewrite and routing.
   - Exact invoice/PO/DO entity matches are prioritized.
   - Semantic retrieval uses pgvector when available, otherwise a structured/text
     fallback.
   - Cross-conversation cues such as "previous", "before", "上次", or "之前" can
     rewrite a question to reference a remembered invoice/PO/DO.
   - Entity-specific cross-conversation cues such as "last invoice",
     "previous PO", and "last DO" prefer memories of the requested entity type.
   - Ambiguous cross-conversation references prefer memories whose original user
     query explicitly mentioned the referenced invoice/PO/DO number, reducing
     accidental selection of entities introduced only by later summaries.
   - Retrieved memories are included in structured memory metadata rather than
     appending full history to user prompts.
5. Added memory APIs:
   - `GET /memories?limit=...&q=...&memory_scope_id=...`
   - `DELETE /memories/{memory_id}?memory_scope_id=...`
   - Existing conversation APIs now accept `memory_scope_id`.
6. Updated frontend scope handling:
   - Browser requests include `memory_scope_id` so conversations and memories are
     isolated per local user scope.
   - The sidebar intentionally shows only `History`; long-term memory remains a
     backend capability and is not displayed as a separate frontend panel.
   - Conversation deletion remains separate from long-term memory deletion.

### Configuration

- `DOXA_LONG_TERM_MEMORY_ENABLED=1`
- `DOXA_MEMORY_SCOPE_ID=local-user`
- `DOXA_LONG_TERM_MEMORY_LIMIT=5`
- `DOXA_EMBEDDING_MODEL=text-embedding-004`
- `DOXA_MEMORY_MIN_IMPORTANCE=0.4`

### Verification

- Python compilation passed for A2A types, task/memory stores, Gemini helpers,
  HostAgent graph/server, long-term memory module, and CLI.
- Frontend inline JavaScript syntax validation passed.
- `init_db()` successfully applied the long-term memory schema to the local
  PostgreSQL task store.
- Local schema inspection confirmed `invoice_poc_conversations.memory_scope_id`
  and `invoice_poc_long_term_memories` were created.
- Local PostgreSQL did not expose pgvector, so the optional vector column was not
  created; fallback retrieval remains active.
- HostAgent route registration confirmed `/memories`, `/memories/{memory_id}`,
  scoped conversation APIs, and existing task endpoints.
- Pure function checks confirmed cross-conversation rewrite resolves remembered
  invoice references, prefers the entity type requested by "last invoice"/"last
  PO"/"last DO" phrasing, and does not override explicit current invoice IDs.
