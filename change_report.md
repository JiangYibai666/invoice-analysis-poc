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
