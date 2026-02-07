# availableNow vs Batch 速記

## 一句話
`trigger(availableNow=True)` = **用 streaming 的增量 + checkpoint 追進度**，但**跑完就停**（像 batch）。

---

## 核心差異
- **Batch**：你自己負責「增量邏輯 + 容錯/重跑一致性」
- **availableNow**：把「增量 + 進度 + 容錯」交給 Spark checkpoint

---

## Batch 的典型做法
你要自己決定這次讀哪些新資料：
- `where ingest_date >= last_run_time`
- 掃檔案列表、比對 watermark、自己存 offset
- 重跑時自己確保不重複、不漏資料

### 優點
- 直覺、簡單
- 對「明確分區（日期/批次ID）」很有效

### 缺點
- 增量判斷一旦寫錯 → 漏資料或重複
- 失敗重跑需要你自己設計 exactly-once / idempotent

---

## availableNow=True 的行為
### 1) 增量追進度靠 checkpoint
- 進度寫在 `checkpointLocation`
- 同一 query + 同一 checkpoint → 只處理沒處理過的資料

### 2) 執行方式像 batch
- 用 micro-batch 把 backlog 分批處理
- **處理完就停止** → 適合排程、成本低

### 3) 失敗重跑更安全
- checkpoint 記錄進度與狀態
- 重跑會接著未完成部分，而不是你猜 `last_run_time`

---

## 你省掉的工作
- 不用自己維護 last_processed_time / last_file / offsets
- 不用寫「這次要抓哪些新檔」判斷
- 不用處理「寫到一半失敗要不要回滾」的邏輯

## 你仍要做的事
- 設計 output 的一致性（寫 Delta table 通常最穩）
- 正確設定 `checkpointLocation`（最重要）
- 若有 stateful（聚合、join）要理解 watermark/state store

---

## 何時 Batch 反而更好？
- 資料天生是乾淨批次分區
  - `date=YYYY-MM-DD`
  - 或 `batch_id`
- 你只要 `MERGE INTO` 特定分區

---

## 何時 availableNow 特別有優勢？
- 檔案持續進來（尤其 Auto Loader）
- 不想自己管「哪些檔案處理過」
- 想要「像 batch 一樣排程」又要 streaming 的增量與容錯

---

## 一句話總結
- **Batch**：你自己寫增量、自己扛重跑一致性
- **availableNow**：增量 + 進度 + 容錯交給 Spark checkpoint，跑完就停
