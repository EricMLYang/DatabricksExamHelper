# Question 1

## Question
A data engineering team manages Unity Catalog tables with predictive optimization enabled. They are unsure which operations are automatically performed on these tables as part of predictive optimization’s automatic maintenance.




Which of the following operations is Not handled automatically by predictive optimization for enabled tables?

## Options
- A. VACUUM 
- B. ANALYZE 
- C. OPTIMIZE 
- D. ZORDER (Correct)

## Explanation
Z-order indexing is not handled automatically by predictive optimization for Unity Catalog tables. While predictive optimization can automatically manage the OPTIMIZE, ANALYZE, and VACUUM tasks to maintain table performance, it does not execute ZORDER, and any Z-ordered files are ignored when predictive optimization runs.

---

# Question 2

## Question
The data engineering team is using the LOCATION keyword for every new Delta Lake table created in the Lakehouse.




Which of the following describes the purpose of using the LOCATION keyword in this case ?

## Options
- A. The LOCATION keyword is used to set a default schema and checkpoint location for the created Delta Lake tables. 
- B. The LOCATION keyword is used to configure the created Delta Lake tables as external tables. (Correct)
- C. The LOCATION keyword is used to configure the created Delta Lake tables as managed tables. 
- D. The LOCATION keyword is used to define the created Delta Lake tables in an external database. 

## Explanation
External (unmanaged) tables are tables whose data is stored in an external storage path by using a LOCATION clause.




Study materials from our exam preparation course on Udemy:

Lecture (Associate course)

Hands-on (Associate course)

---

# Question 3

## Question
A data engineer wanted to create the job ‘process-sales’ using Databricks REST API.




However, they sent by mistake 2 POST requests to the endpoint ‘api/2.2/jobs/create’




Which statement describes the result of these requests ?

## Options
- A. 2 jobs will be created in the workspace, but the second one will be renamed to “process-sales (1)” 
- B. The second job will overwrite the previous one created using the first request. 
- C. 2 jobs named “process-sales” will be created in the workspace, but with different job_id (Correct)
- D. Only the first job will be created in the workspace. The second request will fail with an error indicating that a job named “process-sales” is already created. 

## Explanation
Sending the same job definition in multiple POST requests to the endpoint ‘api/2.2/jobs/create’ will create a new job for each request, but each job will have its own unique job_id.




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 4

## Question
Which of the following describes the minimal permissions a data engineer needs to modify permissions of an existing cluster?

## Options
- A. “Can Restart” privilege on the cluster 
- B. “Can Manage” privilege on the cluster (Correct)
- C. Cluster creation allowed + “Can Restart” privileges on the cluster 
- D. Cluster creation allowed + “Can Manage” privileges on the cluster 

## Explanation
You can configure two types of cluster permissions:




1- The ‘Allow cluster creation’ entitlement controls your ability to create clusters.




2- Cluster-level permissions control your ability to use and modify a specific cluster. There are four permission levels for a cluster: No Permissions, Can Attach To, Can Restart, and Can Manage. The table lists the abilities for each permission:









Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 5

## Question
A junior data engineer creates a Databricks job with 15 notebook tasks, each performing the same data validation logic on 15 different tables. Each task depends on the completion of the previous one, making the workflow long and difficult to maintain.




What would be a more efficient and scalable solution for this use case?

## Options
- A. Use a foreach task to run the same validation notebook for each table in parallel, passing the table name as a parameter (Correct)
- B. Schedule 15 separate jobs instead of having multiple tasks in one job 
- C. Configure the 15 notebook tasks to run in parallel, each with a separate cluster configuration 
- D. Combine all table validations into one large notebook and loop through all tables sequentially 

## Explanation
A more efficient and scalable solution in this scenario is to use a For Each task. The For Each task allows you to run a nested task in a loop, passing different parameters to each iteration. In this case, the data engineer can pass each table name as a parameter, running the same validation notebook for all tables. This approach reduces maintenance overhead, and allows the validations to run concurrently to avoid sequential dependencies, making the workflow faster and easier to manage.

---

# Question 6

## Question
The data engineering team has a dynamic view with following definition:



```

- CREATE VIEW students_vw AS
- SELECT * FROM students
- WHERE
-     CASE
-         WHEN is_member("instructors") THEN TRUE
-         ELSE is_active IS FALSE
-     END
```





Which statement describes the results returned by querying this view?

## Options
- A. Only members of the instructors group will see the records of all students no matter if they are active or not. While users that are not members of the specified group will only see the records of inactive students (Correct)
- B. Members of the instructors group will only see the records of active students. While users that are not members of the specified group will see null values for the records of inactive students 
- C. Only members of the instructors group will see the records of all students no matter if they are active or not. While users that are not members of the specified group will see null values for the records of inactive students 
- D. Members of the instructors group will only see the records of active students. While users that are not members of the specified group will only see the records of inactive students. 

## Explanation
Only members of the instructors group will have full access to the underlying data since the WHERE condition will be True for every record. On the other hand, users that are not members of the specified group will only be able to see records of students with active status = false.




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 7

## Question
A data engineer is noticing that a large UC-managed Delta table (≈750GB) has become slow when applying intensive CDC feeds.




Which of the following actions should the data engineer take to improve the performance?

## Options
- A. Enable deletion vectors on the table and apply Z-order indexing on the primary keys. 
- B. Partition the table and apply Z-order indexing on the primary keys. 
- C. Partition the table and apply liquid clustering using the primary keys. 
- D. Enable deletion vectors on the table and apply liquid clustering using the primary keys. (Correct)

## Explanation
Since Change Data Capture (CDC) involves processing updates and deletions, to improve the performance of a large Delta table experiencing slow CDC feeds, the data engineer should enable deletion vectors on the table and apply liquid clustering using the primary keys.




Enabling deletion vectors allows Delta to efficiently track and manage rows that are deleted or updated without requiring full rewrites of the underlying files, which significantly reduces the overhead for CDC operations. Applying liquid clustering on the CDC merging keys organizes the data physically based on these keys, ensuring that related records are colocated and minimizing the amount of data scanned during updates and deletions. Together, these optimizations help maintain high ingestion and query performance, reduce latency for CDC workloads, and make the table more manageable at scale.

---

# Question 8

## Question
The data engineering team has a secret scope named “prod-scope” that contains sensitive secrets in a production workspace.




A data engineer in the team is writing a security and compliance documentation, and wants to explain who could use the secrets in this secret scope. 




Which of the following roles is able to use the secrets in the specified secret scope ?

## Options
- A. Workspace Administrators 
- B. Users with READ or MANAGE permission on the secret scope 
- C. Secret creators 
- D. All the mentioned roles are able to use the secrets in the secret scope (Correct)

## Explanation
Administrators*, secret creators, and users granted access permission can use Databricks secrets. The secret access permissions are as follows:



- 

MANAGE - Allowed to change ACLs, and read and write to this secret scope.
- 

WRITE - Allowed to read and write to this secret scope.
- 

READ - Allowed to read this secret scope and list what secrets are available.




Each permission level is a subset of the previous level’s permissions (that is, a principal with WRITE permission for a given scope can perform all actions that require READ permission).




* Workspace administrators have MANAGE permissions to all secret scopes in the workspace.







Reference:




https://docs.databricks.com/security/auth-authz/access-control/secret-acl.html#permission-levels




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 9

## Question
A data engineer is responsible for managing a bronze Delta Lake table in Unity Catalog. As part of maintaining data integrity and enforcing governance policies, the engineer wants to restrict modifications to the table by disabling UPDATE and DELETE operations.




Which of the following commands can the data engineer use to enforce this restriction?

