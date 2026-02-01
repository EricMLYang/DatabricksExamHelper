下面是把你書上那段，用**目前 Databricks 官方文件**重新整理成「可直接放筆記／教別人」的版本（把重點、限制、介面分頁名稱都補齊，並保持在 DBSQL/SQL Warehouses 的語境）。 ([docs.databricks.com][1])

---

## Query History（DBSQL / SQL Warehouses）

### 它是什麼

* **Query History** 會列出在 **SQL warehouses** 上執行的查詢。 ([docs.databricks.com][1])
* **保留期：30 天**（到期自動刪除）。 ([docs.databricks.com][1])

### 權限與誰看得到

* 你是 query owner 就能看。
* 其他人需至少對該 SQL warehouse 有 **CAN VIEW** 才能看 Query History。 ([docs.databricks.com][1])

### 你在 Query History 會看到什麼（右側 Query details / summary panel）

點進某筆查詢後，右側摘要會提供（常用來 debug）：

* **Query status**：Queued / Running / Finished / Failed / Cancelled
* **User & compute details**：執行者、compute 類型、runtime
* **ID (UUID)**：該次執行的識別
* **完整 Query statement**（過長可展開）
* **Query metrics**：常見指標；部分指標旁的 filter icon 代表掃描時的 **data pruning 比例**
* **See query profile**：會先給你 DAG 預覽，可再點進 Query Profile ([docs.databricks.com][1])

---

## Query Profile（查詢剖析）

### 它是什麼、能解什麼問題

Query Profile 用來把一次查詢的執行細節「視覺化」：

* 看每個 operator 的指標（time spent、rows、memory…）
* 一眼找出最慢/最貴的部分，評估你改 SQL 後的影響
* 抓常見錯誤：例如 **exploding joins**、**full table scans** ([docs.databricks.com][2])

### Requirements（誰可以看）

要看 Query Profile，你必須：

* 是 query owner，或
* 對執行該查詢的 SQL warehouse 至少有 **CAN MONITOR** 權限 ([docs.databricks.com][2])

### 進入方式（UI 操作路徑）

Query History → 點某筆 query → 右側摘要 → **See query profile** ([docs.databricks.com][2])

### Query Profile 介面結構（務必記住三個分頁名稱）

左側有三個 tabs： ([docs.databricks.com][2])

1. **Details**：摘要 metrics
2. **Top operators**：最昂貴/最耗時 operators（找優化點）
3. **Query text**：完整 SQL

右側是 **DAG (directed acyclic graph)**，可切換顯示不同指標（例如 **Time spent / Memory peak / Rows**），並支援搜尋、縮放、點 operator 看細節。 ([docs.databricks.com][2])

### 重要限制（書上常沒寫，但很常踩到）

* 若畫面顯示 **“Query profile is not available”**，常見原因是該查詢命中 **query cache**；官方建議用「很小的改動」繞過 cache，例如更改或移除 `LIMIT`。 ([docs.databricks.com][2])

### 你應該補記的實用功能（分享/匯出/匯入/看更多指標）

* **Enable verbose mode**：預設部分 metrics 會隱藏；開啟後可看到全部 operations 與更多指標。 ([docs.databricks.com][2])
* **Share / Download JSON**：

  * 對方若有 query 的 CAN MANAGE，可直接分享 URL
  * 否則可 **Download** Query Profile JSON 給對方 ([docs.databricks.com][2])
* **Import query profile (JSON)**：可匯入別人給你的 JSON 來看 profile；但「只在瀏覽器 session 動態載入，不會保存」，每次要看得重新匯入。 ([docs.databricks.com][2])
* **Spark UI**：對 Databricks SQL queries 也可從 Query Profile 介面選單開到 Spark UI 看。 ([docs.databricks.com][2])

---

## 進階補充：Query history system table（`system.query.history`）

如果你要用 SQL 做「帳號級」統計/稽核/追查（跨 workspace），可用 system table：

* 表位置：`system.query.history`（Public Preview） ([docs.databricks.com][3])
* 內容涵蓋：SQL warehouses + **serverless compute for notebooks and jobs** ([docs.databricks.com][3])
* 權限：預設只有 admins 可存取；官方建議用 **dynamic view** 分享給特定 user/group ([docs.databricks.com][3])

---

如果你願意，我也可以把上面這份再「縮成考試用 1 頁小抄」：只保留會考的名詞（CAN VIEW / CAN MONITOR、30 days、Details/Top operators/Query text、cache→LIMIT、verbose mode、JSON 分享/匯入、`system.query.history` 覆蓋範圍）。

[1]: https://docs.databricks.com/gcp/en/sql/user/queries/query-history "Query history | Databricks on Google Cloud"
[2]: https://docs.databricks.com/aws/en/sql/user/queries/query-profile "Query profile | Databricks on AWS"
[3]: https://docs.databricks.com/aws/en/admin/system-tables/query-history "Query history system table reference | Databricks on AWS"
