# SA61 INDUSTRIAL ATTACHMENT REPORT

Project Title: AI-Powered Invoice Analysis and Document Matching Agent POC

Students: Project Team / To be filled

Organisation:        Doxa Holdings International Pte Ltd.

IN PARTIAL FULFILLMENT OF THE REQUIREMENTS FOR THE

GRADUATE DIPLOMA IN SYSTEMS ANALYSIS

July 2026

NUS-ISS

NATIONAL UNIVERSITY OF SINGAPORE

---

# Contents in the Industrial attachment Report

1. Introduction
   - Project Background
2. Overview of Activities
   - Project Plan and schedules
   - Phases / activities / deliverables (high level description ONLY!)
3. Recommendations
   - Short term recommendation
   - Long term recommendation
4. Things Learned
5. Problems and Solutions
6. Looking Back
7. Acknowledgement
8. Appendix A
9. Appendix B

---

# Introduction

This industrial attachment project delivered a proof of concept for an AI-powered invoice analysis and document matching agent for Doxa's procurement, finance, and logistics workflows. The project is one functional module within the broader DOXA CONNEX AI agent programme. It focuses on the invoice matching capability under the finance and payment domain, allowing users to query invoice, purchase order (PO), and delivery order (DO) data through natural language and receive explainable business analysis.

The implemented system is a local multi-agent application. Users can ask business questions through a command-line interface or a browser chat interface. HostAgent routes each request to the appropriate specialist agent, including InvoiceAgent, PurchaseOrderAgent, and DeliveryOrderAgent. The specialist agents convert natural-language questions into read-only PostgreSQL queries, execute validated database queries, and return business-oriented summaries. For cross-document questions, the system coordinates multiple agents and uses invoice line-item reference fields as the authoritative linkage between invoices, POs, and DOs.

The purpose of this project is not to replace the full DOXA CONNEX production platform immediately. Instead, it validates the feasibility of multi-agent orchestration, natural-language data access, deterministic document matching, conversation memory, long-term memory, task traceability, and a lightweight user interface. These capabilities provide a foundation for a future production-ready invoice matching agent.

## Project Background

The DOXA CONNEX AI agent strategy includes 16 agents across procurement, finance and payment, deep-tier financing, logistics and delivery, compliance and risk, analytics and reporting, and customer success. The invoice matching agent belongs to the finance and payment domain. Its business value is to automate three-way or four-way matching, reduce manual checking, explain exceptions, and shorten invoice processing time from days to hours.

This POC is a functional implementation of that strategy. It connects to existing PostgreSQL data sources, reads invoice, PO, and DO records, exposes multiple agent services through a lightweight A2A HTTP protocol, and supports questions such as:

- Which invoices have been pending for more than 60 days?
- Which suppliers have the highest invoice amounts?
- Which purchase orders have the highest value?
- Which delivery orders are still pending?
- Does a specific invoice match its related PO and DO?
- What about its PO or DO after a previous question?

The system uses a modular architecture:

```text
CLI / Browser Frontend
  -> HostAgent
       -> InvoiceAgent
       -> PurchaseOrderAgent
       -> DeliveryOrderAgent
  -> PostgreSQL task/session/conversation/memory store
```

HostAgent handles intent routing, memory handling, cross-agent coordination, and final response composition. InvoiceAgent handles invoice, supplier, buyer, payment status, and amount analysis. PurchaseOrderAgent handles purchase order analysis. DeliveryOrderAgent handles delivery order analysis. The deterministic document matching tool checks invoice-to-PO and invoice-to-DO matching based on invoice item fields and UUID linkage.

The project aligns with the DOXA roadmap as follows:

| Overall programme item | POC contribution |
| --- | --- |
| Finance and payment: Invoice Matching Agent | Implements the first working natural-language invoice analysis and document matching POC. |
| Agent orchestration | Implements HostAgent routing and specialist-agent dispatch. |
| PostgreSQL data foundation | Reads invoice, PO, and DO data from configured invoice and purchase databases. |
| Human-facing agent UI | Provides both CLI and browser chat interfaces. |
| Auditability and memory | Persists sessions, tasks, messages, artifacts, conversation turns, and memory records. |
| Future Connex integration foundation | Uses modular APIs, environment-based configuration, and frontend/backend separation. |

# Overview of Activities

The project activities covered business understanding, requirement capture, system analysis, architecture design, implementation, UI development, verification, and documentation.

**Business and workflow understanding**

The project first analysed where invoice analysis fits within the DOXA CONNEX AI agent landscape. Invoice matching is a high-priority finance and payment capability because manual invoice checking requires users to cross-reference multiple systems and documents, which is time-consuming and error-prone.

The key business tables used by this POC include:

- `public.invoice`
- `public.invoice_item`
- `public.supplier_information`
- `public.buyer_information`
- `public.purchase_order`
- `public.po_item`
- `public.delivery_order`
- `public.delivery_order_item`