## Options
- A. ALTER TABLE bronze_raw SET TBLPROPERTIES ('delta.disableUpdate' = true, 'delta.disableDelete' = true); 
- B. ALTER TABLE bronze_raw SET TBLPROPERTIES ('delta.disableUpdate' = true);

ALTER TABLE bronze_raw SET TBLPROPERTIES ('delta.disableDelete' = true); 
- C. ALTER TABLE bronze_raw SET TBLPROPERTIES ('delta.preventModification' = true); 
- D. ALTER TABLE bronze_raw SET TBLPROPERTIES ('delta.appendOnly' = true); (Correct)

## Explanation
The data engineer can disable UPDATE and DELETE operations on the bronze Delta Lake table by setting the table to append-only mode, which prevents modifications while still allowing inserts. The correct command for this is:

`ALTER TABLE bronze_raw SET TBLPROPERTIES ('delta.appendOnly' = true);`




`delta.appendOnly` is the recognized Delta Lake property to disallow updates and deletes, whereas the other options are not valid Delta table properties.

---

# Question 10

## Question
Two junior data analysts are collaborating on a data analytics project using a Databricks notebook. Currently, they are relying on the built-in notebook versioning feature within Databricks to manage changes and maintain some level of version control. While this approach works for small-scale, individual work, the team faces challenges when multiple people are editing notebooks simultaneously. Observing this, a senior data engineer suggested that they consider using Git folders for source control instead of relying solely on the notebook’s built-in versioning system.




Which of the following reasons could explain why Git folders are recommended over Databricks notebook versioning for collaborative team work?

## Options
- A. Git folders support creating and managing branches for development work, which helps prevent accidental overwrites and allows multiple team members to work on features simultaneously. (Correct)
- B. Git folders provide AI-generated code suggestions by analyzing the contributions and coding patterns of other team members, helping developers write compatible code. 
- C. Git folders ensure that the team always has the latest notebook version by automatically synchronizing all project notebooks without requiring any commits or pushes. 
- D. Git folders support resolving merge conflicts automatically, making it faster to integrate contributions from different team members without constant manual intervention. 

## Explanation
The main reason Git folders are recommended over Databricks notebook versioning for collaborative teamwork is that Git folders support creating and managing branches for development work. In practice, each team member creates their own Git folder linked to the same remote Git repository and works within their personal branch, so changes can be made independently without impacting others. This approach prevents accidental overwrites and allows multiple team members to work on features simultaneously, enabling proper version control and structured collaboration.

---

# Question 11

## Question
A data engineer has noticed the comment `# Databricks notebook source` on the first line of each Databricks Python file’s source code pushed to Github.




Which of the following explain the purpose of this comment ?

## Options
- A. This comment establishes the Python files as Databricks notebooks (Correct)
- B. This comment add the Python file to the search index in Databricks workspace 
- C. This comment is used for Python auto-generated documentation 
- D. This comment makes it easier for humans to understand the source of the generated code from Databricks 

## Explanation
You can convert Python, SQL, Scala, and R scripts to single-cell notebooks by adding a comment to the first cell of the file:




`# Databricks notebook source`




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 12

## Question
The data engineering team has a large Delta Lake table named ‘user_posts’ which is partitioned over the ‘year’ column. The table is used as an input streaming source in a streaming job. The streaming query is displayed below with a blank:



```

- spark.readStream
-        .table("user_posts")
-        ________________
-        .groupBy("post_category", "post_date")
-        .agg(
-            count("psot_id").alias("posts_count"),
-            sum("likes").alias("total_likes"))
-     .writeStream
-        .option("checkpointLocation", "dbfs:/path/checkpoint")
-        .table("psots_stats")
```





They want to remove previous 2 years data from the table without breaking the append-only requirement of streaming sources.




Which option correctly fills in the blank to enable stream processing from the table after deleting the partitions?

## Options
- A. .window("year", "INTERVAL 2 YEARS") 
- B. .option("ignoreDeletes", True) (Correct)
- C. .withWatermark("year", "INTERVAL 2 YEARS") 
- D. .option("ignoreDeletes", “year”) 

## Explanation
Partitioning on datetime columns can be leveraged when removing data older than a certain age from the table. For example, you can decide to delete previous years data. In this case, file deletion will be cleanly along partition boundaries.




However, if you are using this table as a streaming source, deleting data breaks the append-only requirement of streaming sources, which makes the table no more streamable. To avoid this, you can use the ignoreDeletes option when streaming from this table. This option enables streaming processing from Delta tables with partition deletes.

`option("ignoreDeletes", True)`




Study materials from our exam preparation course on Udemy:

Lecture

Hands-on

---

# Question 13

## Question
The data engineering team needs to share a dataset containing Social Security numbers with an external analytics vendor. They want to ensure that the original values are not exposed, while still allowing the vendor to perform matching operations. To achieve this, they implemented the following code:



```

- df_masked = df_original.withColumn("ssn_hash", sha2("ssn", 256))
- df_masked.write.saveAsTable("masked_analytics")
```





However, this code still exposes the original values.




Which of the following statements correctly explains the reason for this behavior?

## Options
- A. The `sha2` function is not available in PySpark. The table masked_analytics should be created in Spark SQL using a CTAS statement. 
- B. The code adds a new column to df_masked instead of overriding the original value. They need to use `withColumn("ssn", sha2("ssn", 256))` instead. (Correct)
- C. The `sha2` function doesn’t apply to numerical values. They need to use `withColumn("ssn_hash", sha1("ssn"))` instead. 
- D. The code adds a new column to df_masked without dropping the original value. It must be followed by a `.drop("ssn_hash")` command. 

## Explanation
In PySpark, the withColumn function creates a new column or replaces an existing column in a DataFrame based on the given expression. The code in this question adds a new column (ssn_hash) to df_masked but does not remove or overwrite the original ssn column, so the original Social Security numbers are still present in the table.




To properly mask the data, the team should either overwrite the ssn column with the hash (`withColumn("ssn", sha2("ssn", 256))`) or drop the original column after hashing.

---

# Question 14

## Question
Which of the following Databricks CLI commands allows a data engineer to list all runs of a job that completed successfully?

## Options
- A. databricks jobs list-runs --job-id <job-id> --success-only 
- B. databricks jobs list-runs --job-id <job-id> --completed 
- C. databricks jobs list-runs --job-id <job-id> --success 
- D. databricks jobs list-runs --job-id <job-id> --completed-only (Correct)

## Explanation
The correct Databricks CLI command that allows a data engineer to list all runs of a job that completed successfully is:




`databricks jobs list-runs --job-id <job-id> --completed-only.`




The --completed-only parameter is the proper flag to include only completed runs in the results; otherwise, the command will list both active and completed runs.

---

# Question 15

## Question
A data engineer has the following Databricks Asset Bundle (DAB) project:



```

- resources:
-     apps:
-         bookstore_app:
-             name: "bookstore_demo"
-             source_code_path: ../src/bookstore
-  
-     volumes:
-         bookstore_volume:
-             name: "bookstore"
-             catalog_name: demo_catalog
-             schema_name: demo_schema
-             grants:
-                 - principal: ${resources.apps.bookstore_app.id}
-                 privileges:
-                     - READ_VOLUME
-                     - WRITE_VOLUME
```





Which of the following correctly describes the result of deploying this DAB project?

