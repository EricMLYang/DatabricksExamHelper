#考者的答對比例
Developing Code for Data Processing using Python and SQL: 53%
Data Ingestion & Acquisition: 75%
Data Transformation, Cleansing and Quality: 50%
Data Sharing and Federation: 33%
Monitoring and Alerting: 40%
Cost & Performance Optimisation : 50%
Ensuring Data Security and Compliance: 66%
Data Governance: 75%
Debugging and Deploying: 66%
Data Modelling : 50%

## 
以上是這次的考題分享~~! 題目的英文 都算很長,所以英文的理解很重要 QQ~
考前 要注意注意 通知信, 裡面有 Authorization Code (可以先截圖)
考前的安檢很嚴, 會請你拉衣袖與褲管, 不能戴手錶(一般的也不行), 也會檢查眼鏡, 不能帶紙筆(有提供小白板)

## 印象中的考題
### Data Skiping 的概念
 
### liquid clustering 概念
In this scenario, using liquid clustering on the combination of user_id and event_date is the best choice to avoid expensive scans. This technique incrementally optimizes data layout based on both columns, efficiently supporting filters on these columns and avoiding costly table scans.
 
  Partitioning only on event_date helps queries filtering by date but doesn’t optimize filtering by user_id, leading to potential full scans within partitions. Z-order indexing on user_id optimizes queries filtering on user_id but ignores event_date filtering, resulting in inefficient scans when filtering by date. Lastly, partitioning on user_id + Z-order on event_date supports filtering on both columns but can create many small partitions (if users are numerous), causing management and performance issues.

### The Query Profile
 The Query Profile view provides three panels: Details, Top operators, and Query text, which give insights into query execution metrics, the main operations involved, and the actual SQL code.

### Apache Arrow
Apache Arrow provides an efficient columnar in-memory data format that allows Spark to transfer data between the JVM and Python processes without serialization overhead. This significantly speeds up data processing compared to standard row-based formats.
- Databricks Asset Bundles 好像考三題
http://docs.databricks.com/aws/en/dev-tools/bundles/jobs-tutorial
https://docs.databricks.com/aws/en/dev-tools/cli/bundle-commands#databricks-bundle-deployment-bind

### Lakehouse Federation
Lakehouse Federation is a feature in Databricks that enables users to query data in external databases directly, such as Oracle and SQL Server, without the need for data replication, ingestion, or movement. It provides a unified analytics layer on top of multiple data sources and allows for federated queries, where data from various platforms can be combined into a single logical view.

### Job 的修復
In Databricks, when you use the “Repair run” for a failed job, the dialog allows you to tweak parameters for that specific run. These changes do not overwrite the job’s original configuration. They only apply to this repair run.

### 安全
databricks secrets create-scope api_scope
databricks secrets put-secret api_scope api_key
 
### Lakeflow Declarative Pipeline (LDP)
LDP supports the following expectation functions:
dlt.expect: it writes invalid rows to the target (warning semantics)
dlt.expect_or_drop: drops invalid rows before writing to the target.
dlt.expect_or_fail: fails the update if violation occurs
https://docs.databricks.com/aws/en/ldp/expectations
 
 
### AUTO Loader 的  option("mergeSchema", True)
 
### assertDataFrameEqual(actual_df, expected_df)
 
### CDF https://docs.databricks.com/aws/en/delta/delta-change-data-feed
 
### Python library
A data engineering team wants to ensure that a specific Python library is available every time a cluster starts.
Use an init script to install the library during cluster startup
 
### 有類似
df = spark.readStream.format("cloudFiles") \
          .option("cloudFiles.format", "binaryFile") \
          .option("pathGlobfilter", "*.jpg") \
          .load(“/source/x-ray”)
### 類似
window_spec = Window.partitionBy("department").orderBy(df["salary"].desc())          
df.withColumn("tier", row_number().over(window_spec))
 
### unit TEST 概念
https://docs.databricks.com/aws/en/notebooks/testing
 
### It allows for modular, composable, and testable transformations.
def normalize_email(df):
    return df.withColumn("email", col("email").lower())
def calculate_total(df):
    return df.withColumn("total_amount", col("quantity") * col("unit_price"))
 
orders_transformed = orders.transform(normalize_email).transform(calculate_total)
 
### Delta Sharing
Delta Sharing is designed to securely share data across platforms using an open protocol. Since the vendor does not use Databricks, Delta Sharing ensures secure, real-time access without manual exports or third-party workarounds.
 
### 費用的部分,考的sql 比這個複雜
SELECT
    identity_metadata.run_as,
    sku_name,
    usage_date,
    usage_quantity
FROM system.billing.usage
WHERE usage_unit = 'DBU'
 
### Git 的概念有考
 
### UDF(user-defined functions) 有考
CREATE FUNCTION mask_ssn(ssn STRING)
RETURN CASE WHEN is_member('hr_team')
THEN ssn ELSE '***-**-****' END;
CREATE TABLE persons(name STRING, ssn STRING MASK mask_ssn);
 
https://docs.databricks.com/aws/en/data-governance/unity-catalog/filters-and-masks/manually-apply
 
### 這個有命中
A data engineering team at a retail company frequently collaborates with business analysts to generate insights from Unity Catalog tables. Over time, the analysts have reported confusion about several columns in key tables because the existing company documentation is outdated. To improve efficiency and reduce misinterpretation, the team lead recommends adding clear descriptions for all table columns. However, manually documenting hundreds of tables and columns would be time-consuming and likely to introduce inconsistencies.
Which of the following approaches allows the team to achieve this task automatically?
答案
Use the AI-generated column comments feature in Unity Catalog Explorer.
 
### 考類似的語法
ALTER TABLE table_name SET TAGS ('tag_key1' = 'tag_value1', 'tag_key2' = 'tag_value2');
 
### LDP 的 log table 有考
 
### shuffle 的解法 答案好像是這個
Use salting by appending a random prefix to skewed user_id values to distribute the load across partitions.
 
### 類似 %pip install my_package.whl 的概念
 
### Spark UI 的選項內容
 
### USE SCHEMA 的權限
 
### databricks jobs list-runs --job-id <job-id> --start-time-from <time-value>
 