The analysis identified `invoice_item` as the core pivot for document matching because it contains the PO and DO reference fields needed to connect invoice line items to procurement and delivery records.

**Requirement capture**

The business goals were translated into the following POC functional requirements:

- Support natural-language invoice analysis.
- Support natural-language PO and DO analysis.
- Route each request to the correct specialist agent through HostAgent.
- Support multi-agent collaboration for cross-domain questions.
- Generate, validate, and execute read-only SQL.
- Provide deterministic invoice-to-PO and invoice-to-DO matching.
- Provide a browser chat interface with conversation History.
- Support recent-turn memory for follow-up questions.
- Support scoped long-term memory across conversations.
- Persist sessions, tasks, messages, artifacts, and conversation turns for traceability.

The main non-functional requirements were safety, traceability, maintainability, and local operability:

- Business data sources are accessed through read-only database connections.
- Generated SQL is validated to block write operations, DDL, and administrative statements.
- Query result sizes are capped to avoid accidental large result sets.
- Database connections, ports, Gemini API key, and memory settings are configured through environment variables.
- HostAgent, specialist agents, tools, storage, and frontend are separated into clear modules.
- Session and memory data are stored in separate `invoice_poc_*` tables for audit and debugging.

**Analysis and design**

The project uses a multi-agent architecture instead of a single monolithic chatbot. This design fits the long-term DOXA CONNEX roadmap because additional business domains can be added as independent specialist agents.

The main design decisions were:

- Use HostAgent as the unified entry point for user requests.
- Use `agents/capabilities.py` to describe each specialist agent's responsibility boundary.
- Use Gemini for routing, SQL generation, summarisation, embeddings, and follow-up rewriting.
- Use deterministic code for critical document matching logic rather than relying only on generated responses.
- Access invoice and purchase data sources in read-only mode.
- Store task, session, message, result, recent memory, and long-term memory data in PostgreSQL.
- Use a simple browser chat interface and History panel for demonstration and business validation.

**Implementation work**

The project implemented the following major components:

| Component | Description |
| --- | --- |
| `main.py` | Starts HostAgent, specialist agents, frontend, database initialisation, and CLI. |
| `a2a/` | Defines lightweight agent-to-agent request, response, task, message, and artifact models. |
| `agents/host_agent/` | Implements routing, orchestration, report composition, recent memory, and long-term memory handling. |
| `agents/invoice_agent/` | Implements invoice analysis with Gemini text-to-SQL and summarisation. |
| `agents/purchase_order_agent/` | Implements purchase order analysis. |
| `agents/delivery_order_agent/` | Implements delivery order analysis. |
| `tools/sql_query.py` | Provides safe read-only SQL validation and execution. |
| `tools/document_match_query.py` | Provides deterministic invoice-to-PO and invoice-to-DO matching utilities. |
| `storage/` | Provides PostgreSQL schema and persistence for sessions, tasks, and memory. |
| `cli/chat.py` | Provides the interactive command-line chat interface. |
| `frontend_app.py` and `doxa-agent-frontend/index.html` | Provide the browser chat UI and History panel. |

**User interface and interaction flow**

Users can run the local POC with:

```bash
python main.py
```

On startup, the system initialises the task database and starts HostAgent, InvoiceAgent, PurchaseOrderAgent, DeliveryOrderAgent, and the browser frontend. Users can ask natural-language questions in either the CLI or the browser. For example, when a user asks "Which invoices have been pending for more than 60 days?", HostAgent routes the request to InvoiceAgent. When a user asks "Check invoice INV-00000001 and its related PO and DO", HostAgent coordinates multiple specialist agents and produces a combined response.

The browser frontend also maintains a local conversation scope and shows saved conversations in the left History panel. Users can reopen historical conversations and delete saved conversation records. This makes the POC closer to a practical business assistant rather than a one-off query tool.

**Verification activities**

The project completed the following verification activities:

- Compiled key Python modules.
- Verified that `init_db()` can apply the database schema.
- Verified HostAgent API route registration.
- Verified fallback behaviour when Gemini routing output is malformed.
- Verified follow-up rewriting for questions such as "What about its PO?".
- Verified that concurrent requests do not duplicate conversation turn indexes.
- Validated inline frontend JavaScript syntax.
- Verified that `python main.py` can start the local agents and frontend.
- Verified that `.env` override prevents stale shell environment variables from affecting runtime configuration.

At the time of this report, the repository contains test cache files but does not contain maintainable `tests/*.py` source files. A future phase should restore or recreate the automated test suite so routing, SQL safety, matching logic, memory behaviour, and frontend APIs can be validated repeatedly.

## Project Plan and schedules

The actual project timeline ran from Week 1 to Week 18. The work started with LLM, RAG, Chain, and Agent capability validation, then moved into business process analysis, A2A multi-agent architecture design, local POC implementation, invoice data integration, PO/DO matching, browser frontend development, and conversation memory. The schedule shows a progression from technical feasibility validation to business POC delivery.