## Options
- A. It deploys a Volume bookstore_volume and a Service Principal bookstore_app with read and write access to the Volume. 
- B. It generates an error because the reference `${resources.apps.bookstore_app.id}` is incorrect and should instead be `${resources.apps.bookstore_demo.id}`. 
- C. It deploys a Catalog demo_catalog, a Schema demo_schema, a Volume bookstore_volume, and a Databricks App bookstore_app with access to the volume using a 3-level namespace. 
- D. It deploys a Databricks App bookstore_app and a Volume bookstore_volume, and grants the Service Principal associated with the Databricks App read and write access to the Volume. (Correct)

## Explanation
When this Databricks Asset Bundle (DAB) project is deployed, it successfully creates two resources: a Databricks App named bookstore_app (with the display name “bookstore_demo”) and a Volume named bookstore_volume within the specified catalog demo_catalog and schema demo_schema.




The configuration includes a grant statement that correctly references the app’s identifier using `${resources.apps.bookstore_app.id}`, which ensures that the Service Principal associated with the deployed Databricks App is automatically given both READ_VOLUME and WRITE_VOLUME privileges on the created volume. This means the app’s service identity can read from and write data to the bookstore volume as part of its operational workflow.

---

# Question 16

## Question
Which of the following is Not a valid Delta Lake File Statistics ?

## Options
- A. The minimum and maximum value in each of the first 32 columns 
- B. The total number of records in the added data file. 
- C. The average value for each of the first 32 columns (Correct)
- D. The number of null values for each of the first 32 columns 

## Explanation
Delta Lake automatically captures statistics in the transaction log for each added data file of the table. These statistics indicate per file:
- 

Total number of records
- 

Minimum value in each column of the first 32 columns of the table
- 

Maximum value in each column of the first 32 columns of the table
- 

Null value counts for in each column of the first 32 columns of the table




The average value in the columns is Not part of Delta Lake File Statistics




Study materials from our exam preparation course on Udemy:

Lecture

Hands-on

---

# Question 17

## Question
Which of the following Spark functions is NOT valid for extracting the date from a timestamp column?

## Options
- A. TO_DATE(ts) 
- B. date_part('day', ts) (Correct)
- C. CAST(ts AS DATE) 
- D. date_trunc('day', ts) 

## Explanation
The valid Spark functions for extracting the date from a timestamp column are:

- 

CAST(ts AS DATE) – This converts a timestamp to a date by dropping the time portion.
 Example: '2025-10-21 15:42:30' becomes '2025-10-21'.



- 

TO_DATE(ts) – This extracts only the date portion from a timestamp.
 Example: '2025-10-21 15:42:30' becomes '2025-10-21'.



- 

date_trunc('day', ts) – This function truncates a timestamp to the start of the specified unit.
 Example: If ts = '2025-10-21 15:42:30', then date_trunc('day', ts) returns '2025-10-21 00:00:00'.


In contrast, date_part can return a numerical component (e.g., day = 21) rather than converting to a full date type.

---

# Question 18

## Question
A data engineer created a new table along with a comment using the following query:



```

- CREATE TABLE payments
- COMMENT "This table contains sensitive information"
- AS SELECT * FROM bank_transactions
```





Which of the following commands allows the data engineer to review the comment of the table?

## Options
- A. DESCRIBE EXTENDED payments (Correct)
- B. SHOW COMMENTS payments 
- C. SHOW TBLPROPERTIES payments 
- D. DESCRIBE TABLE payments 

## Explanation
`DESCRIBE TABLE EXTENDED` or simply `DESCRIBE EXTENDED` allows you to show none only table’s comment, but also columns’ comments, and other custom table properties

---

# Question 19

## Question
Given the following query:



```

- spark.table("stream_sink")
-         .filter("recent = true")
-         .dropDuplicates(["item_id", "item_timestamp"])
-     .write
-         .mode ("overwrite")
-         .table("stream_data_stage")
```





Which statement describes the result of executing this query ?

## Options
- A. An incremental job will overwrite the stream_sink table by those deduplicated records from stream_data_stage that have been added since the last time the job was run. 
- B. A batch job will overwrite the stream_data_stage table by deduplicated records calculated from all “recent” items in the stream_sink table (Correct)
- C. An incremental job will overwrite the stream_data_stage table by those deduplicated records from stream_sink that have been added since the last time the job was run. 
- D. A batch job will overwrite the stream_data_stage table by those deduplicated records from stream_sink that have been added since the last time the job was run. 

## Explanation
Reading a Delta table using spark.table() function means that you are reading it as a static source. So, each time you run the query, all records in the current version of the ‘stream_sink’ table will be read, filtered and deduplicated.




There is no difference between spark.table() and spark.read.table() function. Actually, spark.read.table() internally calls spark.table().




The query in the question then writes the data in mode “overwrite” to the ‘stream_data_stage’ table, which completely overwrites the table at each execution.




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 20

## Question
A data engineer is working with a large Delta Lake table that has deletion vectors enabled. Considering the underlying mechanics of Delta Lake and its handling of updates, which of the following statements most accurately describes how update operations behave within this table directory?

## Options
- A. Update operations are ignored entirely when deletion vectors are enabled. 
- B. Each update triggers a complete rewrite of all Parquet files that contain the affected data. 
- C. The update operation directly modifies the existing Parquet files in place without creating new files. 
- D. The affected rows are flagged as deleted in the deletion vectors, and the updated rows are written as new Parquet files. (Correct)

## Explanation
When deletion vectors are enabled in a Delta Lake table, update operations do not rewrite entire Parquet files or modify them in place. Instead, Delta Lake leverages deletion vectors to efficiently track which rows are soft deleted without physically removing them from the data files. During an update, the rows that need modification are marked as deleted within the deletion vectors, while the updated versions of those rows are written as new data files. This approach allows Delta Lake to perform updates and deletes more efficiently by avoiding costly file rewrites, improving performance especially for large datasets, while still maintaining ACID transaction guarantees and data consistency.

---

# Question 21

## Question
A data engineering team created a new workspace, which is automatically enabled for Unity Catalog. They observed that it contains a default workspace catalog and a default schema.




Which of the following statements correctly describes the default privileges that workspace users have on this catalog and schema?

## Options
- A. Workspace users have `ALL PRIVILEGES` on the default schema, along with `USE CATALOG` on the workspace catalog. 
- B. Workspace users primarily have `CREATE TABLE`, `CREATE VOLUME`, `CREATE FUNCTION`, and `USE SCHEMA` privileges on the default schema, along with `USE CATALOG` on the workspace catalog. (Correct)
- C. Workspace users do not have any privileges on the default schema by default, unless the workspace administrator explicitly grants them the necessary permissions. 
- D. Workspace users have `ALL PRIVILEGES` on the workspace catalog. 

## Explanation
When a new workspace is created with Unity Catalog enabled, Databricks automatically provisions a default workspace catalog and a default schema, and assigns users a set of basic privileges that allow them to perform common data engineering tasks within that schema.




Workspace users have the USE CATALOG privilege on the workspace catalog, and specific privileges on the default schema, including:
- 

CREATE TABLE
- 

CREATE VOLUME
- 

CREATE FUNCTION
- 

CREATE MATERIALIZED VIEW
- 

CREATE MODEL
- 

USE SCHEMA

---

# Question 22

## Question
Which of the following establishes a Python file as a notebook in Databricks ?

## Options
- A. The import of the dbutils.notebook module in the file’s source code 
- B. The comment ‘# Databricks notebook source’ on the first line of the file’s source code (Correct)
- C. The creation of a spark session using SparkSession.builder.getOrCreate() in the file’s source code 
- D. The magic command %databricks on the first line of the file’s source code 

## Explanation
You can convert Python, SQL, Scala, and R scripts to single-cell notebooks by adding a comment to the first cell of the file:




`# Databricks notebook source`




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 23

## Question
For production Databricks jobs, which of the following cluster types is recommended to use?

