# **Spark UI / Debug 知識總整理（精簡版）**

---

---

##  1\. Spark UI 的用途（考試最常考）

Spark UI = **觀察 Spark Job 行為的主要除錯工具**
用來：

- 找出 **Stage/Task 出錯點**

- 找 **Shuffle 是否過大**

- 找 **資料傾斜（skew）**

- 找 **OOM（記憶體不足）**

- 分析 **SQL Physical Plan**

- 查看 **Executors 的 CPU/記憶體使用**

🔥 考試常問：

- 哪裡看到 Task 失敗？ → **Stages / Tasks**

- 哪裡看到記憶體問題？ → **Executors**

- 哪裡看到 shuffle？ → **Stages 的 Shuffle Read/Write**

- 哪裡看到計劃？ → **SQL / Query Plan**

---

##  2\. Spark UI 的主要區塊（考題常考對應）

| Spark UI 區塊 | 功能 | 考點 | 
|---|---|---|
| **Jobs** | 整體 Job DAG、成功/失敗狀態 | 哪個 Job 失敗？ | 
| **Stages** | Shuffle、重試、失敗 task | 找性能瓶頸/找錯誤來源 | 
| **Tasks** | 每個 partition 的執行時間/錯誤 | 找資料傾斜（skew） | 
| **SQL / Query Plan** | Catalyst Plan、物理計畫、join 策略 | 找 broadcast join、找 sorting | 
| **Executors** | 記憶體、spill、executor dead | 判斷 OOM、disk spill | 
| **Environment** | Spark config | 決定是否用 AQE 等參數 | 

---

# ⭐ 3. 常見錯誤與如何在 Spark UI 辨識（高機率考題）

---

## 🔥 **1\. OOM（Out of Memory）記憶體不足**

特徵：

- Executor 死亡 / 重新啟動

- Executors tab 中 Memory Maxed Out

- Stage 中 Task failure message 包含 OOM

原因：

- partition 過大

- wide transformation（groupBy、join）佔了太多 memory

解法：

- 增加 partition（`spark.sql.shuffle.partitions`）

- 使用 broadcast join

- 避免讀取過大的 skew partition

---

## 🔥 **2\. 資料傾斜（Skew）**

特徵：

- 在 Tasks tab，只有少數 task 非常慢

- Stage 只有 1\~2 個 Task 卡住很久

- shuffle read 量不均

如何辨識：

- 看 Tasks Timeline：某個 task 遠比其他慢

解法：

- 使用 salting

- Broadcast 小表

- AQE 開啟（skew join optimization）

---

## 🔥 **3\. Shuffle 過大 / Shuffle Read Timeout**

特徵：

- Stages 裡 Shuffle Read / Write 數百 MB～數 GB

- Shuffle spill to disk 數量過大

- Stage 重試多次

解法：

- 減少資料量（filter pushdown）

- Reduce partitions

- 使用 bucketing

- 打開 AQE 讓 partitions 自動調整

---

## 🔥 **4\. Executor Lost（Executor 掉線）**

特徵：

- Executor Tab 顯示 executor repeatedly restarting

- Logs 出現 `ExecutorLostFailure`

- 可能是 OOM 或網路問題

解法：

- 看 Driver/Executor 日誌

- 增加記憶體

- 減少 shuffle 與 spill

---

# ⭐ 4. Databricks 特有：Jobs Repair（重跑）功能（考試會考）

Databricks Job 有 **Repair**：

- 可以從失敗的 task / step **重新執行**

- 不必重新跑整個 pipeline

- 可使用 **Parameter Override**（調整輸入參數）
   → 例如重跑 2024-11-01 這天的資料

考試可能問：

> 「如何在一個 10-step pipeline 重新執行第 7 步？」
> ✔ 用 **Repair**。

---

# ⭐ 5. 常用排錯工具（考試考「下一步要看哪裡」）

| 工具 | 用來做什麼 | 
|---|---|
| **Spark UI** | 找性能、查 Shuffle、找 OOM、找 Task failure | 
| **Driver Logs** | 找 stack trace、Python / JVM exception | 
| **Executor Logs** | 找 out-of-memory、executor crash 原因 | 
| **System Tables**（`system.query.history`） | 看最近 query 狀態、延遲變化 | 
| **Query Profiler** | 看 SQL operator 哪個最慢 | 
| **Cluster Events** | 看 cluster expansion、executor crash | 

---

##  6\. 考試題型常見模板（你會遇到的）

### ✔ 題型 1：給你 Spark UI 截圖，問問題在哪裡

例：Shuffle 量太大、資料傾斜、OOM。

### ✔ 題型 2：問你下一步該去哪裡查

例：「看到 executor lost，下一步查看？」
👉 Executor log。

### ✔ 題型 3：問你要調哪些 Spark config

例：Shuffle partition、broadcast threshold、AQE。

### ✔ 題型 4：問你如何加快 SQL query

例：Broadcast join、AQE、filter pushdown、減少 shuffle。

### ✔ 題型 5：問你失敗的 Job 怎麼重跑

→ 用 Repair。

---

##  7\. Spark 性能調校（考試必考 4 項）

你一定要記住：

### (A) **使用 broadcast join（小表加入大表）**

### (B) **啟用 AQE（Adaptive Query Execution）**

能自動：

- 合併小 partitions

- 分裂 skew partitions

- 自動改成 broadcast join

### (C) **減少 Shuffle**

例如：

- 使用 bucketing

- 不要重複 repartition

- filter pushdown

### (D) **最佳化 partitioning**

避免：

- partition 過多（scheduler overhead）

- partition 過大（OOM）

---

##  **一頁簡明總結（30 秒記憶版）**

**Spark UI 看什麼？**

- Stages → 找 shuffle / skew / failed task

- Tasks → 找 partition 變慢

- SQL → physical plan

- Executors → OOM / spill

**常見錯誤：**

- OOM → partition 過大

- Skew → 有 task 特別慢

- Shuffle timeout → shuffle 過大

- Executor lost → 記憶體或網路問題

**Databricks 特有：**

- Jobs Repair

- Query Profiler

- System Tables

---