| Week | Date range | Main work focus | Main deliverables / results |
| --- | --- | --- | --- |
| Week 1 | 2026-03-02 to 2026-03-06 | Set up the project environment and validated Gemini, Anthropic, Chain, RAG, and tool-using Agent prototypes. | LLM call validation, Chain prototype, RAG Q&A flow, Agent tool-calling prototype. |
| Week 2 | 2026-03-09 to 2026-03-13 | Reviewed Prompt, structured output, RAG, multi-model integration, and the management plan for 16 agents. | Core AI capability review, design deliverables list, interview template, Agent board draft. |
| Week 3 | 2026-03-13 to 2026-03-19 | Implemented a production-style RAG flow with CSV loading, text splitting, embeddings, vector persistence, and continuous conversation. | Reusable RAG flow, session entry point, retrieval logs, and fallback mechanism. |
| Week 4 | 2026-03-20 to 2026-03-26 | Analysed Procure-to-Pay, subcontractor processes, business roles, core scenarios, and Agent responsibility boundaries. | End-to-end workflow understanding, Concierge and specialist Agent collaboration model, team task split. |
| Week 5 | 2026-03-27 to 2026-04-02 | Deepened business process and database understanding, and refined RFQ, PO, receiving, invoice matching, and payment scheduling requirements. | Procurement module requirements, 3-5 single-responsibility Agent plan, infrastructure execution sequence. |
| Week 6 | 2026-04-03 to 2026-04-09 | Validated the procure-to-pay document loop and designed the Doxa Connex multi-agent architecture and security boundary. | Multi-agent architecture, A2A/Bedrock/Pinecone/Aurora choices, JWT/RBAC design, four-phase roadmap. |
| Week 7 | 2026-04-10 to 2026-04-16 | Designed the A2A POC scenario and created a local implementation plan based on LangChain, LangGraph, and A2A. | A2A POC business design, technical architecture review, VPC/JWT/RBAC security design updates. |
| Week 8 | 2026-04-17 to 2026-04-23 | Froze the A2A POC architecture and completed local implementation, protocol structures, orchestration, mock queries, state tables, and end-to-end validation. | A2A protocol data structures, Orchestrator and child Agents, PostgreSQL state tables, Docker Compose local validation. |
| Week 9 | 2026-04-24 to 2026-04-30 | Progressed ECS Fargate, Cloud Map, API Gateway, Lambda Authorizer, NLB, and Aurora permission preparation. | Infrastructure preparation, call-chain design, Invoice/Entity API samples, blocker summary. |
| Week 10 | 2026-05-01 to 2026-05-07 | Scoped the AML A2A POC and designed the Host, Market, and Transaction three-agent collaboration model. | AML POC scope, technology choices, LangGraph dispatch loop, SQLite state tables, risk report demo flow. |
| Week 11 | 2026-05-08 to 2026-05-14 | Completed AML multi-agent specifications, AgentCards, A2A messages, state transitions, and demo path, then shifted focus to invoice data. | Executable-level specifications, two-stage validation plan, sample data, invoice data direction. |
| Week 12 | 2026-05-18 to 2026-05-22 | Started the Invoice Analysis POC, analysed PostgreSQL database structure, and implemented task/session storage and the Host/Invoice A2A loop. | Invoice database analysis, PostgreSQL task/session store, three invoice query scenarios, interactive CLI. |
| Week 13 | 2026-05-25 to 2026-05-29 | Completed the natural-language-to-SQL-to-summary flow and added read-only query execution and forbidden keyword blocking. | End-to-end text-to-SQL flow, safe SQL execution, task/session tracking, four demo query scenarios. |
| Week 14 | 2026-06-01 to 2026-06-05 | Prepared Invoice Agent demos, reviewed key invoice workflows and multi-role views, and selected PO/DO capability as the next focus. | Complex query demo, invoice workflow review, Buyer login and multi-role requirements, PO/DO next plan. |
| Week 15 | 2026-06-08 to 2026-06-12 | Added PurchaseOrderAgent and DeliveryOrderAgent, and implemented deterministic Invoice-to-PO/DO matching plus two-way and three-way orchestration. | PO/DO natural-language analysis, deterministic matching logic, batch matching, 15 regression tests. |
| Week 16 | 2026-06-15 to 2026-06-19 | Fixed CLI rendering, standardised Router JSON output, and improved Top-N summaries, document matching routing, and PO-to-DO context. | Stable CLI output, Router contract, calibrated matching result wording, stability closure before frontend work. |
| Week 17 | 2026-06-22 to 2026-06-28 | Built the browser frontend, connected HostAgent SSE streaming, and implemented Live/Demo modes, result rendering, responsive layout, and CORS hardening. | Browser chat UI, History interaction foundation, SSE communication, SQL/table/error rendering, frontend runtime configuration. |
| Week 18 | 2026-06-29 to 2026-07-06 | Designed and implemented conversation_id-based multi-turn memory, recent context, History, memory_scope_id, and long-term memory. | Conversation and turn tables, follow-up rewriting, browser History, memory isolation, long-term memory, concurrency and regression verification. |

