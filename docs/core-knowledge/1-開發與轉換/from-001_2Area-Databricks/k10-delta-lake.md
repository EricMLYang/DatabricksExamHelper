---
tags:
  - databricks
---
# Delta Lake

- But why did Armbrust create Delta Lake? He created it to address the limitations of Apache Spark’s file synchronization. Specifically, he wanted to handle large-scale data operations and needed robust transactional support

![CleanShot 2025-03-15 at 08.34.57@2x.png](./Delta%20Lake-assets/CleanShot%202025-03-15%20at%2008.34.57@2x.png)



近期因為在研究 Databricks 上的分析 Code，如果真有客戶想在地端應用的話，應該要怎麼做到變動最小化，因為一樣結果的程式要維護多套其後續一致性會變的很難維持，\
\
開始拆解 Databricks, 其底層的組合越挖越多，這些東西在雲端的 Databricks 服務因為包裝的太好，所以不太會去接觸到，但要在地端部署的話，我想這些組成都要開始去更深入理解才行，以下一些筆記：\
\
\- Databricks 上的 PySpark Code 要可以應用在地端，只要把核心的運算 - Spark (+ Python for pySpark), 跟核心的儲存 - Delta Lake, 在地端安裝即可，當然 IO 相關的 Code 應該要把不同儲存環境的資訊 Config 化，另寫一些介面來維持彈性\
\
\- 當數據量大，需要多台電腦來處理時，雲端 Databricks 的優勢就顯現出來，因為我們開始必須自己管理運算和儲存資源，幾個 Node 下 Spark 也許還管理的了，但 Delta Lake 需要的儲存層，可能就必須要部署成多 Node 的檔案管理服務，從這開始讓我開始感到雲端服務真的是有其方便性， 包含地端 job 就必須自己另外寫排程去串\
\
\- 當看到這裡，就會開始好奇是否有其他方案的可能性，因此發現 Lakehouse 的相關技術架構五花八門，但其實很多都有一點歷史了，不會像前端或 AI 工具這樣層出不窮



Lakehouse 就是 Warehouse + Data Lake 的結合，想解決傳統資料倉儲在大量多變數據的擴展和進階運算不足，以及 Data Lake 本質上不可靠的性質，

其中 Databricks 就是這領域很獨特的優質服務，其 Delta Lake + Spark 方案希望讓企業可以很便利的進行各種大量數據的管理跟進階分析，



