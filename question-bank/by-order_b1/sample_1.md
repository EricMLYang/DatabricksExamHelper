# Question 1

## Question
A data engineering team at a supply chain company uses Lakeflow Declarative Pipelines to manage inventory data. The team maintains a streaming table, inventory_updates, with Change Data Feed (CDF) enabled. The table captures real-time changes to product inventory levels, with columns: product_id, quantity, and update_timestamp.




The team needs to incrementally propagate all inventory changes from the inventory_updates table to downstream layers.




Which implementation approach correctly satisfies this requirement?

## Options
- A. Use spark.readStream to consume the inventory_updates table with skipChangeCommits, and propagate the newly added data incrementally to downstream tables. 
- B. Use spark.readStream to consume the inventory_updates table directly, and propagate the new updates incrementally to downstream tables. 
- C. Use spark.readStream to consume the inventory_updates table’s CDF, and apply the changes into downstream tables using AUTO CDC APIs. (Correct)
- D. Use spark.read to consume the inventory_updates table’s CDF, and merge the changes into downstream tables using MERGE INTO. 

## Explanation
Because the inventory_updates table contains updates and deletes, it breaks the append-only requirement of standard streaming tables. This means that we cannot directly stream from the base table or just skip change commits. Instead, since Change Data Feed (CDF) is enabled, the correct approach is to use spark.readStream to consume all inventory changes - including inserts, updates, and deletes - from the CDF output and apply them downstream using AUTO CDC APIs (previously known as APPLY CHANGES APIs).




Remember, to read the change data feed from a table, you need to set the option readChangeFeed to true when configuring a stream read from the table, as shown in the following syntax example:



```

- (spark.readStream
-       .option("readChangeFeed", "true")
-       .table("inventory_updates")
- )
```





Note that using spark.read here is a completely incorrect approach as it performs batch processing, not incremental processing, which would require a full table refresh each time. In addition, MERGE INTO command is not supported in Lakeflow Declarative Pipelines, making this method unsuitable for incremental change propagation.

---

# Question 2

## Question
A data engineering team at a large analytics company is working on improving data governance and cataloging across their Databricks environment. As part of this initiative, the lead data engineer is tasked with applying descriptive tags to several tables in the company’s Delta Lake to make data discovery and management easier. While reviewing documentation, the engineer encounters multiple SQL command formats for setting tags on tables in Databricks and wants to confirm which command syntax is valid.




Which of the following is Not a correct command to set tags on a table in Databicks?

## Options
- A. ALTER TABLE table_name SET TAG tag_key = tag_value; (Correct)
- B. ALTER TABLE table_name SET TAGS ('tag_key1' = 'tag_value1', 'tag_key2' = 'tag_value2'); 
- C. SET TAG ON TABLE table_name tag_key = tag_value; 
- D. SET TAG ON TABLE table_name tag_key; 

## Explanation
In Databricks SQL, there are two forms to set tags on tables:



- 

The plural form using ALTER TABLE ... SET TAGS (...), which allows setting or one or multiple tags at once:

`ALTER TABLE table_name SET TAGS ('tag_key1' = 'tag_value1', 'tag_key2' = 'tag_value2');`

`ALTER TABLE table_name SET TAGS ('tag_key' = 'tag_value');`



- 

The singular form using SET TAG ON TABLE ... which is used to set individual tags.

`SET TAG ON TABLE table_name tag_key = tag_value;`




Notice that the tag_value is an optional identifier. If not specified, the tag assignment will be set as key-only.

`SET TAG ON TABLE table_name tag_key;`

---

# Question 3

## Question
A data engineer wants to pass multiple parameters from a Databricks Job to a notebook. They already configured the key and value of each parameter in the configurations of the job.




Which of the following utilities can the data engineer use to read the passed parameters inside the notebook ?

## Options
- A. dbutils.library 
- B. dbutils.notebook 
- C. dbutils.widgets (Correct)
- D. dbutils.secrets 

## Explanation
dbutils.widgets allow you to add parameters to your notebooks.




Example: Adding a parameter named ‘param1’
```

- ​​dbutils.widgets.text("param1", "default")
- param1 = dbutils.widgets.get("param1")
```





The defined parameters can be passed from Databricks Jobs by adding them to the Parameters section in the task configuration.







Reference: https://docs.databricks.com/notebooks/widgets.html




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 4

## Question
Which of the following functions can a data engineer use to return a new DataFrame containing the distinct rows from a given DataFrame based on multiple columns?

## Options
- A. pyspark.sql.DataFrame.dropDuplicates (Correct)
- B. pyspark.sql.DataFrame.distinct 
- C. pyspark.sql.DataFrame.drop 
- D. pyspark.sql.DataFrame.dropna 

## Explanation
pyspark.sql.DataFrame.dropDuplicates function returns a new DataFrame with duplicate rows removed, optionally only considering certain columns.




Reference:

https://spark.apache.org/docs/3.1.2/api/python/reference/api/pyspark.sql.DataFrame.dropDuplicates.html




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 5

## Question
The data engineering team has a singleplex bronze table called ‘orders_raw’ where new orders data is appended every night. They created a new Silver table called ‘orders_cleaned’ in order to provide a more refined view of the orders data.




The team wants to create a batch processing pipeline to process all new records inserted in the orders_raw table and propagate them to the orders_cleaned table.




Which solution minimizes the compute costs to propagate this batch of data?

## Options
- A. Use Spark Structured Streaming's foreachBatch logic to process the new records from orders_raw using trigger(processingTime=”24 hours") 
- B. Use batch overwrite logic to reprocess all records in orders_raw and overwrite the orders_cleaned table 
- C. Use time travel capabilities in Delta Lake to compare the latest version of orders_raw with one version prior, then write the difference to the orders_cleaned table. 
- D. Use Spark Structured Streaming to process the new records from orders_raw in batch mode using the trigger availableNow option (Correct)

## Explanation
`trigger(availableNow=True)` is more compute-efficient for one-time or scheduled batch runs, as it processes all available data once and stops, avoiding the overhead of keeping a cluster running. While, the `processingTime` option keeps the stream active continuously, so it’s less efficient for nightly jobs.




There is also the `trigger(once=True)` option for incremental batch processing. However, this setting is now deprecated in the newer Databricks Runtime versions.

NOTE: You may still see this option in the current certification exam version. However, Databricks recommends you use `trigger(availableNow=True)` for all future incremental batch processing workloads.




Study materials from our exam preparation course on Udemy:
- 

Lecture
- 

Hands-on
- 

Lecture (Associate course)

---

# Question 6

## Question
Given the following streaming query:



```

- spark.readStream
-         .table("orders_cleaned")
-         .withWatermark("order_timestamp", "10 minutes")
-         .groupBy(
-             window("order_timestamp", "5 minutes").alias("time"),
-             "author")
-         .agg(
-             count("order_id").alias("orders_count"),
-             avg("quantity").alias("avg_quantity"))
-     .writeStream
-         .option("checkpointLocation", "dbfs:/path/checkpoint")
-         .table("orders_stats")
```





Which of the following statements best describe this query ?

## Options
- A. It calculates business-level aggregates for each overlapping ten-minute interval. Incremental state information is maintained for 5 minutes for late-arriving data. 
- B. It calculates business-level aggregates for each overlapping five-minute interval. Incremental state information is maintained for 10 minutes for late-arriving data. 
- C. It calculates business-level aggregates for each non-overlapping five-minute interval. Incremental state information is maintained for 10 minutes for late-arriving data. (Correct)
- D. It calculates business-level aggregates for each non-overlapping ten-minute interval. Incremental state information is maintained for 5 minutes for late-arriving data. 

## Explanation
Pyspark.sql.functions.window function bucketizes rows into one or more time windows given a timestamp specifying column. In this query, we are performing aggregations per order_timestamp for each non-overlapping five minute interval.




pyspark.sql.DataFrame.withWatermark function allows you to only track state information for a window of time in which we expect records could be delayed. Here we define a watermark of 10 minutes.




Reference:

https://spark.apache.org/docs/3.1.3/api/python/reference/api/pyspark.sql.functions.window.html

https://spark.apache.org/docs/3.1.1/api/python/reference/api/pyspark.sql.DataFrame.withWatermark.html




Study materials from our exam preparation course on Udemy:

Hands-on

Hands-on

---

# Question 7

## Question
A data engineer has the following query to join the large sales table (about 10 billion records) with a smaller customers table (about 5 million records):



```

- SELECT ______________
-     s.sale_id, s.amount, c.customer_name
- FROM sales AS s
- INNER JOIN customers AS c
- ON s.customer_id = c.customer_id;
```





