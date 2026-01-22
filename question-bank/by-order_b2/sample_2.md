# Question 1

## Question
A data engineer is tasked with ingesting x-ray image files of type JPEG into a Delta table using Auto Loader.




Which of the following code snippets can the data engineer use to achieve this task?

## Options
- A. ```

- df = spark.readStream.format("cloudFiles") \
-           .option("cloudFiles.format", "jpg") \
-           .load(“/source/x-ray”)
``` 
- B. ```

- df = spark.readStream.format("cloudFiles") \
-           .option("cloudFiles.format", "binaryFile") \
-           .option("pathGlobfilter", "*.jpg") \
-           .load(“/source/x-ray”)
``` (Correct)
- C. ```

- df = spark.readStream.format("cloudFiles") \
-           .option("cloudFiles.format", "binaryFile") \
-           .load(“/source/x-ray/*.jpg”)
``` 
- D. ```

- df = spark.readStream.format("cloudFiles") \
-           .option("cloudFiles.format", "image") \
-           .option("pathGlobfilter", "*.jpg") \
-           .load(“/source/x-ray”)
``` 

## Explanation
When ingesting image files using Auto Loader, you should use "binaryFile" as the cloudFiles.format because images are binary data. The pathGlobFilter option allows you to filter input files based on a glob pattern, such as *.jpg.

---

# Question 2

## Question
A data engineer has the following streaming query with a blank:



```

- spark.readStream
-        .table("orders_cleaned")
-        .groupBy(
-            ___________________________,
-            "author")
-        .agg(
-            count("order_id").alias("orders_count"),
-            avg("quantity").alias("avg_quantity"))
-     .writeStream
-        .option("checkpointLocation", "dbfs:/path/checkpoint")
-        .table("orders_stats")
```





They want to calculate the orders count and average quantity for each non-overlapping 15-minute interval.




Which option correctly fills in the blank to meet this requirement ?

