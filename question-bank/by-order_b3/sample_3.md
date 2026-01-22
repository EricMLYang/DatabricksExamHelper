# Question 1

## Question
A data engineer is using the following spark configurations in a pipeline to enable Optimized Writes and Auto Compaction:



```

- spark.conf.set("spark.databricks.delta.optimizeWrite.enabled", True)
- spark.conf.set("spark.databricks.delta.autoCompact.enabled", True)
```





They also want to enable Z-order indexing with Auto Compaction to leverage data skipping on all the pipeline’s tables.




Which of the following solutions allows the data engineer to complete this task ?

## Options
- A. Use spark.conf.set("spark.databricks.delta.autoZorder.enabled", True) 
- B. Z-order indexing with Auto Compaction can only be enabled on each table separately using:




ALTER TABLE table_name

SET TBLPROPERTIES (delta.autoOptimize.zorder.enabled = true) 
- C. There is no way to enable Z-order indexing with Auto Compaction since it does not support Z-Ordering (Correct)
- D. Use spark.conf.set("spark.databricks.delta.autoCompact.zorder.enabled", True) 

## Explanation
Auto Compaction does not support Z-Ordering as Z-Ordering is significantly more expensive than just compaction.




Study materials from our exam preparation course on Udemy:

Lecture

---

# Question 2

## Question
The data engineering team maintains the following join logic between three Delta tables:



```

- df_students =  spark.table("students")
- df_courses =  spark.table("courses")
- df_enrollments =  spark.table("enrollments")
-  
- df_join_1  = (df_students.join(df_enrollments, df_students.student_id == df_enrollments.student_id)
-                         .select(df_students.student_id,
-                                 df_students.student_name,
-                                 df_enrollments.course_id)
-               )
-  
- df_join_2 = (df_join_1.join(df_courses, df_join_1.course_id == df_courses.course_id)
-                        .select(df_join_1.student_id,
-                                df_join_1.student_name,
-                                df_courses.course_name)
- 	    )
-  
- (df_join_2.write
- .mode("overwrite")
- .table("students_courses_details"))
```





Which statement describes the result of this code block each time it is executed ?

## Options
- A. All records in the current version of the source tables will be considered in the join operations. The unmatched records will overwrite the students_courses_details table. 
- B. Only newly added records to any of the source tables will be considered in the join operations. The matched records will overwrite the students_courses_details table. 
- C. Only newly added records to any of the source tables will be considered in the join operations. The unmatched records will overwrite the students_courses_details table. 
- D. All records in the current version of the source tables will be considered in the join operations. The matched records will overwrite the students_courses_details table. (Correct)

## Explanation
The query reads three static Delta tables using spark.table() function, which means that all records in the current version of these tables will be read and considered in the join operations.




There is no difference between spark.table() and spark.read.table() function. Actually, spark.read.table() internally calls spark.table().




The pyspark.sql.DataFrame.join() function performs inner join operation by default, so the matched records will be written to the target table. In our case, the query writes the data in mode “overwrite” to the target table, which completely overwrites the table.

---

# Question 3

## Question
A data scientist from the marketing department requires read-only access to the ‘customer_insights’ table located in the analytics schema, which is part of the BI catalog. The data will be used to generate quarterly customer engagement reports. In accordance with the principle of least privilege, only the minimum permissions necessary to perform the required tasks should be granted.




Which SQL commands will correctly grant access with the least privileges?

## Options
- A. ```

- GRANT SELECT ON TABLE bi.analytics.insights TO marketing_team;
- GRANT USE SCHEMA ON SCHEMA bi.analytics TO marketing_team;
``` 
- B. ```

- GRANT SELECT ON TABLE bi.analytics.insights TO marketing_team;
- GRANT USE SCHEMA ON SCHEMA bi.analytics TO marketing_team;
- GRANT USE CATALOG ON CATALOG bi TO marketing_team;
``` (Correct)
- C. ```

- GRANT SELECT ON TABLE bi.analytics.insights TO marketing_team; 
``` 
- D. ```

- GRANT SELECT ON TABLE bi.analytics.insights TO marketing_team;
- GRANT USE CATALOG ON CATALOG bi TO marketing_team;
``` 

## Explanation
To access a specific table, the user must be granted SELECT on the table itself, `USE SCHEMA` on the containing schema, and `USE CATALOG` on the parent catalog. This provides just enough access for read operations without overprovisioning.

---

# Question 4

## Question
A team consisting of multiple data analysts wants to work on an analytics project that involves performing basic data exploration, querying small datasets, and running analyses using Python and SQL. They ask a data engineer to configure interactive clusters to support their workloads.




Which of the following cluster access modes should the engineer configure to best support this use case?

## Options
- A. SINGLE USER 
- B. DEDICATED 
- C. STANDARD (Correct)
- D. NO_ISOLATION_SHARED 

## Explanation
For a team of data analysts performing exploratory analysis, querying small datasets, and running Python and SQL workloads collaboratively, the STANDARD cluster access mode is the most suitable choice. Standard clusters are designed to provide shared access to the cluster resources for general workloads, providing cost-effective compute options while isolating users’ workloads from each other. They efficiently handle Python and SQL workloads, and since the project does not involve specialized computations like R, MLlib, or RDD-based tasks, there is no need for the additional capabilities of Dedicated Access mode. This mode balances operational efficiency with simplicity, making it ideal for collaborative but non-specialized analytics tasks.




Other modes are less appropriate for this scenario. Dedicated Access is intended for specialized workloads or group-based secure collaboration, which is overkill for standard Python/SQL analytics. Single-user clusters, which are now part of Dedicated Access mode, are designed for isolated operational workloads, not team collaboration. No Isolation Shared clusters provide minimal data isolation and are generally discouraged for multi-user environments due to security concerns.




Therefore, configuring Standard mode clusters ensures the analysts can collaborate effectively while keeping the environment secure, efficient, and cost-effective.

---

# Question 5

## Question
As a general rule, before scheduling notebooks in production, which of the following commands should be removed from the code ?

## Options
- A. Markup language commands 
- B. Display commands (Correct)
- C. Import commands 
- D. Magic commands 

## Explanation
Before scheduling notebooks in production, you may need to refactor your code. As a general rule, make sure you comment out:
- 

Unwanted files removal or tables dropping commands added during development
- 

Display actions or SQL queries added for debugging purposes




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 6

## Question
During the setup of Delta Sharing with an external partner, a data engineer asks the partner for their sharing identifier.




Which of the following best describes the sharing identifier within the context of Databricks-to-Databricks Sharing?

## Options
- A. It acts as the authentication token for API calls with the recipient's endpoint 
- B. It provides a unique reference for the recipient’s Unity Catalog metastore (Correct)
- C. It serves as a public encryption key used during data writes to the partner’s tables 
- D. It identify the partner’s network IP address for firewall whitelisting 

## Explanation
A Delta Sharing identifier is a unique string used in Databricks-to-Databricks sharing to identify a recipient's Unity Catalog metastore. This identifier allows the data provider to grant access to shared data.




The format of the sharing identifier is:

`<cloud>:<region>:<uuid>`




Example:

`aws:us-west-2:19a84bee-54bc-43a2-87de-023d0ec16016`




In this example:
- 

aws: represents the cloud provider (Amazon Web Services).
- 

us-west-2: represents the specific AWS region.
- 

19a84bee-54bc-43a2-87de-023d0ec16016: is the Universally Unique Identifier (UUID) of the recipient's Unity Catalog metastore.




