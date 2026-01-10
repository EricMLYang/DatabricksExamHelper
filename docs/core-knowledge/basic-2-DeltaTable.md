# 【Databricks 考照第二篇 - Delta Table 簡介】



想起第一次聽到 databricks Table 有靈活的 Time Travel 功能，

這讓我非常好奇，

因為這通常要有滿巧妙的底層安排才能做到，

而且 delta lake 這類的 Open Table Format ，

又是 Lakehouse 的種有核心，

因此我花了一點時間理解，

本篇將涵蓋 Delta Table 最基礎概述：

---



▋資料湖的痛點救星： Open Table Format 

在傳統資料湖（Data Lake）中，

資料通常以 Parquet、CSV、JSON 等檔案形式儲存在雲端，

如 AWS S3、Azure Data Lake Storage，

但這樣的資料湖缺少「資料庫的管理能力」，例如：

\-沒有 ACID Transaction（交易保證）\
\-無法正確追蹤更新、刪除或版本控制\
\-同時多人或多任務寫入容易導致資料不一致 



Open Table Format 的出現，

就是為了解決這些問題。

它讓資料湖具有類似資料庫的可靠，

同時仍保持開放與可擴充性。

幾個常見的有：

**\-Delta Lake**： Databricks 開發，最早、最成熟， 原生支援時間旅行、Merge 操作與 ACID。

**\-Apache Iceberg**：Netflix 開發並貢獻給 Apache， 特別強調 schema 演進的靈活性與快照版本控制。

**\-Apache Hudi**：Uber 開發並貢獻給 Apache， 強項是即時資料更新與低延遲查詢。





▋Open Table Format 的組成探討

Open Table Format 是**實體檔案 ＋** 一層交易層，

檔案可以放到雲端空間（就像你電腦資料夾放檔案一樣），

主流大多都把資料用 Parquet 檔存放，

Parquet 是 2013 年就出現的成熟格式，

因為其 **columnar storage、支援各種壓縮、生態系齊全 …等特點，**

變成大數據的實體層霸主。



因此，

目前 Open Table Format 主要區別是交易層的實作差異，

交易層決定了怎麼做 ACID、怎麼回溯/分支、怎麼即時 upsert、

怎麼跨引擎查、怎麼管 schema 與 metadata。





▋開山始祖 Delta Table 

**Delta Table 是 Parquet 檔 和 Transaction Log 結合，**

 讓資料操作具備「ACID」特性，

讓數據處理具備資料庫的可靠性。



我們簡單看一下 Delta Table 結構，

```
/data/g_app_ad_eye_tracking/
│
├── part-0001.snappy.parquet
├── part-0002.snappy.parquet
└── _delta_log/
    ├── 00000000000000000000.json
    ├── 00000000000000000001.json
    └── ...
```

可發現一個 **\_delta_log 資料夾放了 Json 檔，**

這裏記錄所有的交易操作，例如：

\-Insert、Update、Delete

\-Schema 變更

\-Metadata（版本、時間戳、使用者）

所以交易層有對應的程式根據 Json 檔來做數據處理，

新增的處理流程也都放到新的 Json 檔，

這樣安排，讓資料湖具備以下能力：

---



▋ACID 保證

**\-Atomicity**：交易要嘛全部成功，要嘛全部失敗

**\-Consistency**：確保交易前後資料都符合定義

**\-Isolation**：多個任務同時操作不會互相干擾

**\-Durability**：交易完成後，結果永久保存

例如：

```sql
UPDATE delta.`/data/sales/`
SET revenue = revenue * 1.1
WHERE region = 'APAC';
```

這筆更新不會中途失敗導致資料錯亂；失敗會自動回滾。





▋Time Travel（時間旅行）

```sql
-- 查詢 5 個版本前的資料
SELECT * FROM delta.`/data/sales/` VERSION AS OF 5;

-- 查詢昨天的資料快照
SELECT * FROM delta.`/data/sales/` 
TIMESTAMP AS OF '2024-10-01 00:00:00';

-- 查看所有歷史版本
DESCRIBE HISTORY delta.`/data/sales/`;
```

**實戰應用**：

\- 除錯：「昨天的報表是對的，今天為什麼錯了？」

\- 回滾：「誤刪資料，回到 10 分鐘前」

\-審計：「這個客戶的訂單何時被修改過？」





▋MERGE 的 Upsert (update + insert)，

傳統 SQL 需要 `INSERT ... ON DUPLICATE KEY UPDATE`，

Delta 提供更簡潔語法：

```sql
MERGE INTO target_sales t
USING source_updates s
ON t.order_id = s.order_id
WHEN MATCHED THEN 
  UPDATE SET t.amount = s.amount, t.updated_at = current_timestamp()
WHEN NOT MATCHED THEN 
  INSERT (order_id, amount, updated_at) 
  VALUES (s.order_id, s.amount, current_timestamp());
```

**這個在** 每日增量更新（CDC）、同步 API 資料到資料湖、去重與合併都會用到。



▋Delta Table 與傳統 SQL 的底層差異

傳統 SQL DB 就是透過 DB 查詢引擎操作硬碟裡面的表，

Delta Table 則是透過 Apache Spark 去運算雲端的檔案，

只是執行起來讓你覺得很像 SQL DB 的表。



假設我們要更新 1000 萬筆中的 100 筆，

傳統 SQL：直接更新索引，毫秒級完成，

Delta Table 要重寫 Parquet 、 UPDATE delta … 等，

可能花費數秒。



查詢效能更是傳統 SQL 優勢，

\-B-Tree 索引，點查詢極快

\-複雜 JOIN 優化器成熟

\-熱資料在記憶體中



**Delta Table 優勢**

\-列式儲存（Parquet），一次取 3個 columns 查詢快

\-自動分區裁剪（Partition Pruning）

\-Z-Order 優化跳過不相關檔案

\-雲端平行運算，PB 級資料也快

---



▋**選擇**建議

高頻點查詢不建議用 Delta 的場景，

因此一般來說應用系統都還是以 SLQ DB 為主軸，



 **適合用 Delta 的場景包含，**

\-批次寫入 + 歷史追蹤

\-批次 Upsert

\-分析系統



---



▋ 重點回顧

1. Open Table Format 旨在解決傳統資料湖缺乏 ACID 交易與版本控制等資料庫管理能力的問題。

2. Open Table Format 由實體資料檔案（如 Parquet）與一層交易層（Transaction Log）組成，其主要差異在於交易層的實作方式。

3. Delta Table 透過 Parquet 檔案與 `_delta_log`（JSON 交易日誌）的結合，來記錄所有操作並實現 ACID 特性。

4. Delta Table 確保 ACID 交易保證，使資料操作要麼全部成功，要麼在失敗時自動回滾，確保資料一致性。

5. Time Travel 功能允許使用者透過版本號或時間戳查詢歷史資料快照，可用於除錯、回滾資料或進行審計。

6. `MERGE` 語法提供簡潔的 Upsert（更新+插入）操作，能高效處理每日增量更新或資料同步。

7. 傳統 SQL DB 透過索引優化高頻點查詢，而 Delta Table 則依賴 Spark 對雲端 Parquet 檔案進行大規模平行運算分析。

8. 建議高頻點查詢的應用系統使用傳統 SQL DB，而需批次處理、歷史追蹤與分析的場景則適合使用 Delta Table。