The overall plan can be summarised into four phases: Week 1-6 covered AI capability validation and business modelling; Week 7-11 covered A2A and multi-agent architecture design with preliminary POCs; Week 12-16 delivered the core Invoice Analysis POC; and Week 17-18 completed the frontend, conversation history, and memory capabilities.

## Phases / activities / deliverables (high level description ONLY!)

| Phase/Workflow | Weeks | Activities | Deliverables |
| --- | --- | --- | --- |
| Business Modelling Workflow | Week 1-6 | Validated LLM, RAG, Chain, and Agent tool-calling capabilities, and analysed Procure-to-Pay, subcontractor processes, procurement modules, and invoice matching business background. | AI capability validation, business workflow understanding, Agent responsibility boundaries, initial project roadmap. |
| Requirement Capture Workflow | Week 2-7 | Collected BRD, architecture, data model, API, security, KPI, RFQ, PO, receiving, invoice matching, and payment scheduling requirements. | Functional requirements, non-functional requirements, security and permission requirements, Agent board draft. |
| Analysis Workflow | Week 4-12 | Analysed business roles, core scenarios, database structures, A2A interaction flows, and PostgreSQL data sources required by the Invoice Analysis POC. | Business object analysis, database structure analysis, invoice query scenarios, Host/Invoice A2A loop. |
| Design Workflow | Week 6-11 | Designed the Doxa Connex multi-agent architecture, A2A POC, LangChain/LangGraph orchestration, state tables, JWT/RBAC, security boundary, and AML preliminary POC. | Multi-agent architecture design, A2A protocol structure, state storage model, demo path. |
| Implementation Workflow | Week 8-18 | Implemented the A2A prototype, Invoice Analysis POC, PO/DO agents, deterministic matching, browser frontend, conversation history, and long-term memory. | Runnable local POC, CLI, browser frontend, PO/DO matching, and memory capability. |
| Test Workflow | Week 12-18 | Verified invoice queries, SQL safety, A2A calls, PO/DO matching, frontend rendering, memory rewriting, concurrency, and regression scenarios. | Query demos, 15 regression tests, concurrency verification, frontend syntax and runtime verification. |
| Deployment Workflow | Week 17-18 | Connected the frontend to the main startup flow and refined runtime configuration, URL discovery, CORS, default ports, and local execution. | `python main.py` local startup, browser frontend, runtime configuration, and user instructions. |

# Recommendations

This section provides recommendations for the system and future development phases.

## Short term recommendation

1. **Restore automated tests.** The repository should include source test files for routing, SQL validation, matching logic, memory rewriting, and frontend APIs. Current verification is useful, but repeatable tests are required before production hardening.

2. **Add realistic fixtures for matching logic.** Invoice-to-PO and invoice-to-DO matching are business-critical. Test data should cover full matches, missing PO/DO references, quantity mismatch, amount mismatch, missing invoices, multi-line invoices, and batch matching.

3. **Strengthen SQL safety.** The current system blocks dangerous keywords and uses read-only database connections. Future work should add a PostgreSQL-aware parser, schema/table allowlists, statement timeouts, and row/byte limits at the database level.

4. **Improve schema context and business definitions.** Text-to-SQL accuracy depends heavily on schema prompts. The system should define invoice status, payment status, supplier, buyer, currency, overdue logic, and other business terms more explicitly.

5. **Improve user-facing error messages.** Gemini configuration errors, database connection failures, ambiguous questions, and unsupported business concepts should return clear and actionable messages.

6. **Clarify document matching boundaries.** PO matching checks quantity, unit price, and net amount. DO matching is currently quantity-based because current DO data does not carry invoice amount fields. This distinction should be visible in the UI and reports.

7. **Define role and data access assumptions.** Before Connex integration, the system should define which roles can access which company, project, supplier, invoice, PO, and DO records.

## Long term recommendation

1. **Integrate with Connex APIs and authentication.** The local POC should evolve into a service that uses Connex identity, authorisation, tenant boundaries, audit logs, and production API contracts.

2. **Add document AI extraction.** Future phases should support invoice, PO, and DO document upload, structured line-item extraction, and confidence scores.

3. **Build a human-in-the-loop exception workflow.** Production invoice matching should allow finance users to approve matches, reject mismatches, add notes, escalate exceptions, and export audit records.

4. **Introduce confidence scoring and explainability.** The system should explain why a match passed or failed, which fields were compared, where the values came from, what variances were found, and which records require manual review.

5. **Upgrade POC memory into governed enterprise memory.** Long-term memory needs privacy controls, retention rules, tenant isolation, deletion workflows, and monitoring for incorrect memory reuse.

