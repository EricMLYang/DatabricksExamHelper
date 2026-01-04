# Databricks 模擬考（Eric_v2）

說明：共 30 題單選題。每題 4 個選項（A–D）。做完後請檢查答案鍵。

---

1. 在 Databricks 中，哪一項最適合用來執行交互式探索性資料分析？

A. Databricks Jobs

B. Databricks Repos

C. Databricks Notebooks

D. Databricks Workflows

2. Delta Lake 的主要優點不包括以下哪一項？

A. ACID 交易支援

B. Schema enforcement（架構強制）

C. 自動化成本優化（自動調整雲資源價格）

D. Time travel（歷史版本）

3. 在處理大量小文件造成元資料爆炸（small files problem）時，下列哪個操作最直接有助於改善？

A. 使用更高等級的 VM

B. 合併小檔案為更大的檔案（compaction / optimize）

C. 增加 cluster 節點數

D. 將檔案上傳到不同的 storage 帳號

4. 若要在 Databricks Workspace 中追蹤程式碼變更並與團隊協作，應使用：

A. DBFS

B. Databricks Repos（整合 Git）

C. Unity Catalog

D. Delta Live Tables

5. 為了限制不同使用者對資料表的存取權限，最佳做法是使用：

A. Cluster policies

B. Unity Catalog 的授權和資料列級安全（RLS）

C. Databricks Filesystem 路徑權限

D. Notebook ACL

6. 在 Notebook 中使用 `%sql` magic 指令的主要目的是：

A. 在 Notebook 中執行原生 SQL 查詢

B. 上傳檔案到 DBFS

C. 建立 cluster

D. 排程作業

7. Delta Lake 的 vacuum 操作主要用來：

A. 刪除整個表格

B. 清除未被引用的檔案以回收儲存空間（刪除已過期的檔案）

C. 添加索引

D. 更新 schema

8. 在實作資料攝取（ingestion）時，若需要處理即時（near real-time）事件流，應選擇：

A. Batch ETL 每日跑一次

B. Delta Live Tables

C. 使用 Structured Streaming 或 Databricks 的 Streaming 功能

D. Databricks Repos

9. 哪一項不是 Databricks Cluster 的類型？

A. Interactive cluster

B. Job cluster

C. SQL warehouse

D. Storage cluster

10. 為了在 Databricks 中節省成本，最可行的策略是：

A. 永久保留大量大型 cluster

B. 使用 spot/預留實例、設定自動終止（auto-termination）與合理的排程

C. 將所有工作搬到本地機房

D. 不進行任何變更以避免風險

11. 在 Unity Catalog 中管理資料資產，哪一項描述是正確的？

A. Unity Catalog 只能管理 Databricks Repos

B. Unity Catalog 提供統一的資產與存取控制（catalog → schema → tables）

C. Unity Catalog 與雲端 IAM 無法整合

D. Unity Catalog 會自動優化 SQL 查詢性能

12. 在設計 ETL 程式時，遵守 idempotency（冪等性）的好處是：

A. 提高查詢速度

B. 允許重試而不會造成重複資料或不一致狀態

C. 減少檔案大小

D. 自動提升權限

13. 用於長期儲存 cold data 的最佳選擇通常是：

A. 高頻 IOPS 的本地 SSD

B. 雲端物件儲存（S3 / ADLS / GCS）的低成本層級

C. Cluster 的 ephemeral 本地磁碟

D. Notebook 的儲存區

14. 在 Spark 中，要有效利用 partition pruning，應該：

A. 在查詢中使用分割欄位作為 filter 條件

B. 把所有資料寫成單一檔案

C. 禁用 predicate pushdown

D. 使用更小的 partition （每 partition 僅一行）

15. Delta Lake 的 schema evolution（架構演進）允許：

A. 自動刪除欄位

B. 在寫入時新增欄位（在允許的情況下）

C. 將資料轉換成非結構化格式

D. 關閉事務

16. 要在 Databricks 中排程每天凌晨 ETL 作業，建議使用：

A. Notebook 中的 sleep loop

B. Databricks Jobs 或 Workflows 的排程功能

C. 手動登入執行 Notebook

D. Databricks Repos 的 webhook

17. 在處理敏感資料（PII）時，下列哪一項不是推薦做法？

A. 使用最小權限原則（least privilege）

