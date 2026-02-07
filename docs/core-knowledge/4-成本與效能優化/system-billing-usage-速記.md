# system.billing.usage 速記（計費與使用量）

## 一句話
`system.billing.usage` = **DBU 消耗明細**；`run_as` 看人，`sku_name` 看資源。

---

## 正確解讀（Q-015 類型）
以下欄位組合 → **每位使用者 + 每種計算資源** 的 DBU 使用量
- `identity_metadata.run_as`
- `sku_name`
- `usage_date`
- `usage_quantity`

---

## 欄位對照表
| 分析維度 | 欄位 | 備註 |
|---|---|---|
| 按使用者 | `identity_metadata.run_as` | 使用者或服務主體 |
| 按計算類型 | `sku_name` | ALL_PURPOSE / JOBS / SERVERLESS 等 |
| 按日期 | `usage_date` | 時間維度 |
| 量化 | `usage_quantity` | DBU 消耗量 |

---

## 常見 sku_name
```
ALL_PURPOSE_COMPUTE
JOBS_COMPUTE
SERVERLESS_SQL
SERVERLESS_REAL_TIME
DLT_CORE
DLT_PRO
DLT_ADVANCED
```

---

## 常見誤判
- 想看 **workspace** → 應該選 `workspace_id`
- 想看 **pipeline** → 用 `usage_metadata.pipeline_id`
- 想看 **job run** → 用 `usage_metadata.job_run_id`

---

## 快速判斷口訣
```
run_as 看人頭
sku_name 看資源
workspace_id 看工作區
job_run_id 看作業次
```