6. **Add observability and cost monitoring.** Production deployment should monitor request traces, LLM token usage, latency, error rate, SQL validation failures, routing accuracy, and user feedback.

7. **Expand toward the 16-agent roadmap.** The HostAgent and specialist-agent structure can be reused for RFQ automation, supplier catalogue synchronisation, payment scheduling, financing eligibility, risk monitoring, spend analysis, and support automation.

# Things Learned

This project provided practical learning in business analysis, system design, and AI engineering.

From a business perspective, invoice matching is not just a data retrieval problem. It requires understanding the relationships among invoices, purchase orders, delivery orders, suppliers, buyers, payment status, and line-item references. A simple question such as "Does this invoice match?" involves multiple checks: whether the invoice exists, whether line items exist, whether PO and DO references exist, whether linked records can be found, whether quantities match, whether amounts match, and whether manual review is needed.

From a system design perspective, the multi-agent architecture has clear value. Invoice analysis, PO analysis, and DO analysis use different data sources and business semantics. Separating them into specialist agents keeps each schema context smaller and each responsibility clearer. At the same time, real business questions often cross domain boundaries, so HostAgent orchestration is still required for routing and result integration.

From an AI engineering perspective, LLMs are useful for flexible routing, text-to-SQL, summarisation, and follow-up rewriting. However, critical business logic should not rely entirely on generated output. Document matching requires deterministic computation and clear data provenance, so the project uses explicit database fields and variance checks to make results more auditable.

From a data safety perspective, the project reinforced the need for layered protection. The system uses read-only database connections, SQL validation, dangerous keyword blocking, and result row limits. These are still POC-level controls, but they show the correct direction for production hardening.

From a user experience perspective, memory and conversation history are important for a useful business assistant. Users naturally ask follow-up questions such as "What about its PO?" or "What was the previous invoice status?". Recent-turn memory and scoped long-term memory make the system closer to a real business assistant and reduce repeated user input.

# Problems and Solutions

This section describes the problems encountered during the project and the solutions applied.

| Problem | Impact | Solution |
| --- | --- | --- |
| Ambiguous user questions | Follow-up questions may omit invoice, PO, or DO identifiers. | Added recent-turn memory, follow-up rewriting, entity reference extraction, and long-term memory retrieval. |
| Cross-domain document linkage can be incorrect | PO/DO agents may not directly access invoice tables and could infer relationships incorrectly. | HostAgent enriches context using invoice item UUID linkage and prevents agents from relying only on display numbers. |
| LLM router output may be malformed | Invalid routing output can prevent request dispatch. | Router normalises JSON and falls back to keyword routing when model output is malformed. |
| Gemini runtime or authorisation errors | Silent fallback could hide configuration problems. | Runtime and authorisation failures are returned as actionable configuration errors. |
| Model-generated SQL can be risky | Generated SQL may include write operations, DDL, or excessive result sets. | Added SQL validation, forbidden keyword blocking, read-only database sessions, and maximum row limits. |
| Concurrent turn indexes can collide | Concurrent requests in one conversation may produce duplicate turn indexes. | Conversation turn reservation uses database transactions to ensure unique turn indexes. |
| Stale environment variables can override `.env` values | Runtime may use outdated Gemini keys or database settings. | Local startup uses `DOXA_DOTENV_OVERRIDE=1` by default. |
| Local PostgreSQL may not have pgvector | Semantic retrieval may be limited. | Long-term memory falls back to JSONB embeddings, entity matching, and text matching. |
| Maintainable test source files are missing | Future development cannot easily repeat verification. | Current verification is captured as milestone results; future work should recreate `tests/*.py`. |

# Looking Back

If assigned to a similar project again, the first improvement would be to create a small but complete automated test suite before adding memory and frontend features. The project completed many manual and scripted verification steps, but source-controlled tests would make later changes safer.

The second improvement would be to define a business glossary earlier. Terms such as pending, overdue, matched, linked, paid, delivered, received, rejected, and financed may have specific meanings inside Connex. Clarifying those definitions early would improve text-to-SQL accuracy and reduce ambiguity in user-facing answers.

The third improvement would be to separate POC assumptions from production requirements more clearly. The current system is suitable for local demonstration, but production deployment requires tenant isolation, role-based permissions, formal audit logging, data retention policies, monitoring, and stronger SQL safety.

The fourth improvement would be to prepare a small repeatable demonstration dataset. Realistic fixtures would make it easier to consistently demonstrate matching pass, matching failure, missing PO/DO, overdue invoices, supplier ranking, and follow-up memory scenarios.

# Acknowledgement

The project team would like to thank Doxa Holdings International Pte Ltd. for providing the business context, project direction, and opportunity to explore AI agents in procurement, finance, and logistics workflows. The team also thanks the NUS-ISS Graduate Diploma in Systems Analysis programme for providing the industrial attachment framework that connects business analysis, system design, implementation, testing, and reflection.