Recipients can obtain their sharing identifier from their Databricks workspace using Catalog Explorer or by running a SQL query like SELECT CURRENT_METASTORE();. This identifier is then provided to the data provider, who uses it to create a recipient and grant access to shares.

---

# Question 7

## Question
A data engineer executed a query that took a long time. To investigate, they use the Query Profiler associated with this query to check the Total wall-clock duration metric.




Which of the following statements correctly describe what this metric measures?

## Options
- A. The total time from the start of scheduling to the end of query execution (Correct)
- B. The time spent on actual query execution 
- C. The total time spent on query optimization and file pruning 
- D. The time spent on query scheduling 

## Explanation
The Total wall-clock duration metric measures the total time from the start of scheduling to the end of query execution, covering the entire period the query takes to run, including scheduling, optimization and file pruning, and actual execution.

---

# Question 8

## Question
Which of the following Databricks CLI commands allows a data engineer to list all runs of a job that started at or after a specific time?

## Options
- A. databricks jobs list-runs --job-id <job-id> --time-from <time-value> 
- B. databricks jobs list-runs --job-id <job-id> --from <time-value> 
- C. databricks jobs list-runs --job-id <job-id> --start-time-from <time-value> (Correct)
- D. databricks jobs list-runs --job-id <job-id> --start <time-value> 

## Explanation
The correct Databricks CLI command that allows a data engineer to list all runs of a job that started at or after a specific time is `databricks jobs list-runs --job-id <job-id> --start-time-from <time-value>`, as `--start-time-from` is the proper parameter used to filter job runs based on their start time in the Databricks CLI.

---

# Question 9

## Question
A data engineer at a healthcare organization manages a Delta Lake table patient_records with columns: patient_id, name, department, and diagnosis. They want to create a user-defined function that masks the diagnosis column so that only doctors can view values in that column.




Which of the following functions can the data engineer use to achieve this?

## Options
- A. ```

- CREATE FUNCTION patient_mask(diagnosis STRING)
- RETURN CASE WHEN is_account_group_member('doctors') THEN 'CONFIDENTIAL' ELSE diagnosis END;
``` 
- B. ```

- CREATE FUNCTION patient_mask(doctors STRING)
- RETURN CASE WHEN is_account_group_member('diagnosis') THEN doctors ELSE 'CONFIDENTIAL' END;
``` 
- C. ```

- CREATE FUNCTION patient_mask(diagnosis STRING)
- RETURN CASE WHEN is_account_group_member('doctors') THEN diagnosis ELSE 'CONFIDENTIAL' END;
``` (Correct)
- D. ```

- CREATE FUNCTION patient_mask(diagnosis STRING)
- RETURN CASE WHEN diagnosis IS NOT NULL THEN diagnosis ELSE 'CONFIDENTIAL' END;
``` 

## Explanation
The correct answer is:



```

- CREATE FUNCTION patient_mask(diagnosis STRING)
- RETURN CASE WHEN is_account_group_member('doctors') THEN diagnosis ELSE 'CONFIDENTIAL' END;
```





This fucntion properly implements role-based access control by verifying if the current user belongs to the "doctors" group using the is_account_group_member('doctors') function. If the user is a doctor, the function reveals the actual diagnosis value; otherwise, it replaces the diagnosis with the string "CONFIDENTIAL" to protect sensitive patient information.




This approach ensures compliance with healthcare data privacy requirements while allowing authorized medical staff to access the necessary information.

---

# Question 10

## Question
Given a Delta table ‘products’ with the following schema:




name STRING, category STRING, expiration_date DATE,  price FLOAT




When executing the below query:



```

- SELECT * FROM products
- WHERE price > 30.5
```





Which of the following will be leveraged by the query optimizer to identify the data files to load?

## Options
- A. Columns statistics in the Hive metastore 
- B. Files statistics in Unity Catalog metastore 
- C. Columns statistics in the metadata of Parquet files 
- D. Files statistics in the Delta transaction log (Correct)

## Explanation
In the Transaction log, Delta Lake captures statistics for each data file of the table. These statistics indicate per file:
- 

Total number of records
- 

Minimum value in each column of the first 32 columns of the table
- 

Maximum value in each column of the first 32 columns of the table
- 

Null value counts for in each column of the first 32 columns of the table




When a query with a selective filter is executed against the table, the query optimizer uses these statistics to generate the query result. it leverages them to identify data files that may contain records matching the conditional filter.




For the SELECT query in the question, The transaction log is scanned for min and max statistics for the price column.




Study materials from our exam preparation course on Udemy:

Lecture

Hands-on

---

# Question 11

## Question
Which of the following tools does Not allow data engineers to programmatically trigger a multi-task job run?

## Options
- A. Databricks SDKs 
- B. Workspace Jobs UI (Correct)
- C. REST API 
- D. Command-line interface (CLI) 

## Explanation
The Workspace Jobs UI does not allow data engineers to programmatically trigger a multi-task job run. It’s a graphical interface that requires manual interaction and cannot be used for automated or code-based job execution.




While the REST API, Command-line interface (CLI), and Databricks SDKs all provide programmatic ways to run jobs.

---

# Question 12

## Question
A production environment has an S3 bucket receiving thousands of image files daily in different formats (.png, .jpg, .gif). A data engineer has been tasked with modifying the following streaming ingestion script to ensure only .png files are processed.



```

- df = spark.readStream.format("cloudFiles") \
-           .option("cloudFiles.format", "binaryFile") \
-           .option("_____________", "*.png") \
-           .load("s3://shop/raw/invoices/")
```





Which option correctly fills in the blank to meet the specified requirement ?

## Options
- A. fileExtension 
- B. cloudFiles.fileExtension 
- C. pathGlobFilter (Correct)
- D. cloudFiles.pathGlobFilter 

## Explanation
The `pathGlobFilter` option allows you to filter input files based on a glob pattern, such as *.png, when using Auto Loader.

---

# Question 13

## Question
A data engineering team at a supply chain company uses Lakeflow Declarative Pipelines to manage inventory data. The team maintains an append-only streaming table, inventory_raw, that stores raw inventory status information, with columns: product_id, quantity, and event_timestamp.




A data engineer is tasked with creating a new table, inventory_latest, to capture near real-time changes in product inventory levels from inventory_raw. The new table will include the columns: product_id, current_quantity, and updated_timestamp.




Which of the following types of objects would be most suitable to implement the inventory_latest table?

## Options
- A. Live table 
- B. Temporary view 
- C. Materialized view 
- D. Streaming table (Correct)

## Explanation
The most suitable object to implement the inventory_latest table is a Streaming table, because it is designed to continuously capture and update near real-time changes from an append-only source like inventory_raw. Implementing inventory_latest as a Streaming table allows you to merge incoming changes or apply a CDC (Change Data Capture) feed from inventory_raw so that the table always reflects the latest inventory state per product_id. Each new event—whether an update or insertion—can be applied in real time, updating current_quantity and updated_timestamp without rebuilding the entire table, which is the main advantage over a materialized view or temporary view.




Materialized Views (formerly known as Live Tables) provide batch-oriented or scheduled incremental processing for precomputed queries rather than continuously updating individual records in real time. Temporary views, in contrast, are ephemeral and not suited for persistent state tracking.




Note: Databricks has recenlty open-sourced this solution, integrating it into the Apache Spark ecosystem under the name Spark Declarative Pipelines (SDP).

---

# Question 14

## Question
Which of the following statements regarding cloning tables on Databricks is correct?