## Options
- A. On-premises clusters 
- B. Job clusters (Correct)
- C. All-purpose clusters 
- D. Production clusters 

## Explanation
Job Clusters are dedicated clusters for a job or task run. A job cluster auto terminates once the job is completed, which saves cost compared to all-purpose clusters.

In addition, Databricks recommends using job clusters in production so that each job runs in a fully isolated environment.




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 24

## Question
Which of the following statements correctly describes assertions in unit testing?

## Options
- A. An assertion is a command that shows the differences between the current version of a code unit and the most recently edited version 
- B. An assertion is a command that logs failed units of code in production for later debugging and analysis 
- C. An assertion is a boolean expression that checks if assumptions made in the code remain true while development (Correct)
- D. An assertion is a boolean expression that checks if two code blocks are integrated logically and interacted as a group. 

## Explanation
Assertions are boolean expressions that enable you to test the assumptions you have made in your code. They are used in unit tests to check if certain assumptions remain true while you're developing your code.




`assert func() == expected_value`




Study materials from our exam preparation course on Udemy:

Lecture

Hands-on

---

# Question 25

## Question
A junior data engineer is using the `%sh` magic command to run some legacy code. A senior data engineer has recommended refactoring the code instead.




Which of the following could explain why a data engineer may need to avoid using the %sh magic command ?

## Options
- A. %sh restarts the Python interpreter. This clears all the variables declared in the notebook 
- B. %sh executes shell code only on the local driver machine which leads to significant performance overhead. (Correct)
- C. %sh can not access storage to persist the output 
- D. All the listed reasons explain why %sh may need to be avoided 

## Explanation
Databricks support the %sh auxiliary magic command to run shell code in notebooks. This command runs only on the Apache Spark driver, and not on the worker nodes.




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 26

## Question
Which of the following users have the ability to create and manage Delta Shares in Unity Catalog?




Choose 2 answers:

## Options
- A. Users with CREATE SHARE privilege for the metastore (Correct)
- B. Metastore admins (Correct)
- C. Workspace admins 
- D. Users with MANAGE privilege for the metastore 
- E. Account admins 

## Explanation
The users who have the ability to create and manage Delta Shares in Unity Catalog are Metastore admins and Users with CREATE SHARE privilege for the metastore, as these roles explicitly have the necessary permissions to create and manage Delta Shares.

---

# Question 27

## Question
The data engineering team has a table ‘orders_backup’ that was created using Delta Lake’s SHALLOW CLONE functionality from the table ‘orders’. Recently, the team started getting an error when querying the ‘orders_backup’ table indicating that some data files are no longer present.




Which of the following correctly explains this error ?

## Options
- A. The VACUUM command was run on the orders table (Correct)
- B. The OPTIMIZE command was run on the orders table 
- C. The OPTIMIZE command was run on the orders_backup table 
- D. The VACUUM command was run on the orders_backup table 

## Explanation
With Shallow Clone, you create a copy of a table by just copying the Delta transaction logs.

That means that there is no data moving during Shallow Cloning.

Running the VACUUM command on the source table may purge data files referenced in the transaction log of the clone. In this case, you will get an error when querying the clone indicating that some data files are no longer present.




Study materials from our exam preparation course on Udemy:

Lecture (Associate course)

---

# Question 28

## Question
A data engineer at a global bank manages a Delta Lake table customer_accounts with columns:

customer_id, name, account_number, credit_card. They want to apply a mask on the credit_card column so that only analysts in the Fraud Detection Department can view the actual values. To achieve this, they implemented the following user-defined function:



```

- CREATE FUNCTION card_mask(credit_card STRING)
- RETURN CASE WHEN is_account_group_member('FraudDetectionDept') THEN credit_card
-         ELSE '****-****-****-****' END;
```





Which command can the data engineer use to apply this function as a column mask to the table?

## Options
- A. ALTER TABLE customer_accounts SET MASK card_mask ON (credit_card); 
- B. SET MASK card_mask ON TABLE customer_accounts TO COLUMN credit_card; 
- C. ALTER TABLE customer_accounts SET MASK card_mask; 
- D. ALTER TABLE customer_accounts ALTER COLUMN credit_card SET MASK card_mask; (Correct)

## Explanation
To ensure that only analysts in the Fraud Detection Department can view the actual credit card numbers while others see masked values, the data engineer should apply the masking function directly to the specific column in the Delta Lake table. The correct SQL command to achieve this is:




`ALTER TABLE customer_accounts ALTER COLUMN credit_card SET MASK card_mask;`




This command modifies the existing credit_card column by associating it with the card_mask function, which conditionally reveals or masks the credit card data based on the user’s group membership.

---

# Question 29

## Question
Given the following Structured Streaming query:



```

- (spark.table("orders")
-         .withColumn("total_after_tax", col("total")+col("tax"))
-     .writeStream
-         .option("checkpointLocation", checkpointPath)
-         .outputMode("append")
-         ._____________
-         .table("new_orders")
- )
```





Fill in the blank to make the query executes a micro-batch to process data every 2 minutes