# Appendix A

**Phase/Workflow and Deliverables**

| Phase/Workflow | Deliverables |
| --- | --- |
| Business Modelling Workflow | Project plan, business use case model survey, business object model survey. |
| Requirement Capture Workflow | Functional requirement specification, non-functional requirement specification, UI design. |
| Analysis Workflow | Analysis models, database structure analysis, agent responsibility model. |
| Design Workflow | Design models, relational database design for task/session/memory store, A2A protocol design, agent orchestration design. |
| Implementation Workflow | HostAgent, InvoiceAgent, PurchaseOrderAgent, DeliveryOrderAgent, A2A layer, SQL tool, matching tool, storage layer, CLI, and browser frontend code. |
| Test Workflow | Test result summary based on compilation, schema initialisation, routing checks, memory checks, frontend syntax validation, and startup verification. |
| Deployment Workflow | Local application execution through `python main.py`, local agent ports, browser frontend, and environment variable configuration. |
| Others | README, change log, database structure reference, overall DOXA AI agent plan, and final report. |

**Business Modelling Workflow**

**Project Plan**

This POC supports the DOXA CONNEX AI agent roadmap by implementing the first runnable version of the invoice analysis and matching assistant. The overall roadmap targets 16 agents across four months. This POC focuses on the finance and payment domain while also creating reusable infrastructure for later agents.

**Business Use Case Model Survey**

| Use case | Primary actor | Expected outcome |
| --- | --- | --- |
| Ask an invoice analysis question | Finance user | User receives a summary and supporting result rows. |
| Ask supplier or buyer questions | Finance or procurement user | User receives invoice totals, counts, or status breakdowns. |
| Ask purchase order questions | Procurement user | User receives PO analysis results. |
| Ask delivery order questions | Logistics or operations user | User receives DO analysis results. |
| Check invoice matching against PO/DO | Finance user | User receives a cross-document matching conclusion. |
| Ask a follow-up question | Any business user | Agent resolves the reference using recent or long-term memory. |
| Review conversation history | Browser user | User reopens previous turns from the History panel. |

**Business Object Model Survey**

| Business object | Description |
| --- | --- |
| Invoice | Header-level invoice record including status, amount, supplier, buyer, currency, and dates. |
| Invoice Item | Line-level invoice record containing quantity, price, PO reference, and DO reference. |
| Supplier | Supplier master data used for supplier-level analysis. |
| Buyer | Buyer master data used for buyer-level analysis. |
| Purchase Order | PO header record used for PO analysis and invoice-to-PO linkage. |
| PO Item | PO line record used for detailed comparison. |
| Delivery Order | DO header record used for delivery analysis and invoice-to-DO linkage. |
| Delivery Order Item | DO line record used for quantity coverage checks. |
| Conversation | A set of user and assistant turns under one conversation ID. |
| Long-term Memory | Scoped memory derived from completed business turns. |

**Requirement Capture Workflow**

**Requirement Specification (Function Requirements)**

| ID | Functional requirement | Implementation reference |
| --- | --- | --- |
| FR-01 | The system shall accept natural-language business questions. | CLI and browser frontend. |
| FR-02 | The system shall route questions to the correct specialist agent. | `agents/host_agent/router.py`, `agents/capabilities.py`. |
| FR-03 | The system shall support invoice analysis. | `agents/invoice_agent/graph.py`. |
| FR-04 | The system shall support purchase order analysis. | `agents/purchase_order_agent/graph.py`. |
| FR-05 | The system shall support delivery order analysis. | `agents/delivery_order_agent/graph.py`. |
| FR-06 | The system shall execute only read-only analytics SQL. | `tools/sql_query.py`. |
| FR-07 | The system shall provide invoice-to-PO and invoice-to-DO matching utilities. | `tools/document_match_query.py`. |
| FR-08 | The system shall store sessions, tasks, messages, artifacts, and conversation turns. | `storage/schema.sql`, `storage/task_store.py`, `storage/memory_store.py`. |
| FR-09 | The system shall support follow-up questions using recent conversation memory. | `agents/host_agent/graph.py`, `storage/memory_store.py`. |
| FR-10 | The system shall support scoped long-term memory. | `agents/host_agent/long_term_memory.py`, `storage/schema.sql`. |
| FR-11 | The system shall show saved conversations in the browser History panel. | `doxa-agent-frontend/index.html`, HostAgent conversation APIs. |

**Requirement Specification (Non Functional)**

| ID | Non-functional requirement | Implementation or recommendation |
| --- | --- | --- |
| NFR-01 | Safety | Read-only database sessions, SQL keyword blocking, row caps. |
| NFR-02 | Traceability | Task, session, message, artifact, and memory persistence. |
| NFR-03 | Configurability | Environment variable based configuration. |
| NFR-04 | Maintainability | Modular agents, tools, storage, CLI, and frontend. |
| NFR-05 | Usability | Natural-language chat interface and saved conversation History. |
| NFR-06 | Reliability | Startup port checks and verification records. |
| NFR-07 | Scalability | Current version is a local POC; production should use managed deployment and queues. |
| NFR-08 | Security and compliance | POC guardrails exist; production requires Connex auth, tenant isolation, and stricter SQL policy. |