## Options
- A. Changes made to either deep or shallow clones affect the source table. 
- B. Any changes made to shallow clones affect only the clones themselves and not the source table. While, changes made to deep clones affect the source table. 
- C. Any changes made to either deep or shallow clones affect only the clones themselves and not the source table. (Correct)
- D. Any changes made to deep clones affect only the clones themselves and not the source table. While, changes made to shallow clones affect the source table. 

## Explanation
In either case, deep or shallow cloning, data modifications applied to the cloned version of the table will be tracked and stored separately from the source, so it will not affect the source table.




Study materials from our exam preparation course on Udemy:

Lecture (Associate course)

---

# Question 15

## Question
A data engineer has a PySpark DataFrame with the following columns: employee_name, department, and salary. They want to assign a tier to each employee within their department based on salary, where employees earning the same salary share the same tier. The expected output is as follows:








To achieve this, they define a window by department and order by salary in descending order:




`window_spec = Window.partitionBy("department").orderBy(df["salary"].desc())`




Which of the following functions correctly use this window to calculate the tier column?

## Options
- A. df.withColumn("tier", row_number().over(window_spec)) 
- B. df.withColumn("tier", dense_rank().over(window_spec)) 
- C. df.withColumn("tier", rank().over(window_spec)) (Correct)
- D. df.withColumn("tier", percent_rank().over(window_spec)) 

## Explanation
The correct function to use is `rank()` because it assigns the same rank (or tier) to employees with identical salaries within each department while maintaining the correct order when salaries differ. In this case, employees with the same salary value share the same tier number, and the next unique salary receives a rank that accounts for the number of preceding entries, which results in skipped tier numbers when ties occur. This matches the expected output, where, for example, Eve and Frank in the HR department both have a salary of 4000 and share tier 1, while David, with a lower salary of 3900, gets tier 3.




Other functions such as `row_number()` would assign unique sequential numbers even for ties, `dense_rank() `would not skip numbers after ties, and `percent_rank()` would assign fractional ranks between 0 and 1, none of which align with the desired behavior.

---

# Question 16

## Question
The data engineering team has a Silver table called ‘sales_cleaned’ where new sales data is appended in near real-time.




They want to create a new Gold-layer entity against the ‘sales_cleaned’ table to calculate the year-to-date (YTD) of the sales amount. The new entity will have the following schema:




country_code STRING, category STRING, ytd_total_sales FLOAT, updated TIMESTAMP




It’s enough for these metrics to be recalculated once daily. But since they will be queried very frequently by several business teams, the data engineering team wants to cut down the potential costs and latency associated with materializing the results.




Which of the following solutions meets these requirements?

## Options
- A. Define the new entity as a view to avoid persisting the results each time the metrics are recalculated 
- B. Create multiple tables, one per business team so the metrics can be queried quickly and efficiently. 
- C. Configuring a nightly batch job to recalculate the metrics and store them as a table overwritten with each update. (Correct)
- D. Define the new entity as a global temporary view since it can be shared between notebooks or jobs that share computing resources. 

## Explanation
Data engineers must understand how materializing results is different between views and tables on Databricks, and how to reduce total compute and storage cost associated with each materialization depending on the scenario.




Consider using a view when:
- 

Your query is not complex. Because views are computed on demand, the view is re-computed every time the view is queried. So, frequently querying complex queries with joins and subqueries increases compute costs
- 

You want to reduce storage costs. Views do not require additional storage resources.

Consider using a gold table when:
- 

Multiple downstream queries consume the table, so you want to avoid re-computing complex ad-hoc queries every time.
- 

Query results should be computed incrementally from a data source that is continuously or incrementally growing.




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 17

## Question
The data engineering team is looking for a simple solution to share part of a large Delta Lake table with the data science team. Only department-specific columns in the table need to be shared, but with different names. In addition, there is some sensitive data that must be filtered out before sharing.




Which of the following objects can be created to meet the specified requirements ?

## Options
- A. A new Delta Table created using CTAS statement on the existing table 
- B. A new Delta Table created using SHALLOW CLONE from the existing table 
- C. A new Delta Table created using DEEP CLONE from the existing table 
- D. A stored view on the existing table (Correct)

## Explanation
The solution in this case is to create a view on the table where the required columns can be renamed, and the sensitive data that can be filtered out with the WHERE clause.




Study materials from our exam preparation course on Udemy:
- 

Lecture (Associate course)
- 

Hands-on (Associate course)

---

# Question 18

## Question
A data engineering team wants to use Delta Sharing but is unsure whether to use Databricks-to-Databricks sharing (D2D) or the open Delta Sharing protocol (D2O).




Which of the following statements correctly explains the difference between D2D and D2O?

## Options
- A. Databricks-to-Databricks sharing (D2D) supports sharing data only through managed tables, while the Open Sharing protocol (D2O) supports both managed and external tables. 
- B. Databricks-to-Databricks sharing (D2D) uses the legacy Hive metastore, whereas the Open Sharing protocol (D2O) is built on Unity Catalog for newer implementations. 
- C. Databricks-to-Databricks sharing (D2D) enables data sharing exclusively between Databricks clients, while the Open Sharing protocol (D2O) allows any platform that implements the Delta Sharing open standard to access shared data. (Correct)
- D. Databricks-to-Databricks sharing (D2D) allows sharing with any platform that supports the Delta Sharing open standard, while the Open Sharing protocol (D2O) restricts sharing only to Databricks clients. 

## Explanation
There are mainly two ways to share data using Delta Sharing:




1- Databricks-to-Databricks sharing (D2D): it lets you share data from your Unity Catalog-enabled workspace with clients who also have access to a Unity Catalog-enabled Databricks workspace.




This approach uses the Delta Sharing server that is built into Databricks and provides support for notebook sharing, Unity Catalog data governance, auditing, and usage tracking for both providers and recipients.




2- Databricks open sharing protocol (D2O): It lets you share data that you manage in a Unity Catalog-enabled Databricks workspace with users on any computing platform.




This approach also uses the Delta Sharing server that is built into Databricks and is useful when you manage data using Unity Catalog and want to share it with users who don't use Databricks or don't have access to a Unity Catalog-enabled Databricks workspace.







So, D2D is optimized for seamless sharing within the Databricks ecosystem, whereas D2O extends interoperability to external platforms that support the open Delta Sharing protocol.

---

# Question 19

## Question
A data engineering team wants to automate job monitoring and improve observability by retrieving available jobs in the production Databricks workspace using REST API.




Which of the following REST API calls achieves this requirement?

## Options
- A. Send POST request to the endpoint ‘/api/2.2/jobs/get’ 
- B. Send GET request to the endpoint ‘/api/2.2/jobs/list’ (Correct)
- C. Send GET request to the endpoint ‘/api/2.2/jobs/get’ 
- D. Send POST request to the endpoint ‘/api/2.2/jobs/list’ 

## Explanation
Sending GET requests to the endpoint ‘/api/2.2/jobs/list’ allows you to retrieve available jobs in a Databricks workspace.

---

# Question 20

## Question
A data engineer is building a Lakeflow Declarative Pipeline to process product sales data. The pipeline needs to enforce the following data quality rules:




`valid_products = {"valid_id": "products_id IS NOT NULL", "recent_sales": "date >= '2025-01-01", "quantity_within_range": "quantity BETWEEN 0 AND 1000"}`




Any invalid records should still be written to the target, while metrics about these violations are captured by the pipeline.