## Options
- A. trigger(”2 minutes") 
- B. trigger(processingTime=”2 minutes") (Correct)
- C. processingTime(”2 minutes") 
- D. trigger(once=”2 minutes”) 

## Explanation
In Spark Structured Streaming, in order to process data in micro-batches at a user-specified intervals, you can use the processingTime trigger method. This allows you to specify a time duration as a string. By default, it’s “500ms”.




Study materials from our exam preparation course on Udemy:
- 

Lecture (Associate course)

---

# Question 30

## Question
A data governance team notices that different business units have implemented their own versions of masking policies on the same columns. How does Unity Catalog improve this situation?

## Options
- A. It provides a single source of truth for masking functions, preventing inconsistent exposure. (Correct)
- B. It allows teams to disable masking for testing purposes, providing more flexibility during development. 
- C. It allows teams to leverage data object privileges to mask data differently for different groups. 
- D. It lets each team manage its version of masking rules, increasing control over data privacy. 

## Explanation
Unity Catalog improves this situation by providing a single source of truth for masking functions, ensuring that all business units use consistent and centrally governed masking policies across the same data columns.




In Unity Catalog, masking logic can be implemented and managed as user-defined functions (UDFs), which encapsulate the masking rules in reusable and standardized code. This means that instead of each team creating its own version of a masking rule—potentially leading to inconsistent or insecure data handling—a single, validated UDF can be registered and referenced by all teams. As a result, Unity Catalog enforces consistent data governance, enhances compliance, and reduces the risk of inconsistent exposure of sensitive information across the organization.

---

# Question 31

## Question
Which of the following statements best describes Auto Loader?

## Options
- A. Auto loader monitors a source location, in which files accumulate, to identify and ingest only new arriving files with each command run. While the files that have already been ingested in previous runs are skipped. (Correct)
- B. Auto loader allows cloning a source Delta table to a target destination at a specific version. 
- C. Auto loader enables efficient insert, update, deletes, and rollback capabilities by adding a storage layer that provides better data reliability to data lakes. 
- D. Auto loader allows applying Change Data Capture (CDC) feed to update tables based on changes captured in source data. 

## Explanation
Auto Loader incrementally and idempotently processes new data files as they arrive in cloud storage and load them into a target Delta Lake table.




Study materials from our Associate exam preparation course on Udemy:
- 

Hands-on
- 

Lecture (Associate course)

---

# Question 32

## Question
A multinational company wants to share sales analytics data with both its internal Databricks teams located in a different country and external consulting partners. Internal teams access the data via Databricks-to-Databricks sharing (D2D), while external partners use the open Delta Sharing (D2O) protocol.




In this scenario, how does authentication differ between the D2D sharing and the D2O protocol?

## Options
- A. Databricks-to-Databricks sharing (D2D) and open Delta Sharing (D2O) both use the same authentication method, so there is no difference. 
- B. Databricks-to-Databricks sharing (D2D) relies on OIDC federation, whereas open Delta Sharing (D2O) requires authentication via bearer tokens. 
- C. Databricks-to-Databricks sharing (D2D) relies on unified login with single sign-on (SSO), whereas open Delta Sharing (D2O) uses external login with OIDC federation. 
- D. Databricks-to-Databricks sharing (D2D) uses built-in authentication with no token exchange, whereas open Delta Sharing (D2O) requires external authentication via bearer tokens or OIDC federation. (Correct)

## Explanation
Databricks-to-Databricks sharing (D2D) uses built-in authentication with no token exchange, allowing internal teams to access shared data seamlessly within the Databricks environment, whereas open Delta Sharing (D2O) requires external authentication, typically via bearer tokens or OIDC federation, to securely grant external partners access to the data.

---

# Question 33

## Question
Which of the following source locations can no longer be used to store init scripts?

## Options
- A. Workspace files 
- B. Cloud storage 
- C. DBFS (Correct)
- D. Volumes 

## Explanation
As of recent Databricks updates, DBFS (Databricks File System) can no longer be used to store init scripts. Databricks has deprecated the use of DBFS root (/dbfs/) for storing cluster init scripts due to reliability and security concerns.




Init scripts can now only be stored in the following locations:
- 

Volumes
- 

Cloud storage
- 

Workspace files

---

# Question 34

## Question
“A declarative ETL framework for implementing incremental data processing, while minimizing operational overhead and maintaining table dependencies and data quality.”




Which of the following technologies is being described above?

## Options
- A. ETL 
- B. DAB 
- C. DBU 
- D. LDP (Correct)

## Explanation
The technology described is LDP (Lakeflow Declarative Pipelines). LDP is a declarative ETL framework specifically designed to handle incremental data processing efficiently while minimizing operational overhead. It supports automatic orchestration that ensures dependencies between tables are properly managed, and maintains high data quality throughout the pipeline.




Unlike traditional ETL pipeline development that often requires procedural coding and manual orchestration, LDP allows users to define data transformations and workflows declaratively, making pipelines easier to maintain, scale, and monitor.




Note: Databricks has recenlty open-sourced this solution, integrating it into the Apache Spark ecosystem under the name Spark Declarative Pipelines (SDP).

---

# Question 35

## Question
In Spark UI, which of the following SQL metrics is displayed on the query’s details page?

## Options
- A. Succeeded Jobs 
- B. Query execution time 
- C. Query duration 
- D. Spill size (Correct)

## Explanation
In Spark UI, the query’s details page displays general information about the query execution time, its duration, the list of associated jobs, and the query execution DAG.




In addition, it shows SQL metrics in the block of physical operators. The SQL metrics can be useful when we want to dive into the execution details of each operator. For example, “number of output rows” can answer how many rows are output after a Filter operator, “Spill size” which is the number of bytes spilled to disk from memory in the operator.

---

# Question 36

## Question
The data engineering team has a Delta Lake table named ‘daily_activities’ that is completely overwritten each night with new data received from the source system.




For auditing purposes, the team wants to set up a post-processing task that uses Delta Lake Time Travel functionality to determine the difference between the new version and the previous version of the table. They start by getting the current table version via this code:



```

- current_version = spark.sql("SELECT max(version) FROM (DESCRIBE HISTORY daily_activities)").collect()[0][0]
```





Which of the following queries can be used by the team to complete this task ?

## Options
- A. ```

- SELECT * FROM daily_activities
- MINUS
- SELECT * FROM daily_activities AS VERSION = {current_version-1}
``` 
- B. ```

- SELECT * FROM daily_activities
- UNION
- SELECT * FROM daily_activities AS VERSION = {current_version-1}
``` 
- C. ```

- SELECT * FROM daily_activities
- INTERSECT
- SELECT * FROM daily_activities AS VERSION = {current_version-1}
``` 
- D. ```

- SELECT * FROM daily_activities
- EXCEPT
- SELECT * FROM daily_activities@v{current_version-1}
``` (Correct)

## Explanation
Each operation that modifies a Delta Lake table creates a new table version. You can use history information to audit operations or query a table at a specific point in time using:



- 

Version number
```

- SELECT * FROM my_table@v36
- SELECT * FROM my_table VERSION AS OF 36
```




- 

Timestamp
```

- SELECT * FROM my_table TIMESTAMP AS OF "2019-01-01"
```





Using the EXCEPT set operator, you can get the difference between the new version and the previous version of the table




Study materials from our exam preparation course on Udemy:
- 

Hands-on
- 

Lecture (Associate course)
- 

Hands-on (Associate course)

---

# Question 37

## Question
An IoT company processes live sensor readings from thousands of devices using a streaming pipeline. Occasionally, devices send corrupted or incomplete events that fail schema validation. The engineering team must ensure that production analytics dashboards, which rely on clean data, continue to update in real time. However, the corrupted records should still be captured for later investigation, using minimal computing resources.




What should the engineers do to meet these requirements?

## Options
- A. Filter out corrupted events in the main real-time stream and write only valid records to the production tables. Create a separate lightweight process that periodically reads and stores the corrupted messages for analysis. (Correct)
- B. Include all data, valid or not, in the main stream and use a flag to mark corrupted records. 
- C. Merge both valid and invalid data into the same Delta table and use downstream queries to apply data quality rules to exclude invalid entries from dashboards. 
- D. Add retry logic to the main stream so that it attempts to reprocess corrupted messages until they succeed. 

## Explanation
The engineers should filter out corrupted or incomplete events from the main real-time streaming pipeline and write only the valid records to the production analytics tables, ensuring that dashboards continue to update accurately and without delay. At the same time, they should implement a separate lightweight process that periodically collects and stores the corrupted messages for later investigation, such as debugging or auditing.




This design maintains the integrity and performance of the real-time analytics system by preventing invalid data from affecting dashboards, while still preserving all incoming data for offline analysis, and it does so efficiently without overloading computing resources or complicating the main pipeline.




Study materials from our exam preparation course on Udemy:
- 

Hands-on

---

# Question 38

## Question
A data engineer in an international school has implemented the following PySpark code:



```

- from pyspark.sql.window import Window
- from pyspark.sql.functions import avg, col
-  
- window_spec = Window.partitionBy("student_id").orderBy("exam_date")\
-                 .rowsBetween(Window.unboundedPreceding, Window.currentRow)
-  
- df_new = df_student_results.withColumn("avg_score", avg("score").over(window_spec))
```





Which of the following correctly describes what this code does?

## Options
- A. It adds a column showing the overall average score of each student, ordered by exam date. 
- B. It adds a column showing the cumulative average score of each exam from the first enrolled student to and including the current student. 
- C. It adds a column showing the cumulative average score of each student from their first exam up to and including the current exam. (Correct)
- D. It adds a column showing the overall average score of each exam, regardless of student. 

## Explanation
The PySpark code uses a Window function to calculate a cumulative or running average score for each student.
- 

Window.partitionBy("student_id"): This divides the data into partitions (groups) based on the student_id. The average calculation will be performed independently within each student's set of results.
- 

.orderBy("exam_date"): This sorts the rows within each student's partition by the exam_date (oldest to newest). This is crucial for a running calculation.
- 

.rowsBetween(Window.unboundedPreceding, Window.currentRow): This defines the frame for the window.
- 

Window.unboundedPreceding means the frame starts at the very first row in the current student's partition (the first exam).
- 

Window.currentRow means the frame ends at the current row being processed (the current exam).
- 

This combination ensures that for any given row, the calculation includes all preceding rows and the current row, effectively defining a cumulative set of data.
- 

avg("score").over(window_spec): The avg("score") function is applied over the defined window_spec. Because the window is partitioned by student_id and is cumulative over exam_date, the result in the new avg_score column is the cumulative average score for that specific student up to that specific exam date.

---

# Question 39

## Question
A data engineer is configuring the follwoing Databricks Auto Loader stream to ingest JSON data from an S3 bucket:



```

- spark.readStream \
-      .format("cloudFiles") \
-      .option("cloudFiles.format", "json") \
-      .option("cloudFiles.schemaLocation", "s3://shop/checkpoints/orders")
-      .option("cloudFiles.schemaEvolutionMode", "_______________") \
-      .load("s3://shop/raw/orders/json/") \
-     .writeStream \
-      .option("checkpointLocation", "s3://shop/checkpoints/orders") \
-      .start("orders_table")
```





The pipeline should fail when new columns are detected in the incoming data, but those new columns should still be added to the schema so that subsequent runs can resume successfully with the updated schema. Existing columns must retain their data types.




Which option correctly fills in the blank to meet the specified requirement?

## Options
- A. addNewColumns (Correct)
- B. none 
- C. rescue 
- D. failOnNewColumns 

## Explanation
The `addNewColumns` mode is the default schema evolution behavior in Auto Loader. In this mode, when a new column is detected, the stream fails, but the new column is added to the schema. This allows the job to be restarted and continue processing with the updated schema. Importantly, existing columns' data types are not changed.

---

# Question 40

## Question
A data engineering team at an enterprise organization has recently completed the setup of a new Databricks Asset Bundle project. After successfully configuring the bundle with their CI/CD system, the team wants to ensure that future automated deployments to the production environment run smoothly and reliably.




In this scenario, which of the following commands should the CI/CD pipeline avoid rerunning during subsequent deployments?

## Options
- A. databricks bundle deploy 
- B. databricks bundle run 
- C. databricks bundle validate 
- D. databricks bundle init (Correct)

## Explanation
The CI/CD pipeline should avoid rerunning the databricks bundle init command during subsequent deployments because it is only used once to initialize a new Databricks Asset Bundle project by creating its configuration and structure. Re-running it could overwrite existing configurations or reset the project setup. In contrast, commands like databricks bundle validate, databricks bundle deploy, and databricks bundle run are safe and appropriate for repeated use in automated deployment pipelines to validate, deploy, and execute workflows as part of regular CI/CD operations.

---

# Question 41

## Question
A data engineer has implemented the following Auto Loader stream to incrementally ingest a large volume of JSON files from cloud storage:



```

- (spark.readStream.format("cloudFiles")
-         .option("cloudFiles.format", "json")
-         ____________________________
-         .load("/path/to/files")
- )
```


By default, Auto Loader infers the schema by sampling the first 50 GB or 1000 files it discovers. However, the data engineer wants to avoid re-sampling and reduce the cost of schema inference in subsequent runs, while still tracking schema changes over time.




Which option correctly fills in the blank to meet the specified requirement?

## Options
- A. .option("cloudFiles.schemaEvolutionMode", "addNewColumns") 
- B. .option("cloudFiles.schemaLocation", "/path/to/checkpoint") (Correct)
- C. .option("mergeSchema", true) 
- D. .option("checkpointLocation", "/path/to/checkpoint") 

## Explanation
The correct option to fill in the blank is .option("cloudFiles.schemaLocation", "/path/to/checkpoint"). This tells Auto Loader to store the inferred schema in the specified location so that subsequent runs do not need to re-sample the files, reducing the cost of schema inference while still allowing schema evolution to be tracked over time.

---

# Question 42

## Question
A data engineer in a call center needs to implement an SQL alert to track ticket volume and status changes. They want to set the alert based on multiple columns of the tickets table. The alert should be triggered when both of the following conditions are met:



- 

The number of new tickets exceeds 200.
- 

The number of tickets under processing exceeds 150.




Which of the following SQL queries correctly implements this alert logic?

## Options
- A. ```

- SELECT new_tickets, under_processing
- FROM (
-   SELECT
-     SUM(CASE WHEN status = 'new' THEN 1 ELSE 0 END) AS new_tickets,
-     SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) AS under_processing
-   FROM tickets
- ) statistics
- WHERE new_tickets > 200
- AND under_processing > 150
``` 
- B. ```

- SELECT new_tickets + under_processing
- FROM (
-   SELECT
-     SUM(CASE WHEN status = 'new' THEN 1 ELSE 0 END) AS new_tickets,
-     SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) AS under_processing
-   FROM tickets
- ) statistics
- WHERE new_tickets + under_processing > 350
``` 
- C. ```

- SELECT
-   SUM(CASE WHEN status = 'new' THEN 1 ELSE 0 END) AS new_tickets,
-   SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) AS under_processing
- FROM tickets
- WHERE new_tickets > 200
- AND under_processing > 150
``` 
- D. ```

- SELECT CASE
-   WHEN new_tickets > 200 AND under_processing > 150 THEN 1
-     ELSE 0
-   END
- FROM (
-   SELECT
-     SUM(CASE WHEN status = “new” THEN 1 ELSE 0 END) AS new_tickets,
-     SUM(CASE WHEN status = “in_progress” THEN 1 ELSE 0 END) AS under_processing
-   FROM tickets
- ) statistics
``` (Correct)

## Explanation
This query correctly calculates the sums of new and in-progress tickets in a subquery, and then uses a CASE statement to trigger the alert when both conditions are met (new_tickets > 200 AND under_processing > 150), which matches the intended alert logic.




Remember, alerts in Databricks can only evaluate a single field. That’s why we use a CASE WHEN expression to combine multiple conditions into one alert field.

---

# Question 43

## Question
Which of the following describes the minimal permissions a data engineer needs to view the metrics and Spark UI of an existing cluster?

## Options
- A. Cluster creation allowed + “Can Attach To” privileges on the cluster 
- B. “Can Manage” privilege on the cluster 
- C. “Can Attach To” privilege on the cluster (Correct)
- D. “Can Restart” privilege on the cluster 

## Explanation
You can configure two types of cluster permissions:




1- The ‘Allow cluster creation’ entitlement controls your ability to create clusters.




2- Cluster-level permissions control your ability to use and modify a specific cluster. There are four permission levels for a cluster: No Permissions, Can Attach To, Can Restart, and Can Manage. The table lists the abilities for each permission:








Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 44

## Question
Which of the following privileges is not included in the ALL PRIVILEGES permission?

## Options
- A. MANAGE (Correct)
- B. BROWSE 
- C. EXECUTE 
- D. MODIFY 

## Explanation
The privilege MANAGE is not included in the ALL PRIVILEGES permission. While ALL PRIVILEGES grants a comprehensive set of permissions such as EXECUTE, BROWSE, and MODIFY, it explicitly excludes MANAGE to prevent accidental data exfiltration or privilege escalation.




Remember, MANAGE allows a user to view and manage privileges, transfer ownership, drop, and rename an object. It is similar to object ownership, but holding the MANAGE privilege does not automatically grant all other privileges on the object, although the user can grant themselves additional privileges if needed.

---

# Question 45

## Question
A data engineer is using the following Auto Loader stream to incrementally ingest large JSON files. These files cause long micro-batch processing times and occasional memory issues:



```

- df = (spark.readStream
-             .format("cloudFiles")
-             .option("cloudFiles.format", "json")
-             _________________________________
-             .load("s3://project/source/"))
```





They want to process only a portion of the data per micro-batch, improving stability and keeping batch times predictable.




Which option correctly fills in the blank to process only 128 MB of data per micro-batch?

## Options
- A. .option(‘cloudFiles.maxBytesPerTrigger’, ‘128mb’) (Correct)
- B. .option(‘cloudFiles.maxDataPerTrigger’, ‘128mb’) 
- C. .option(‘triggerInterval’, ‘128mb’) 
- D. .option(‘batchSize’, ‘128mb’) 

## Explanation
In Auto Loader, `cloudFiles.maxBytesPerTrigger` controls the maximum amount of data to process in each micro-batch, allowing the stream to handle large files incrementally and keep batch processing times predictable.

---

# Question 46

## Question
Which of the following statements correctly describes the SQL/DataFrame tab in Spark UI?

## Options
- A. It presents an in-depth view of all stages, showing their dependencies, task execution times, shuffle read/write metrics, and the distribution of tasks across worker nodes, giving insight into stage-level performance. 
- B. It shows all RDDs and DataFrames that are cached or persisted in memory and on disk, along with their sizes, storage levels, and block locations, helping users monitor memory usage and optimize caching strategies. 
- C. It shows the executed operations, including their query plans, execution metrics, physical and logical plans, DAG visualizations, stage and task breakdowns, and performance statistics for monitoring and debugging. (Correct)
- D. It provides a list of all the Spark jobs that have been submitted, including details about their start and end times, status, associated stages, and task metrics, allowing users to drill down into individual task performance 

## Explanation
The SQL/DataFrame tab in Spark UI is specifically focused on Spark SQL and DataFrame operations for debugging, monitoring, and understanding complex workloads. It provides a detailed view of queries, including:
- 

Logical and physical query plans
- 

DAG visualizations of operations
- 

Metrics for execution stages and tasks
- 

Performance statistics for debugging and monitoring queries




The other options describe different tabs in Spark UI:
- 

Spark Jobs tab: It provides a list of all the Spark jobs that have been submitted, including details about their start and end times, status, associated stages, and task metrics, allowing users to drill down into individual task performance
- 

Stages tab: It presents an in-depth view of all stages, showing their dependencies, task execution times, shuffle read/write metrics, and the distribution of tasks across worker nodes, giving insight into stage-level performance.
- 

Storage tab: It shows all RDDs and DataFrames that are cached or persisted in memory and on disk, along with their sizes, storage levels, and block locations, helping users monitor memory usage and optimize caching strategies.

---

# Question 47

## Question
A data engineer has defined the following data quality constraint in a LDP pipeline:




`CONSTRAINT valid_id EXPECT (id IS NOT NULL) _____________`




Which clause correctly fills in the blank to immediately stop execution when a record violates this constraint?

## Options
- A. ON VIOLATION FAIL UPDATE (Correct)
- B. ON VIOLATION STOP 
- C. ON VIOLATION DROP ROW 
- D. ON VIOLATION FAIL PIPELINE 

## Explanation
The correct clause to fill in the blank is `ON VIOLATION FAIL UPDATE`, as this ensures that any record violating the `valid_id` constraint prevents the update from proceeding. This enforces strict data quality and prevents downstream processing of invalid records.




In this case, manual intervention is required before reprocessing. When a pipeline fails because of an expectation violation, you must decide how to handle the invalid data correctly before re-running the pipeline.




Note that this expectation causes a failure of a single flow and does not cause other flows in your pipeline to fail.




Study materials from our exam preparation course on Udemy:
- 

Hands-on

---

# Question 48

## Question
A data engineer is using the Query Profile in Databricks SQL to investigate a slow-performing SQL query. They want to find out which operations in the query are taking the most time.




Which section of the Query Profile highlights the most expensive operations in the query, helping to identify potential optimization opportunities?

## Options
- A. Top operators (Correct)
- B. Aggregated task time 
- C. Query status 
- D. Query wall-clock duration 

## Explanation
The correct answer is Top operators. In Databricks SQL, the Top operators section of the Query Profile highlights the most expensive operations within a query by showing which specific operations (such as joins, scans, or aggregations) are consuming the most time. This allows the data engineer to pinpoint performance bottlenecks and focus on optimizing the parts of the query that have the highest impact on overall execution time.

---

# Question 49

## Question
Which statement regarding checkpointing in Spark Structured Streaming is Not correct?

## Options
- A. Checkpointing allows the streaming engine to track the progress of a stream processing 
- B. Checkpoints stores the current state of a streaming job to cloud storage 
- C. Checkpointing with write-ahead logs mechanism ensure fault-tolerant stream processing 
- D. Checkpoints can be shared between separate streams (Correct)

## Explanation
Checkpoints cannot be shared between separate streams. Each stream needs to have its own checkpoint directory to ensure processing guarantees.




Study materials from our exam preparation course on Udemy:

Lecture (Associate course)

---

# Question 50

## Question
A data engineer is using Databricks REST API to send a GET request to the endpoint ‘api/2.1/jobs/runs/get’ to retrieve the run’s metadata of a multi-task job using its run_id.




Which statement correctly describes the response structure of this API call?

## Options
- A. Each task of this job run will have a unique job_id 
- B. Each task of this job run will have a unique run_id (Correct)
- C. Each task of this job run will have a unique orchestration_id 
- D. Each task of this job run will have a unique task_id 

## Explanation
Each task of this job run will have a unique run_id to retrieve its output with endpoint ‘api/2.1/jobs/runs/get-output’




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 51

## Question
A data engineer has an existing Databricks job and wants to manage it using Databricks Asset Bundles. They have already generated the YAML definition of the job and downloaded its referenced artifacts. However, they want to ensure that updates to the bundle's YAML will modify the existing job rather than creating a new job.




Which of the following commands allows the data engineer to achieve this?

## Options
- A. databricks bundle deployment match <bundle_job> <remote-job-id> 
- B. databricks bundle deployment link <bundle_job> <remote-job-id> 
- C. databricks bundle deployment mirror <bundle_job> <remote-job-id> 
- D. databricks bundle deployment bind <bundle_job> <remote-job-id> (Correct)

## Explanation
The correct command is `databricks bundle deployment bind <bundle_job> <remote-job-id>`, as this links the existing remote job to a defined resource in the Databricks Asset Bundle, ensuring that any updates to the bundle’s YAML definition will modify the linked job rather than creating a new one.

---

# Question 52

## Question
A data engineer uses the following SQL query:




`GRANT MODIFY ON TABLE employees TO hr_team`




Which of the following describes the ability given by the MODIFY privilege ?

## Options
- A. It gives the ability to modify data in the table 
- B. It gives the ability to add data from the table 
- C. All the listed abilities are given by the MODIFY privilege (Correct)
- D. It gives the ability to delete data from the table 

## Explanation
The MODIFY privilege gives the ability to add, delete, and modify data to or from an object.




Study materials from our exam preparation course on Udemy:
- 

Lecture
- 

Hands-on

---

# Question 53

## Question
A data engineer has the following logic to handle duplicates in Spark Structured Streaming:



```

- (spark.readStream
-        .table("bronze")
-        .filter("topic = 'orders'")
-        .select(F.from_json(F.col("value").cast("string"), schema).alias("v"))
-        .select("v.*")
-        .withWatermark("order_timestamp", "30 seconds")
-        .dropDuplicates(["order_id", "order_timestamp"]))
```





However, they notice that this logic is not sufficient to prevent duplicates for events that arrive later than the watermark threshold.




Which of the following code snippets can the data engineer include in a `foreachBatch` function to completely handle streaming duplicates?

## Options
- A. ```

- MERGE INTO orders_silver a
- USING microbatch b
- ON a.order_id=b.order_id AND a.order_timestamp=b.order_timestamp
- WHEN NOT MATCHED THEN INSERT *
``` (Correct)
- B. ```

- (spark.readStream
- .table("microbatch")
- .withWatermark("order_timestamp", "7 days")
- .dropDuplicates(["order_id", "order_timestamp"]))
``` 
- C. ```

- APPLY CHANGES INTO orders_silver a
- FROM STREAM(microbatch)
- KEYS (order_id, order_timestamp)
- SEQUENCE BY order_timestamp
- COLUMNS *
``` 
- D. ```

- COPY INTO orders_silver
- FROM microbatch
- DISTINCT ALL
- COPY_OPTIONS ('mergeSchema' = 'true');
``` 

## Explanation
In Spark Structured Streaming, dropDuplicates with a watermark only removes duplicates that arrive within the defined event-time threshold, for example, within 30 seconds of order_timestamp. However, any records arriving later than that threshold are considered “too late” and are not deduplicated by Spark’s in-memory state. To ensure complete deduplication (including very late-arriving data), the foreachBatch sink can use an idempotent write pattern with Delta Lake’s MERGE operation.




The MERGE INTO statement compares each micro-batch of incoming data (microbatch) with the target Delta table (orders_silver) based on unique keys (order_id and order_timestamp). It only inserts rows that do not already exist in the target table, preventing duplicates even across micro-batches or late arrivals. This combination of in-stream deduplication (for near-real-time performance) and MERGE-based deduplication (for completeness and correctness) provides an end-to-end reliable way to handle duplicates in streaming pipelines.




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 54

## Question
The data engineering team created a new Databricks job for processing sensitive financial data. A financial analyst asked the team to transfer the "Owner" privilege of this job to the “finance” group.




A junior data engineer that has the “CAN MANAGE” permission on the job is attempting to make this privilege transfer via Databricks Job UI, but it keeps failing.




Which of the following explains the cause of this failure?

## Options
- A. Having the “CAN MANAGE” permission is not enough to grant "Owner" privileges to a group. The data engineer must be the current owner of the job. 
- B. Groups can not be owners of Databricks jobs. The owner must be an individual user. (Correct)
- C. Having the “CAN MANAGE” permission is not enough to grant "Owner" privileges to a group. The data engineer must be a workspace administrator. 
- D. The "Owner" privilege is assigned at job creation to the creator and cannot be changed. The job must be re-created using the “finance” group’s credentials. 

## Explanation
A job cannot have a group as an owner. If you try to set a group as the owner of a job, you get the error “Groups can not be owners”




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 55

## Question
Which of the following commands prints the current working directory of a notebook?

## Options
- A. print(sys.path) 
- B. os.path.abspath() 
- C. os.environ['PYTHONPATH'] 
- D. %sh pwd (Correct)

## Explanation
The %sh magic command allows you to run shell code in a notebook.




The pwd is an acronym for print working directory.




Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 56

## Question
The data engineering team has a large Delta table named ‘user_messages’ with the following schema:




msg_id INT, user_id INT, msg_time TIMESTAMP, msg_title STRING, msg_body STRING




The msg_body field represents user messages in free-form text. The table has a performance issue when it’s queried with filters on this field.




Which of the following could explain the reason for this performance issue ?

## Options
- A. The table does not leverage file skipping because it's not optimized with Z-ORDER on the msg_body column. 
- B. The table does not leverage file skipping because Delta Lake statistics are not captured on columns of type STRING 
- C. The table does not leverage file skipping because Delta Lake statistics are uninformative for string fields with very high cardinality (Correct)
- D. The table does not leverage file skipping because it's not partitioned on the msg_body column. 

## Explanation
Delta Lake automatically captures statistics in the transaction log for each added data file of the table. By default, Delta Lake collects the statistics on the first 32 columns of each table. However, statistics are generally uninformative for string fields with very high cardinality (such as free text fields).




Calculating statistics on free-form text fields (like user messages, product reviews, etc) can be time consuming. So, you need to omit these fields from statistics collection by setting them later in the schema after the first 32 columns.




Study materials from our exam preparation course on Udemy:

Lecture

Hands-on

---

# Question 57

## Question
A data engineer is using a foreachBatch logic to upsert data in a target Delta table.




The function to be called at each new microbatch processing is displayed below with a blank:



```

- def upsert_data(microBatchDF, batch_id):
-     microBatchDF.createOrReplaceTempView("sales_microbatch")
-  
-     sql_query = """
-                 MERGE INTO sales_silver a
-                 USING sales_microbatch b
-                 ON a.item_id=b.item_id
-                     AND a.item_timestamp=b.item_timestamp
-                 WHEN NOT MATCHED THEN INSERT *
-                 """
-  
-     ________________
```





Which option correctly fills in the blank to execute the sql query in the function on a cluster with Databricks Runtime below 10.5 ?

## Options
- A. microBatchDF.sparkSession.sql(sql_query) 
- B. spark.sql(sql_query) 
- C. microBatchDF._jdf.sparkSession().sql(sql_query) (Correct)
- D. microBatchDF.sql(sql_query) 

## Explanation
Usually, we use spark.sq() function to run SQL queries. However, in this particular case, the spark session can not be accessed from within the microbatch process. Instead, we can access the local spark session from the microbatch dataframe.




For clusters with Databricks Runtime version below 10.5, the syntax to access the local spark session is:

`microBatchDF._jdf.sparkSession().sql(sql_query)`




For additional clarification, refer to the official Databricks documentation (Python syntax) at the following link: https://docs.databricks.com/aws/en/structured-streaming/delta-lake?language=Python#upsert-from-streaming-queries-using-foreachbatch 





Study materials from our exam preparation course on Udemy:

Hands-on

---

# Question 58

## Question
A data engineer is tasked with enabling analysts and data scientists to query tables stored in an external PostgreSQL database directly from Databricks, without moving or replicating the data. They plan to use Lakehouse Federation and Unity Catalog to set up a foreign catalog for seamless access to the external data.




What is the very first step the data engineer should take in this process?

## Options
- A. Configure a connection in Unity Catalog to securely connect to the PostgreSQL database, establishing the necessary credentials and network access. (Correct)
- B. Navigate to the account console as an account administrator to enable the option “Allow Delta Sharing with parties outside your organization” 
- C. Grant CREATE SHARE and CREATE RECIPIENT permissions on the metastore to the metastore administrators. 
- D. Configure an external location and storage credentials in Unity Catalog to securely connect to the PostgreSQL’s underlying storage. 

## Explanation
The very first step the data engineer should take is to configure a connection in Unity Catalog to securely connect to the PostgreSQL database, establishing the necessary credentials and network access. This is essential because before creating any foreign catalogs, Databricks needs a secure, authenticated connection to the external PostgreSQL database to allow seamless querying without moving the data.

---

# Question 59

## Question
A data engineer manages a Delta Lake table with liquid clustering enabled. They understand that liquid clustering operates incrementally, but they are unsure how to trigger the clustering operation when new data is ingested into the table.




Which of the following commands should be executed to cluster the newly added data?

## Options
- A. VACUUM 
- B. OPTIMIZE (Correct)
- C. ZORDER 
- D. ANALYZE 

## Explanation
To cluster the newly added data in a Delta Lake table with liquid clustering enabled, the data engineer should execute the OPTIMIZE command. OPTIMIZE triggers the clustering operation by physically reorganizing the data files to improve query performance.

---