**UI Design**

The POC UI is intentionally simple for demonstration and validation:

- The browser chat interface runs on the configured frontend port.
- The left panel shows conversation History.
- New chat creates a new conversation ID.
- Selecting a history item loads saved user and assistant turns.
- Deleting a history item removes the conversation records from the task-store memory tables.
- CLI users can inspect memory using `memory` or `memory <conversation_id>`.

**Analysis Workflow**

**Analysis Models**

The main analysis model is a routed multi-agent flow:

```text
User question
  -> HostAgent
  -> Retrieve recent and long-term memory
  -> Route decision
  -> Optional cross-document reference enrichment
  -> Specialist agent execution
  -> SQL validation and read-only query execution
  -> Summarisation
  -> Final report persistence
  -> User response
```

The document matching model uses invoice line items as the authoritative pivot:

```text
Invoice
  -> invoice_item
      -> po_uuid -> purchase_order.uuid
      -> do_uuid -> delivery_order.uuid
```

This model avoids inferring relationships only from visible document numbers and reduces incorrect matching risk.

**Design Workflow**

**Design Models**

| Design area | Design decision |
| --- | --- |
| Agent orchestration | HostAgent acts as the central router and coordinator. |
| Agent specialisation | InvoiceAgent, PurchaseOrderAgent, and DeliveryOrderAgent are separated. |
| Data access | Business data is accessed through read-only PostgreSQL connections. |
| AI use | Gemini is used for routing, SQL generation, summarisation, embeddings, and follow-up rewriting. |
| Deterministic logic | Matching utilities perform invoice-to-PO and invoice-to-DO checks. |
| Persistence | PostgreSQL `invoice_poc_*` tables store sessions, tasks, messages, artifacts, conversation turns, and memories. |
| Frontend | Lightweight browser chat UI with local memory scope and History panel. |

**Relational DB Design**

The POC does not modify source invoice or purchase data. The system creates the following tables in the configured task database:

- `invoice_poc_conversations`
- `invoice_poc_sessions`
- `invoice_poc_tasks`
- `invoice_poc_messages`
- `invoice_poc_artifacts`
- `invoice_poc_conversation_turns`
- `invoice_poc_long_term_memories`

These tables support traceability, recent-turn memory, long-term memory, and browser History.

**Implementation Workflow**

**Code**

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

**Test Workflow**

**Test Case and Test Result**

| Test area | Result summary |
| --- | --- |
| Python compilation | Key modules compiled successfully. |
| Database initialisation | `init_db()` successfully applied schema during verification. |
| Routing behaviour | Malformed Gemini routing JSON falls back safely; critical configuration errors are surfaced. |
| Conversation turn allocation | Local concurrency verification confirmed that turn indexes are not duplicated. |
| Follow-up rewriting | Questions such as "What about its PO?" are rewritten correctly. |
| Frontend syntax | Inline JavaScript syntax validation passed. |
| Startup verification | `python main.py` can enter CLI and start local agents/frontend after stale processes are stopped. |
| Long-term memory | Schema and fallback retrieval were verified; missing pgvector does not block functionality. |

**Deployment Workflow**

**Running application**

The local POC is run with:

```bash
python main.py
```

Default local services are:

| Service | Default URL |
| --- | --- |
| HostAgent | `http://127.0.0.1:10000` |
| InvoiceAgent | `http://127.0.0.1:10001` |
| PurchaseOrderAgent | `http://127.0.0.1:10002` |
| DeliveryOrderAgent | `http://127.0.0.1:10003` |
| Browser frontend | `http://127.0.0.1:8080` |

Required configuration includes PostgreSQL connection parameters and `GEMINI_API_KEY`.

**Others**

Other project-specific deliverables include:

- README: setup, architecture, safety model, and limitations.
- Overall plan document: DOXA CONNEX AI agent strategy.
- Database structure reference: source database structure.
- Change log: implementation and verification history.

# Appendix B

**Progress Reports - Attach all 20 weekly progress reports, Project Plans/Schedules**

The actual weekly report scope is Week 1 to Week 18. The following progress summary reflects the most important task in each week and does not add tasks for dates without actual recorded work.