Which of the following configurations would satisfy these requirements?

## Options
- A. ```

- @dlt.table
- @dlt.expect_all(valid_products)
- def silver_sales():
-     return dlt.read_stream("bronze_sales")
``` (Correct)
- B. ```

- @dlt.table
- @dlt.expect_or_fail(valid_products)
- def silver_sales():
-     return dlt.read_stream("bronze_sales")
``` 
- C. ```

- @dlt.table
- @dlt.expect(valid_products)
- def silver_sales():
-     return dlt.read_stream("bronze_sales")
``` 
- D. ```

- @dlt.table
- @dlt.expect_or_drop(valid_products)
- def silver_sales():
-     return dlt.read_stream("bronze_sales")
``` 

## Explanation
`dlt.expect_all` enforces all the specified data quality rules, writes both valid and invalid records to the target table, and captures metrics about any rule violations.




`dlt.expect` would not fully meet the requirements because it applies expectations individually but doesn’t automatically enforce all of them together as a group. Similarly, `dlt.expect_or_drop` removes individual invalid records, and `dlt.expect_or_fail` stops the pipeline on individual rule violations. You can group multiple expectations together and specify collective actions using the functions `dlt.expect_all_or_drop`, and `dlt.expect_all_or_fail`.




Note: Databricks has recenlty open-sourced this solution, integrating it into the Apache Spark ecosystem under the name Spark Declarative Pipelines (SDP).

---

# Question 21

## Question
The data engineering team at an analytics firm has started implementing Lakeflow Declarative Pipelines to process large-scale data transformation. During a routine code review session, the data engineering lead emphasizes a critical best practice: before performing any pipeline runs, the team must always click the “Validate” button in the notebook associated with the pipeline.




What is the main benefit of this practice?

## Options
- A. It executes the pipeline on a small dataset to preview the transformation results. 
- B. It runs unit tests on all pipeline components to verify their correctness. 
- C. It validates that the user has access permissions to create tables in the catalog. 
- D. It checks for any syntax errors in the pipeline code without actually processing data (Correct)

## Explanation
The “validate” option in the notebook identifies syntax or configuration errors in the pipeline definition before execution, reducing the risk of runtime failures or writing partial data.

---

# Question 22

## Question
A data engineer wants to use Databricks Asset Bundles (DABs) in a fully automated CI/CD pipeline on GitHub.




What is the recommended method for authenticating DABs to the target Databricks workspace in this scenario?

## Options
- A. Personal Access Token for a Databricks service principal 
- B. Personal Access Token for an administrator user 
- C. OAuth token federation for a Databricks service principal (Correct)
- D. OAuth client secret for a Databricks service principal 

## Explanation
Databricks Asset Bundles are a feature of the Databricks CLI. To enable the CLI to authenticate to Databricks without managing Databricks secrets, it’s recommended to use OAuth token federation for a Databricks service principal in the target workspace.

---

# Question 23

## Question
A data engineer has heard recently that users who have access to Databricks Secrets could be able to display the values of secrets in notebooks.




Which of the following could be a workaround to print the value of a Databricks secret in plain text?

## Options
- A. db_password = dbutils.secrets.get("prod-scope", "db-password", redacted=False)

print(db_password) 
- B. db_password = dbutils.secrets.get("prod-scope", "db-password")

display(db_password) 
- C. db_password = dbutils.secrets.get("prod-scope", "db-password")

print(db_password, redacted=False) 
- D. db_password = dbutils.secrets.get("prod-scope", "db-password")

for char in db_password:

       print(char) (Correct)

## Explanation
Databricks redacts secret values that are read using dbutils.secrets.get(). When displayed in notebook cell output, the secret values are replaced with [REDACTED] string.




However, is there a workaround to print the values of Databricks secrets in plain text by Iterating through the secret and printing each character.




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 24

## Question
A data engineer uses the following code to process CDC data in Lakeflow Declarative Pipelines:



```

- CREATE OR REFRESH STREAMING TABLE cdc_target;
-  
- CREATE FLOW cdc_flow AS AUTO CDC INTO users_target
- FROM stream(users_raw)
- KEYS (user_id)
- APPLY AS DELETE WHEN operation = "DELETE"
- SEQUENCE BY updated_timestamp
- COLUMNS *;
```





After running this code, the data engineer noticed that two objects were created the metastore in addition to the users_target table:
- 

A view named users_target.
- 

A table named __apply_changes_storage_users_target.




Which of the following correctly explains the purpose of these objects?

## Options
- A. These objects are used for internal CDC processing leveraging sequence_by along with extra information such as, tombstones and versions required to handle out-of-order data. (Correct)
- B. The view users_target is a materialized snapshot of the raw data, while the table __apply_changes_storage_users_target stores user activity logs for auditing purposes. 
- C. The users_target view is a virtual index on the target table to speed up queries, and __apply_changes_storage_users_target is a backup of the original users_target index. 
- D. The view users_target and the table __apply_changes_storage_users_target are temporary objects created for write optimization and are deleted immediately after the pipeline runs. 

## Explanation
In Lakeflow Declarative Pipelines*, when you create a CDC (Change Data Capture) flow with operations like `APPLY AS DELETE` and `SEQUENCE BY`, the system needs a way to manage incremental updates, including insertions, updates, and deletions, while maintaining the correct order of events based on sequence keys. The __apply_changes_storage_users_target table is an internal storage table that keeps track of these changes along with “tombstone” markers for deleted rows and versioning metadata to ensure that out-of-order or late-arriving events are applied correctly. This internal table is not meant for direct querying but is essential for maintaining CDC consistency.




The users_target view, on the other hand, is a virtual layer over this internal table that presents the current state of the data as a clean, queryable snapshot. This allows the CDC logic to remain encapsulated and transparent.




* Databricks has recenlty open-sourced this solution, integrating it into the Apache Spark ecosystem under the name Spark Declarative Pipelines (SDP).

---

# Question 25

## Question
A data engineer has implemented the following streaming ingestion code using Databricks Auto Loader:



```

- spark.readStream \
-      .format("cloudFiles") \
-      .schema(expected_schema) \
-      .option("cloudFiles.format", "json") \
-      .option("cloudFiles.schemaEvolutionMode", "failOnNewColumns") \
-      .load("s3://vendor/raw/sales/json/") \
-     .writeStream \
-      .option("checkpointLocation", "s3://vendor/checkpoints/sales") \
-      .start("sales_table")
```





What is the expected behavior of this streaming job if a new column appears in the incoming JSON files that is not part of the original schema?




If a new column appears in the incoming JSON files that is not present in the existing schema, what will happen to the streaming job?

## Options
- A. The stream fails and will not restart unless the schema is manually updated or the problematic data file is removed. (Correct)
- B. The stream fails temporarily but continues by ignoring the new columns without schema update. 
- C. The stream fails, but it automatically restarts after updating the schema with the new columns. 
- D. The stream fails, and all new columns are saved in a rescued data column for later processing. 

## Explanation
With the `failOnNewColumns` mode, the stream detects any new columns and fails immediately to enforce strict schema consistency. It will not automatically restart until the schema has been manually updated to include the new columns or the data files causing the schema mismatch are removed. This prevents silent schema drift and ensures deliberate schema management.

---

# Question 26

## Question
Which statement regarding static Delta tables in Stream-Static joins is correct?