另一個雲端倉儲代表是 Snowflake，這是雲端大數據資料倉儲代表，雖然分析上比較侷限於傳統Query 模式，但是可串接多種雲、支持多數據源的特性還是非常好用，其儲存用 Iceberg，一個更類似傳統 SQL Table 的 Storage Layer\
\
\- Delta Lake 與 Spark 因為 Databricks 設計的關係而強綁定，但這強綁定對於只需要 Spark 單一分析引擎的團隊來說會單純很多; Iceberg 可以配合多種大數據處理引擎 ( Query Base, Spark，到更即時串流的都可以），但他們實體數據層配合 parquet 都可以運作的很好，Parquet 本質上就是一個被特別優化過的檔案，並存在雲端的 Objective storage，所以  open table format (Delta Lake 和 Iceberg) + 實體儲存檔案 ( Parquet) +  實體儲存層 ( cloud storage ) 就是 Lakehouse 的重要基礎，可以進行大量數據的類 SQL Table 處理(EX: ACID)



\-Parquet 的 column-oriented layout，以及 Row group  > Column Chunk > Page > Page Metadata + Value 的層次設計，以及 Column Chunk 本身因為數據同質性高所產生的高效能，讓其在大數據扮演重要角色



以上的底層細節要再一一去釐清，一方面位自架設方案鋪路，一方面可以減少 Databricks 雲端成本暴漲的意外







## **\[Parquet File layout\]**

![image 113.png](./Delta%20Lake-assets/image%20113.png)

![image 114.png](./Delta%20Lake-assets/image%20114.png)

- **The Parquet file structure is as follows:**

   - **File:  Header, Footer, Data Block.**

   - **Header:  details that indicate the file is in Parquet format**

   - **Data Block: Row Groups that logically combine various rows within the file**

   - **Row Groups: consist of columns present in the file**

   - **Column:  Value are stored as Aages.**

   - **Pages: the most granular data elements within Parquet**

   - **Footer:  consists of metadata of row groups and columns.**

      - **includes stats like min/max values for data skipping.**

### Does each row group contain all columns?   Yes.

In Delta Lake tables (built on Parquet format), each **row group** typically contains **all columns** for its subset of rows. A row group is essentially a horizontal slice of the table:

- Suppose you have a table with **100 columns** and 1 million rows.

- Delta Lake might divide your table into several row groups (for example, each row group with 100,000 rows).

- **Each row group** will contain data for **all 100 columns**, organized as separate column chunks.

---

#### **How much data is in each page; how many pages in row group?**

- A **column chunk** within a row group is further divided into multiple **pages**.  

- A **page** is typically around 8KB to 1MB (usually defaulting to around 1MB, though configurable).

- The number of pages per column chunk (and hence per row group) depends on:

   - Total data volume.

   - Compression ratio.

   - Data type and encoding.

**Typical example:**

Suppose we have one column chunk (`salary` column):

- **Column chunk size**: \~1 MB (uncompressed).

- **Page size**: \~128 KB per page (typical default size, adjustable by configuration).

Then:

- You might have approximately **10 pages** per column chunk (each \~100KB compressed, totaling 1 MB).

For **100 columns** within one row group:

- Each column chunk might have multiple pages (ranging from a few KBs to hundreds of KBs per page).

- A typical Parquet page usually stores roughly 10,000 to 100,000 values, depending on compression, encoding, and data size.

---

### **Summarized Example Scenario**:

- **Table**: 1 million rows, 100 columns.

- **Row Groups**: 10 groups (each with 100,000 rows).

- **Column Chunks**: Each row group has 100 column chunks (one per column).

- **Pages per Column Chunk**: \~5-20 pages per chunk, depending on data compression.

- **Data per Page**: Typically around 10,000\~100,000 individual data values (often optimized to \~100KB each page, though this varies)





## \[ DeltaLog - Transaction Log\]

- The Delta Lake transaction log (also known as DeltaLog) is a sequential record of every transaction performed on a Delta Lake table since its creation.

- it is at the core of its important features, including ACID transactions, scalable metadata handling, and time travel.

- Main goal of the transaction log is to enable multiple readers and writers to operate on a given version of a dataset file simultaneously and to provide additional information,

### Action

- These actions are recorded in the transaction log entries *(\*.json*) as ordered\\

- Atomic units known as commits. Each commit is written as a JSON file

- This is similar to how the Git source control system tracks changes as atomic commits.

- File starting with *0000000000000000000\.json*. 

- Delta Lake will generate additional JSON files in ascending numerical order when make changes( next commit - *0000000000000000001\.json*、 *0000000000000000002\.json)*

![CleanShot 2025-03-15 at 08.49.12@2x.png](./Delta%20Lake-assets/CleanShot%202025-03-15%20at%2008.49.12@2x.png)

![CleanShot 2025-03-15 at 08.56.50@2x.png](./Delta%20Lake-assets/CleanShot%202025-03-15%20at%2008.56.50@2x.png)



- In Delta Lake, each Parquet file is written **exactly once** and is immutable after creation. This is a fundamental aspect of the Delta Lake architecture

- Each transaction (write operation) creates a new JSON log file in sequence

### Action Performance

- Append

   -  avoid hight frequency write small data into delta table is very important

- Why insert/update/delete operations are less efficient

   1. **Immutable files**: Since Parquet files are immutable, Delta Lake can't directly modify records in place

   2. **How updates/deletes actually work**:

      - Delta Lake identifies files containing records to modify

      - It marks these files as "removed" in the transaction log

      - It writes new Parquet files with updated data

      - This is effectively "copy-on-write" - entire files are rewritten for changes

   3. **Performance impact**:

      - More transaction log entries

      - More file churn (new files created, old files marked for deletion)

      - Increased file count until compaction occurs

      - Potentially fragmented data

- Best practices for handling updates/deletes:

   1. **Batch modifications**: Collect multiple updates/deletes into batches when possible

   2. **Use merge commands**: The `MERGE INTO` operation is more efficient for multiple changes than individual updates

   3. **Schedule regular optimization**: Run `OPTIMIZE` more frequently on tables with many updates/deletes

   4. **Consider partitioning strategy**: Well-designed partitioning can limit the impact of updates to specific partitions

   5. **Update frequency planning**: Design your data pipeline to minimize the need for frequent updates/deletes

### Read Table

- reads a Delta table will iterate through all transaction log to “compile” the current state of the table.

- The sequence of events when reading a file is as follows:

   1. **The transaction log files are read first.**

   2. **The data files are read based on the log files.**

- *Checkpoint file*

   - Once the Delta Lake writer has made the commits to the transaction log, it will save a *checkpoint file* in Parquet format in the *\_delta_log* folder.

   - The Delta Lake writer will continue to generate a new checkpoint every 10 commits. EX: *000010\.checkpoint.parquet*

![CleanShot 2025-03-15 at 09.11.01@2x.png](./Delta%20Lake-assets/CleanShot%202025-03-15%20at%2009.11.01@2x.png)

## \[**Delta Sharing**\]

Data sharing is a common use case in business. For example, a mining company might want to securely share IoT information from its massive mining truck engines with the manufacturer for preventative maintenance and diagnostic purposes. A thermostat manufacturer might want to securely share HVAC data with a public utility to optimize the power grid load on high-usage days. However, in the past, implementing a secure, reliable data sharing solution was very challenging, and required expensive, custom development.

*Delta Sharing* is an open source protocol for securely sharing large datasets of Delta Lake data. It allows users to securely share data stored in Amazon S3, ADLS, or GCS. With Delta Sharing, users can directly connect to the shared data, using their favorite toolsets like Spark, Rust, Power BI, etc., without having to deploy any additional components. Notice that the data can be shared across cloud providers, without any custom development.