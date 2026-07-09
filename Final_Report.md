# SA61 INDUSTRIAL ATTACHMENT REPORT

## Project Title: AI-Powered Invoice Analysis and Document Matching Agent POC

**Student(s):** Project Team / To be filled  
**Organisation:** Doxa Holdings International Pte Ltd.  
**Project Repository:** `invoice-analysis-poc`  
**Report Date:** July 2026  

**IN PARTIAL FULFILLMENT OF THE REQUIREMENTS FOR THE**  
**GRADUATE DIPLOMA IN SYSTEMS ANALYSIS**

**NUS-ISS**  
**NATIONAL UNIVERSITY OF SINGAPORE**

---

# Contents in the Industrial Attachment Report

1. [Introduction](#introduction)
2. [Project Background](#project-background)
3. [Overview of Activities](#overview-of-activities)
4. [Project Plan and schedules](#project-plan-and-schedules)
5. [Recommendations](#recommendations)
6. [Things Learned](#things-learned)
7. [Problems and Solutions](#problems-and-solutions)
8. [Looking Back](#looking-back)
9. [Acknowledgement](#acknowledgement)
10. [Appendix A](#appendix-a)
11. [Appendix B](#appendix-b)

---

# Introduction

This industrial attachment project delivered a proof of concept for an AI-powered invoice analysis and document matching assistant for Doxa's procurement, finance, and logistics workflows. The project focuses on one function within the broader DOXA CONNEX AI agent programme: the invoice matching and analysis capability that helps users query invoice, purchase order (PO), and delivery order (DO) records using natural language.

The implemented system is a local multi-agent application. A user can ask business questions through a command-line interface or browser chat UI, and a HostAgent routes the request to specialist agents for invoice, purchase order, and delivery order analysis. The specialist agents translate natural-language questions into read-only PostgreSQL queries, execute them safely, and return concise business summaries. For cross-document questions, the system coordinates multiple agents and uses invoice line-item references as the authoritative linkage between invoices, POs, and DOs.

The objective of the project was not to replace the full DOXA CONNEX production platform immediately. Instead, it demonstrates the feasibility of using agent orchestration, natural-language data access, deterministic document-link matching, conversation memory, and a lightweight browser interface as the foundation for a future production-ready invoice matching agent.

# Project Background

DOXA CONNEX's strategic AI plan describes a suite of 16 agents across procurement, finance and payment, deep-tier financing, logistics and delivery, compliance and risk, analytics and reporting, and customer success. Within that plan, the **Invoice Matching Agent** is positioned under the finance and payment domain. Its intended business value is to automate three-way or four-way invoice matching, reduce manual checking, explain exceptions, and shorten invoice processing time from days to hours.

The current POC implements the core technical foundation for that vision. It connects to existing PostgreSQL data sources for invoice, PO, and DO records, exposes specialist agents over a lightweight A2A HTTP protocol, and allows business users to ask questions such as:

- Which invoices have been pending for more than 60 days?
- Which suppliers have the highest invoice amounts?
- Which purchase orders have the highest value?
- Which delivery orders are pending?
- Does an invoice match its related PO and DO?
- What about its PO or DO in a follow-up question?

The project uses a modular architecture:

```text
CLI / Browser Frontend
  -> HostAgent
       -> InvoiceAgent
       -> PurchaseOrderAgent
       -> DeliveryOrderAgent
  -> PostgreSQL task, session, conversation, and memory store
```

The HostAgent is responsible for routing, memory handling, cross-agent coordination, and final response composition. The InvoiceAgent handles invoice, supplier, buyer, payment status, and invoice amount analytics. The PurchaseOrderAgent handles purchase order analytics. The DeliveryOrderAgent handles delivery order analytics. A deterministic matching utility provides invoice-to-PO and invoice-to-DO checks using invoice item fields and UUID-based linkage.

The project is aligned with the overall DOXA plan in the following ways:

| Overall programme item | POC contribution |
| --- | --- |
| Finance and payment: Invoice Matching Agent | Implements the first working natural-language invoice analysis and document matching POC. |
| Agent orchestration | Implements HostAgent routing and specialist-agent dispatch. |
| PostgreSQL data foundation | Reads invoice, PO, and DO records from configured PostgreSQL databases. |
| Human-facing agent UI | Provides both CLI and browser chat interfaces. |
| Auditability and memory | Persists sessions, turns, messages, artifacts, recent memory, and long-term memory records. |
| Future Connex integration | Uses modular API, environment configuration, and frontend separation that can be extended into Connex workflows. |

# Overview of Activities

The project activities were organised around understanding the business workflow, designing the POC architecture, implementing the multi-agent backend, building a usable interface, and documenting limitations and future improvements.

## Business and workflow understanding

The first activity was to understand where invoice analysis fits within the DOXA CONNEX agent programme. The overall plan identified invoice matching as a high-priority finance and payment function because manual invoice checking is time-consuming, error-prone, and dependent on cross-referencing multiple documents. The POC therefore focused on the practical business questions that finance, procurement, and operations users would ask during invoice review.

The source data model was studied through `database_structure.md` and the active application code. The key tables used by this POC are:

- `public.invoice`
- `public.invoice_item`
- `public.supplier_information`
- `public.buyer_information`
- `public.purchase_order`
- `public.po_item`
- `public.delivery_order`
- `public.delivery_order_item`

The analysis showed that `invoice_item` is the most important pivot for document matching because it contains the PO and DO reference fields used to relate invoice line items to purchase and delivery records.

## Requirements capture

The functional requirements were translated into the following POC capabilities:

- Natural-language invoice analytics.
- Natural-language PO and DO analytics.
- HostAgent routing to the correct specialist agent.
- Multi-agent responses for cross-domain questions.
- Read-only SQL generation and execution.
- Deterministic invoice-to-PO and invoice-to-DO matching checks.
- Browser chat interface with saved conversation history.
- Recent-turn memory for follow-up questions.
- Long-term scoped memory for cross-conversation references.
- Session and task persistence for traceability.

The non-functional requirements were framed around safety, traceability, maintainability, and local deployability:

- Read-only database access for analytics databases.
- SQL validation to block write, DDL, and administrative statements.
- Result row limits to reduce accidental large result sets.
- Environment-based configuration.
- Separate specialist modules for clearer responsibility boundaries.
- Persistent task/session/memory storage for audit and debugging.

## Analysis and design

The system was designed as a multi-agent POC rather than a single monolithic chatbot. This design supports the broader DOXA plan, where each business domain can be represented by a specialist agent.

The main design decisions were:

- Use HostAgent as the single entry point for user requests.
- Use capability metadata in `agents/capabilities.py` to describe each specialist agent.
- Use Gemini for routing, SQL generation, summarisation, and memory-related rewriting.
- Use deterministic code for document-link resolution where correctness is more important than open-ended generation.
- Keep the invoice and purchase data sources read-only.
- Store task, session, conversation, and memory data in separate `invoice_poc_*` tables.
- Keep the POC frontend simple but usable through a chat interface and History panel.

## Implementation

The implementation delivered the following major components:

| Component | Description |
| --- | --- |
| `main.py` | Starts the HostAgent, specialist agents, frontend, database initialisation, and CLI. |
| `a2a/` | Defines the lightweight agent-to-agent request, response, task, message, and artifact protocol. |
| `agents/host_agent/` | Implements routing, orchestration, final report composition, recent memory, and long-term memory handling. |
| `agents/invoice_agent/` | Implements invoice analytics with Gemini text-to-SQL and summarisation. |
| `agents/purchase_order_agent/` | Implements purchase order analytics against purchase data. |
| `agents/delivery_order_agent/` | Implements delivery order analytics against purchase data. |
| `tools/sql_query.py` | Provides safe read-only SQL validation and execution. |
| `tools/document_match_query.py` | Provides deterministic invoice-to-PO and invoice-to-DO matching utilities. |
| `storage/` | Provides PostgreSQL schema and persistence for sessions, tasks, conversation turns, and memories. |
| `cli/chat.py` | Provides an interactive terminal chat interface. |
| `frontend_app.py` and `doxa-agent-frontend/index.html` | Provide the browser chat UI and History panel. |

## User interface and interaction flow

The user can run the application with:

```bash
python main.py
```

The application starts the local agents and browser frontend. A user can then ask natural-language questions from the CLI or browser. For example, if the user asks "Which invoices have been pending for more than 60 days?", the HostAgent routes the request to the InvoiceAgent. If the user asks "Check invoice INV-00000001 and its related PO and DO", the HostAgent can coordinate multiple agents and return a combined answer.

The browser interface also maintains a local conversation scope and shows saved conversations in the History sidebar. This makes the POC more practical for demonstration because users can revisit previous question-and-answer turns rather than treating every query as isolated.

## Verification activities

The project includes recorded verification in `change_report.md`. The verification activities include:

- Python compilation checks for key modules.
- Database schema initialisation checks.
- HostAgent route registration checks.
- Router fallback behaviour checks.
- Query rewrite checks for follow-up questions.
- Threaded turn-index checks to avoid duplicated conversation turn numbers.
- Frontend JavaScript syntax validation.
- Startup verification for `python main.py`.
- Environment handling checks for `.env` override behaviour.

At the time of this report, the repository contains test cache files but does not contain maintainable `tests/*.py` source files. A future project phase should restore or recreate the automated test suite so that the verification steps can be repeated consistently.

# Project Plan and schedules

The project follows the high-level phases required by the attachment report guideline. Because this is a POC within a larger 16-agent programme, the schedule is expressed at feature and milestone level rather than as a full production delivery plan.

| Phase | Activities | Deliverables | Status |
| --- | --- | --- | --- |
| Business Modelling Workflow | Understand invoice, PO, and DO business workflow; identify manual matching pain points; map the POC to the broader DOXA CONNEX agent plan. | Project scope, business context, target users, high-level use cases. | Completed for POC. |
| Requirement Capture Workflow | Define natural-language query requirements, document matching requirements, memory requirements, UI requirements, and safety constraints. | Functional and non-functional requirement summary; query examples; environment requirements. | Completed for POC. |
| Analysis Workflow | Analyse database structure, identify key tables, define agent responsibilities, and determine invoice-item linkage strategy. | Database reference, agent capability model, matching analysis. | Completed for POC. |
| Design Workflow | Design HostAgent orchestration, specialist agent APIs, safe SQL tool, task/session store, memory model, and frontend interaction model. | Architecture design, data model, module structure, route flow. | Completed for POC. |
| Implementation Workflow | Build backend agents, A2A layer, SQL tools, document matching utilities, memory persistence, CLI, and browser frontend. | Working POC codebase. | Completed for POC. |
| Test Workflow | Compile key modules, initialise schema, verify routing, memory, frontend syntax, startup, and selected query flows. | Verification notes in `change_report.md`. | Partially completed; automated tests should be restored. |
| Deployment Workflow | Provide local startup through `python main.py`, environment configuration, and frontend on local port. | Local running application and README instructions. | Completed for local POC; production deployment pending. |

The broader DOXA CONNEX plan describes a four-month delivery model: discovery, design, development, and UAT/production rollout. This POC aligns most closely with the first production candidate from Month 3: **Sprint 1 - Invoice Matching Agent v1**. It also includes supporting infrastructure that would be useful for later agents, such as HostAgent routing, task storage, conversation memory, and frontend history.

# Recommendations

This section states recommendations for the system and future phases of development.

## Short term recommendation

1. **Restore automated tests.** The repository should include source test files for router behaviour, SQL validation, matching logic, memory rewriting, and frontend API behaviour. Current verification is documented, but repeatable tests are necessary before production hardening.

2. **Add deterministic matching tests using realistic fixtures.** Invoice-to-PO and invoice-to-DO matching are business-critical. Tests should cover matched lines, missing PO/DO references, quantity mismatch, amount mismatch, missing invoice, multi-line invoice, and batch matching.

3. **Strengthen SQL validation.** The current validator blocks dangerous keywords and enforces read-only execution. For a stronger safety model, it should be enhanced with a PostgreSQL-aware parser, schema/table allowlist, statement timeout, and row/byte limits at the database level.

4. **Expand schema context carefully.** Text-to-SQL accuracy depends heavily on prompt schema context. More business definitions should be added for invoice status, payment status, supplier naming, buyer naming, currency treatment, and overdue calculations.

5. **Improve user-facing error handling.** Gemini configuration, database connectivity, ambiguous questions, and unsupported business concepts should produce clear user-facing messages and operational logs.

6. **Clarify document matching scope.** PO matching currently checks quantity, unit price, and net amount. DO matching is quantity-based because the current delivery order records do not carry invoice amounts. This distinction should be visible in the UI and reports.

7. **Add role-based access assumptions.** Before integration into Connex, the system should define which user roles can query which company, project, supplier, invoice, PO, and DO records.

## Long term recommendation

1. **Integrate with Connex APIs and authentication.** The local POC should evolve into a service that uses Connex identity, authorisation, tenant boundaries, audit logs, and production API contracts.

2. **Add document AI extraction.** The broader plan mentions AWS Textract for structured document extraction. Future phases should connect uploaded invoice, PO, and DO documents to extracted line-item data and confidence scores.

3. **Build a human-in-the-loop exception workflow.** Production invoice matching should allow finance users to approve matches, reject mismatches, add notes, escalate exceptions, and export audit trails.

4. **Introduce confidence scoring and explainability.** The agent should explain why a match passed or failed, which fields were compared, where values came from, and which records require manual review.

5. **Move from POC memory to governed enterprise memory.** Long-term memory should include privacy controls, retention policies, tenant isolation, deletion workflows, and monitoring for incorrect memory reuse.

6. **Implement observability and cost monitoring.** Production deployment should include request tracing, LLM token usage, latency, error rates, SQL validation failures, routing accuracy, and user feedback metrics.

7. **Extend to the full 16-agent roadmap.** The HostAgent and specialist-agent structure can be reused for RFQ automation, supplier catalogue sync, payment scheduling, financing eligibility, risk monitoring, spend analysis, and support automation.

# Things Learned

This project provided practical learning in both business analysis and technical delivery.

From a business perspective, the project showed that invoice matching is not only a data retrieval problem. It requires understanding the relationship between invoices, purchase orders, delivery orders, suppliers, buyers, payment status, and line-level references. A seemingly simple user question such as "Does this invoice match?" must be translated into several checks: whether the invoice exists, whether line items exist, whether PO and DO references exist, whether linked records are found, and whether quantities and amounts agree.

From a system design perspective, the project showed why multi-agent separation is useful. Invoice analytics, PO analytics, and DO analytics have overlapping but different data sources. Separating them into specialist agents keeps each schema context smaller and makes routing decisions explicit. At the same time, HostAgent orchestration is necessary because real business questions often span more than one domain.

From an AI engineering perspective, the project showed that LLMs are useful for flexible routing, text-to-SQL generation, summarisation, and follow-up rewriting, but deterministic code is still needed for critical business logic. Document matching should not rely only on generative output. The implemented matching utilities use explicit database fields and variance checks, which makes the result more auditable.

From a data safety perspective, the project reinforced the need for layered protection. The analytics databases are opened in read-only mode, generated SQL is validated, dangerous keywords are blocked, and row caps are applied. These safeguards are still POC-level, but they demonstrate the correct direction for production hardening.

From a user experience perspective, the project showed that memory and history are important for a useful business assistant. Users naturally ask follow-up questions such as "What about its PO?" or "What was the previous invoice?". The recent-turn memory and scoped long-term memory features make the assistant feel more practical and reduce the need for repetitive user input.

# Problems and Solutions

This section describes the problems encountered during the project and the solutions applied.

| Problem | Impact | Solution |
| --- | --- | --- |
| Ambiguous user questions | Short follow-up questions may omit the invoice, PO, or DO number. | Added recent-turn memory, follow-up rewriting, entity reference extraction, and long-term memory retrieval. |
| Cross-domain document linkage | PO and DO agents may not have direct access to invoice tables, causing incorrect inferred links. | HostAgent enriches queries using invoice-item UUID linkage and explicitly warns agents not to infer links from plain numbers alone. |
| LLM routing may return malformed JSON | Invalid router output could break routing. | Router normalises structured JSON and falls back to keyword routing for malformed model output. |
| Gemini runtime or authorisation errors | Silent fallback could hide configuration issues. | Runtime and authorisation failures are surfaced as actionable configuration errors. |
| Unsafe model-generated SQL | LLM-generated SQL could include write operations or excessive result sets. | Added SQL validation, forbidden keyword checks, read-only database sessions, and maximum row limits. |
| Conversation turn race conditions | Concurrent requests could receive duplicate turn indexes. | Conversation turn reservation uses database transaction logic to allocate distinct turn indexes. |
| Stale environment variables | Old shell-level values could override the intended `.env` values. | `DOXA_DOTENV_OVERRIDE=1` is used by default for local POC startup. |
| Missing vector extension | Local PostgreSQL may not support pgvector. | Long-term memory falls back to JSONB embeddings, entity matching, and text fallback retrieval. |
| Lack of maintainable test sources | Verification cannot be repeated easily by future developers. | Verification was recorded in `change_report.md`; the next step is to recreate proper `tests/*.py` files. |

# Looking Back

If assigned to a similar project again, the first improvement would be to define a small but complete automated test suite before adding memory and frontend features. The project made significant progress through manual and scripted verification, but source-controlled tests would make future changes safer and easier to review.

The second improvement would be to formalise the business glossary earlier. Terms such as pending, overdue, matched, linked, paid, delivered, received, rejected, and financed may have specific meanings inside Connex. Adding these definitions early would improve text-to-SQL accuracy and reduce ambiguity in user-facing answers.

The third improvement would be to separate POC-only assumptions from production requirements more explicitly. The current code is useful for local demonstration, but production deployment will require tenant isolation, role-based access control, formal audit logging, data retention rules, monitoring, and stronger SQL safety.

The fourth improvement would be to create a small curated dataset for repeatable demonstrations. Realistic fixtures would allow the team to show matching pass/fail cases, missing PO or DO references, overdue invoices, supplier rankings, and follow-up memory behaviour consistently.

# Acknowledgement

The project team would like to acknowledge Doxa Holdings International Pte Ltd. for providing the business context, project direction, and opportunity to explore AI agents for procurement, finance, and logistics workflows. The team also acknowledges the NUS-ISS Graduate Diploma in Systems Analysis programme for providing the industrial attachment structure and guidance for connecting software delivery with business analysis, system design, implementation, testing, and reflection.

# Appendix A

## Phase/Workflow and Deliverables

| Phase/Workflow | Deliverables |
| --- | --- |
| Business Modelling Workflow | Project plan, business use case model survey, business object model survey. |
| Requirement Capture Workflow | Functional requirement specification, non-functional requirement specification, UI design. |
| Analysis Workflow | Analysis models, database structure analysis, agent responsibility model. |
| Design Workflow | Design models, relational database design for task/session/memory store, A2A protocol design, agent orchestration design. |
| Implementation Workflow | Source code for HostAgent, InvoiceAgent, PurchaseOrderAgent, DeliveryOrderAgent, A2A layer, SQL tool, matching tool, storage layer, CLI, and browser frontend. |
| Test Workflow | Test case and test result summary based on compilation, schema initialisation, routing checks, memory checks, frontend syntax validation, and startup verification. |
| Deployment Workflow | Running application through `python main.py`, local agent ports, browser frontend, and environment variable configuration. |
| Others | README, change report, database structure reference, overall DOXA AI agent plan, and final report. |

## Business Modelling Workflow

### Project Plan

The POC supports the DOXA CONNEX AI agent roadmap by implementing the first functional version of the invoice analysis and matching assistant. The broader roadmap targets 16 agents over four months. This POC contributes specifically to the finance and payment domain and also creates reusable infrastructure for later agents.

### Business Use Case Model Survey

| Use case | Primary actor | Expected outcome |
| --- | --- | --- |
| Ask invoice analytics question | Finance user | User receives a summary and supporting result rows. |
| Ask supplier or buyer question | Finance or procurement user | User receives invoice totals, counts, or status breakdowns. |
| Ask purchase order question | Procurement user | User receives PO analytics from purchase data. |
| Ask delivery order question | Logistics or operations user | User receives DO analytics from delivery data. |
| Check invoice against PO and DO | Finance user | User receives a cross-document matching conclusion. |
| Ask follow-up question | Any business user | Agent resolves the reference using recent or long-term memory. |
| Review saved conversation | Any browser user | User reopens prior chat turns from the History panel. |

### Business Object Model Survey

| Business object | Description |
| --- | --- |
| Invoice | Header-level invoice record including status, amount, supplier, buyer, currency, and dates. |
| Invoice Item | Line-level invoice record containing quantities, prices, PO references, and DO references. |
| Supplier | Supplier master data used for supplier-level analysis. |
| Buyer | Buyer master data used for buyer-level analysis. |
| Purchase Order | Header-level PO record used for PO analytics and invoice-to-PO linkage. |
| PO Item | Line-level PO record used for detailed comparison. |
| Delivery Order | Header-level DO record used for delivery analytics and invoice-to-DO linkage. |
| Delivery Order Item | Line-level DO record used for quantity coverage checks. |
| Conversation | A sequence of user and assistant turns under one conversation ID. |
| Long-term Memory | Scoped remembered business facts derived from completed turns. |

## Requirement Capture Workflow

### Requirement Specification (Function Requirements)

| ID | Functional requirement | Implementation reference |
| --- | --- | --- |
| FR-01 | The system shall accept natural-language business questions. | CLI and browser frontend. |
| FR-02 | The system shall route questions to the correct specialist agent. | `agents/host_agent/router.py`, `agents/capabilities.py`. |
| FR-03 | The system shall support invoice analytics. | `agents/invoice_agent/graph.py`. |
| FR-04 | The system shall support purchase order analytics. | `agents/purchase_order_agent/graph.py`. |
| FR-05 | The system shall support delivery order analytics. | `agents/delivery_order_agent/graph.py`. |
| FR-06 | The system shall execute only read-only analytics SQL. | `tools/sql_query.py`. |
| FR-07 | The system shall provide invoice-to-PO and invoice-to-DO matching utilities. | `tools/document_match_query.py`. |
| FR-08 | The system shall store sessions, tasks, messages, artifacts, and conversation turns. | `storage/schema.sql`, `storage/task_store.py`, `storage/memory_store.py`. |
| FR-09 | The system shall support follow-up questions using recent conversation memory. | `agents/host_agent/graph.py`, `storage/memory_store.py`. |
| FR-10 | The system shall support scoped long-term memory. | `agents/host_agent/long_term_memory.py`, `storage/schema.sql`. |
| FR-11 | The system shall show saved conversations in the browser History panel. | `doxa-agent-frontend/index.html`, HostAgent conversation APIs. |

### Requirement Specification (Non Functional)

| ID | Non-functional requirement | Implementation or recommendation |
| --- | --- | --- |
| NFR-01 | Safety | Read-only DB sessions, SQL keyword blocking, row caps. |
| NFR-02 | Traceability | Task, session, message, artifact, and memory persistence. |
| NFR-03 | Configurability | Environment variables documented in README. |
| NFR-04 | Maintainability | Modular agents, tools, storage, CLI, and frontend. |
| NFR-05 | Usability | Natural-language chat interface and saved History panel. |
| NFR-06 | Reliability | Startup port checks and recorded verification. |
| NFR-07 | Scalability | POC uses local processes; future production should use managed deployment and queues. |
| NFR-08 | Security | POC guardrails exist; production requires Connex auth, tenant isolation, and stricter SQL policy. |

### UI Design

The UI design is intentionally simple for POC demonstration:

- A browser chat interface is served on the configured frontend port.
- The left panel shows conversation History.
- A new chat creates a new conversation ID.
- A selected history item loads saved user and assistant turns.
- Deleting a history item removes the conversation memory records from the task-store memory tables.
- CLI users can inspect memory with `memory` and `memory <conversation_id>`.

## Analysis Workflow

### Analysis Models

The main analysis model is a routed multi-agent flow:

```text
User question
  -> HostAgent
  -> Recent and long-term memory retrieval
  -> Route decision
  -> Optional cross-document reference enrichment
  -> Specialist agent execution
  -> SQL validation and read-only query execution
  -> Summarisation
  -> Final report persistence
  -> User response
```

The document matching analysis model uses invoice line items as the authoritative pivot:

```text
Invoice
  -> invoice_item
      -> po_uuid -> purchase_order.uuid
      -> do_uuid -> delivery_order.uuid
```

This avoids unsafe assumptions based only on visible document numbers.

## Design Workflow

### Design Models

| Design area | Design decision |
| --- | --- |
| Agent orchestration | HostAgent is the central router and coordinator. |
| Agent specialisation | Separate InvoiceAgent, PurchaseOrderAgent, and DeliveryOrderAgent. |
| Data access | Read-only PostgreSQL connections for business data. |
| AI use | Gemini for routing, SQL generation, summarisation, embeddings, and follow-up rewriting. |
| Deterministic logic | Matching utilities for invoice-to-PO and invoice-to-DO checks. |
| Persistence | PostgreSQL `invoice_poc_*` tables for sessions, tasks, messages, artifacts, conversations, turns, and memories. |
| Frontend | Lightweight browser chat with local memory scope and History panel. |

### Relational DB Design

The POC does not modify source invoice or purchase data. It creates task and memory tables in the configured task database:

- `invoice_poc_conversations`
- `invoice_poc_sessions`
- `invoice_poc_tasks`
- `invoice_poc_messages`
- `invoice_poc_artifacts`
- `invoice_poc_conversation_turns`
- `invoice_poc_long_term_memories`

These tables support traceability, recent-turn memory, long-term memory, and frontend History.

## Implementation Workflow

### Code

The main implementation files are:

- `main.py`
- `frontend_app.py`
- `a2a/types.py`
- `a2a/client.py`
- `a2a/server.py`
- `a2a/registry.py`
- `agents/capabilities.py`
- `agents/host_agent/graph.py`
- `agents/host_agent/router.py`
- `agents/host_agent/long_term_memory.py`
- `agents/invoice_agent/graph.py`
- `agents/purchase_order_agent/graph.py`
- `agents/delivery_order_agent/graph.py`
- `tools/sql_query.py`
- `tools/document_match_query.py`
- `tools/gemini_sql.py`
- `storage/schema.sql`
- `storage/task_store.py`
- `storage/memory_store.py`
- `cli/chat.py`
- `doxa-agent-frontend/index.html`

## Test Workflow

### Test Case and Test Result

| Test area | Result summary |
| --- | --- |
| Python compilation | Key modules compiled successfully according to `change_report.md`. |
| Database initialisation | `init_db()` successfully applied schemas during verification. |
| Router behaviour | Malformed Gemini routing JSON falls back to keyword routing; critical Gemini configuration errors are surfaced. |
| Conversation turn allocation | Concurrent turn allocation produced distinct turn indexes during local threaded verification. |
| Follow-up rewriting | Query rewrite checks confirmed correct handling of references such as "What about its PO?". |
| Frontend syntax | Inline JavaScript syntax validation passed. |
| Startup | `python main.py` reached CLI and started local agents/frontend after stale processes were stopped. |
| Long-term memory | Schema and fallback retrieval were verified; pgvector absence did not block functionality. |

## Deployment Workflow

### Running application

The local POC is run with:

```bash
python main.py
```

The default local services are:

| Service | Default URL |
| --- | --- |
| HostAgent | `http://127.0.0.1:10000` |
| InvoiceAgent | `http://127.0.0.1:10001` |
| PurchaseOrderAgent | `http://127.0.0.1:10002` |
| DeliveryOrderAgent | `http://127.0.0.1:10003` |
| Browser frontend | `http://127.0.0.1:8080` |

The required configuration includes PostgreSQL connection details and `GEMINI_API_KEY`.

## Others

Other deliverables unique to the project include:

- `README.md` for setup, architecture, safety model, and limitations.
- `overall_plan.md` for the broader DOXA CONNEX AI agent strategy.
- `database_structure.md` for source database reference.
- `change_report.md` for implementation and verification history.

# Appendix B

## Progress Reports and Project Plans/Schedules

The attachment guideline refers to 20 weekly progress reports. The available repository contains implementation change reports for several key milestones rather than 20 separate weekly reports. The table below adapts the required progress-report appendix to the POC evidence available in the repository and the broader four-month project schedule.

| Week | Progress summary | Deliverable or evidence |
| --- | --- | --- |
| 1 | Reviewed overall DOXA CONNEX AI agent plan and identified invoice matching as a finance and payment priority. | `overall_plan.md`. |
| 2 | Studied invoice, PO, DO, supplier, buyer, and task-store database structures. | `database_structure.md`. |
| 3 | Defined POC scope and natural-language query examples. | `README.md`. |
| 4 | Designed multi-agent architecture with HostAgent and specialist agents. | `README.md`, `agents/capabilities.py`. |
| 5 | Implemented A2A protocol layer and local agent service structure. | `a2a/`, `agents/*/server.py`. |
| 6 | Implemented InvoiceAgent text-to-SQL analytics. | `agents/invoice_agent/graph.py`. |
| 7 | Implemented PurchaseOrderAgent and DeliveryOrderAgent analytics. | `agents/purchase_order_agent/graph.py`, `agents/delivery_order_agent/graph.py`. |
| 8 | Implemented SQL safety checks and read-only query execution. | `tools/sql_query.py`. |
| 9 | Implemented deterministic invoice-to-PO and invoice-to-DO matching utilities. | `tools/document_match_query.py`. |
| 10 | Implemented HostAgent routing and multi-agent response composition. | `agents/host_agent/graph.py`, `agents/host_agent/router.py`. |
| 11 | Added task and session persistence. | `storage/schema.sql`, `storage/task_store.py`. |
| 12 | Added recent-turn conversation memory MVP. | `change_report.md` dated 2026-07-02. |
| 13 | Hardened conversation memory and added frontend History. | `change_report.md` dated 2026-07-03. |
| 14 | Added scoped long-term memory and memory APIs. | `change_report.md` dated 2026-07-06. |
| 15 | Updated README, environment handling, and runtime configuration notes. | `README.md`, `.env.example` references. |
| 16 | Verified startup, route registration, schema initialisation, and memory behaviours. | `change_report.md`. |
| 17 | Prepared final report structure according to the industrial attachment report requirement. | `Final_Report.md`. |
| 18 | Recommended automated test restoration and production security hardening. | Recommendations section. |
| 19 | Recommended Connex integration, document AI extraction, and human-in-loop workflow. | Recommendations section. |
| 20 | Recommended expansion path from this POC to the wider 16-agent roadmap. | Recommendations section and `overall_plan.md`. |

## Project Plans/Schedules

The POC should be viewed as the foundation for the Invoice Matching Agent v1 in the broader roadmap:

| Month | Planned focus from overall programme | Relationship to this POC |
| --- | --- | --- |
| Month 1 | Discovery, stakeholder interviews, workflow mapping, use-case prioritisation. | POC uses the invoice matching priority and business workflow assumptions. |
| Month 2 | BRD, UX design, agent architecture, API specification, security review. | POC implements initial architecture and frontend flow but does not replace formal BRD/security review. |
| Month 3 | Agile development of high/medium priority agents, including Invoice Matching Agent v1. | POC implements the local first version of invoice analysis and matching capability. |
| Month 4 | UAT, performance testing, training, phased production rollout. | POC provides a basis for UAT planning but still requires production hardening. |