## Options
- A. The latest version of the static Delta table is returned each time it is queried by a microbatch of the stream-static join (Correct)
- B. The latest version of the static Delta table is returned only for the first microbatch of the stream-static join. Then, it will be cached to be used by any upcoming microbatch. 
- C. Static Delta tables need to be refreshed with REFRESH TABLE command for each microbatch of a stream-static join 
- D. Static Delta tables must be small enough to be broadcasted to all worker nodes in the cluster. 

## Explanation
Stream-static joins take advantage of Delta Lake guarantee that the latest version of the static delta table is returned each time it is queried in a join operation with a data stream.




Study materials from our exam preparation course on Udemy:

Lecture

Hands-on

---

# Question 27

## Question
The data engineering team has a Delta Lake table created with following query:



```

- CREATE TABLE customers_clone
- LOCATION 'dbfs:/mnt/backup'
- AS SELECT * FROM customers
```





A data engineer wants to drop the table with the following query:

`DROP TABLE customers_clone`




Which statement describes the result of running this drop command ?

## Options
- A. Only the table's metadata will be deleted from the catalog, while the data files will be kept in the storage (Correct)
- B. The table will not be dropped until VACUUM command is run 
- C. Both the table's metadata and the data files will be deleted 
- D. An error will occur as the table is shallowly cloned from the customers table 

## Explanation
External (unmanaged) tables are tables whose data is stored in an external storage path by using a LOCATION clause.

When you run DROP TABLE on an external table, only the table's metadata is deleted, while the underlying data files are kept.




Study materials from our exam preparation course on Udemy:

Lecture (Associate course)

Hands-on (Associate course)

---

# Question 28

## Question
A data engineer wants to install a Python wheel scoped to the current notebook’s session, so only the current notebook and any jobs associated with this notebook have access to that library.




Which of the following commands can the data engineer use to complete this task?

## Options
- A. %pip install my_package.whl (Correct)
- B. %fs install my_package.whl 
- C. %whl install my_package 
- D. %python install my_package.whl 

## Explanation
‘%pip install’ allows you to install a Python wheel scoped to the current notebook’s session. This library will be only accessible in the current notebook and any jobs associated with this notebook.




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 29

## Question
Which of the following is the default target file size when compacting small files of a Delta table by manually running OPTIMIZE command ?

## Options
- A. 128 MB 
- B. 1024 MB (Correct)
- C. 256 MB 
- D. 512 MB 

## Explanation
The OPTIMIZE command compact small data files into larger ones. The default value is 1073741824, which sets the size to 1 GB.




Study materials from our exam preparation course on Udemy:
- 

Lecture
- 

Lecture (Associate course)
- 

Hands-on (Associate course)

---

# Question 30

## Question
Which of the following statements best describes the use of Python wheels in Databricks?

## Options
- A. A Python wheel is a repository for hosting, managing, and distributing Python binaries and artifacts in a Databricks workspace 
- B. A Python wheel is a binary distribution format for installing custom Python code packages on Databricks Clusters (Correct)
- C. A Python wheel is package installer tool alternative to ‘pip’ 
- D. A Python wheel is a virtual environment for isolating the Python interpreter, libraries and modules in a notebook from other notebooks. 

## Explanation
Python wheel is a binary distribution format for installing custom Python code packages on Databricks Clusters.




A wheel is a ZIP-format archive with the .whl extension.




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 31

## Question
Which two prerequisites are required to enable Automatic Liquid Clustering on a Delta table?




Choose 2 answers:

## Options
- A. Table must be a Unity Catalog-managed table (Correct)
- B. Table must be partitioned by a date column 
- C. Table must be a Unity Catalog-external table 
- D. Table must have deletion vectors enabled 
- E. Table must have predictive optimization enabled (Correct)

## Explanation
To enable Automatic Liquid Clustering on a Delta table in Databricks, two prerequisites are required:



- 

Table must be a Unity Catalog-managed table
- 

Automatic Liquid Clustering works only on tables managed by Unity Catalog. External tables are currently not supported.

- 

Table must have predictive optimization enabled
- 

Predictive optimization provides the system with insights on access patterns, which Liquid Clustering leverages to automatically optimize data layout.

---

# Question 32

## Question
The data engineering team has a large Delta table named ‘users’. A recent query on the table returned some entries with negative values in the ‘age’ column.




To avoid this issue and enforce data quality, a junior data engineer decided to add a CHECK constraint to the table with the following command:




`ALTER TABLE users ADD CONSTRAINT valid_age CHECK (age> 0);`




However, the command fails when executed.




Which statement explains the cause of this failure?

## Options
- A. The users table already contains rows that violate the new constraint; all existing rows must satisfy the constraint before adding it to the table. (Correct)
- B. The users table already exists; CHECK constraints can only be added during table creation using CREATE TABLE command. 
- C. The users table already contains rows; CHECK constraints can only be added on empty tables 
- D. The syntax for adding the CHECK constraint is incorrect. Instead, the command should be:

ALTER TABLE users ADD CONSTRAINT ON COLUMN age (CHECK > 0) 

## Explanation
ADD CONSTRAINT command verifies that all existing rows in the table satisfy the constraint before adding it to the table. Otherwise, the command failed with an error that says some rows in the table violate the new CHECK constraint.




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 33

## Question
A data engineering team manages a multi-task job where each task may be retried multiple times. They noticed that job notifications are not sent when failed tasks are retried.




Which of the following configurations will ensure that a failure notification is received for every failed task?

## Options
- A. Use task-level notifications in the job definition (Correct)
- B. Implement custom notification logic within each task 
- C. Create a separate job for each task with job-level retries 
- D. Disable all task retries to rely on job-level notifications 

## Explanation
In a multi-task job, notifications can be configured at two levels:



- 

Job-level notifications: Trigger only when the entire job succeeds or fails.
- 

This means if an individual task fails but is retried successfully, no notification is sent until the overall job completes or fails.

- 

Task-level notifications: Trigger for each task event, including failures, or successful completions.








Configuring task-level notifications ensures a notification is sent for every failed task, even if it’s later retried.

---

# Question 34

## Question
A data engineer needs to programmatically extract the data quality results of a LDP pipeline from the associated event log table.




Which of the following code snippets can the data engineer use to achieve this task?

## Options
- A. ```

- SELECT data_quality
- FROM catalog.schema.event_log
- WHERE event_type = 'metrics'
``` 
- B. ```

- SELECT expectations
- FROM catalog.schema.event_log
- WHERE event_type = 'flow_progress'
``` 
- C. ```

- SELECT details:flow_progress.data_quality.expectations
- FROM catalog.schema.event_log
- WHERE event_type = 'flow_progress'
``` (Correct)
- D. ```

- SELECT expectations
- FROM catalog.schema.event_log
- WHERE event_type = 'metrics'
``` 

## Explanation
In the event log table for LDP* pipelines, the data quality results are logged under events of type 'flow_progress' and stored inside the details column in a nested JSON structure:



- 

details:flow_progress: contains information about a pipeline’s execution progress
- 

details:flow_progress.data_quality: contains the data quality results (expectations, dropped_records, etc.)
- 

details:flow_progress:data_quality.expectations: specifically holds the expectation results


* Databricks has recenlty open-sourced this solution, integrating it into the Apache Spark ecosystem under the name Spark Declarative Pipelines (SDP).

---

# Question 35

## Question
In Spark UI, which of the following is Not part of the metrics displayed in a stage’s details page ?

## Options
- A. Spill (Disk and Memory) 
- B. Duration 
- C. GC time 
- D. DBU Cost (Correct)

## Explanation
In Spark UI, the stage’s details page shows summary metrics for completed tasks. This includes:



