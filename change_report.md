# 修改报告

## 背景

原来的 document matching 流程强依赖用户在问题里明确写出 invoice number。
如果用户只问“三方匹配”“检查最近几张发票的匹配情况”这类问题，PurchaseOrderAgent
和 DeliveryOrderAgent 都会因为找不到发票号而返回错误，导致两个 agent 无法正常协作。

## 修改内容

1. 修改 `tools/document_match_query.py`
   - 新增批量匹配默认数量和最大数量限制。
   - 新增从自然语言中提取批量数量的能力，例如 `latest 5`、`检查最近 5 张发票`。
   - 新增按最近发票查询候选 invoice number 的方法。
   - 新增批量 Invoice-to-PO 匹配方法。
   - 新增批量 Invoice-to-DO 匹配方法。
   - 批量结果不会携带每一行明细，避免多发票场景下返回数据过大。

2. 修改 `agents/host_agent/graph.py`
   - HostAgent 在 document matching 请求中检测是否缺少 invoice number。
   - 如果缺少 invoice number，HostAgent 会先查询一批候选发票号。
   - HostAgent 会把同一批候选发票号通过 A2A `DataPart` 传给 PO/DO 两个 agent。
   - 汇总文案支持区分“单张发票匹配”和“多张发票批量匹配”。

3. 修改 `agents/purchase_order_agent/graph.py`
   - 保留原有单张发票匹配逻辑：问题里有 invoice number 时行为不变。
   - 当问题里没有 invoice number 时，改为使用 HostAgent 传入的候选发票号做批量 PO 匹配。
   - 如果 PurchaseOrderAgent 被单独调用且没有 HostAgent 上下文，会自行查询最近发票作为候选。

4. 修改 `agents/delivery_order_agent/graph.py`
   - 保留原有单张发票匹配逻辑：问题里有 invoice number 时行为不变。
   - 当问题里没有 invoice number 时，改为使用 HostAgent 传入的候选发票号做批量 DO 匹配。
   - 如果 DeliveryOrderAgent 被单独调用且没有 HostAgent 上下文，会自行查询最近发票作为候选。

## 修改后的行为

- `Check three-way matching for invoice INV-00000001`
  - 仍然执行原来的单张发票 PO + DO 匹配。

- `Check three-way matching`
  - 不再直接报缺少 invoice number。
  - 系统会默认检查最近 20 张有明细的发票。

- `Check latest 5 invoices for three-way matching`
  - 系统会检查最近 5 张有明细的发票。

- `检查最近 5 张发票的三方匹配`
  - 系统会识别中文数量提示，并检查最近 5 张发票。

## 验证

已完成以下验证：

1. 使用 Python 3.11 编译检查整个项目，确认没有语法错误。
2. 使用 mock 数据验证 PurchaseOrderAgent：
   - 缺少 invoice number 但存在候选发票号时，会返回 `po_batch_match`。
3. 使用 mock 数据验证 DeliveryOrderAgent：
   - 缺少 invoice number 但存在候选发票号时，会返回 `do_batch_match`。
4. 使用 mock 数据验证 HostAgent：
   - 能生成共享的候选发票上下文。
   - 能正确生成批量 document matching 汇总。
5. 使用 `git diff --check` 检查格式，没有发现 whitespace 问题。

## 注意事项

- 批量匹配默认检查 20 张发票，最大限制为 50 张，避免一句宽泛问题触发过大的匹配任务。
- 当前批量匹配内部仍然按发票逐张调用已有确定性匹配逻辑。对 POC 来说足够直接；如果后续要支持大量发票批处理，建议改成 set-based SQL 来提升性能。

---

# 追加修改：修复最高金额发票查询卡死问题

## 问题

用户提问：

```text
List the 5 invoices with the highest amounts
```

时存在长时间无响应或看起来“死机”的风险。

## 潜在原因分析

1. HostAgent 路由依赖 Gemini。
   - 系统设计上仍然保留 Gemini 路由能力。
   - 曾短暂加入确定性路由来绕开 Gemini，但后续根据要求已撤回，恢复为原来的 Gemini 路由优先设定。

2. InvoiceAgent 查询依赖 Gemini 生成 SQL 和汇总。
   - 该问题其实可以用固定 SQL 稳定回答，不需要 LLM 生成 SQL。
   - 原流程还会把查询结果交给 Gemini 汇总，增加等待时间和外部依赖。

3. SQL 执行器会额外执行 count wrapper。
   - 原逻辑会把用户 SQL 去掉 `LIMIT` 后包成 `COUNT(*)` 查询。
   - 对 `ORDER BY total_amount DESC LIMIT 5` 这类 top-N 查询，count 不需要排序。
   - 如果保留不必要的排序，数据量变大后可能造成慢查询。

4. 金额排序存在 NULL 排在前面的风险。
   - PostgreSQL 中 `ORDER BY total_amount DESC` 默认可能把 NULL 放在前面。
   - 这会导致“最高金额”结果不准确。