B. 使用 Unity Catalog 與列級、欄位級存取控管

C. 在 Notebook 中將明文敏感資料分享給所有使用者

D. 對儲存層加密以及審計存取

18. Delta Live Tables (DLT) 的主要用途包括：

A. 建立和管理可重複、可監控的資料管線（pipelines）

B. 管理 Git repository

C. 做為資料湖的物件儲存服務

D. 直接管理 Unity Catalog 權限

19. 在大規模 join 操作時，使用 broadcast join 的最佳條件是：

A. 兩邊的表都非常大（TB 級）

B. 被 broadcast 的表相對較小，可放入每個執行器的記憶體

C. 無法使用 shuffle

D. 當資料需要 time travel

20. 若要保護查詢過程中的憑證（例如 JDBC 密碼），建議使用：

A. 將憑證寫死在 Notebook 中

B. Databricks Secret Manager（Secrets）或雲端秘密管理服務

C. 將憑證放到 DBFS 的公開路徑

D. 在 cluster 的 init script 中回傳明文

21. Spark 的 Catalyst optimizer 的職責是：

A. 儲存資料到 Delta 時壓縮檔案

B. 對 SQL 查詢進行解析、優化與產生執行計畫

C. 管理使用者權限

D. 做為資料儲存層

22. 在 Databricks SQL Warehouse（前身為 SQL Endpoint）中，最佳做法是：

A. 將所有 ETL 流程放在 SQL Warehouse 上無限運行

B. 為 BI 查詢建立專用的 SQL Warehouse 並設定查詢加速與資源大小

C. 用 SQL Warehouse 儲存原始資料檔案

D. 禁用 query caching

23. 當需要在不同環境（開發/測試/生產）同步 SQL 與 Notebook 內容，應採用：

A. 手動複製 Notebook

B. 使用 Databricks Repos 與 Git-based CI/CD 流程

C. 在 production notebook 直接修改開發內容

D. 把 Notebook 存成純文字到 DBFS

24. 在寫入 Delta 表時若遇到 schema mismatch（欄位型態不符），最安全的處理方式是：

A. 直接跳過錯誤並繼續寫入

B. 停止寫入，排查並採取 schema 合併或轉換的明確步驟

C. 刪除目標表並重新建立

D. 忽略並使用 vacuum

25. 在 Databricks 中要追蹤 Job 執行歷史與錯誤，應查看：

A. Cluster event logs

B. Jobs UI（Runs / Tasks），以及相關的作業記錄與告警設定

C. Notebook 的輸出只有

D. DBFS 檔案列表

26. 要在 Delta 表上實作資料版本回滾（roll-back），可使用：

A. DELETE FROM table

B. Time travel（使用版本號或 timestamp）並以 CREATE OR REPLACE 或 CLONE 恢復

C. 直接在物件儲存上手動還原檔案

D. 更新 Unity Catalog

27. 在設定 cluster policies 時，主要目的包括：

A. 控制 cluster 建立的可接受設定以節省成本與維持合規性

B. 管理 Delta table 的 schema

C. 自動建立 Git 分支

D. 儲存 notebook 的歷史版本

28. 當使用 Structured Streaming 讀取 Kafka 資料時，要確保的設定不包含：

A. 正確的 offset 起始位置與 checkpoint 位置

B. 適當的 shuffle partitions 設定以避免資料傾斜

C. 將所有資料先寫入本地磁碟再處理

D. 監控延遲與處理速率

29. 在 Databricks SQL 中使用 materialized views 的主要好處是：

A. 自動把資料備份到外部儲存

B. 預先計算並快取查詢結果以加速查詢

C. 避免使用索引

D. 自動管理使用者權限

30. 若團隊需要共享、驗證資料資產的 lineage（血緣），最佳選擇是：

A. 手動在 README 記錄血緣

B. 使用 Unity Catalog 與資料血緣/系統記錄工具，或結合 Delta 的 audit logs

C. 把 Notebook 內容直接貼在 Slack

D. 在 cluster 上執行 ad-hoc 查詢

---

答案鍵：

1: C

2: C

3: B

4: B

5: B

6: A

7: B

8: C

9: D

10: B

11: B

12: B

13: B

14: A

15: B

16: B

17: C

18: A

19: B

20: B

21: B

22: B

23: B

24: B

25: B

26: B

27: A

28: C

29: B

30: B