- 

Duration of tasks.
- 

GC time: is the total JVM garbage collection time.
- 

Shuffle spill (memory): is the size of the deserialized form of the shuffled data in memory.
- 

Shuffle spill (disk): is the size of the serialized form of the data on disk.
- 

and others …




DBU Cost is not part of Spark UI. DBU stands for Databricks Unit and it is a unit of processing capability per hour for pricing purposes. This depends on your cluster configuration which tells you how much DBUs would be consumed if a virtual machine runs for an hour, and then pays for each DBU consumed.




Study materials from our exam preparation course on Udemy:

Hands-on (Associate course)

---

# Question 36

## Question
A data engineering team has successfully established a new connection named mysql_connection in Databricks to connect to their external MySQL database. Their goal is to make the MySQL tables available and queryable through Unity Catalog by leveraging Lakehouse Federation, allowing downstream analytics teams to seamlessly access this data.




Given that the connection is already in place, the team now needs to take the next step to add the MySQL tables within Unity Catalog so that they can be queried in a governed and secure manner, consistent with their organization’s data governance policies.




What is the next step the team should take to achieve this goal?

## Options
- A. Create a foreign catalog in Unity Catalog using the existing mysql_connection. (Correct)
- B. Create an external catalog with a default location defined via the existing mysql_connection. 
- C. Create an external table referencing MySQL data through the existing mysql_connection. 
- D. Set up a Unity Catalog metastore for MySQL using the existing mysql_connection. 

## Explanation
The next step the team should take is to create a foreign catalog in Unity Catalog using the existing mysql_connection, as Lakehouse Federation in Databricks allows Unity Catalog to register external data sources like MySQL as foreign catalogs. This makes the tables accessible and queryable in a governed, secure way without moving the data, which aligns with the team’s goal.

---

# Question 37

## Question
The data engineering team noticed that a partitioned Delta Lake table is suffering greatly. They are experiencing slowdowns for most general queries on this table.




The team tried to run an OPTIMIZE command on the table, but this did not help to resolve the issue.




Which of the following likely explains the cause of these slowdowns?

## Options
- A. They are applying the OPTIMIZE command on the whole table. It must be applied at each partition separately. 
- B. They are applying the OPTIMIZE command without ZORDER. Z-ordering is needed on the partitioning columns. 
- C. The table is over-partitioned or incorrectly partitioned. This requires a full rewrite of all data files to resolve the issue. (Correct)
- D. The table has too many old data files that need to be purged. They need to run a VACUUM command instead. 

## Explanation
Data that is over-partitioned or incorrectly partitioned will suffer greatly. Files cannot be combined or compacted across partition boundaries, so partitioned small tables increase storage costs and total number of files to scan. This leads to slowdowns for most general queries. Such an issue requires a full rewrite of all data files to remedy.




Study materials from our exam preparation course on Udemy:

Lecture

Hands-on

---

# Question 38

## Question
A data engineer has defined the following data quality constraint in a LDP pipeline:




`CONSTRAINT valid_id EXPECT (id IS NOT NULL) _____________`




Which clause correctly fills in the blank so records violating this constraint will be dropped, and reported in metrics?

## Options
- A. ON VIOLATION DELETE ROW 
- B. ON VIOLATION DROP ROW (Correct)
- C. ON VIOLATION FAIL UPDATE 
- D. ON VIOLATION DISCARD ROW 

## Explanation
The correct clause to fill in the blank is ON VIOLATION DROP ROW, so the full constraint becomes `CONSTRAINT valid_id EXPECT (id IS NOT NULL) ON VIOLATION DROP ROW`. This ensures that any record with a null id will be automatically dropped from the pipeline, while still being tracked in the pipeline’s metrics, allowing the data engineer to monitor the number of violations without failing the entire job.




Note: Databricks has recenlty open-sourced this solution, integrating it into the Apache Spark ecosystem under the name Spark Declarative Pipelines (SDP).




Study materials from our exam preparation course on Udemy:
- 

Hands-on

---

# Question 39

## Question
Which statement regarding Delta Lake File Statistics is Not correct?

## Options
- A. The statistics are generally uninformative for string fields with very high cardinality. 
- B. Nested fields do not count when determining the first 32 columns in the table. (Correct)
- C. Delta Lake captures statistics in the transaction log for each added data file 
- D. The statistics are leveraged for data skipping when executing selective queries. 

## Explanation
Delta Lake automatically captures statistics in the transaction log for each added data file of the table. By default, Delta Lake collects the statistics on the first 32 columns of each table. Nested fields count when determining the first 32 columns




Example: 4 struct fields with 8 nested fields will total to the 32 columns.




Study materials from our exam preparation course on Udemy:

Lecture

Hands-on

---

# Question 40

## Question
Which of the following techniques can a data engineer use to handle late-arriving data in Spark Structured Streaming?

## Options
- A. Watermarking (Correct)
- B. Windowing 
- C. Partitioning 
- D. Checkpointing 

## Explanation
In Spark Structured Streaming, you can handle late-arriving data primarily using watermarking, which allows the system to track event-time progress and specify how long to wait for late data before considering a window complete.




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 41

## Question
Which of the following statements correctly describes Integration Testing?

## Options
- A. It’s an approach to verify if each feature of the application works as per the business requirements 
- B. It’s an approach to simulate a user experience to ensure that the application can run properly under real-world scenarios 
- C. It’s an approach to test the interaction between subsystems of an application to ensure that modules work properly as a group. (Correct)
- D. It’s an approach to test individual units of code to determine whether they still work as expected if new changes are made to them in the future 

## Explanation
Integration Testing is an approach to testing the interaction between subsystems of an application. It tests that the software modules are integrated logically and tested as a group.




Study materials from our exam preparation course on Udemy:

Lecture

---

# Question 42

## Question
Which of the following is Not an advantage of using cluster policies?

## Options
- A. Control cost by limiting per-cluster maximum cost 
- B. Ensure clusters are created with consistent system settings, environment variables, and Spark configuration. 
- C. Enforce cluster-scoped library installations. 
- D. Schedule clusters to start and stop at specific times. (Correct)

## Explanation
Scheduling clusters to start and stop at specific times is not supported with cluster policies.

Cluster policies are primarily designed to enforce consistent configurations, manage library installations, control costs by setting limits and defaults on cluster creation.

---

# Question 43

## Question
A data engineer defines the following function in their LDP pipeline:



```

- @dlt.table
- @dlt.expect_or_drop("quantity_within_range", "quantity BETWEEN 0 AND 1000")
- @dlt.expect_or_drop("recent_transaction", "transaction_date >= '2025-01-01'")
- @dlt.expect_or_drop("valid_transaction", "transaction_id IS NOT NULL'")
- def silver_sales():
-     return dlt.read_stream("bronze_sales")
```





Which of the following correctly describes the result of running this pipeline?

## Options
- A. Rows that violate the defined expectations are deleted from both tables. 
- B. Rows that violate the defined expectations are deleted from the bronze_sales table. 
- C. Rows that violate the defined expectations are filtered out, and only valid rows are written to silver_sales. (Correct)
- D. Rows that violate the defined expectations are streamed into the silver_sales table. 

## Explanation
The expect_or_drop function is a data quality enforcement rule in LDP (previously known as DLT):
- 

The expect part defines the quality constraint (e.g., "quantity BETWEEN 0 AND 1000").
- 