## 修改内容

1. 修改 `agents/host_agent/router.py`
   - 已撤回最高金额发票查询的确定性路由。
   - HostAgent 恢复为使用 Gemini 进行路由判断。
   - `GEMINI_API_KEY` 继续保留，其他依赖 Gemini 的查询不受影响。

2. 修改 `agents/invoice_agent/graph.py`
   - 新增最高金额发票查询 fast path。
   - 对 `List the 5 invoices with the highest amounts` 这类问题直接执行本地固定 SQL。
   - SQL 使用 `WHERE i.total_amount IS NOT NULL` 排除空金额。
   - SQL 使用 `ORDER BY i.total_amount DESC NULLS LAST` 保证最高金额排序正确。
   - 摘要和 markdown 表格由本地代码生成，不再调用 Gemini 汇总。

3. 修改 `tools/sql_query.py`
   - 新增单语句校验，拒绝包含内部分号的多 SQL 语句。
   - 新增数据库连接超时，默认 `SQL_CONNECT_TIMEOUT_SECONDS=5`。
   - 新增数据库 statement timeout，默认 `SQL_STATEMENT_TIMEOUT_MS=15000`。
   - 优化 count wrapper：对顶层尾部 `ORDER BY` 和 `LIMIT` 做安全移除，避免 top-N count 查询进行不必要排序。

## 修改后的行为

- `List the 5 invoices with the highest amounts`
  - HostAgent 仍通过 Gemini 路由到 InvoiceAgent。
  - InvoiceAgent 直接执行固定 SQL。
  - 返回前 5 张 `total_amount` 非空且金额最高的发票。
  - InvoiceAgent 不再依赖 Gemini 生成 SQL 或汇总结果。

## 验证

已完成以下验证：

1. 目标问题本地执行验证：
   - `List the 5 invoices with the highest amounts`
   - InvoiceAgent 返回时间约 0.074 秒。
   - 返回 `count=5`，`total_count=9287`。
   - 返回结果不再出现 NULL 金额排在最前的问题。

2. 路由设定验证：
   - 已确认确定性路由代码被移除。
   - HostAgent 继续保留 `GEMINI_API_KEY` 并使用 Gemini 路由。

3. SQL count wrapper 验证：
   - 对 `ORDER BY total_amount DESC NULLS LAST LIMIT 5` 查询生成 count SQL。
   - 确认 count SQL 不再包含顶层 `ORDER BY` 或 `LIMIT`。

4. 编译检查：
   - 使用 Python 3.11 编译检查整个项目，确认没有语法错误。

## 注意事项

- 该 fast path 只覆盖明确的“最高金额发票 top-N”查询，不会替代所有 invoice analysis。
- 其他复杂自然语言分析问题仍会走 Gemini text-to-SQL 流程。
- SQL 执行器已增加超时保护，但如果未来查询场景更多，建议继续补充更多确定性查询模板和正式测试用例。

---

# 追加修改：新增 pytest 回归测试

## 背景

项目此前没有自动化测试。路由、SQL 校验和 document matching 都是核心链路，后续改 prompt、路由规则或匹配逻辑时容易产生回归。

## 修改内容

1. 修改 `pyproject.toml`
   - 新增 `dev` optional dependency：`pytest>=8.0.0`。
   - 新增 pytest 配置：
     - `testpaths = ["tests"]`
     - `pythonpath = ["."]`

2. 新增 `tests/test_router.py`
   - 覆盖 HostAgent 对有效 LLM JSON 的 route normalize。
   - 覆盖 LLM 返回非法 JSON 时的 keyword fallback。
   - 覆盖最高金额发票查询不会被 HostAgent 本地确定性路由短路，仍会调用 Gemini 路由函数。

3. 新增 `tests/test_sql_query.py`
   - 覆盖 `validate_sql` 对合法 SELECT 的处理。
   - 覆盖危险 SQL 和多语句 SQL 的拒绝。
   - 覆盖 top-N 查询 count wrapper 会移除顶层 `ORDER BY` 和 `LIMIT`。
   - 覆盖嵌套子查询中的 `ORDER BY` 不会被错误移除。
   - 覆盖 `execute_safe_sql` 会设置连接超时、statement timeout、只读 session，并在缺少 `LIMIT` 时自动追加行数限制。

4. 新增 `tests/test_matching.py`
   - 覆盖 invoice number 提取和中英文批量数量提取。
   - 覆盖 PO batch matching 去重、统计和移除明细行。
   - 覆盖 DO batch matching 空候选场景。
   - 覆盖 PurchaseOrderAgent 在 document matching 缺少 invoice number 时会进入 batch PO matching。
   - 覆盖 DeliveryOrderAgent 在 document matching 缺少 invoice number 时会进入 batch DO matching。

## 验证

已完成以下验证：

```text
python3.11 -m pytest
```

结果：

```text
15 passed in 1.64s
```

同时已完成 Python 3.11 编译检查，确认测试文件和项目代码没有语法错误。