## Options
- A. window("order_timestamp", "15 minutes") (Correct)
- B. trigger(processingTime=”15 minutes") 
- C. withWatermark("order_timestamp", "15 minutes") 
- D. withWindow("order_timestamp", "15 minutes") 

## Explanation
Pyspark.sql.functions.window function bucketizes rows into one or more time windows given a timestamp specifying column.




Reference:

https://spark.apache.org/docs/3.1.3/api/python/reference/api/pyspark.sql.functions.window.html




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 3

## Question
Given the following Structured Streaming query:



```

- (spark.readStream
-         .table("orders")
-     .writeStream
-         .option("checkpointLocation", checkpointPath)
-         .table("Output_Table")
- )
```





Which of the following is the trigger Interval for this query ?

## Options
- A. Every half second (Correct)
- B. Every half min 
- C. Every half hour 
- D. The query will run in batch mode to process all available data at once, then the trigger stops. 

## Explanation
By default, if you don’t provide any trigger interval, the data will be processed every half second. This is equivalent to trigger(processingTime=”500ms")




Reference: https://docs.databricks.com/structured-streaming/triggers.html#what-is-the-default-trigger-interval




Study materials from our exam preparation course on Udemy:
- 

Lecture (Associate course)
- 

Hands-on (Associate course)

---

# Question 4

## Question
The data engineering team has a Delta table named ‘users’. A recent CHECK constraint has been added to the table using the following command:



```

- ALTER TABLE users
- ADD CONSTRAINT valid_age CHECK (age> 0);
```





The team attempted to insert a batch of new records to the table, but there were some records with negative age values which caused the write to fail because of the constraint violation.




Which statement describes the outcome of this batch insert?

## Options
- A. None of the records have been inserted into the table. (Correct)
- B. All records except those that violate the table constraint have been inserted in the table. Records violating the constraint have been ignored. 
- C. Only records processed before reaching the first violating record have been inserted in the table 
- D. All records except those that violate the table constraint have been inserted in the table. Records violating the constraint have been recorded into the transaction log. 

## Explanation
Write operations failed because of the constraint violation. However, ACID guarantees on Delta Lake ensure that all transactions are atomic. That is, they will either succeed or fail completely. So in this case, none of these records have been inserted into the table, even the ones that don't violate the constraints.







Reference:

https://www.databricks.com/glossary/acid-transactions




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 5

## Question
A scheduled job failed due to an upstream data source issue. After resolving the issue, the data engineer wants to use the Jobs API to trigger the same job again without waiting for its next scheduled run.




Which of the following REST API calls achieves this requirement?

## Options
- A. Send GET request to the endpoint ‘/api/2.2/jobs/run’ 
- B. Send POST request to the endpoint ‘/api/2.2/jobs/run-now’ (Correct)
- C. Send POST request to the endpoint ‘/api/2.2/jobs/start’ 
- D. Send POST request to the endpoint ‘/api/2.2/jobs/run’ 

## Explanation
Sending POST requests to the endpoint ‘/api/2.2/jobs/run-now’ allows you to trigger a job run using the job_id.

---

# Question 6

## Question
A data engineering team is building a LDP pipeline to clean and validate product data streaming in from various sources. They notice that some records in the bronze_products table contain invalid price values, specifically some prices are zero or negative, which violates business rules.




To handle this issue, they implemented the following LDP code:



```

- @dlt.table
- @dlt.expect_or_drop("positive_price", "price > 0")
- def silver_products():
-     return spark.readStream.table("bronze_products")
-  
- @dlt.table
- @dlt.expect_or_drop("invalid_price", "price <= 0")
- def quarantine_products():
-     return spark.readStream.table("bronze_products")
```





Which of the following correctly describes the result of running this pipeline?

## Options
- A. Records with positive prices are loaded into the silver_products table, while records with zero or negative prices are loaded into the quarantine_products table. (Correct)
- B. All records are loaded into the silver_products table, with a flag “quarantine_products” indicating whether the price is valid or not. 
- C. Records with positive prices are loaded into the silver_products table, while records with zero or negative prices are deleted from the bronze_products table. 
- D. All records are updated in the bronze_products table with a flag “quarantine_products” that indicates whether the price is valid or not. 

## Explanation
This LDP* pipeline uses a common pattern for quarantining records by creating a second table that stores the invalid records.




The silver_products table uses `@dlt.expect_or_drop("positive_price", "price > 0")`, which means that only records meeting the condition price > 0 are kept, while any records with zero or negative prices are dropped. As a result, the silver_products table contains only valid product records where prices are positive, ensuring that downstream processes receive clean and business-rule-compliant data.




On the other hand, the quarantine_products table is defined with `@dlt.expect_or_drop("invalid_price", "price <= 0")`, meaning only records with zero or negative prices satisfy this expectation and are retained. This effectively routes all invalid price records into the quarantine table for further inspection or correction.




The original bronze_products table remains unchanged, and no records are deleted from it.




* Databricks has recenlty open-sourced this solution, integrating it into the Apache Spark ecosystem under the name Spark Declarative Pipelines (SDP).

---

# Question 7

## Question
The data engineering team maintains a Delta Lake table of SCD Type 1. A junior data engineer noticed a folder named ‘_change_data’ in the table directory, and wants to understand what this folder is used for.




Which of the following describes the purpose of this folder ?

## Options
- A. CDF feature is enabled on the table. The ‘_change_data’ folder is the location where CDF data is stored (Correct)
- B. The ‘_change_data’ folder is the default directory to track the evolution in schema definition 
- C. Optimized Writes feature is enabled on the table. The ‘_change_data’ folder is the location where the optimized data is stored 
- D. All SCD Type 1 tables have the ‘_change_data’ folder to track the updates applied on the table’s data. 

## Explanation
Databricks records change data for UPDATE, DELETE, and MERGE operations in the _change_data folder under the table directory.




The files in the _change_data folder follow the retention policy of the table. Therefore, if you run the VACUUM command, change data feed data is also deleted.







Reference:

https://docs.databricks.com/delta/delta-change-data-feed.html#change-data-storage




Study materials from our exam preparation course on Udemy:

Lecture

Hands-on

---

# Question 8

## Question
A data engineer wants to store passwords securely in a Unity Catalog managed table. They need to hash user passwords using `SHA2(password, 256)` before storing them. To ensure proper storage, the engineer must also set a constraint on the column length to accommodate the full hash value.




The engineer tests hashing the passwords "spark123" and "ApacheSpark111".




What will the engineer notice about the resulting hash lengths?

## Options
- A. Both hashes will have the same length, regardless of input size (Correct)
- B. Both hashes will have the same length because hash length depends on the number of numeric characters 
- C. The hash of "spark123" will be shorter than the hash of "ApacheSpark111" 
- D. The hash of "ApacheSpark111" will be shorter than the hash of "spark123" 

## Explanation
The reason both hashes have the same length comes from how cryptographic hash functions are designed. SHA-256 always produces a 256-bit output, no matter how long or short the input is. This is a fundamental property of cryptographic hash functions—they map inputs of arbitrary size to a fixed-length output.




Whether you hash "spark123" (8 characters) or "ApacheSpark111" (14 characters), SHA-256 will still generate 256 bits, typically represented as 64 hexadecimal characters. When represented as a hexadecimal string (which is standard for storing hashes), a 256-bit hash is always 64 characters long.




`SELECT sha2('spark123', 256);`

92f55da1cdca0fd9811daa0bc97455c9e9e2b16d29e4e142c56e5924a1446175




`SELECT sha2('ApacheSpark111', 256);`

5385cb3eb8907791fe9efad61f847bb9af6145a6db5689f7687bf7f1c3e25086




As you can see, both the hash of "spark123" and the hash of "ApacheSpark111" have the same length, which is 64 hexadecimal characters. So, for the data engineer in this question, the column constraint should be set to accommodate 64-character.

---

# Question 9

## Question
Which of the following describes Cron syntax in Databricks Jobs?

## Options
- A. It’s an expression to represent the retry policy of a job 
- B. It’s an expression to represent the run timeout of a job 
- C. It’s an expression to represent the maximum concurrent runs of a job 
- D. It’s an expression to represent complex job schedule that can be defined programmatically (Correct)

## Explanation
To define a schedule for a Databricks job, you can either interactively specify the period and starting time, or write a Cron Syntax expression. The Cron Syntax allows to represent complex job schedule that can be defined programmatically.









Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 10

## Question
Which of the following statements best describes deletion vectors in Delta Lake?

## Options
- A. Temporary files that store deleted rows until they are archived in a separate table partition called “_deletion_log”. 
- B. Metadata structures that track which rows in a data file have been logically deleted without physically rewriting the file. (Correct)
- C. Indexes that accelerate queries on deleted rows by storing their physical locations directly in Unity Catalog volumes. 
- D. Data structures that permanently remove deleted rows from all data files in a Delta Lake table. 

## Explanation
In Delta Lake, deletion vectors are a performance optimization feature introduced to handle row-level deletes and updates efficiently.
- 

Instead of rewriting entire Parquet files when some rows are deleted or updated, deletion vectors keep track of which rows in a data file are logically deleted.
- 

This tracking is done through metadata structures stored separately from the data files.
- 

Queries automatically skip these deleted rows, even though the original Parquet files remain unchanged.


This significantly improves performance for frequent DELETE, UPDATE, and MERGE operations.

---

# Question 11

## Question
A data engineer at a retail company shared a large Delta table with an external analytics company using Delta Sharing without history. However, the company noticed slow performance when querying the shared data.




A senior data engineer suggested using the following command to share the data with history in order to improve query performance:

`ALTER SHARE sales_share ADD TABLE products WITH HISTORY;`




Which benefit is achieved by using WITH HISTORY?

## Options
- A. It leverages temporary security credentials from the cloud storage, scoped-down to the root directory of the provider's shared Delta table. (Correct)
- B. It replicates the table to balance query requests through the Delta Sharing server. 
- C. It performs a shallow clone of the table to share only the table’s transaction log. 
- D. It leverages disk caching of the Delta Sharing server, resulting in performance that is comparable to direct access to source tables. 

## Explanation
Databricks-to-Databricks table shares can improve performance by enabling history sharing using the WITH HISTORY clause. Sharing history improves performance by leveraging temporary security credentials from your cloud storage, scoped-down to the root directory of the provider's shared Delta table, resulting in performance that is comparable to direct access to source tables.

---

# Question 12

## Question
A data engineer has defined the following data quality constraint in a LDP pipeline:




`CONSTRAINT valid_id EXPECT (id IS NOT NULL) _____________`




Which clause correctly fills in the blank so records violating this constraint will be written to the target table, but reported in metrics?

## Options
- A. ON VIOLATION WARNING 
- B. There is no need to add the ON VIOLATION clause. By default, records violating the constraint will be kept, and reported as invalid in the pipeline metrics. (Correct)
- C. ON VIOLATION NULL 
- D. ON VIOLATION ADD ROW 

## Explanation
By default, records that violate the constraint will still be written to the target table and reported as invalid in the pipeline metrics. Therefore, the constraint can simply be defined as `CONSTRAINT valid_id EXPECT (id IS NOT NULL)` without any `ON VIOLATION` clause.




Note: Databricks has recenlty open-sourced this solution, integrating it into the Apache Spark ecosystem under the name Spark Declarative Pipelines (SDP).




Study materials from our exam preparation course on Udemy:
- 

Hands-on

---

# Question 13

## Question
For production Structured Streaming jobs, which of the following retry policies is recommended to use?

## Options
- A. Unlimited Retries, with 1 Maximum Concurrent Run (Correct)
- B. Unlimited Retries, with Unlimited Concurrent Runs 
- C. No Retries, with 1 Maximum Concurrent Run 
- D. No Retries, with Unlimited Concurrent Runs 

## Explanation
In order to restart streaming queries on failure, it’s recommended to configure Structured Streaming jobs with the following job configuration:



- 

Retries: Set to Unlimited.
- 

Maximum concurrent runs: Set to 1. There must be only one instance of each query concurrently active.
- 

Cluster: Set this always to use a new job cluster and use the latest Spark version (or at least version 2.1). Queries started in Spark 2.1 and above are recoverable after query and Spark version upgrades.
- 

Notifications: Set this if you want email notification on failures.
- 

Schedule: Do not set a schedule.
- 

Timeout: Do not set a timeout. Streaming queries run for an indefinitely long time.







Reference:

https://docs.databricks.com/structured-streaming/query-recovery.html#configure-structured-streaming-jobs-to-restart-streaming-queries-on-failure







Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 14

## Question
Given the following two versions of a Delta Lake table before and after an update:




Before:



After:




Which SCD Type is this table ?

## Options
- A. SCD Type 2 (Correct)
- B. It's a combination of Type 0 and Type 2 SCDs 
- C. SCD Type 0 
- D. SCD Type 1 

## Explanation
In a Type 2 SCD table, a new record is added with the changed data values, and this new record becomes the current active record, while the old record is marked as no longer active. So, Type 2 SCD retains the full history of values







Reference:

https://en.wikipedia.org/wiki/Slowly_changing_dimension




Study materials from our exam preparation course on Udemy:

Lecture

Hands-on

---

# Question 15

## Question
A data engineering team is working on a user activity events table stored in Unity Catalog. Queries often involve filters on multiple columns like user_id and event_date.




Which data layout technique should the team implement to avoid expensive table scans?

## Options
- A. Use partitioning on the event_date column. 
- B. Use Z-order indexing on the user_id 
- C. Use liquid clustering on the combination of user_id and event_date (Correct)
- D. Use partitioning on the user_id column, along with Z-order indexing on the event_date column. 

## Explanation
In this scenario, using liquid clustering on the combination of user_id and event_date is the best choice to avoid expensive scans. This technique incrementally optimizes data layout based on both columns, efficiently supporting filters on these columns and avoiding costly table scans.




Partitioning only on event_date helps queries filtering by date but doesn’t optimize filtering by user_id, leading to potential full scans within partitions. Z-order indexing on user_id optimizes queries filtering on user_id but ignores event_date filtering, resulting in inefficient scans when filtering by date. Lastly, partitioning on user_id + Z-order on event_date supports filtering on both columns but can create many small partitions (if users are numerous), causing management and performance issues.

---

# Question 16

## Question
A data engineering team is managing a Delta Lake table called orders. They want to ensure that they can access the table’s historical data using time travel for the same duration as Delta Lake’s default transaction log retention.




Which of the following commands meet this requirement?

## Options
- A. ALTER TABLE orders SET TBLPROPERTIES ('delta.deletedFileRetentionDuration’ = 'interval 90 days") 
- B. ALTER TABLE orders SET TBLPROPERTIES ('delta.deletedFileRetentionDuration’ = 'interval 30 days") (Correct)
- C. ALTER TABLE orders SET TBLPROPERTIES ('delta.deletedFileRetentionDuration’ = 'interval 7 days") 
- D. ALTER TABLE orders SET TBLPROPERTIES ('delta.deletedFileRetentionDuration’ = 'interval 365 days") 

## Explanation
Delta Lake’s default transaction log retention period is 30 days, which determines how long historical data is kept available for time travel before being permanently deleted. To match this retention period for the deleted data files, we need to alter the table to set the table property 'delta.deletedFileRetentionDuration', as follows:




`ALTER TABLE orders SET TBLPROPERTIES ('delta.deletedFileRetentionDuration’ = 'interval 30 days")`

---

# Question 17

## Question
Which of the following statements regarding the retention policy of Delta lake CDF is correct?

## Options
- A. Running the VACUUM command on the table does not deletes CDF data 
- B. Running the VACUUM command on the table does not deletes CDF data unless CASCADE clause is set to true 
- C. Running the VACUUM command on the table deletes CDF data as well (Correct)
- D. CDF data files can be purged by running VACUUM CHANGES command 

## Explanation
Databricks records change data for UPDATE, DELETE, and MERGE operations in the _change_data folder under the table directory.




The files in the _change_data folder follow the retention policy of the table. Therefore, if you run the VACUUM command, change data feed data is also deleted.







Reference:

https://docs.databricks.com/delta/delta-change-data-feed.html#change-data-storage




Study materials from our exam preparation course on Udemy:

Lecture

Hands-on

---

# Question 18

## Question
A junior data engineer has created the table ‘orders_backup’ as a copy of the table “orders”. Recently, the team started getting an error when querying the orders_backup indicating that some data files are no longer present. The transaction logs for the orders tables show a recent run of VACUUM command.




Which of the following explains how the data engineer created the orders_backup table ?

## Options
- A. The orders_backup table was created using Delta Lake’s SHALLOW CLONE functionality from the orders table (Correct)
- B. The orders_backup table was created using CTAS statement from orders table 
- C. The orders_backup table was created using CRAS statement from orders table 
- D. The orders_backup table was created using Delta Lake’s DEEP CLONE functionality from the orders table 

## Explanation
With Shallow Clone, you create a copy of a table by just copying the Delta transaction logs.

That means that there is no data moving during Shallow Cloning.

Running the VACUUM command on the source table may purge data files referenced in the transaction log of the clone. In this case, you will get an error when querying the clone indicating that some data files are no longer present.







Reference:

https://docs.databricks.com/delta/clone.html




Study materials from our exam preparation course on Udemy:

Lecture (Associate course)

---

# Question 19

## Question
The data engineering team has a Delta Lake table created with following query:



```

- CREATE TABLE customers_clone
- AS SELECT * FROM customers
```





A data engineer wants to drop the table with the following query:




`DROP TABLE customers_clone`




Which statement describes the result of running this drop command ?

## Options
- A. The table will not be dropped until VACUUM command is run 
- B. Both the table's metadata and the data files will be deleted (Correct)
- C. An error will occur as the table is deep cloned from the customers table 
- D. Only the table's metadata will be deleted from the catalog, while the data files will be kept in the storage 

## Explanation
The table is created without the LOCATION clause, which means that it’s a managed table. Managed tables are tables whose metadata and data are managed by Databricks.

When you run DROP TABLE on a managed table, both the metadata and the underlying data files are deleted.




Reference:

https://docs.databricks.com/lakehouse/data-objects.html#what-is-a-managed-table




Study materials from our exam preparation course on Udemy:
- 

Lecture (Associate course)
- 

Hands-on (Associate course)

---

# Question 20

## Question
A data engineer is using a foreachBatch logic to upsert data in a target Delta table.




The function to be called at each new microbatch processing is displayed below with a blank:



```

- def upsert_data(microBatchDF, batch_id):
-     microBatchDF.createOrReplaceTempView("sales_microbatch")
-     
-     sql_query = """
-       MERGE INTO sales_silver a
-       USING sales_microbatch b
-       ON a.item_id=b.item_id AND a.item_timestamp=b.item_timestamp
-       WHEN NOT MATCHED THEN INSERT *
-     """    
-    
-     ________________
```





Which option correctly fills in the blank to execute the sql query in the function on a cluster with recent Databricks Runtime above 10.5 ?

## Options
- A. microBatchDF._jdf.sparkSession().sql(sql_query) 
- B. microBatchDF.sparkSession.sql(sql_query) (Correct)
- C. microBatchDF.sql(sql_query) 
- D. spark.sql(sql_query) 

## Explanation
Usually, we use spark.sq() function to run SQL queries. However, in this particular case, the spark session can not be accessed from within the microbatch process. Instead, we can access the local spark session from the microbatch dataframe.




For clusters with recent Databricks Runtime version above 10.5, the syntax to access the local spark session is:

microBatchDF.sparkSession.sql(sql_query)







Reference: https://docs.gcp.databricks.com/structured-streaming/delta-lake.html#language-python




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 21

## Question
A data engineer uses the dynamic reference `{{job.start_time.iso_datetime}}` to configure the value of a task parameter in a job.




Which of the following statements correctly describes the timezone of the returned timestamp?

## Options
- A. The timestamp is based on the workspace cloud region’s local time. 
- B. The timestamp is based on the cluster virtual machine’s local time. 
- C. The timestamp is in UTC. (Correct)
- D. The timestamp is based on the user’s local time who triggered the job. 

## Explanation
In Databricks jobs, all time-based references are based on a timestamp in the UTC timezone, including: `is_weekday`, `iso_weekday`, `iso_datetime`, and `iso_date`.




This ensures consistency across regions, clusters, and users regardless of their local time zones.

---

# Question 22

## Question
A data engineer wants to optimize the following join operation by allowing the smaller dataFrame to be sent to all executor nodes in the cluster:



```

- largeDF.join(smallerDF, [“key”], "inner")
```





Which of the following functions can be used to mark a dataFrame as small enough to fit in memory on all executors ?

## Options
- A. pyspark.sql.functions.distribute 
- B. pyspark.sql.functions.broadcast (Correct)
- C. pyspark.sql.functions.explode 
- D. pyspark.sql.functions.shuffle 

## Explanation
`pyspark.sql.functions.broadcast` function marks a DataFrame as small enough for use in broadcast joins.




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 23

## Question
A data engineer repaired a failed multi-task job run in Databricks. Before clicking Repair run, they changed a task parameter value in the Repair run dialog.




Which of the following best describes the effect of this change?

## Options
- A. The updated parameter applies only to the current repair run and does not modify the job’s stored parameters. (Correct)
- B. The updated parameter value is permanently saved to the job configuration. 
- C. The repair run will fail because this feature only supports adding new parameters, not updating existing ones. 
- D. The change is ignored because the job parameters always override the run’s parameters. 

## Explanation
In Databricks, when you use the “Repair run” for a failed job, the dialog allows you to tweak parameters for that specific run. These changes do not overwrite the job’s original configuration. They only apply to this repair run.








To make the parameter change permanent, you need to update the job’s configuration itself.

---

# Question 24

## Question
Which of the following describes the minimal permissions a data engineer needs to start an existing cluster, and attach a notebook to it?

## Options
- A. “Can Attach To” privilege on the cluster 
- B. Cluster creation allowed + “Can Restart” privileges on the cluster 
- C. “Can Manage” privilege on the cluster 
- D. “Can Restart” privilege on the cluster (Correct)

## Explanation
You can configure two types of cluster permissions:




1- The ‘Allow cluster creation’ entitlement controls your ability to create clusters.




2- Cluster-level permissions control your ability to use and modify a specific cluster. There are four permission levels for a cluster: No Permissions, Can Attach To, Can Restart, and Can Manage. The table lists the abilities for each permission:










Reference:

https://docs.databricks.com/security/auth-authz/access-control/cluster-acl.html




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 25

## Question
A data engineer wants to use Autoloader to ingest input data into a target table, and automatically evolve the schema of the table when new fields are detected.




They use the below query with a blank:



```

- spark.readStream
-         .format("cloudFiles")
-         .option("cloudFiles.format", "json")
-         .option("cloudFiles.schemaLocation", checkpointPath)
-         .load(source_path)
-     .writeStream
-         .option("checkpointLocation", checkpointPath)
-         .___________
-         .start("target_table")
```





Which option correctly fills in the blank to meet the specified requirement ?

## Options
- A. option("mergeSchema", True) (Correct)
- B. option("cloudFiles.mergeSchema", True) 
- C. option("cloudFiles.schemaEvolutionMode", "addNewColumns") 
- D. schema(schema_definition, mergeSchema=True) 

## Explanation
Schema evolution is a feature that allows adding new detected fields to the table. It’s activated by adding .option('mergeSchema', 'true') to your .write or .writeStream Spark command.




Reference:

https://docs.databricks.com/delta/update-schema.html#add-columns-with-automatic-schema-update




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 26

## Question
A junior data engineer is using the following code to de-duplicate raw streaming data and insert them in a target Delta table



```

- spark.readStream
-         .table("orders_raw")
-         .dropDuplicates(["order_id", "order_timestamp"])
-     .writeStream
-         .option("checkpointLocation", "dbfs:/checkpoints")
-         .table("orders_unique")
```





A senior data engineer pointed out that this approach is not enough for having distinct records in the target table when there are late-arriving, duplicate records.




Which of the following could explain the senior data engineer’s remark?

## Options
- A. A window function is also needed to apply deduplication for each non-overlapping interval. 
- B. A ranking function is also needed to ensure processing only the most recent records 
- C. Watermarking is also needed to only track state information for a window of time in which we expect records could be delayed. 
- D. The new records need also to be deduplicated against previously inserted data into the table. (Correct)

## Explanation
To perform streaming deduplication, we use dropDuplicates() function to eliminate duplicate records within each new micro batch. In addition, we need to ensure that records to be inserted are not already in the target table. We can achieve this using insert-only merge.

Reference:

https://spark.apache.org/docs/3.1.2/api/python/reference/api/pyspark.sql.DataFrame.dropDuplicates.html

https://docs.databricks.com/delta/merge.html#data-deduplication-when-writing-into-delta-tables




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 27

## Question
A data engineer is designing a streaming ingestion pipeline using Auto Loader. The requirement is that the pipeline should never fail on schema changes but must capture any new columns that arrive in the data for later inspection.




Which configuration should the engineer use?

## Options
- A. none 
- B. addNewColumns 
- C. rescue (Correct)
- D. failOnNewColumns 

## Explanation
The `rescue` mode ensures that the schema does not evolve, so the stream will not fail if new columns are added. Instead, any new columns are stored in the rescued data column, allowing later inspection without interrupting the stream. This meets the requirement to keep the stream running without failures and still capture new schema elements.

---

# Question 28

## Question
Which of the following methods does Not allow data engineers to create a multi-task job in Databricks?

## Options
- A. Databricks Asset Bundles (DABs) 
- B. Lakeflow Declarative Pipelines (Correct)
- C. Workspace UI 
- D. REST API 

## Explanation
The method that does not allow data engineers to create a multi-task job in Databricks is Lakeflow Declarative Pipelines. Lakeflow Declarative Pipelines are meant for defining transformation logic in a declarative way (SQL/Python) and can function as a single task within a job rather than creating multi-task jobs themselves.




While the Workspace UI and REST API let you define jobs with multiple tasks, and Databricks Asset Bundles (DABs) can package and deploy multi-task job definitions.

---

# Question 29

## Question
A data engineering team manages a Delta Lake table in Unity Catalog called employees, with columns: id, name, salary, and region. They want to apply row filtering on this table so that only members of the HR team can access all records. If the table is queried by a non-HR team member, it should only show records in the France (FR) region. To achieve this, they implemented the following user-defined function:



```

- CREATE FUNCTION fr_filter(region STRING)
- RETURN IF(IS_ACCOUNT_GROUP_MEMBER('hr_team'), true, region='FR');
```





Which of the following commands can the team use to apply this function as a row filter to the table?

## Options
- A. SET ROW FILTER fr_filter ON TABLE employees TO COLUMN region 
- B. ALTER TABLE employees SET ROW FILTER fr_filter; 
- C. ALTER TABLE employees SET ROW FILTER fr_filter ON (region); (Correct)
- D. ALTER TABLE employees ALTER COLUMN region SET ROW FILTER fr_filter; 

## Explanation
The correct command to apply the function as a row filter to the Delta Lake table is:




`ALTER TABLE employees SET ROW FILTER fr_filter ON (region);`




This command correctly associates the user-defined function fr_filter with the region column of the employees table, ensuring that access to rows is filtered based on the function’s logic. In this setup, when a user queries the table, if they belong to the hr_team account group, they will be able to see all rows; otherwise, only rows where the region column equals 'FR' will be visible.

---

# Question 30

## Question
A data engineer wants to use Databricks REST API to retrieve the metadata of a job run using its run_id.




Which of the following REST API calls achieves this requirement ?

## Options
- A. Send POST request to the endpoint ‘api/2.2/jobs/runs/get’ 
- B. Send GET request to the endpoint ‘api/2.2/jobs/runs/get’ (Correct)
- C. Send GET request to the endpoint ‘api/2.2/jobs/runs/get-metadata’ 
- D. Send GET request to the endpoint ‘api/2.2/jobs/runs/get-output’ 

## Explanation
Sending GET requests to the endpoint ‘/api/2.2/jobs/runs/get’ allows us to retrieve the metadata of a job run using its run_id.




Reference:

https://docs.databricks.com/dev-tools/api/latest/jobs.html#operation/JobsRunsGet




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 31

## Question
Which two of the following describe benefits of enabling predictive optimization on managed tables in Unity Catalog?




Choose 2 answers:

## Options
- A. It simplifies maintenance by automatically running maintenance operations on the table. (Correct)
- B. It reduces overall cost by forecasting storage usage and reallocating data across tiers. 
- C. It enhances query performance by collecting statistics as data is written to the table. (Correct)
- D. It boosts data privacy by automatically encrypting data on write and masking sensitive columns. 
- E. It improves data profiling by automatically predicting missing values in the table columns. 

## Explanation
Predictive Optimization in Databricks Unity Catalog automatically optimizes managed tables in Unity Catalog by:



- 

Running background maintenance tasks like VACUUM, OPTIMIZE, and ANALYZE to reduce fragmentation and improve performance.
- 

Collecting table statistics during writes, which helps the query optimizer make better decisions and improve query speed.

---

# Question 32

## Question
“A feature built into Delta Lake that allows to automatically generate CDC feeds about Delta Lake tables”




Which of the following is being described in the above statement?

## Options
- A. Optimized writes 
- B. Slowly Changing Dimension (SCD) 
- C. Auto Optimize 
- D. Change Data Feed (CDF) (Correct)

## Explanation
Change Data Feed ,or CDF, is a new feature built into Delta Lake that allows it to automatically generate CDC feeds about Delta Lake tables.




CDF records row-level changes for all the data written into a Delta table. This includes the row data along with metadata indicating whether the specified row was inserted, deleted, or updated.







Reference:

https://docs.databricks.com/delta/delta-change-data-feed.html




Study materials from our exam preparation course on Udemy:

Lecture

Hands-on

---

# Question 33

## Question
An organization plans to use Delta Sharing for enabling large dataset access by multiple clients across AWS, Azure, and GCP. A senior data engineer has recommended migrating the dataset to Cloudflare R2 object storage prior to initiating the data sharing process.




Which benefit does Cloudflare R2 offer in this Delta Sharing setup?

## Options
- A. Provides standard API to avoid cloud vendor lock-in 
- B. Eliminates cloud provider egress cost for outbound data transfers (Correct)
- C. Provides native support for dynamic data masking 
- D. Offer built-in support for streaming data with automatic checkpointing 

## Explanation
Cloudflare R2 removes egress costs, which helps significantly lower expenses when sharing data across cloud environments.

---

# Question 34

## Question
Which of the following Delta Sharing implementations support sharing Unity Catalog Volumes, Unity Catalog Models, and notebooks in addition to static Delta tables?

## Options
- A. None of the listed options support sharing these assets 
- B. Customer-managed implementation of the open-source Delta Sharing server 
- C. Databricks open sharing protocol 
- D. Databricks-to-Databricks sharing protocol (Correct)

## Explanation
The Databricks-to-Databricks sharing protocol is the only Delta Sharing implementation that supports sharing not just static Delta tables, but also additional Unity Catalog assets such as Volumes, Models, and Notebooks. This protocol extends the open Delta Sharing standard, enabling seamless collaboration and governance between Databricks workspaces and organizations within the Databricks ecosystem.




In contrast, the open Delta Sharing protocol and customer-managed implementations of the open-source Delta Sharing server are limited to sharing static Delta tables only. They do not support Unity Catalog assets or Databricks-native objects beyond data tables.

---

# Question 35

## Question
Given the following query on the Delta table ‘customers’ on which Change Data Feed is enabled:



```

- spark.read
-         .option("readChangeFeed", "true")
-         .option("startingVersion", 0)
-         .table ("customers")
-         .filter (col("_change_type").isin(["update_postimage"]))
-     .write
-         .mode("append")
-         .table("customers_updates")
```





Which statement describes the result of this query each time it is executed ?

## Options
- A. The entire history of updated records will overwrite the target table at each execution. 
- B. Newly updated records will overwrite the target table. 
- C. The entire history of updated records will be appended to the target table at each execution, which leads to duplicate entries. (Correct)
- D. Newly updated records will be appended to the target table. 

## Explanation
Reading table’s changes, captured by CDF, using spark.read means that you are reading them as a static source. So, each time you run the query, all table’s changes (starting from the specified startingVersion) will be read.




The query in the question then appends the data to the target table at each execution since it’s using the ‘append’ writing mode.







Reference:

https://docs.databricks.com/delta/delta-change-data-feed.html#read-changes-in-batch-queries




Study materials from our exam preparation course on Udemy:

Lecture

Hands-on

---

# Question 36

## Question
The data engineering team wants to create a multiplex bronze Delta table from a Kafka source. The Delta Table has the following schema:




key BINARY, value BINARY, topic STRING, partition LONG, offset LONG, timestamp LONG




Since the “value” column contains Personal Identifiable Information (PII) for some topics, the team wants to apply Access Control Lists (ACLs) at partition boundaries to restrict access to this PII data.




Based on the above schema and the specified requirement, which column is a good candidate for partitioning?

## Options
- A. timestamp 
- B. key 
- C. partition 
- D. topic (Correct)

## Explanation
Table partitioning helps improve security. You can separate sensitive and nonsensitive data into different partitions and apply different security controls to the sensitive data.




* Personally Identifiable Information or PII represents any information that allows identifying individuals by either direct or indirect means, such as the name and the email of the user.




Study materials from our exam preparation course on Udemy:

Lecture

Hands-on

---

# Question 37

## Question
Which of the following correctly orders the Lakeflow Declarative pipeline permissions from least privilege to most privilege?

## Options
- A. CAN VIEW → CAN RUN → CAN MANAGE (Correct)
- B. CAN RUN → CAN VIEW → CAN MANAGE 
- C. CAN MANAGE → CAN VIEW → CAN RUN 
- D. CAN VIEW → CAN MANAGE → CAN RUN 

## Explanation
In permission hierarchies, least privilege to most privilege means starting with the minimal access and ending with full control.



- 

CAN VIEW: allows only viewing pipeline details, Spark UI, and driver logs.
- 

CAN RUN: allows executing the pipeline but not modifying it.
- 

CAN MANAGE: allows full control, including executing, editing, deleting, and managing permissions.




The same concept applies to job permissions.









Note: Databricks has recenlty open-sourced this solution, integrating it into the Apache Spark ecosystem under the name Spark Declarative Pipelines (SDP).

---

# Question 38

## Question
A data engineer has a streaming job that updates a Delta table named ‘user_activities’ by the results of a join between a streaming Delta table ‘activity_logs’ and a static Delta table ‘users’.




They noticed that adding new users into the ‘users’ table does not automatically trigger updates to the ‘user_activities’ table, even when there were activities for those users in the ‘activity_logs’ table.




Which of the following likely explains this issue?

## Options
- A. The static portion of the stream-static join drives this join process only in batch mode. 
- B. The streaming portion of this stream-static join drives the join process. Only new data appearing on the streaming side of the join will trigger the processing. (Correct)
- C. The users table must be refreshed with REFRESH TABLE command for each microbatch of this join 
- D. This stream-static join is not stateful by default unless they set the spark configuration delta.statefulStreamStaticJoin to true. 

## Explanation
In stream-static join, the streaming portion of this join drives this join process. So, only new data appearing on the streaming side of the join will trigger the processing. While, adding new records into the static table will not automatically trigger updates to the results of the stream-static join.







Reference: https://docs.databricks.com/structured-streaming/delta-lake.html#performing-stream-static-joins




Study materials from our exam preparation course on Udemy:

Lecture

Hands-on

---

# Question 39

## Question
A data engineer is testing a transformation pipeline that adds a new column to an existing DataFrame. They want to ensure the resulting DataFrame matches the expected output.




Which of the following functions can a data engineer use to verify equality?

## Options
- A. verifyEquality(actual_df, expected_df) 
- B. assert(actual_df = expected_df) 
- C. assertDataFrameEqual(actual_df, expected_df) (Correct)
- D. assertEqual(actual_df, expected_df) 

## Explanation
In PySpark, to verify the equality of two DataFrames, the correct function to use is `pyspark.testing.assertDataFrameEqual(actual, expected)`. This function compares the two DataFrames element-wise, checking for exact equality by default. It allows for optional parameters to control the comparison behavior, such as `ignoreColumnOrder` and `ignoreNullable`. If the DataFrames do not match, the function raises a `PySparkAssertionError` and provides a detailed diff of the differences.

---

# Question 40

## Question
A data engineer is responsible for managing and orchestrating data workflows in their organization’s Databricks environment. They have deployed a job called events_process_job using Databricks Asset Bundles. To execute this job, the engineer runs the following command from their terminal:




`databricks bundle run events_process_job`




After observing the command, a senior data engineer suggests that they could improve the execution process by adding the `-t` option when running the command.




Which of the following explain the primary purpose of this option?

## Options
- A. To trigger dry run of the job without actually processing data 
- B. To enable temporary logging during job execution 
- C. To select the target environment for the job run (Correct)
- D. To specify the target cluster size for the job run 

## Explanation
The primary purpose of the -t option in the databricks bundle run command is to select the target environment for the job run.




When a data engineer runs a job using Databricks Asset Bundles, the -t (or --target) flag allows them to specify which environment—such as development, staging, or production—the job should execute in.




`databricks bundle run events_process_job -t prod`




This helps ensure that jobs run against the correct resources and datasets for that environment, avoiding accidental changes or processing in the wrong context, and streamlines deployment workflows across multiple environments.

---

# Question 41

## Question
A data analyst at a retail company is responsible for generating daily reports on sales performance across multiple regions and product categories. The company ingests transaction data continuously from its online stores using Lakeflow Declarative Pipelines. The analyst needs to create a relational object that can efficiently precompute business-level aggregations, such as total revenue, average order value, and units sold per category, so that downstream reporting and dashboards can access the data quickly without recalculating it every time.




Which of the following objects is most suitable for this use case?

## Options
- A. Standard view 
- B. Temporary view 
- C. Materialized view (Correct)
- D. Streaming table 

## Explanation
The most suitable object for this use case is a materialized view because it allows the data analyst to precompute and store business-level aggregations, such as total revenue, average order value, and units sold per category, so that downstream reports and dashboards can access the results quickly without recalculating them every time, unlike a temporary or standard view, which either exist only for the session or require repeated recomputation, and unlike a streaming table, which is designed for processing raw, real-time event streams rather than pre-aggregated summaries.

---

# Question 42

## Question
Which of the following commands can a data engineer use to create a Delta table “orders” with Automatic Liquid Clustering enabled?

## Options
- A. ```

- CREATE OR REPLACE TABLE orders(id int, updated date, value double)
- CLUSTER BY ALL;
``` 
- B. ```

- CREATE OR REPLACE TABLE orders(id int, updated date, value double)
- CLUSTER BY NONE;
``` 
- C. ```

- CREATE OR REPLACE TABLE orders(id int, updated date, value double)
- CLUSTER BY AUTO;
``` (Correct)
- D. ```

- CREATE OR REPLACE TABLE orders(id int, updated date, value double)
- CLUSTER BY (id, updated, value);
``` 

## Explanation
Automatic Liquid Clustering in Delta Lake is enabled using `CLUSTER BY AUTO`. This allows Delta to automatically manage clustering based on query patterns and data distribution, without manually specifying columns.




The other options are incorrect because CLUSTER BY (id, updated, value) manually specifies clustering columns, so it does not enable automatic clustering. CLUSTER BY NONE explicitly disables liquid clustering, and CLUSTER BY ALL is not valid Delta Lake syntax.

---

# Question 43

## Question
Which of the following panels is Not included in the Query Profile view within Databricks SQL?

## Options
- A. Details 
- B. Query text 
- C. Query source (Correct)
- D. Top operators 

## Explanation
The Query Profile view provides three panels: Details, Top operators, and Query text, which give insights into query execution metrics, the main operations involved, and the actual SQL code.

---

# Question 44

## Question
Which of the following statements correctly describes Unit Testing?

## Options
- A. It’s an approach to test individual units of code to determine whether they still work as expected if new changes are made to them in the future (Correct)
- B. It’s an approach to measure the reliability, speed, scalability, and responsiveness of an application 
- C. It’s an approach to test the interaction between subsystems of an application to ensure that modules work properly as a group. 
- D. It’s an approach to verify if each feature of the application works as per the business requirements 

## Explanation
Unit testing is an approach to testing units of code, such as functions. So, If you make any changes to them in the future, you can use unit tests to determine whether they still work as you expect them to.




Assertions are used in unit tests to check if certain assumptions remain true while you're developing your code.




`assert func() == expected_value`







Reference:

https://docs.databricks.com/notebooks/testing.html




Study materials from our exam preparation course on Udemy:

Lecture

---

# Question 45

## Question
A data engineer run the following CTAS statement in a SQL notebook attached to an All-purpose cluster:



```

- CREATE TABLE course_students
- AS ( 	SELECT c.course_name, t.student_id, t.student_name
-         FROM courses c
-         LEFT JOIN (
-             SELECT s.student_id, s.student_name, e.course_id
-             FROM students s 
-             INNER JOIN enrollments e
-             ON s.student_id = e.student_id
-         ) t
-         ON c.course_id = t.course_id
-         WHERE c.active = true
- )
```





Which statement describes the resulting course_students table ?

## Options
- A. It’s a session-scoped table. The SELECT statement will be executed at the table creation, but its output will be stored in the cache of the current active Spark session. 
- B. It’s a virtual table that has no physical data. The SELECT statement will be executed each time the course_students table is queried. 
- C. It’s a cluster-scoped table. The SELECT statement will be executed at the table creation, but its output will be stored in the memory of the currently active cluster. 
- D. It’s a Delta Lake table. The SELECT statement will be executed at the table creation, and its output will be stored in Delta format on the underlying storage. (Correct)

## Explanation
`CREATE TABLE AS SELECT` statements, or CTAS statements create new Delta tables and populate them using the output of a SELECT query. So, The query result is stored in Delta format in the directory of the newly created table.







Reference: (cf. AS query clause)

https://docs.databricks.com/sql/language-manual/sql-ref-syntax-ddl-create-table-using.html




Study materials from our exam preparation course on Udemy:
- 

Lecture (Associate course)
- 

Hands-on (Associate course)

---

# Question 46

## Question
A data engineer is working on a project that requires integrating data from an external API into a Databricks workspace. For security reasons, they decided not to hardcode the API key directly in their notebooks. Instead, they used Databricks Secrets to securely store and manage sensitive credentials, as follows:



```

- databricks secrets create-scope api_scope
- databricks secrets put-secret api_scope api_key
```





They now want to read the API key in order to query the external API endpoint from a Databricks notebook.




Which of the following code lines allows the data engineer to achieve this task?

## Options
- A. api_key = dbutils.secrets.read("api_scope", "api_key") 
- B. api_key = dbutils.secrets.get("api_scope", "api_key") (Correct)
- C. api_key = dbutils.secrets.read("api_key", "api_scope") 
- D. api_key = dbutils.secrets.get("api_key", "api_scope") 

## Explanation
`dbutils.secrets.get(SCOPE, KEY)` is used to securely retrieve a secret where the first argument is the scope name (api_scope) and the second argument is the secret key (api_key).




Study materials from our exam preparation course on Udemy:
- 

Hands-on

---

# Question 47

## Question
A data engineer is analyzing a Spark job via the Spark UI. They have the following summary metrics for 27 completed tasks in a particular stage







Which conclusion can the data engineer draw from the above statistics ?

## Options
- A. All task are operating over partitions with even amounts of data 
- B. All task are operating over empty or near empty partitions 
- C. Number of tasks are operating over near empty partitions (Correct)
- D. Number of tasks are operating over partitions with larger skewed amounts of data. 

## Explanation
Usually, if your computation was completely symmetric across tasks, you would see all of the statistics clustered tightly around the 50th percentile value.




Here, we see the distribution is reasonable, except that we have a bunch of “Min” values near zero. This suggests that we have almost empty partitions.

---

# Question 48

## Question
Which of the following statements best describes dynamic file pruning in Apache Spark?

## Options
- A. An optimization technique that dynamically repartitions files into smaller chunks at runtime to balance workload across executors. 
- B. An optimization technique that skips reading irrelevant data files during query execution based on runtime filter information. (Correct)
- C. An optimization technique that automatically compresses large files during Spark job execution to prune storage usage. 
- D. An optimization technique that duplicates data files across worker nodes to improve data locality and query performance. 

## Explanation
Dynamic file pruning in Apache Spark is an optimization technique that skips reading irrelevant data files during query execution by leveraging runtime filter information, which allows Spark to avoid scanning files that do not match the query predicates, thereby improving performance and reducing I/O.

---

# Question 49

## Question
A data engineer has a PySpark DataFrame with the following columns: employee_name, department, and salary. They want to assign a tier to each employee within their department based on salary, where each employee has a unique tier number, even if they have the same salary. The expected output is as follows:








To achieve this, they define a window by department and order by salary in descending order:




`window_spec = Window.partitionBy("department").orderBy(df["salary"].desc())`




Which of the following functions correctly use this window to calculate the tier column?

## Options
- A. df.withColumn("tier", rank().over(window_spec)) 
- B. df.withColumn("tier", row_number().over(window_spec)) (Correct)
- C. df.withColumn("tier", dense_rank().over(window_spec)) 
- D. df.withColumn("tier", percent_rank().over(window_spec)) 

## Explanation
The expected output has a unique tier number to each employee within their department based on salary, even when multiple employees have the same salary. To achieve this, the data engineer should use the `row_number()` function. This is because r`ow_number()` generates a sequential number for each row within the specified window, guaranteeing uniqueness regardless of duplicate salary values.




In this case, the window is defined by department and ordered by salary in descending order:

`window_spec = Window.partitionBy("department").orderBy(df["salary"].desc())`




Using `row_number().over(window_spec)` will assign 1, 2, 3, … to employees in order of their salaries within each department, exactly matching the expected output.




Functions like `rank()` or `dense_rank()` would assign the same number to employees with identical salaries, and `percent_rank()` would produce fractional values between 0 and 1, so they would not meet the requirement of unique tier numbers.

---

# Question 50

## Question
A financial services firm manages highly sensitive client investment portfolios in Oracle databases and maintains its transactional market data in Microsoft SQL Server. Due to HIPAA regulations, data must remain in place and not be duplicated or exported unnecessarily. However, internal audit teams need to generate unified reports across both systems in Databricks while maintaining tight access control.




What solution should the data team use to enable direct querying to these databases without duplicating the data?

## Options
- A. Delta Sharing 
- B. Lakehouse Federation (Correct)
- C. Partner Connect 
- D. Shallow clone 

## Explanation
Lakehouse Federation is a feature in Databricks that enables users to query data in external databases directly, such as Oracle and SQL Server, without the need for data replication, ingestion, or movement. It provides a unified analytics layer on top of multiple data sources and allows for federated queries, where data from various platforms can be combined into a single logical view.




This aligns perfectly with the firm's needs

---

# Question 51

## Question
Given the following multi-task job







If there is an error in the notebook 1 that is associated with Task 1, which statement describes the run result of this job ?

## Options
- A. Task 1 will completely fail. Tasks 2 and 3 will run and succeed 
- B. Task 1 will completely fail. Tasks 2 and 3 will be skipped 
- C. Task 1 will partially fail. Tasks 2 and 3 will be skipped (Correct)
- D. Task 1 will partially fail. Tasks 2 and 3 will run and succeed 

## Explanation
If a task fails during a job run, all dependent tasks will be skipped.




The failure of a task will always be partial, which means that the operations in the notebook before the code failure will be successfully run and committed, while the operations after the code failure will be skipped.







Reference:

https://docs.databricks.com/workflows/jobs/repair-job-failures.html




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 52

## Question
Which of the following formats is used by Pandas UDFs to improve execution performance in Apache Spark?

## Options
- A. Delta Lake 
- B. Apache Kafka 
- C. Apache Iceberg 
- D. Apache Arrow (Correct)

## Explanation
Apache Arrow provides an efficient columnar in-memory data format that allows Spark to transfer data between the JVM and Python processes without serialization overhead. This significantly speeds up data processing compared to standard row-based formats.

---

# Question 53

## Question
A retail company stores sales data in Delta tables within Databricks Unity Catalog. They need to securely share specific tables with an external auditing firm, who uses Databricks on a different cloud provider.




Which of the following options enable achieving this task without data replication?

## Options
- A. Databricks-to-Databricks Delta Sharing (Correct)
- B. Shallow clone 
- C. External schema in Unity Catalog 
- D. Databricks Connect 

## Explanation
Databricks-to-Databricks Delta Sharing enables sharing data securely with any Databricks client, regardless of account or cloud host, as long as that the client has access to a workspace enabled for Unity Catalog.

---

# Question 54

## Question
A data engineering team wants to ensure that a specific Python library is available every time a cluster starts.




Which approach best achieves this goal?

## Options
- A. Install the library when running a Python notebook 
- B. Use an init script to install the library during cluster startup (Correct)
- C. Manually install the library on the driver node each time the cluster starts 
- D. Use Databricks CLI to upload the library files to the cluster after startup 

## Explanation
The best approach is use an init script to install the library during cluster startup, because init scripts run automatically whenever the cluster starts, ensuring the Python library is consistently installed on all nodes before any jobs or notebooks execute, whereas manual installation, per-notebook installation, or uploading files post-startup are error-prone, inconsistent, and require extra manual steps.

---

# Question 55

## Question
A junior data engineer has been tasked with implementing data quality validation in a Lakeflow Declarative Pipeline (LDP). They added several expectation functions to ensure that incoming datasets meet certain criteria before being processed further. After the junior engineer submitted a pull request, a senior data engineer began reviewing the code and noticed that one of the function calls used for validation was not correct.




As part of the review, the senior engineer wants to ensure that all expectation functions used in the pipeline are valid according to Databricks documentation.




Which of the following function calls is Not a valid expectation function in Lakeflow Declarative Pipelines?

## Options
- A. dlt.expect 
- B. dlt.expect_or_warn (Correct)
- C. dlt.expect_or_drop 
- D. dlt.expect_or_fail 

## Explanation
dlt.expect_or_warn is not a supported expectation function in Lakeflow Declarative Pipelines (LDP).




LDP supports the following expectation functions:
- 

dlt.expect: it writes invalid rows to the target (warning semantics)
- 

dlt.expect_or_drop: drops invalid rows before writing to the target.
- 

dlt.expect_or_fail: fails the update if violation occurs




Note: Databricks has recenlty open-sourced this solution, integrating it into the Apache Spark ecosystem under the name Spark Declarative Pipelines (SDP).

---

# Question 56

## Question
The data engineering team wants to know if the tables that they maintain in the Lakehouse are over-partitioned.




Which of the following is an indicator that a Delta Lake table is over-partitioned?

## Options
- A. If most partitions in the table have less than 1 GB of data (Correct)
- B. If the data in the table continues to arrive indefinitely. 
- C. If most partitions in the table have more than 1 GB of data 
- D. If the number of partitions in the table are too low 

## Explanation
Data that is over-partitioned or incorrectly partitioned will suffer greatly. Files cannot be combined or compacted across partition boundaries, so partitioned small tables increase storage costs and total number of files to scan. This leads to slowdowns for most general queries.




If most partitions in a table have less than 1GB of data, the table is likely over-partitioned




Reference:

https://docs.databricks.com/tables/partitions.html




Study materials from our exam preparation course on Udemy:

Lecture

Hands-on

---

# Question 57

## Question
Which of the following is considered a limitation when using the MERGE INTO command?

## Options
- A. Merge can not be performed if multiple source rows matched and attempted to modify the same target row in the table (Correct)
- B. Merge does not support records deletion. It supports only upsert operations. 
- C. Merge can not be performed in streaming jobs unless it uses Watermarking 
- D. Merge can not be performed if single source row matched and attempted to modify the multiple target rows in the table 

## Explanation
Merge operation can not be performed if multiple source rows matched and attempted to modify the same target row in the table. The result may be ambiguous as it is unclear which source row should be used to update or delete the matching target row.




For such an issue, you need to preprocess the source table to eliminate the possibility of multiple matches. 




Reference:

https://docs.databricks.com/error-messages/index.html#delta_multiple_source_row_matching_target_row_in_merge




Study materials from our exam preparation course on Udemy:

Lecture

---

# Question 58

## Question
The data engineering team has a pipeline that ingest Kafka source data into a Multiplex bronze table. This Delta table is partitioned based on the topic and month columns.  




A new data engineer notices that the ‘user_activity’ topic contains Personal Identifiable Information (PII) that needs to to be deleted every two months based on the company’s Service-Level Agreement (SLA).




Which statement describes how table partitioning can help to meet this requirement?

## Options
- A. Table partitioning allows delete queries to leverage partition boundaries. (Correct)
- B. Table partitioning reduces query latency when deleting large data files 
- C. Table partitioning does not allow to time travel the PII data after deletion 
- D. Table partitioning allows immediate files deletion without running VACUUM command 

## Explanation
Partitioning on datetime columns can be leveraged when removing data older than a certain age from the table. For example, you can decide to delete previous months data. In this case, file deletion will be cleanly along partition boundaries.




Similarly, data could be archived and backed up at partition boundaries to a cheaper storage tier. This drives a huge savings on cloud storage.




Reference: https://delta.io/blog/2023-01-18-add-remove-partition-delta-lake/




Study materials from our exam preparation course on Udemy:

Lecture

---

# Question 59

## Question
Which of the following commands can a data engineer use to grant full permissions to the HR team on the table employees?

## Options
- A. GRANT SELECT, MODIFY, CREATE, READ_METADATA ON TABLE employees TO hr_team 
- B. GRANT FULL PRIVILEGES ON TABLE employees TO hr_team 
- C. GRANT ALL PRIVILEGES ON TABLE employees TO hr_team (Correct)
- D. GRANT ALL PRIVILEGES ON TABLE hr_team TO employees 

## Explanation
ALL PRIVILEGES is used to grant full permissions on an object to a user or group of users. It is translated into all the below privileges:
- 

SELECT
- 

CREATE
- 

MODIFY
- 

USAGE
- 

READ_METADATA




Reference: https://docs.databricks.com/security/access-control/table-acls/object-privileges.html#privileges




Study materials from our exam preparation course on Udemy:
- 

Lecture (Associate course)
- 

Hands-on (Associate course)

---