| Week | Date range | Progress summary | Deliverable |
| --- | --- | --- | --- |
| Week 1 | 2026-03-02 to 2026-03-06 | Set up the environment and validated Gemini, Anthropic, Chain, RAG, and tool-using Agent prototypes. | LLM validation, Chain/RAG/Agent prototypes. |
| Week 2 | 2026-03-09 to 2026-03-13 | Reviewed Prompt, structured output, RAG, multi-model integration, and the 16-agent management plan. | Core capability review, deliverables list, interview template, Agent board draft. |
| Week 3 | 2026-03-13 to 2026-03-19 | Implemented production-style RAG with CSV loading, embeddings, vector persistence, and continuous conversation. | RAG ingestion and retrieval flow, session entry, exception handling, fallback mechanism. |
| Week 4 | 2026-03-20 to 2026-03-26 | Analysed Procure-to-Pay, subcontractor processes, business roles, core scenarios, and Agent boundaries. | Workflow understanding, Concierge/specialist Agent collaboration model, task split. |
| Week 5 | 2026-03-27 to 2026-04-02 | Deepened business and database analysis and refined RFQ, PO, receiving, invoice matching, and payment scheduling requirements. | Procurement requirements, single-responsibility Agent plan, infrastructure sequence. |
| Week 6 | 2026-04-03 to 2026-04-09 | Validated the procure-to-pay loop and designed the Doxa Connex multi-agent architecture, security boundary, and implementation route. | Multi-agent architecture, technology choices, JWT/RBAC design, four-phase route. |
| Week 7 | 2026-04-10 to 2026-04-16 | Defined the A2A POC scenario and planned local implementation using LangChain, LangGraph, and A2A. | A2A POC business design, architecture review, security design updates. |
| Week 8 | 2026-04-17 to 2026-04-23 | Froze A2A POC architecture and completed protocol structures, orchestration, mock queries, state tables, and end-to-end validation. | A2A structures, Orchestrator/child Agents, state tables, local validation. |
| Week 9 | 2026-04-24 to 2026-04-30 | Progressed ECS Fargate, Cloud Map, API Gateway, Lambda Authorizer, NLB, and Aurora preparation. | Infrastructure preparation, call-chain design, API samples, blocker summary. |
| Week 10 | 2026-05-01 to 2026-05-07 | Scoped the AML A2A POC and designed the Host, Market, and Transaction three-agent model. | AML scope, technology choices, LangGraph dispatch loop, risk report demo flow. |
| Week 11 | 2026-05-08 to 2026-05-14 | Completed AML multi-agent specifications, AgentCards, A2A messages, state transitions, and shifted to invoice data. | Executable specifications, validation plan, sample data, invoice data direction. |
| Week 12 | 2026-05-18 to 2026-05-22 | Started Invoice Analysis POC, analysed PostgreSQL structure, and implemented task/session store and Host/Invoice A2A loop. | Database analysis, task/session storage, three invoice queries, CLI. |
| Week 13 | 2026-05-25 to 2026-05-29 | Completed natural-language-to-SQL-to-summary flow and added read-only execution and forbidden keyword blocking. | End-to-end text-to-SQL, safe SQL execution, four demo queries. |
| Week 14 | 2026-06-01 to 2026-06-05 | Prepared Invoice Agent demo, reviewed invoice workflow and multi-role views, and selected PO/DO as the next focus. | Complex query demo, workflow review, multi-role requirements, PO/DO plan. |
| Week 15 | 2026-06-08 to 2026-06-12 | Added PO/DO agents and implemented Invoice-to-PO/DO matching, two-way/three-way orchestration, and batch matching. | PO/DO analysis, deterministic matching, batch matching, 15 regression tests. |
| Week 16 | 2026-06-15 to 2026-06-19 | Fixed CLI rendering, standardised Router JSON, improved Top-N summaries, matching routing, and PO-to-DO context. | Stable CLI output, Router contract, matching result calibration, stability closure. |
| Week 17 | 2026-06-22 to 2026-06-28 | Built the browser frontend, connected SSE streaming, implemented Live/Demo modes, result rendering, and CORS hardening. | Browser chat UI, SSE communication, table/SQL/error rendering, frontend config. |
| Week 18 | 2026-06-29 to 2026-07-06 | Implemented multi-turn memory, recent context, History, memory_scope_id, long-term memory, and concurrency verification. | Conversation/turn tables, follow-up rewriting, History, memory isolation, long-term memory. |

**Project Plans/Schedules**

This POC can be viewed as the foundation for Invoice Matching Agent v1 in the broader roadmap:

| Month | Overall programme focus | Relationship to this POC |
| --- | --- | --- |
| Month 1 | Discovery: stakeholder interviews, workflow mapping, and use-case prioritisation. | The POC uses invoice matching priority and business workflow assumptions as input. |
| Month 2 | Design: BRD, UX design, agent architecture, API specification, and security review. | The POC implements the initial architecture and frontend interaction but does not replace formal BRD and security review. |
| Month 3 | Development: high and medium priority agents, including Invoice Matching Agent v1. | The POC implements the first local version of invoice analysis and matching capability. |
| Month 4 | UAT, performance testing, training, and phased production rollout. | The POC provides a basis for UAT planning but still requires production hardening. |

