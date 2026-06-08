# Invoice Intelligent Analytics Project Brief

## 1. Capabilities Implemented to Date

1. Natural-language analytics: Business users can ask questions directly without writing SQL, including supplier invoicing frequency, amount distribution, and long-pending invoices.
2. Multi-agent collaboration: The system uses a layered architecture with a coordinator agent and an analysis agent, with clear responsibilities and strong extensibility for additional scenarios.
3. Database integration: PostgreSQL-based structured invoice data is connected (read-only on the invoice database), with full task and session traceability.
4. Baseline safety controls: Read-only query constraints, SQL type restrictions, and dangerous keyword blocking are enabled to reduce risks from model-generated SQL.

## 2. Core Workflow (End-to-End)

1. The user enters a business question in the CLI.
2. The coordinator agent receives the request and delegates it to the analysis agent.
3. The analysis agent converts natural language into SQL using the model.
4. The system validates SQL safety, then queries the PostgreSQL invoice database.
5. Results are returned and transformed into a business-readable summary.
6. The final answer is returned to the user, while task execution logs are written for traceability.

## 3. Supported Query Types

1. Long-pending invoice query: Identifies invoices that remain in non-terminal status beyond a specified number of days.
2. Supplier invoicing frequency analysis: Ranks suppliers by invoice count.
3. Supplier invoicing amount analysis: Ranks suppliers by total, average, minimum, and maximum invoice amount metrics.
4. Comprehensive analysis: Returns a multi-dimensional summary in a single query.

## 4. Key Risks and Limitations

1. Semantic ambiguity risk: Some field names and business abbreviations in the current database are unclear, which can produce SQL that is executable but not aligned with business definitions. Terms such as invoice, payment, and purchase_order are easier to interpret, but terms like dbq, pc, rfq, and mt may lead to incorrect SQL without a manually maintained mapping dictionary.
2. Static schema understanding: The current design mainly relies on preloaded schema context and tends to place large schema content directly into prompts, which can increase token cost and reduce accuracy due to information overload.