The engineer wants to add a broadcast hint to instruct the query optimizer to perform a broadcast join on the customers table.




Which option correctly fills in the blank to achieve this?

## Options
- A. BROADCAST(c) 
- B. /*+ BROADCAST(c) */ (Correct)
- C. - - BROADCAST(c) -- 
- D. BROADCAST ON (c) 

## Explanation
In Spark SQL, to explicitly hint that a smaller table should be broadcast in a join, you use the `/*+ BROADCAST(table_alias) */` syntax before the SELECT keyword:



```

- SELECT /*+ BROADCAST(c) */
-     s.sale_id, s.amount, c.customer_name
- FROM sales AS s
- INNER JOIN customers AS c
- ON s.customer_id = c.customer_id;
```





This tells Spark to broadcast the customers table (small table) to all worker nodes, enabling a much faster join with the huge sales table.




Remember, broadcasting the smaller table sends it to all worker nodes so each partition of the large table can join locally, avoiding expensive shuffles across the cluster. This drastically reduces network I/O and speeds up the join when one table is much smaller than the other.

---

# Question 8

## Question
A data engineering team at a large cloud services company is responsible for ensuring high availability and performance of hundreds of servers. To proactively detect unusual spikes or drops in CPU utilization that could indicate potential issues, the team decides to analyze server CPU usage. They want to capture both the minimum and maximum CPU usage during predefined intervals for each server, allowing them to quickly identify patterns of high or low utilization and trigger alerts if necessary.




The team writes the following query:
```

- SELECT
-     server_id,
-     window.start AS window_start,
-     window.end AS window_end,
-     MIN(cpu_usage) AS min_cpu,
-     MAX(cpu_usage) AS max_cpu
- FROM server_metrics
- GROUP BY server_id,
-          window(event_time, '10 minutes', '10 minutes', '3 minutes')
- ORDER BY server_id,
-          window_start;
```


 

What is the primary purpose of this query in the context of the data engineering team’s objectives?

## Options
- A. To calculate the metrics per server for every 10-minute interval, sliding every 3 minutes, with a 10-minute offset. 
- B. To calculate the metrics per server for every non-overlapping 10-minute interval, offset by 3 minutes (Correct)
- C. To calculate the metrics per server for every non-overlapping 3-minute interval, offset by 10 minutes 
- D. To calculate the metrics per server for every 3-minute interval, sliding every 10 minutes, with a 10-minute offset. 

## Explanation
The signature of the window function in Spark SQL is:

`window(time_column, window_size, slide_interval, starting_offset)`



- 

window_size: how long each window lasts.
- 

slide_interval (sometimes called step): how often a new window starts.
- 

starting_offset: shifts all windows forward or backward in time.




In this question, the function was:

`window(event_time, '10 minutes', '10 minutes', '3 minutes')`



- 

window_size = '10 minutes' → Each window spans 10 minutes.
- 

slide_interval = '10 minutes' → Windows slide every 10 minutes, i.e., non-overlapping.
- 

starting_offset= '3 minutes' → Windows start 3 minutes later than the natural alignment.




So, the query is computing 10-minute windows for each server, with a 3-minute offset, and aggregating MIN and MAX CPU usage in each window.

---

# Question 9

## Question
A data engineer claims that if they grant SELECT on the HR catalog to a reporting team, the team will automatically have SELECT access to any new tables or views added to the catalog next month. The engineer argues that this approach will save time because they won’t have to grant access for each new table or view individually.




What is the accuracy of this claim?

## Options
- A. True, because grants at the catalog level apply to current and future objects in the catalog. (Correct)
- B. True, but only for tables, not views. 
- C. True, but only for views, not tables. 
- D. False, new tables and views must be granted SELECT privileges separately. 

## Explanation
With the Unity Catalog inheritance model, you can grant a user the SELECT privilege on a catalog or schema, which automatically grants the user SELECT privilege on all current and future tables, and views in the catalog or schema.

---

# Question 10

## Question
A data engineer has a Delta Lake table named ‘orders_archive’ created using the following command:



```

- CREATE TABLE orders_archive
- DEEP CLONE orders
```





They want to sync up the new changes in the orders table to the clone.




Which of the following commands can be run to achieve this task ?

## Options
- A. SYNC orders_archive 
- B. INSERT OVERWRITE orders_archive

SELECT * FROM orders 
- C. REFRESH orders_archive 
- D. CREATE OR REPLACE TABLE orders_archive

DEEP CLONE orders (Correct)

## Explanation
Cloning can occur incrementally. Executing the `CREATE OR REPLACE TABLE` command can sync changes from the source to the target location.

Now, If you run `DESCRIBE HISTORY orders_archive`, you will see a new version of CLONE operation occurred on the table.




* The last choice in the question is incorrect since dropping the table will lead to removing all the table's history.







Reference:

https://docs.databricks.com/delta/clone.html




Study materials from our exam preparation course on Udemy:

Lecture (Associate course)

---

# Question 11

## Question
A data engineer has a PySpark DataFrame with the following columns: employee_name, department, and salary. They want to assign a tier to each employee within their department based on salary, where employees earning the same salary share the same tier. The expected output is as follows:








To achieve this, they define a window by department and order by salary in descending order:




`window_spec = Window.partitionBy("department").orderBy(df["salary"].desc())`




Which of the following functions correctly use this window to calculate the tier column?

## Options
- A. df.withColumn("tier", percent_rank().over(window_spec)) 
- B. df.withColumn("tier", row_number().over(window_spec)) 
- C. df.withColumn("tier", rank().over(window_spec)) 
- D. df.withColumn("tier", dense_rank().over(window_spec)) (Correct)

## Explanation
The `dense_rank()` function assigns consecutive rank numbers based on the ordering within each department while ensuring that employees with the same salary receive the same rank or “tier”.




Unlike `rank()`, which skips numbers after ties (e.g., 1, 1, 3), `dense_rank()` produces a continuous sequence (e.g., 1, 1, 2), matching the desired output. `row_number()` would give each row a unique rank even if salaries are the same, and `percent_rank()` would instead assign fractional values between 0 and 1 rather than integer tiers.




Therefore, `dense_rank()` is the appropriate function to correctly assign salary-based tiers within each department.

---

# Question 12

## Question
A data engineer has the following streaming query with a blank:



```

- spark.readStream
-        .table("orders_cleaned")
-        ____________________________
-        .groupBy(
-            "order_timestamp",
-            "author")
-        .agg(
-            count("order_id").alias("orders_count"),
-            avg("quantity").alias("avg_quantity"))
-     .writeStream
-        .option("checkpointLocation", "dbfs:/path/checkpoint")
-        .table("orders_stats")
```





For handling late-arriving data, they want to maintain the streaming state information for 30 minutes. 




Which option correctly fills in the blank to meet this requirement ?

