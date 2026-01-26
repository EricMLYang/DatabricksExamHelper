Developing Code for Data Processing using Python and SQL: 61%
Data Ingestion & Acquisition: 75%
Data Transformation, Cleansing and Quality: 66%
Data Sharing and Federation: 100%
Monitoring and Alerting: 100%
Cost & Performance Optimisation : 37%
Ensuring Data Security and Compliance: 66%
Data Governance: 75%
Debugging and Deploying: 100%
Data Modelling : 75%


考試小筆記:
出了bob上週說到的那些都要記，再額外補充以下給大家~
另外有些題目會把兩三個概念放一起考，重要觀念要記清楚
很多是考code 每個選項都很像要看仔細!
 
*每個都要知道
SCD Type 0（Slowly Changing Dimension Type 0）
原始值不變（Fixed Dimension）；不更新、不維護歷史，多用於不應被變更的屬性。
SCD Type 1
直接 UPDATE 覆蓋舊值，不保留歷史；只有一個最新版本。
SCD Type 2
每次變更都 新增一列，並把舊列標記為非 current（例如 current=false, end_date 設為結束時間）；
可完整保留所有歷史版本。
SCD Type 3
在同一列中保存現在值與有限數量的舊值（例如 current_address、previous_address），
不是多列歷史，而是「多欄位歷史」。
Delta Lake MERGE for SCD
常用 MERGE INTO + WHEN MATCHED ... UPDATE + WHEN NOT MATCHED ... INSERT
來實作各種型別的 SCD（尤其 Type 1, Type 2）。
 
*Materialized view 會將 view 的查詢結果 實際儲存成實體資料。
 
*Lakeflow Declarative Pipelines 中使用 AUTO CDC
 
*Databricks Unity Catalog權限
 
*使用 broadcast join 來避免大表 shuffle
 
*Deletion vectors 是 Delta Lake 的一種 metadata 結構，用來標記 data file 中哪些列「邏輯上被刪除」，而不需要立刻重寫整個檔案
 
*databricks secrets create-scope api_scope
databricks secrets put-secret api_scope api_key
api_key = dbutils.secrets.get("api_scope", "api_key")
 
*rank /dense rank/row number
 
*Auto optimize=Optimized+ Auto compaction:
 
*系統計費資料表 system.billing.usage 裡幾個重要欄位、以及怎麼用它們來看 DBU 使用量。逐項對應說明如下：
system.billing.usage: This is a system table that tracks billable usage in detail.
usage_unit = 'DBU': This explicitly filters the records to only show consumption measured in Databricks Units (DBUs), the standard unit of consumption for compute.
identity_metadata.run_as: This column logs the user or service principal (identity) who ran the workload. This is the per user component.
sku_name: This column identifies the specific type of computing resource (e.g., ALL_PURPOSE_COMPUTE, JOBS_COMPUTE, SERVERLESS_SQL) that consumed the DBUs. This gives the type of computing resource detail.
usage_quantity: This is the actual DBU consumption amount.
usage_date: This provides the daily temporal detail.
 
*兩個一起考
databricks jobs list-runs --job-id <job-id> --start-time-from <time-value>
databricks jobs list-runs --job-id <job-id> --completed-only
 
*In Auto Loader, “cloudFiles.maxBytesPerTrigger” controls the maximum amount of data to process in each micro-batch, allowing the stream to handle large files incrementally and keep batch processing times predictable.
* details:flow_progress:data_quality.expectations: specifically holds the expectation results。