The or_drop part defines the action to take when the expectation is violated. "Drop" means that the violating row is discarded (filtered out) and will not be written to the target table (silver_sales).




In this example, only rows that successfully pass all three defined expectations (quantity_within_range, recent_transaction, and valid_transaction) will be included in the silver_sales table. Rows failing any of them are discarded.




Note: Databricks has recenlty open-sourced this solution, integrating it into the Apache Spark ecosystem under the name Spark Declarative Pipelines (SDP).

---

# Question 44

## Question
A data engineer has a Job with multiple tasks that takes more than 2 hours to complete. In the last run, the final task unexpectedly failed.




Which of the following actions can the data engineer perform to complete this run while minimizing the execution time ?

## Options
- A. They need to delete the failed Run, and start a new Run for the Job 
- B. They can keep the failed Run, and simply start a new Run for the Job 
- C. They can rerun this Job Run to execute all the tasks 
- D. They can repair this Job Run so only the failed tasks will be re-executed (Correct)

## Explanation
You can repair failed multi-task jobs by running only the subset of unsuccessful tasks and any dependent tasks. Because successful tasks are not re-run, this feature reduces the time and resources required to recover from unsuccessful job runs.




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 45

## Question
A data engineer is analyzing a dataset of clickstream events from a high-traffic website. The dataset includes fields such as user_id, timestamp, event_type, and page_url. During a join operation between the clickstream logs and a user profile dataset (joined on user_id), the job’s performance is significantly hindered due to uneven data distribution. Further analysis confirms a data skew caused by a small subset of users generating a disproportionately large number of events.




Which of the following approaches is NOT an appropriate solution to mitigate the skew in this scenario?

## Options
- A. Use salting by appending a random prefix to skewed user_id values to distribute the load across partitions. 
- B. Broadcast the skewed keys to all worker nodes to avoid shuffle during the join. (Correct)
- C. Separate processing of skewed keys by handling high-frequency users in a dedicated job. 
- D. Repartition the clickstream dataset on user_id to increase the number of partitions before the join. 

## Explanation
Broadcasting is typically used to share small lookup datasets with all executors to avoid joins that cause shuffles. However, broadcasting skewed keys, especially if the associated data is large, does not solve the skew problem and may actually increase memory pressure on each executor.




Other options are appropriate solutions:

- Use salting by appending a random prefix to skewed user_id values to distribute the load across partitions.
Salting is an effective technique to mitigate skew by artificially spreading out hot keys across multiple partitions. This approach reduces bottlenecks caused by skewed keys during shuffles.

- Repartition the clickstream dataset to increase the number of partitions before the join.
Increasing the number of partitions via repartition() helps balance the data load and enhances parallelism. It can help mitigate skew by distributing keys more evenly.




- Separate processing of skewed keys by handling high-frequency users in a dedicated job.

Isolating skewed keys for specialized processing prevents them from affecting the entire join operation. This targeted approach can improve performance by tailoring resources to problematic keys.

---

# Question 46

## Question
Which of the following describes the minimal permissions a data engineer needs to attach a notebook to an existing cluster ?

## Options
- A. “Can Manage” privilege on the cluster 
- B. “Can Restart” privilege on the cluster 
- C. “Can Attach To” privilege on the cluster (Correct)
- D. Cluster creation allowed + “Can Attach To” privileges on the cluster 

## Explanation
You can configure two types of cluster permissions:




1- The ‘Allow cluster creation’ entitlement controls your ability to create clusters.




2- Cluster-level permissions control your ability to use and modify a specific cluster. There are four permission levels for a cluster: No Permissions, Can Attach To, Can Restart, and Can Manage. The table lists the abilities for each permission:








Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 47

## Question
The data engineering team has a secret scope named ‘DataOps-Prod’ that contains all secrets needed by DataOps engineers in a production workspace.




Which of the following is the minimum permission required for the DataOps engineers to use the secrets in this scope?

## Options
- A. MANAGE permission on the “DataOps-Prod” scope 
- B. READ permission on each secret in the “DataOps-Prod” scope 
- C. READ permission on the “DataOps-Prod” scope (Correct)
- D. MANAGE permission on each secret in the “DataOps-Prod” scope 

## Explanation
The secret access permissions are as follows:



- 

MANAGE - Allowed to change ACLs, and read and write to this secret scope.
- 

WRITE - Allowed to read and write to this secret scope.
- 

READ - Allowed to read this secret scope and list what secrets are available.




Each permission level is a subset of the previous level’s permissions (that is, a principal with WRITE permission for a given scope can perform all actions that require READ permission).




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 48

## Question
A data engineer has been asked to develop a nightly batch job for workforce productivity analytics. The job will process events of employees productivity of the previous day, and store the performance of each employee in the Delta table “employees_performance“. The table has the following schema:




"date DATE, employee_id STRING, rating DOUBLE"




The data engineering team wants data to be stored in the table with the ability to compare employees' performance across time.




Which of the following code blocks accomplishes this task ?

## Options
- A. performance_df.write.mode("append").saveAsTable("employees_performance") (Correct)
- B. performance_df.write.mode("overwrite").saveAsTable("employees_performance") 
- C. performance_df.write.partitionBy("date").saveAsTable("employees_performance") 
- D. performance_df.write.format("delta").saveAsTable("employees_performance") 

## Explanation
DataFrameWriter.mode defines the writing behaviour when data or table already exists.

Options include:
- 

`append`: Append contents of the DataFrame to existing data.
- 

`overwrite`: Overwrite existing data.
- 

`error` or `errorifexists`: Throw an exception if data already exists.
- 

`ignore`: Silently ignore this operation if data already exists.




This `errorifexists` or `error` is the default save mode. If the table already exists, it will throw the error message Error: pyspark.sql.utils.AnalysisException: table already exists.




The "employees_performance" table has a date column. So, in order to be able to compare employees' performance across time, each new batch of data with new date should be appended into the table using the `append` mode.

---

# Question 49

## Question
When running an existing job via Databricks REST API, which of the following represents the globally unique identifier of the newly triggered run ?

## Options
- A. job_id 
- B. run_key 
- C. run_id (Correct)
- D. task_id 

## Explanation
Running an existing job via the endpoint ‘/api/2.2/jobs/run-now’ returns the run_id of the triggered run. This represents the globally unique identifier of this newly triggered run.




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 50

## Question
Which of the following definitions correctly describes a Slowly Changing Dimension of Type 0?

## Options
- A. It’s a table where the new arriving data overwrites the existing one. 
- B. It’s a table that stores and manages both current and historical data over time. 
- C. It’s a table where no changes are allowed. (Correct)
- D. It’s a table where history will be kept in the additional column 

## Explanation
Type 0 SCD tables never change. Tables of this type are usually static. For example, static lookup tables.




Study materials from our exam preparation course on Udemy:

Lecture

---

# Question 51

## Question
“An object that physically stores precomputed query results, updating automatically or on a schedule to improve performance for complex aggregations and BI workloads”




Which of the following is being described in the above statement?

## Options
- A. Standard view 
- B. Temporary view 
- C. Streaming table 
- D. Materialized view (Correct)

## Explanation
The statement describes a materialized view. In Databricks SQL, materialized views are Unity Catalog managed tables that physically store the results of a query. Unlike standard views, which compute results on demand, materialized views cache the results and update them as the underlying source tables change; either on a schedule or automatically. By pre-computing expensive or frequently used queries, Materialized views lower query latency and resource consumption. This optimizes performance for complex aggregations and accelerate BI dashboard performance.




