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