## Options
- A. .trigger(processingTime=”30 minutes") 
- B. .withWatermark("order_timestamp", "30 minutes") (Correct)
- C. .awaitWatermark("order_timestamp", "30 minutes") 
- D. .window("order_timestamp", "30 minutes") 

## Explanation
pyspark.sql.DataFrame.withWatermark function allows you to only track state information for a window of time in which we expect records could be delayed.




Reference:

https://spark.apache.org/docs/3.1.1/api/python/reference/api/pyspark.sql.DataFrame.withWatermark.html




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 13

## Question
A data engineer is building a streaming pipeline using Databricks Autoloader to ingest JSON files from an S3 bucket into a target Delta table. The engineer wants the pipeline to automatically handle problematic files and store them separately so they can be inspected later. Specifically, the engineer wants to:



- 

Exclude files that are badly-formed JSON.
- 

Exclude files that do not match the expected schema.




Which of the following code blocks meets the specified requirement?

## Options
- A. ```

- df = (spark.readStream
-             .format("cloudFiles")
-             .option("cloudFiles.format", "json")
-             .option("badRecordsPath", "s3://project/quarantine")
-             .schema("id int, value double")
-             .load("s3://project/source/"))
``` (Correct)
- B. ```

- df = (spark.readStream
-             .format("cloudFiles")
-             .option("cloudFiles.format", "json")
-             .option("cloudFiles.schemaLocation", "s3://project/schema")
-             .option("pathGlobFilter", "*.json", "s3://project/quarantine")
-             .load("s3://project/source/"))
``` 
- C. ```

- df = (spark.readStream
-             .format("cloudFiles")
-             .option("cloudFiles.format", "json")
-             .schema("id int, value double")
-             .rescue("s3://project/quarantine")
-             .load("s3://project/source/"))
``` 
- D. ```

- df = (spark.readStream
-             .format("cloudFiles")
-             .option("cloudFiles.format", "json")
-             .option("cloudFiles.schemaEvolutionMode", "rescue", "s3://project/quarantine")
-             .schema("id int, value double")
-             .load("s3://project/source/"))
``` 

## Explanation
The `badRecordsPath` option is the standard configuration for handling bad records in Auto Loader:




1. Handling Badly-Formed Files (e.g., Syntax Errors)

The `badRecordsPath` option is a Spark standard for the JSON format (and other formats like CSV). When set, any file that cannot be parsed due to malformed syntax (e.g., non-JSON content, missing brackets, extra commas) is moved to the specified path, fulfilling the requirement for excluding badly-formed JSON.




2. Handling Schema Mismatches (e.g., Data Type Errors, Missing Fields)

When `badRecordsPath` is set, any record that results in an error during parsing (including schema mismatch errors like failed type casting) is automatically written to the specified quarantine location instead of being dropped or failing the stream.

---

# Question 14

## Question
The data engineering team wants to build a pipeline that receives customers data as change data capture (CDC) feed from a source system. The CDC events logged at the source contain the data of the records along with metadata information. This metadata indicates whether the specified record was inserted, updated, or deleted. In addition to a timestamp column identified by the field update_time indicating the order in which the changes happened. Each record has a primary key identified by the field customer_id.




In the same batch, multiple changes for the same customer could be received with different update_time. The team wants to store only the most recent information for each customer in the target Delta Lake table.




Which of the following solutions meets these requirements?

## Options
- A. Use MERGE INTO to upsert the most recent entry for each customer_id into the table (Correct)
- B. Use dropDuplicates function to remove duplicates by customer_id, then merge the duplicate records into the table. 
- C. Use MERGE INTO with SEQUENCE BY clause on the update_time for ordering how operations should be applied 
- D. Enable Delta Lake's Change Data Feed (CDF) on the target table to automatically merge the received CDC feed 

## Explanation
`MERGE INTO` command allows you to upsert data from a source table, view, or DataFrame into a target Delta table. Delta Lake supports inserts, updates, and deletes in merge operations.




Note: The option to use SEQUENCE BY with MERGE INTO is incorrect because this clause only applies to AUTO CDC and APPLY CHANGES INTO, not to MERGE statements. Attempting to use SEQUENCE BY with MERGE INTO will result in a syntax error.




Reference:

https://docs.databricks.com/delta/merge.html







Study materials from our exam preparation course on Udemy:

Lecture

Hands-on

---

# Question 15

## Question
A data engineer is tasked with creating a comprehensive dashboard to track and analyze the consumption of computing resources across various workloads in their organization. To accomplish this, the engineer writes the following SQL query against the usage system table:



```

- SELECT
-     identity_metadata.run_as,
-     sku_name,
-     usage_date,
-     usage_quantity
- FROM system.billing.usage
- WHERE usage_unit = 'DBU'
```





Which of the following statements most accurately describes the purpose and level of detail provided by this query?

## Options
- A. It monitors the detailed DUB consumption for each type of computing resource per workspace. 
- B. It monitors the detailed DUB consumption for each pipeline run per compute type. 
- C. It monitors the detailed DUB consumption for each type of computing resource per user. (Correct)
- D. It monitors the detailed DUB consumption for each job run per compute type. 

## Explanation
This query aggregates the DBU usage by the user who ran the workload (run_as) and the specific resource type (sku_name) on a daily basis.




Here's a breakdown of why:
- 

system.billing.usage: This is a system table that tracks billable usage in detail.
- 

usage_unit = 'DBU': This explicitly filters the records to only show consumption measured in Databricks Units (DBUs), the standard unit of consumption for compute.
- 

identity_metadata.run_as: This column logs the user or service principal (identity) who ran the workload. This is the per user component.
- 

sku_name: This column identifies the specific type of computing resource (e.g., ALL_PURPOSE_COMPUTE, JOBS_COMPUTE, SERVERLESS_SQL) that consumed the DBUs. This gives the type of computing resource detail.
- 

usage_quantity: This is the actual DBU consumption amount.
- 

usage_date: This provides the daily temporal detail.

---

# Question 16

## Question
Which of the following statements best describes Delta Lake Auto Compaction?

## Options
- A. Auto Compaction occurs after a write to a table has succeeded to check if files can further be compacted; if yes, it runs an OPTIMIZE job with Z-Ordering toward a file size of 128 MB. 
- B. Auto Compaction occurs after a write to a table has succeeded to check if files can further be compacted; if yes, it runs an OPTIMIZE job without Z-Ordering toward a file size of 128 MB. (Correct)
- C. Auto Compaction occurs after a write to a table has succeeded to check if files can further be compacted; if yes, it runs an OPTIMIZE job without Z-Ordering toward a file size of 1 GB. 
- D. Auto Compaction occurs after a write to a table has succeeded to check if files can further be compacted; if yes, it runs an OPTIMIZE job with Z-Ordering toward a file size of 1 GB. 

## Explanation
Auto Compaction is part of the Auto Optimize feature in Databricks. it checks after an individual write, if files can further be compacted, if yes, it runs an OPTIMIZE job with 128 MB file sizes instead of the 1 GB file size used in the standard OPTIMIZE




Auto compaction does not support Z-Ordering as Z-Ordering is significantly more expensive than just compaction.




Reference:

https://docs.databricks.com/delta/tune-file-size.html#auto-compaction-for-delta-lake-on-databricks




Study materials from our exam preparation course on Udemy:

Lecture

---

# Question 17

## Question
A junior data engineer is testing the following code block to get the newest entry for each item added in the ‘sales’ table since the last table update.



```

- from pyspark.sql import functions as F
- from pyspark.sql.window import Window
-  
- window = Window.partitionBy("item_id").orderBy(F.col("item_time").desc())
-  
- ranked_df = (spark.readStream
-                     .table("sales")
-                     .withColumn("rank", F.rank().over(window))
-                     .filter("rank == 1")
-                     .drop("rank")
-             )
-  
- display(ranked_df)
```





However, the command fails when executed.




Which statement explains the cause of this failure?

## Options
- A. Non-time-based window operations are not supported on streaming DataFrames. They need to be implemented inside a foreachBatch logic instead. (Correct)
- B. The query output can not be displayed. They should use spark.writeStream to persist the query result. 
- C. The item_id field is not unique. Records must be de-duplicated on the item_id using dropDuplicates function 
- D. Watermarking is missing. It should be added to allow tracking state information for the window of time. 

## Explanation
If you try to call such a window operation on a streaming DataFrames, this will generate an error indicating that “Non-time-based window operations are not supported on streaming DataFrames”.

Instead, these window operations need to be implemented inside a foreachBatch logic.




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 18

## Question
A data engineering team at a retail company is planning to implement Liquid Clustering to optimize the performance of an existing Delta table under 1 TB. The team intends to alter the table to use Liquid Clustering and schedule periodic OPTIMIZE commands. Before full deployment, the team wants to understand the key characteristics and limitations of enabling this optimization technique on their existing table.




Which of the following statements is NOT a correct description of Liquid Clustering?

## Options
- A. Liquid Clustering is fully compatible with Z-order indexing and Hive-style table partitioning within the same table. (Correct)
- B. Liquid Clustering helps reduce skew in data distribution by maintaining balanced clustering across data files. 
- C. Liquid Clustering can easily evolve as data patterns change, offering flexibility without manual repartitioning. 
- D. Liquid Clustering supports incremental clustering operations that allow data to be organized efficiently over time. 

## Explanation
Liquid Clustering is a replacement for both partitioning and Z-ordering, and they can’t be used simultaneously on the same Delta table. Liquid Clustering provides a more flexible and efficient way to cluster data than traditional fixed partitioning or Z-ordering.




Correct Characteristics of Liquid Clustering:
- 

Unlike ZORDER, liquid clustering supports incremental clustering operations that allow data to be organized efficiently over time. Clustering operations using the OPTIMIZE command are incremental, meaning they only recluster data files that have changed, making the process efficient and fast.
- 

Liquid Clustering can easily evolve as data patterns change, offering flexibility without manual repartitioning. Unlike traditional static partitioning, liquid clustering adapts seamlessly to new clustering keys.
- 

Liquid Clustering helps reduce skew in data distribution by maintaining balanced clustering across data files. The primary goal of clustering techniques like Liquid Clustering is to group similar data together across a minimal number of data files, which inherently helps to reduce data skew.

---

# Question 19

## Question
The data engineering team has a large external Delta table where new changes are merged very frequently. They enabled Optimized writes and Auto Compaction on the table in order to automatically compact small data files to target files of size 128 MB. However, when they look at the table directory, they see that most data files are smaller than 128 MB.




Which of the following likely explains these smaller file sizes ?

## Options
- A. Auto compaction supports Auto Z-Ordering which is more expensive than just compaction 
- B. Optimized Writes and Auto Compaction have no effect on external tables. The table needs to be managed in order to store the information of file sizes in the Hive metastore. 
- C. Optimized Writes and Auto Compaction automatically generate smaller data files to reduce the duration of future MERGE operations. (Correct)
- D. Optimized Writes and Auto Compaction have no effect on large Delta tables. The table needs to be partitioned so Auto Compaction can be applied at partition level. 

## Explanation
Having many small files can help minimize rewrites during some operations like merges and deletes. For such operations, Databricks can automatically tune the file size of Delta tables. As a result, it can generate data files smaller than the default 128MB. This helps in reducing the duration of future MERGE operations.




Reference:

https://docs.databricks.com/delta/tune-file-size.html#autotune-file-size-based-on-workload




Study materials from our exam preparation course on Udemy:

Lecture

---

# Question 20

## Question
The data engineering team maintains a Type 1 table that is overwritten each night with new data received from the source system.




A junior data engineer has suggested enabling the Change Data Feed (CDF) feature on the table in order to identify those rows that were updated, inserted, or deleted.




Which response to the junior data engineer's suggestion is correct?

## Options
- A. CDF is useful when the table is a Slowly Changing Dimension (SCD) of Type 2 
- B. CDF can not be enabled on existing tables. It can only be enabled on newly created tables. 
- C. CDF is useful when only a small fraction of records are updated in each batch (Correct)
- D. Table’s data changes captured by CDF can only be read in streaming mode 

## Explanation
Generally speaking, we use CDF for sending incremental data changes to downstream tables in a multi-hop architecture. So, use CDF when only small fraction of records updated in each batch. Such updates are usually received from external sources in CDC format. If most of the records in the table are updated, or if the table is overwritten in each batch, like in the question, don’t use CDF.




Here is some guidance for when to use CDF (from the below reference link)







Reference:

https://www.databricks.com/blog/2021/06/09/how-to-simplify-cdc-with-delta-lakes-change-data-feed.html




Study materials from our exam preparation course on Udemy:

Lecture

Hands-on

---

# Question 21

## Question
Which of the following statements correctly describes the sys.path Python variable?

## Options
- A. The sys.path variable contains a list of directories where the Python interpreter searches for modules. (Correct)
- B. The sys.path variable contains a list of all the parameters passed to a Python notebook. 
- C. The sys.path variable contains the full pathname of the current working directory of a Python notebook. 
- D. The sys.path variable contains a list of all the necessary dependencies for a Python notebook. 

## Explanation
The sys.path variable contains a list of directories where the Python interpreter searches for modules.




To import modules from another directory, you must add it to sys.path



```

- import sys
- sys.path.append("/path/to/dir")
```








Reference:

https://docs.databricks.com/files/workspace-modules.html#import-python-and-r-modules-1




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 22

## Question
A data engineer uses the following SQL query:




`GRANT MANAGE ON CATALOG hr_catalog TO hr_team`




Which of the following describes the ability given by the MANAGE privilege ?

## Options
- A. It gives the ability to manage the catalog configurations including the default storage location. 
- B. It gives the ability to control the catalog’s access permissions by granting or revoking privileges. (Correct)
- C. It gives the ability to control the catalog’s query execution and performance settings. 
- D. It gives the ability to manage the catalog’s system tables and their underlying data files. 

## Explanation
In Unity Catalog, the `MANAGE` privilege allows delegating permission management to a user or a group without giving them full admin rights.

---

# Question 23

## Question
A data engineer is cleaning a DataFrame orders and wants to calculate new columns using chained transformations:



```

- def normalize_email(df):
-     return df.withColumn("email", col("email").lower())
-  
- def calculate_total(df):
-     return df.withColumn("total_amount", col("quantity") * col("unit_price"))
-  
- orders_transformed = orders.transform(normalize_email).transform(calculate_total)
```





What is the key advantage of using the transform function in this scenario?

## Options
- A. It converts the DataFrame to an RDD before transformations. 
- B. It ensures transformations run in parallel on multiple nodes automatically. 
- C. It allows for modular, composable, and testable transformations. (Correct)
- D. It automatically caches the DataFrame after each transformation. 

## Explanation
The key advantage of using the transform function in this scenario is that it allows for modular, composable, and testable transformations, because transform lets you apply reusable functions to a DataFrame in a clean, chainable way, making each transformation self-contained and easier to maintain, test, and combine, without affecting execution parallelism.

---

# Question 24

## Question
A data engineer has added a CHECK constraint to the sales table using the following command:




`ALTER TABLE sales ADD CONSTRAINT valid_date CHECK (item_date >= '2024-01-01');`




In addition, they have added a comment on the item_date column using the following command:




`ALTER TABLE sales ALTER COLUMN item_date COMMENT "Date must be newer than Jan 1, 2024";`




Which of the following commands allows the data engineer to verify that both the constraint and the column comment have been successfully added on the table ?

## Options
- A. SHOW TBLPROPERTIES sales 
- B. DESCRIBE DETAIL sales 
- C. DESCRIBE TABLE sales 
- D. DESCRIBE EXTENDED sales (Correct)

## Explanation
`DESCRIBE TABLE EXTENDED` or simply `DESCRIBE EXTENDED` allows to show the added tables constraints in the ‘Table Properties’ field. It shows both the name and the actual condition of the check constraints.




In addition, `DESCRIBE EXTENDED` allows to show the comments on each column, and the comment on the table itself.









Reference:
- 

https://docs.databricks.com/sql/language-manual/sql-ref-syntax-aux-describe-table.html
- 

https://docs.databricks.com/tables/constraints.html#set-a-check-constraint-in-databricks




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 25

## Question
A data engineering team is running a complex analytical query on a large dataset, but they notice that the query execution results in a significant disk spill, which drastically slows down performance.




Which of the following approaches would NOT be an effective solution to minimize this issue?

## Options
- A. Reduce the size of Spark partitions 
- B. Increase memory size 
- C. Increase the number of CPU cores (Correct)
- D. Increase the number of shuffle partitions 

## Explanation
The issue described is disk spill during a Spark analytical query. Disk spill occurs when the data being processed does not fit into the memory allocated for a task, so Spark writes intermediate data to disk, which is much slower than in-memory processing.




The following option would effectively reduce disk spill:

- Reduce the size of Spark partitions
- 

Smaller partitions can help reduce memory pressure per task because each task handles less data that can fit in memory.

- Increase memory size (core-to-memory ratio)
- 

More memory allows Spark to keep more data in-memory and reduce spills.

- Increase the number of shuffle partitions
- 

Increasing shuffle partitions spreads the data across more tasks, reducing memory pressure per task.




However, more CPU cores allow more tasks to run in parallel, but it does not reduce the amount of memory each task requires. If memory per task is insufficient, disk spills will still happen. So, this does NOT directly address disk spill.

---

# Question 26

## Question
The data engineering team has a Delta Lake table created with following query:



```

- CREATE TABLE target
- AS SELECT * FROM source
```





A data engineer wants to drop the source table with the following query:

`DROP TABLE source`




Which statement describes the result of running this drop command ?

## Options
- A. Only the source table will be dropped, but the target table will be no more queryable 
- B. Both the target and source tables will be dropped 
- C. An error will occur indicating that other tables are based on this source table 
- D. Only the source table will be dropped, while the target table will not be affected (Correct)

## Explanation
`CREATE TABLE AS SELECT` statements, or CTAS statements create new Delta tables and populate them using the output of a SELECT query. So, when dropping the source table, the target table will not be affected.




Reference: (cf. AS query clause)

https://docs.databricks.com/sql/language-manual/sql-ref-syntax-ddl-create-table-using.html







Study materials from our exam preparation course on Udemy:
- 

Lecture (Associate course)
- 

Hands-on (Associate course)

---

# Question 27

## Question
A data engineer is working on a project where they need to integrate data from an external API into a Databricks workspace. For security reasons, they do not want to hardcode the API Key directly in their notebooks. Instead, they want to use Databricks Secrets to securely store and manage sensitive credentials.




Which Databricks CLI commands should they use to accomplish this goal?

## Options
- A. ```

- databricks secrets create-secret api_secrets
- databricks secrets put-scope api_key api_secrets
``` 
- B. ```

- databricks secrets create-scope api_scope
- databricks secrets put-secret api_key api_scope
``` 
- C. ```

- databricks secrets create-secret api_secrets
- databricks secrets put-scope api_secrets api_key
``` 
- D. ```

- databricks secrets create-scope api_scope
- databricks secrets put-secret api_scope api_key
``` (Correct)

## Explanation
The correct Databricks CLI commands to securely store a secret in Databricks Secrets are:




1- Create a new secret scope:

`databricks secrets create-scope SCOPE`




2- Add a secret to that scope

`databricks secrets put-secret SCOPE KEY`




This approach ensures that sensitive credentials are managed securely without hardcoding them in notebooks.







Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 28

## Question
A data engineer is tasked with designing an ETL pipeline with Lakeflow Declarative Pipelines to efficiently handle near real-time data ingestion. The goal is to incrementally process incoming data streams using Auto Loader, ensuring that the data pipeline can continuously capture and load new records as they arrive while maintaining high performance and reliability.




Given this requirement, the engineer needs to choose an appropriate type of object that can best support incremental, near real-time data ingestion and processing.




Which of the following objects would be most suitable for this specific use case?

## Options
- A. Materialized view 
- B. Temporary view 
- C. Streaming table (Correct)
- D. Live table 

## Explanation
For this use case, the most suitable object is a Streaming table. Streaming tables are designed to handle near real-time data ingestion and incremental processing, allowing Lakeflow Declarative Pipelines* to continuously capture and process new records as they arrive via Auto Loader, ensuring high performance and reliability. So, streaming tables specifically support continuous, real-time updates, making them ideal for pipelines that require up-to-the-moment data freshness.




While Materialized Views (formerly known as Live Tables) provide batch-oriented or scheduled incremental processing. Temporary views, in contrast, are ephemeral and not suited for persistent, incremental streaming workloads.




* Databricks has recenlty open-sourced this solution, integrating it into the Apache Spark ecosystem under the name Spark Declarative Pipelines (SDP).

---

# Question 29

## Question
A data engineer has a Delta Lake table “products” with Change Data Feed (CDF) enabled. They want to share this table with external recipients using Delta Sharing, allowing the recipients to:



- 

Use the table_changes() function to consume incremental changes.
- 

Perform time travel queries on the table.




Which of the following commands should the data engineer run to achieve this?

## Options
- A. ALTER SHARE sales_share ADD TABLE products WITH TIME TRAVEL; 
- B. ALTER SHARE sales_share ADD TABLE products WITH (CDF AND TIME TRAVEL); 
- C. ALTER SHARE sales_share ADD TABLE products WITH HISTORY; (Correct)
- D. ALTER SHARE sales_share ADD TABLE products WITH CDF; 

## Explanation
In Databricks Delta Sharing, adding a table with history allows external recipients to both perform time travel queries and access Change Data Feed, if it’s enabled. The WITH HISTORY option automatically exposes the complete table directory, enabling CDF consumption and historical queries.

---

# Question 30

## Question
A data engineer wants to create a Delta Lake table for storing user activities of a website. The table has the following schema:




user_id LONG, page STRING, activity_type LONG, ip_address STRING, activity_time TIMESTAMP, activity_date DATE




Based on the above schema, which column is a good candidate for partitioning the Delta Table?

## Options
- A. user_id 
- B. activity_type 
- C. activity_time 
- D. activity_date (Correct)

## Explanation
When choosing partitioning columns, it's good to consider the fact that records with a given value (the activities of a given user) will continue to arrive indefinitely. In such a case, we use a datetime column for partitioning. This allows your partitions to be optimized, and allows you to easily archive those partitions of previous time periods, if necessary.




Study materials from our exam preparation course on Udemy:

Lecture

Hands-on

---

# Question 31

## Question
A data engineer is analyzing a Spark job via the Spark UI. They have the following summary metrics for 27 completed tasks in a particular stage







Which conclusion can the data engineer draw from the above statistics ?

## Options
- A. Number of tasks are operating over empty or near empty partitions 
- B. All task are operating over partitions with even amounts of data 
- C. All tasks are operating over partitions with larger skewed amounts of data. 
- D. Number of tasks are operating over partitions with larger skewed amounts of data. (Correct)

## Explanation
Usually, if your computation was completely symmetric across tasks, you would see all of the statistics clustered tightly around the 50th percentile value.




Here, the “Max” metrics task took 10x the time and read about 5x the data of the 75th-percentile task. This suggests a number of “straggler” tasks that operating over partitions with larger skewed amounts of data.

---

# Question 32

## Question
A data engineer wants to ingest input json data into a target Delta table. They want the data ingestion to happen incrementally in near real-time.




Which option correctly meets the specified requirement ?

## Options
- A. spark.readStream

           .format("cloudFiles")

           .option ("cloudFiles.format", "json")

           .load(source_path)

.writeStream

           .trigger(availableNow=True)

           .start("target_table") 
- B. spark.readStream

           .format("autoloader")

           .option ("autoloader.format", "json")

           .load(source_path)

.writeStream

           .option("checkpointLocation", checkpointPath)

           .trigger(real-time=True)

           .start("target_table") 
- C. spark.readStream

           .format("autoloader")

           .option ("autoloader.format", "json")

           .load(source_path)

.writeStream

           .option("checkpointLocation", checkpointPath)

           .start("target_table") 
- D. spark.readStream

           .format("cloudFiles")

           .option ("cloudFiles.format", "json")

           .load(source_path)

.writeStream

           .option("checkpointLocation", checkpointPath)

           .start("target_table") (Correct)

## Explanation
In order to ingest input json data into a target Delta table, we use Autoloader. Auto Loader is based on Spark Structured Streaming and provides a Structured Streaming source called ‘cloudFiles’.

If you want the data ingestion to happen incrementally in near real-time, you can use the default trigger method which is trigger(processingTime=”500ms"). This allows the processing of data in micro-batches at a fixed interval of half a second.




Reference:

https://docs.databricks.com/ingestion/auto-loader/index.html

https://docs.databricks.com/structured-streaming/triggers.html#what-is-the-default-trigger-interval




Study materials from our exam preparation course on Udemy:

Lecture (Associate course)

Hands-on (Associate course)

Lecture (Associate course)

---

# Question 33

## Question
A data engineering team is discussing the optimal data layout strategy on a growing managed Delta table in Unity Catalog. They are considering partitioning, Z-ordering, and Liquid Clustering to improve query performance.




Which scenario best indicates that Automatic Liquid Clustering is the recommended choice?

## Options
- A. The table experiences diverse, frequently changing query filters across multiple columns, with unpredictable access patterns. (Correct)
- B. None of the listed options are correct. Automatic Liquid Clustering can not be applied on managed tables. 
- C. The table is heavily filtered by a consistent, small set of date ranges. 
- D. The team has identified stable clustering keys for the table. 

## Explanation
Automatic Liquid Clustering is designed to dynamically adapt to evolving and unpredictable query patterns by continuously reorganizing data based on recent query filters. This is especially beneficial when query predicates frequently change across multiple columns, making static strategies like partitioning or Z-ordering less effective.




Partitioning works best when filters are stable and predictable, often on date/time columns. Z-ordering optimizes clustering for known high-cardinality columns with consistent filtering. When query filters are varied and unpredictable, Automatic Liquid Clustering provides the agility to improve performance without manual tuning.

---

# Question 34

## Question
A data engineering team at a retail company frequently collaborates with business analysts to generate insights from Unity Catalog tables. Over time, the analysts have reported confusion about several columns in key tables because the existing company documentation is outdated. To improve efficiency and reduce misinterpretation, the team lead recommends adding clear descriptions for all table columns. However, manually documenting hundreds of tables and columns would be time-consuming and likely to introduce inconsistencies.




Which of the following approaches allows the team to achieve this task automatically?

## Options
- A. Use Delta Lake generated columns to automatically create column descriptions based on existing data. 
- B. Use the AI-generated column comments feature in Unity Catalog Explorer. (Correct)
- C. Leverage Databricks Assistant to generate column descriptions, and apply them through ALTER TABLE commands. 
- D. Automate column documentation by creating tables through Lakeflow Declarative Pipelines. 

## Explanation
The Unity Catalog Explorer offers an AI-generated column comments feature. This functionality leverages a Large Language Model (LLM) to automatically draft descriptive comments for columns based on their names, data types, sample values, and data patterns.

---

# Question 35

## Question
A healthcare organization stores sensitive patient data within Databricks Unity Catalog. They need to share this data with an external analytics vendor, who does not use Databricks.




What is the most secure and efficient method to enable this data access?

## Options
- A. Using Delta Sharing with the open sharing protocol (Correct)
- B. Storing the data in an external table for direct access 
- C. Downloading the data as protected Excel files and uploading them via SFTP 
- D. Creating a database stored view for external use 

## Explanation
Delta Sharing is designed to securely share data across platforms using an open protocol. Since the vendor does not use Databricks, Delta Sharing ensures secure, real-time access without manual exports or third-party workarounds.

---

# Question 36

## Question
Which of the following statements correctly describes End-to-End Testing?

## Options
- A. It’s an approach to measure the reliability, speed, scalability, and responsiveness of an application 
- B. It’s an approach to verify if each feature of the application works as per the business requirements 
- C. It’s an approach to test the interaction between subsystems of an application to ensure that modules work properly as a group. 
- D. It’s an approach to simulate a user experience to ensure that the application can run properly under real-world scenarios (Correct)

## Explanation
End-to-end testing is an approach to ensure that your application can run properly under real-world scenarios. The goal of this testing is to simulate a real user experience from start to finish.







Study materials from our exam preparation course on Udemy:

Lecture

---

# Question 37

## Question
Which of the following describes the minimal permissions a data engineer needs to edit the configurations of an existing cluster?

## Options
- A. “Can Restart” privilege on the cluster 
- B. Only administrators can edit the configurations on existing clusters 
- C. Cluster creation allowed + “Can Manage” privileges on the cluster 
- D. “Can Manage” privilege on the cluster (Correct)

## Explanation
You can configure two types of cluster permissions:




1- The ‘Allow cluster creation’ entitlement controls your ability to create clusters.




2- Cluster-level permissions control your ability to use and modify a specific cluster. There are four permission levels for a cluster: No Permissions, Can Attach To, Can Restart, and Can Manage. The table lists the abilities for each permission:







Reference:

https://docs.databricks.com/security/auth-authz/access-control/cluster-acl.html




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 38

## Question
A data engineer is configuring the following CDC data processing using AUTO CDC APIs in Lakeflow Declarative Pipelines:



```

- CREATE FLOW cdc_flow AS AUTO CDC INTO silver_transactions
- FROM stream(bronze_transactions)
- KEYS (transaction_id)
- _________________________
- COLUMNS *
```





The engineer wants to define the processing order of source records and handle late-arriving data using a composite key of multiple columns, ordering by transaction_timestamp first, and in case of ties, by version_number.




Which option correctly fills in the blank to meet this requirement?

## Options
- A. SEQUENCE BY STRUCT (transaction_timestamp, version_number) (Correct)
- B. SEQUENCE BY (transaction_timestamp, version_number) 
- C. ORDER BY STRUCT (transaction_timestamp, version_number) 
- D. ORDER BY transaction_timestamp, version_number 

## Explanation
In Lakeflow Declarative Pipelines*, `SEQUENCE BY` is used to define the processing order for CDC streams, and using `STRUCT` allows specifying a composite key of multiple columns. This ensures that records are ordered first by transaction_timestamp and, in case of ties, by version_number, which also allows handling late-arriving data correctly.




* Databricks has recenlty open-sourced this solution, integrating it into the Apache Spark ecosystem under the name Spark Declarative Pipelines (SDP).

---

# Question 39

## Question
Given the following multi-task job







If there is an error in the notebook 2 that is associated with Task 2, which statement describes the run result of this job ?

## Options
- A. Tasks 1 and 3 will succeed, while Task 2 will partially fail (Correct)
- B. Task 1 will succeed. Task 2 will partially fail. Task 3 will be skipped 
- C. Task 1 will succeed. Task 2 will completely fail. Task 3 will be skipped 
- D. Tasks 1 and 3 will succeed, while Task 2 will completely fail 

## Explanation
If a task fails during a job run, only the dependent tasks, if any, will be skipped. Parallel tasks will run and complete.




The failure of a task will always be partial, which means that the operations in the notebook before the code failure will be successfully run and committed, while the operations after the code failure will be skipped.







Reference:

https://docs.databricks.com/workflows/jobs/repair-job-failures.html




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 40

## Question
A data engineering team is building a LDP pipeline to clean and validate hotel reservations data. Some completed reservations have null check-in or check-out dates, which violates business rules.




To handle this, they implemented the following code:



```

- rules = {
-     "valid_check_in": "(check_in IS NOT NULL)",
-     "valid_check_out": "(check_out IS NOT NULL)",
- }
- quarantine_rules = "NOT({0})".format(" AND ".join(rules.values()))
-  
- @dlt.table(partition_cols=["is_quarantined"])
- @dlt.expect_all(rules)
- def silver_reservations():
- return (
-     spark.readStream.table("bronze_reservations")
-                      .withColumn("is_quarantined", expr(quarantine_rules))
- )
```





Which of the following correctly describes what this function does?

## Options
- A. This function streams all rows into the silver_reservations table, flags those with missing check-in or check-out values as quarantined, and partitions the table by the is_quarantined flag. (Correct)
- B. This function partitions the bronze_reservations table by the is_quarantined flag, streams valid partitions into the silver_reservations table, and drops the invalid partitions. 
- C. This function streams only rows with valid check-in and check-out values into the silver_reservations table, while writing invalid rows into a separate partition. 
- D. This function streams rows based on the quarantine_rules into two separate tables: silver_reservations for valid reservations, and is_quarantined for invalid reservations. 

## Explanation
This function streams all rows from the bronze_reservations table into the silver_reservations table, adds a new Boolean column called is_quarantined to flag records with missing check-in or check-out dates, and partitions the table by that flag.




The `dlt.expect_all(rules)` decorator applies data quality expectations but does not drop invalid rows; it simply records the validation results for monitoring purposes. As a result, both valid and invalid records are retained in the same table, making it easy to trace and fix data quality issues without losing information.




This design is a common pattern in Lakeflow Declarative Pipelines for managing data quality. Instead of discarding bad data outright, teams often quarantine it within the same dataset by tagging and partitioning. This allows for continuous ingestion and validation of streaming data while supporting later review or remediation of problematic records, ensuring both data reliability and auditability in production data pipelines.




Note: Databricks has recenlty open-sourced this solution, integrating it into the Apache Spark ecosystem under the name Spark Declarative Pipelines (SDP).

---

# Question 41

## Question
Which statement regarding Delta Lake File Statistics is correct?

## Options
- A. By default, Delta Lake captures statistics in the transaction log on the first 32 columns of each table. (Correct)
- B. By default, Delta Lake captures statistics in the transaction log on the first 16 columns of each table. 
- C. By default, Delta Lake captures statistics in the Hive metastore on the first 32 columns of each table. 
- D. By default, Delta Lake captures statistics in the Hive metastore on the first 16 columns of each table. 

## Explanation
Delta Lake automatically captures statistics in the transaction log for each added data file of the table. By default, Delta Lake collects the statistics on the first 32 columns of each table. These statistics indicate per file:
- 

Total number of records
- 

Minimum value in each column of the first 32 columns of the table
- 

Maximum value in each column of the first 32 columns of the table
- 

Null value counts for in each column of the first 32 columns of the table

These statistics are leveraged for data skipping based on query filters.




Reference: https://docs.databricks.com/delta/data-skipping.html




Study materials from our exam preparation course on Udemy:

Lecture

Hands-on

---

# Question 42

## Question
A finance analytics team manages a Delta Lake table in Unity Catalog called “transactions” with columns: id, amount, region, and account_manager. They want to apply row filtering on this table so that:



- 

Finance team members can see all transactions, while
- 

Other users can only see records from the US region.




Which of the following user-defined functions help achieve this?

## Options
- A. ```

- CREATE FUNCTION us_filter(region STRING)
- RETURN IF(IS_ACCOUNT_GROUP_MEMBER('finance_team'), true, region='US');
``` (Correct)
- B. ```

- CREATE FUNCTION us_filter(region STRING)
- RETURN CASE
- WHEN IS_ACCOUNT_GROUP_MEMBER('finance_team') THEN region='US'
- ELSE true END
``` 
- C. ```

- CREATE FUNCTION us_filter(region STRING)
- RETURN CASE
- WHEN IS_ACCOUNT_GROUP_MEMBER('finance_team') THEN true
- ELSE region END
``` 
- D. ```

- CREATE FUNCTION us_filter(region STRING)
- RETURN IF(IS_ACCOUNT_GROUP_MEMBER('finance_team'), region='US', true);
``` 

## Explanation
The correct user-defined function is:



```

- CREATE FUNCTION us_filter(region STRING)
- RETURN IF(IS_ACCOUNT_GROUP_MEMBER('finance_team'), true, region='US');
```





This function properly enforces the desired row-level security logic. It first checks whether the current user belongs to the finance_team group using `IS_ACCOUNT_GROUP_MEMBER('finance_team')`. If the user is a member, the function returns true, allowing them to see all transaction records without restriction. For all other users who are not part of the finance team, the function evaluates whether the region value equals 'US', thereby restricting their visibility to only U.S. transactions.

---

# Question 43

## Question
Given the following code block in a notebook



```

- db_password = dbutils.secrets.get(scope="dev", key="database_password")
-  
- print (db_password)
```





Which statement describes what will happen when the above code is executed?

## Options
- A. The string value of the password will be printed in plain text. 
- B. The error message “Secrets can not be printed” will be shown 
- C. An interactive input box will appear in the notebook 
- D. The string "REDACTED" will be printed. (Correct)

## Explanation
Databricks Secrets allows you to securely store your credentials and reference them in notebooks and jobs. To prevent accidentally printing a secret to standard output buffers or displaying the value during variable assignment, Databricks redacts secret values that are read using dbutils.secrets.get(). When displayed in notebook cell output, the secret values are replaced with [REDACTED] string.




Reference:

https://docs.databricks.com/security/secrets/redaction.html

https://docs.databricks.com/security/secrets/index.html




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 44

## Question
A data engineer is working on a feature branch in a Git folder and attempts to create a pull request into the main branch of the project repository. However, Git detects conflicting changes between the feature branch and the main branch, resulting in a merge conflict.




Which two options does the Git folder UI provide for resolving merge conflicts?




Choose 2 answers:

## Options
- A. Automatically merge the changes using the magic fix button 
- B. Accept all incoming or current changes (Correct)
- C. Manually edit the changes and remove the conflict markers (Correct)
- D. Delete the conflicting branch 
- E. Move the changes to a new branch 

## Explanation
Merge conflicts happen when two or more Git users attempt to merge changes to the same lines of a file into a common branch and Git cannot choose the “right” changes to apply. Merge conflicts can also occur when a user attempts to pull or merge changes from another branch into a branch with uncommitted changes.








The Git folders UI has two options to resolve merge conflicts:
- 

Accept all incoming or current changes
If you know you only want to accept all of the current or incoming changes, you can select either Keep all current changes or Take all incoming changes. This allows quick resolution without manual editing.





- 

Manually edit the changes and remove the conflict markers
You can resolve the conflict by directly editing the contents of the file with the conflicts. Simply, select the code lines you want to preserve and delete everything else, including the Git merge conflict markers (`<<<<<<<, =======, >>>>>>>`). This manual conflict resolution lets you determine the desired lines from both versions.

---

# Question 45

## Question
A data engineering team is tasked with anonymizing sensitive customer data in their ETL pipeline. They need to generate a SHA-2 hash for a column holding customer credit card numbers. The team is aware that Spark’s sha2 function supports certain bit lengths but not all arbitrary numbers.




Which of the following SHA-2 function calls would fail due to an invalid bit length?

## Options
- A. sha2(credit_card, 256) 
- B. sha2(credit_card, 128) (Correct)
- C. sha2(credit_card, 512) 
- D. sha2(credit_card, 0) 

## Explanation
In Apache Spark, the `sha2(expression, bitLength)` returns a checksum of the SHA-2 family as a hex string of an expression. It only supports specific SHA-2 bit lengths: 224, 256, 384, and 512. Any other bit length, such as 128, is invalid and would cause the function to fail. Notice that bitLength 0 is equivalent to 256.




So, `sha2(credit_card, 128)` would fail due to an unsupported bit length.

---

# Question 46

## Question
Which statement regarding streaming state in Stream-Stream Joins is correct?

## Options
- A. Spark buffers past inputs as a streaming state only for the right input stream, so that it can match future left inputs with past right inputs. 
- B. Spark buffers past inputs as a streaming state for both input streams, so that it can match every future input with past inputs. (Correct)
- C. Stream-Stream Joins are not stateful. Spark does not buffers past inputs as a streaming state for the input streams 
- D. Spark buffers past inputs as a streaming state only for the left input stream, so that it can match future right inputs with past left inputs. 

## Explanation
When performing stream-stream join, Spark buffers past inputs as a streaming state for both input streams, so that it can match every future input with past inputs. This state can be limited by using watermarks.




Reference: 

https://www.databricks.com/blog/2018/03/13/introducing-stream-stream-joins-in-apache-spark-2-3.html




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 47

## Question
A data engineer is configuring a job using Databricks Asset Bundles and wants to limit its access to authorized users. The following job definition includes tasks and job clusters, but the engineer also needs to define which user groups can manage or view the job.



```

- resources:
-     jobs:
-         my-job:
-             name: analytics-job
-             tasks: [...]
-             job_clusters: [...]
-             __________:
-                 - group_name: devops-team
-                 level: CAN_MANAGE
-                 - group_name: qa-team
-                 level: CAN_VIEW
```





Which option correctly fills in the blank to meet the specified requirement?

## Options
- A. roles 
- B. job_settings 
- C. permissions (Correct)
- D. access_control 

## Explanation
The permissions mapping is used to specify the access control lists (ACLs) for the job, defining which users or groups have what level of access (like CAN_MANAGE or CAN_VIEW).

---

# Question 48

## Question
A data engineer wants to use Databricks REST API to retrieve all runs of a job in order to check their statuses.




Which of the following REST API calls achieves this requirement?

## Options
- A. Send POST request to the endpoint ‘/api/2.2/jobs/runs/list’ 
- B. Send GET request to the endpoint ‘api/2.2/jobs/runs/get’ 
- C. Send POST request to the endpoint ‘api/2.2/jobs/runs/get’ 
- D. Send GET request to the endpoint ‘/api/2.2/jobs/runs/list’ (Correct)

## Explanation
Sending GET requests to the endpoint ‘/api/2.2/jobs/runs/list’ allows you to retrieve all runs of a job.

---

# Question 49

## Question
A data engineer is analyzing demographic segments from a Delta table named customers, which stores millions of customer records including personal details such as customer_id, name, birth_date, email, and country. The team wants to create a “senior customer” segment for a marketing campaign targeting customers born on or before January 1, 1970. The engineer writes the following query:



```

- SELECT *
- FROM customers
- WHERE birth_date <= '1970-01-01';
```





However, the table has not been partitioned on the birth_date column and no Z-Order indexing has been applied.




Given this setup, what will most likely happen in terms of query performance?

## Options
- A. The query will perform a full table scan, reading all data files from storage. (Correct)
- B. The query will only read table metadata since it contains all column statistics. 
- C. The query will skip most files since dynamic file pruning is enabled by default. 
- D. The query will leverage data skipping since the filter column is among the first 32 columns. 

## Explanation
For a large, un-optimized table without partitioning or Z-Ordering on the filter column, the data related to different birth dates is likely scattered across many files, forcing the engine to read all, or almost all, table files.

---

# Question 50

## Question
Which of the following is the benefit of Delta Lake File Statistics?

## Options
- A. They are used as checksums to check data corruption in parquet files. 
- B. They are leveraged for data skipping when executing selective queries. (Correct)
- C. They are leveraged for process time forecasting when executing selective queries. 
- D. They are leveraged for data compression in order to improve Delta Caching. 

## Explanation
Delta Lake File Statistics indicate per file:
- 

Total number of records
- 

Minimum value in each column of the first 32 columns of the table
- 

Maximum value in each column of the first 32 columns of the table
- 

Null value counts for in each column of the first 32 columns of the table




These statistics are leveraged for data skipping based on query filters. For example, if you are querying the total number of records in a table, Delta will not calculate the count by scanning all data files. Instead, it will leverage these statistics to generate the query result







Reference:

https://docs.databricks.com/delta/data-skipping.html




Study materials from our exam preparation course on Udemy:

Lecture

Hands-on

---

# Question 51

## Question
A data engineer has been tasked with creating a Unity Catalog table containing customer information, including email addresses and phone numbers, across multiple regions. The organization wants to ensure that users can query the table, but personally identifiable information (PII) is not exposed to those without proper access.




Which method should the engineer use to efficiently enforce this requirement?

## Options
- A. Apply column masks to configure fine-grained access control (Correct)
- B. Use table object privileges to revoke access on sensitive PII columns 
- C. Use a dynamic view to redacting sensitive PII columns 
- D. Use row-level filters to restrict access to region-specific customers 

## Explanation
Column masks in Unity Catalog are security features that dynamically control the visibility of sensitive data in specific columns based on the identity or role of the user executing a query. Implemented as SQL user-defined functions (UDFs), column masks replace or transform the original column values at query runtime, ensuring that unauthorized users see redacted or anonymized data.




For example, a masking function might display full Social Security Numbers (SSNs) only to users in the Human Resources department, while showing masked values like ***-**-**** to others. These masks are applied declaratively using the MASK clause:



```

- CREATE FUNCTION mask_ssn(ssn STRING)
- RETURN CASE WHEN is_member('hr_team')
- THEN ssn ELSE '***-**-****' END;
-  
- CREATE TABLE persons(name STRING, ssn STRING MASK mask_ssn);
```





Why other options are incorrect:



- 

Use a dynamic view to mask sensitive PII columns

While dynamic views can be used for masking, column-level masking in Unity Catalog is more efficient and built-in for this purpose. Dynamic views require creating and maintaining additional views manually.



- 

Use table object privileges to revoke access on sensitive PII columns

table object privileges control access to entire tables, not specific columns. This would prevent access entirely rather than selectively hiding PII.



- 

Use row-level filters to restrict access to region-specific customers

Row-level filtering controls which rows a user sees, but it does not protect specific columns (like emails or phone numbers) from unauthorized users.

---

# Question 52

## Question
A data engineer at a retail company is tasked with analyzing daily sales trends across hundreds of stores. The raw PySpark DataFrame contains columns store_id, date, and sales_amount. The engineer wants to calculate a 7-day rolling average of sales per store, leveraging Pandas for its convenient rolling window operations. To achieve this task, the engineer created a custom Python function called “calculate_sales” where the input and output of the function are both pandas.DataFrame.




Which of the following allows applying this function to each group of store_id while preserving Spark efficiency?

## Options
- A. pandas_udf(calculate_sales, returnType=Series) 
- B. df.groupBy("store_id").applyInPandas(calculate_sales, schema) (Correct)
- C. df.selectExpr("calculate_sales(store_id)") 
- D. df.mapInPandas("store_id", calculate_sales, schema) 

## Explanation
The `applyInPandas` function, used after a `groupBy` operation, is designed exactly for this scenario: applying a Python function that takes and returns a Pandas DataFrame to each group of data within a Spark DataFrame, while preserving state variables that are local to each group's processing logic.

---

# Question 53

## Question
Which of the following is Not a valid task type in Databricks Jobs?

## Options
- A. SQL query 
- B. If/else condition 
- C. Python wheel 
- D. REST API call (Correct)

## Explanation
In Databricks Jobs, valid task types include:



- 

Python wheel: for running a Python wheel package.
- 

SQL query: for executing an SQL command or query.
- 

If/else condition: for adding a boolean conditional logic within a job workflow.


However, REST API call is not a task type in Databricks Jobs.

---

# Question 54

## Question
Given the following query on the Delta table ‘customers’ on which Change Data Feed is enabled:



```

- spark.readStream
-         .option("readChangeFeed", "true")
-         .option("startingVersion", 0)
-         .table("customers")
-         .filter(col("_change_type").isin(["update_postimage"]))
-     .writeStream
-         .option("checkpointLocation", "dbfs:/checkpoints")
-         .trigger (availableNow=True)
-         .table("customers_updates")
```





Which statement describes the results of this query each time it is executed ?

## Options
- A. Newly updated records will overwrite the target table. 
- B. The entire history of updated records will be appended to the target table at each execution, which leads to duplicate entries. 
- C. Newly updated records will be appended to the target table. (Correct)
- D. The entire history of updated records will overwrite the target table at each execution. 

## Explanation
The query uses `spark.readStream` to read the table's changes captured by CDF as a streaming source. This leverages checkpointing to track the progress of the stream processing and continue the stream from where it left off in the last execution.




The query then appends the data to the target table at each execution since it’s using the default writing mode, which is ‘append’.




Study materials from our exam preparation course on Udemy:

Lecture

Hands-on

---

# Question 55

## Question
A data analytics firm uses Delta Sharing to collaborate with a partner company. The provider stores the data in AWS US-East-1, while the partner is hosted on Azure in Europe. After initiating large-scale data sharing, the firm notices unexpected costs in their billing dashboard.




What is the most likely reason for the unexpected cost increase?

## Options
- A. DBU costs for running Delta Sharing servers across cloud boundaries 
- B. Storage costs because Delta Sharing requires replication of data across clouds and regions 
- C. Egress fees are incurred when data transferred between cloud providers and regions (Correct)
- D. Flat rate fee is applied for all shared data by Delta Sharing protocol 

## Explanation
When data is transferred out of your cloud infrastructure to another cloud platform or to another geographic region, your cloud provider applies "data egress fees". These fees can be significant depending on the volume of data transferred. Delta Sharing itself does not add substantial cost, but the underlying cloud provider’s data transfer pricing—especially egress charges—is the primary contributor to cost increases in such scenarios.




In this scenario, AWS applies egress fees because data is transferred out of AWS to a different cloud provider (Azure) and to another geographic region (Europe).

---

# Question 56

## Question
Which of the following approaches allows to correctly perform streaming deduplication?

## Options
- A. De-duplicate records in all batches with watermarking, and then overwrite the target table by the result 
- B. De-duplicate records within each batch, rank the result, and then insert only records having rank = 1 into the target table 
- C. De-duplicate records within each batch, and then merge the result into the target table using insert-only merge (Correct)
- D. De-duplicate records within each batch, and then append the result into the target table 

## Explanation
To perform streaming deduplication, we use dropDuplicates() function to eliminate duplicate records within each new micro batch. In addition, we need to ensure that records to be inserted are not already in the target table. We can achieve this using insert-only merge.

Reference:

https://spark.apache.org/docs/3.1.2/api/python/reference/api/pyspark.sql.DataFrame.dropDuplicates.html

https://docs.databricks.com/delta/merge.html#data-deduplication-when-writing-into-delta-tables




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 57

## Question
Given the following two versions of a Delta Lake table before and after an update:




Before:




After:




Which SCD Type is this table ?

## Options
- A. It's a combination of Type 0 and Type 2 SCDs 
- B. SCD Type 1 (Correct)
- C. SCD Type 0 
- D. SCD Type 2 

## Explanation
In a Type 1 SCD table the new data overwrites the existing one. Thus, the existing data is lost as it is not stored anywhere else.







Reference:

https://en.wikipedia.org/wiki/Slowly_changing_dimension




Study materials from our exam preparation course on Udemy:

Lecture




For example, our customers_silver table is created as Type 1 SCD. It contains only the latest valid information of each customer

Hands-on

---

# Question 58

## Question
The data engineering team has the following query for processing customers’ requests to be forgotten:



```

- DELETE FROM customers
- WHERE customer_id IN
- (SELECT customer_id FROM delete_requests)
```





Which statement describes the results of executing this query ?

## Options
- A. The identified will be deleted from the both customers and delete_requests tables, and their associated data files will be permanently purged from the tables directories. 
- B. The identified records will be deleted from both customers and delete_requests tables, but they will still be accessible in the table history until VACUUM commands are run. 
- C. The identified records will be deleted from the customers table, but they will still be accessible in the table history until a VACUUM command is run. (Correct)
- D. The identified records will be deleted from the customers tables, and their associated data files will be permanently purged from the table directory. 

## Explanation
Delete requests, also known as requests to be forgotten, require deleting user data that represent Personally Identifiable Information or PII, such as the name and the email of the user.




Because of how Delta Lake tables time travel are implemented, deleted values are still present in older versions of the data. Remember, deleting data does not delete the data files from the table directory. Instead, it creates a copy of the affected files without these deleted records. So, to fully commit these deletes, you need to run VACUUM commands on the customers table.







Reference:

https://www.databricks.com/blog/2022/03/23/implementing-the-gdpr-right-to-be-forgotten-in-delta-lake.html




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 59

## Question
Which of the following statements is Not true about the Query Profile in Databricks SQL?

## Options
- A. The Query Profile allows users to directly edit and re-run specific parts of the query plan to interactively fix issues in the query. (Correct)
- B. The Query Profile helps discover common SQL performance issues, such as exploding joins or full table scans. 
- C. The Query Profile visualizes each query operator and related metrics, such as execution time, memory usage, and number of rows processed. 
- D. The Query Profile helps identify the slowest part of a query execution and assess the impact of query modifications. 

## Explanation
Databricks’ Query Profile is a diagnostic and visualization tool that shows query operators, execution metrics, and performance bottlenecks, helping users understand and optimize queries, but it does not allow direct editing or execution of parts of the query plan.

---