So, in summary, a materialized view has the following characteristics:
- 

Physically stores the results of a query.
- 

Can be refreshed automatically or on a schedule.
- 

Optimized for complex aggregations and business intelligence (BI) workloads.




Why other options are incorrect:
- 

Standard view: Does not store data physically; it’s just a saved query.
- 

Temporary view: Exists only for the session and is not persistent.
- 

Streaming table: incrementally ingests data, but it’s not for storing precomputed query results.

---

# Question 52

## Question
Which of the following describes the minimal permissions a data engineer needs to start and terminate an existing cluster ?

## Options
- A. “Can Attach To” privilege on the cluster 
- B. “Can Manage” privilege on the cluster 
- C. Cluster creation allowed + “Can Restart” privileges on the cluster 
- D. “Can Restart” privilege on the cluster (Correct)

## Explanation
You can configure two types of cluster permissions:




1- The ‘Allow cluster creation’ entitlement controls your ability to create clusters.




2- Cluster-level permissions control your ability to use and modify a specific cluster. There are four permission levels for a cluster: No Permissions, Can Attach To, Can Restart, and Can Manage. The table lists the abilities for each permission:








Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 53

## Question
Which of the following commands allows data engineers to perform an insert-only merge?

## Options
- A. ```

- MERGE INTO orders
- USING new_orders
- ON orders.orders_id = new_orders.orders_id
- WHEN NOT MATCHED
-     INSERT *
- WHEN MATCHED
-     IGNORE *
``` 
- B. ```

- MERGE INTO orders
- USING new_orders
- ON orders.orders_id = new_orders.orders_id
- WHEN MATCHED
-     INSERT *
``` 
- C. ```

- MERGE INTO orders
- USING new_orders
- ON orders.orders_id = new_orders.orders_id
- WHEN NOT MATCHED
-     INSERT *
``` (Correct)
- D. ```

- MERGE INTO orders
- USING new_orders
- ON orders.orders_id = new_orders.orders_id
- WHEN MATCHED
-     INSERT *
- WHEN NOT MATCHED
-     IGNORE *
``` 

## Explanation
The syntax for insert-only merge:



```

- MERGE INTO target_table
- USING soruce_table
- ON merge_condition
- WHEN NOT MATCHED
-     INSERT *
```





You just need to specify the NOT MATCHED clause, which inserts a row when a source row does not match any target row based on the merge_condition (merge keys). Records that have the same keys as an existing record in the table will be simply ignored.




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 54

## Question
“A Delta Lake’s functionality that automatically compacts small files during individual writes to a table by performing two complementary operations on the table”




Which of the following is being described in the above statement?

## Options
- A. OPTIMIZE operation 
- B. Auto Optimize (Correct)
- C. Auto compaction 
- D. Optimized writes 

## Explanation
Auto Optimize is a functionality that allows Delta Lake to automatically compact small data files of Delta tables. This can be achieved during individual writes to the Delta table.




Auto optimize consists of 2 complementary operations:

- Optimized writes: with this feature enabled, Databricks attempts to write out 128 MB files for each table partition.

- Auto compaction: this will check after an individual write, if files can further be compacted. If yes, it runs an OPTIMIZE job with 128 MB file sizes (instead of the 1 GB file size used in the standard OPTIMIZE)




Study materials from our exam preparation course on Udemy:

Lecture

---

# Question 55

## Question
A data engineer from a global logistics company needs to share specific datasets and analysis notebooks with an external analytics vendor, who is a Databricks client. The data is stored as Delta tables in Unity Catalog, and the vendor does not have access to the company Databricks account.




What is the most effective and secure way to share the data and notebooks with the external vendor?

## Options
- A. Share the Delta tables and notebooks using Delta Sharing. (Correct)
- B. Share the Delta tables using Delta Sharing, and grant access to each notebook via its built-in collaboration feature. 
- C. Share the Delta tables using Delta Sharing, and publish the notebooks as HTML pages programmatically. 
- D. Share the Delta tables using Delta Sharing, and send all the notebooks together in a single DBC file. 

## Explanation
Databricks-to-Databricks Delta Sharing enables secure, open, and real-time sharing of tables, notebooks, volumes, and ML models with other Databricks clients. This does not require them to have access to the same Databricks account or workspace. With Unity Catalog, the company can ensure fine-grained access control and governance. This approach is efficient, scalable, and adheres to enterprise-grade security standards.

---

# Question 56

## Question
What is the primary purpose of Lakehouse Federation in data architecture?

## Options
- A. To optimize storage costs by compressing data 
- B. To enable direct querying across multiple data sources without migrating data (Correct)
- C. To create backups of data stored in Databricks 
- D. To migrate all data into Databricks for centralized processing 

## Explanation
Lakehouse Federation allows users and applications to run queries across diverse data sources—such as data lakes, warehouses, and databases—without requiring the physical migration of data into Databricks. This reduces data duplication, lowers latency, and streamlines access, enabling a unified query experience across distributed environments.

---

# Question 57

## Question
A data engineer has an existing Databricks job and wants to manage it using Databricks Asset Bundles. They want to use the Databricks CLI to get the YAML definition of the job and download its referenced artifacts.




Which of the following commands allows the data engineer to achieve this?

## Options
- A. databricks bundle clone job --existing-job-id 
- B. databricks bundle get job --existing-job-id 
- C. databricks bundle download job --existing-job-id 
- D. databricks bundle generate job --existing-job-id (Correct)

## Explanation
The correct command is `databricks bundle generate`, because it allows the data engineer to generate bundle configuration for a resource that already exists in your Databricks workspace. This process generates a YAML definition of a job, pipeline, app, or dashboard and automatically downloads any artifacts it references, such as notebooks.

---

# Question 58

## Question
Given the following query on the Delta table customers on which Change Data Feed is enabled:



```

- spark.read
-         .option("readChangeFeed", "true")
-         .option("startingVersion", 0)
-         .table("customers")
-         .filter(col("_change_type").isin(["update_postimage"]))
-     .write
-         .mode(“overwrite”)
-         .table("customers_updates")
```





Which statement describes the results of this query each time it is executed?

## Options
- A. Newly updated records will be appended to the target table. 
- B. Newly updated records will overwrite the target table. 
- C. The entire history of updated records will be appended to the target table at each execution, which leads to duplicate entries. 
- D. The entire history of updated records will overwrite the target table at each execution. (Correct)

## Explanation
Reading table’s changes, captured by CDF, using spark.read means that you are reading them as a static source. So, each time you run the query, all table’s changes (starting from the specified startingVersion) will be read.




The query in the question then writes the data in mode “overwrite” to the target table, which completely overwrites the table at each execution.




Study materials from our exam preparation course on Udemy:

Lecture

Hands-on

---

# Question 59

## Question
How does Automatic Liquid Clustering determine which columns to use as clustering keys in a Unity Catalog-managed Delta table?

## Options
- A. It leverages advanced sampling strategies to randomize column selection after uniformly balancing data across all files. 
- B. It automatically determines optimal clustering keys based on the type and order of column definition in the schema. 
- C. It intelligently selects clustering keys from predefined clustering columns specified during table creation. 
- D. It leverages Predictive Optimization to choose optimal clustering keys based on observed query behavior. (Correct)

## Explanation
Automatic Liquid Clustering in Databricks is a feature designed to automatically optimize the physical layout of data in Delta tables based on the access patterns and metadata statistics. It leverages Predictive Optimization, which uses query behavior analytics to select clustering keys dynamically.

---

