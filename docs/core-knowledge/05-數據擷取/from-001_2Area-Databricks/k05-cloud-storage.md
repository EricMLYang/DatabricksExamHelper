---
tags:
  - data-platform
---
# Cloud Storage

## **\[Row vs Columnar Storage\]**

![image 126.png](./Cloud%20Storage-assets/image%20126.png)

- in rwo-based approach, the data is stored row by row on the physical disk. When you execute a select query to retrieve the data, it reads the complete row from the disk. 

- This is beneficial in cases where the query wants to read all columns from the data.

- Analytical workloads generally consist of reading a few columns as aggregations or summarizations. Due to the nature of row-based storage, the query has to read all columns across many records, irrespective of the number of columns required by the query.

- For analytical queries, columnar storage helps quickly retrieve the data by scanning only those disk blocks where these columns are stored. Unlike row-based storage, the query does not have to scan the full record for a few specific columns. This approach enables faster data retrieval, especially in cases where the tables have hundreds of attributes and the query needs only a few columns. Also, as the data from the same columns are stored together, it is much easier to apply compression on the same data types, thus reducing the overall file size.

### **Storage-based Performance Optimization**

- Storage also enables the compute engines to retrieve the required result faster by reducing the data to be scanned. 

- It’s not only the compute engines that determine the performance, but also the underlying storage.

- The less data it scans, the less time it takes to fetch the result.

- Some file and table formats help to minimize the data that a query needs to scan for retrieving the results. 

- The process for minimizing that data is also known as data skipping or row skipping.

- There are different approaches to skip unwanted data, including:

   - **Partition or file pruning**: reducing the number of partitions or files that need to be scanned by the query

   - **Indexing and clustering**: fetching the exact records required by queries instead of scanning the whole table

   - **Maintaining column-level statistics:**  EX: min, max values for each column, help to scan only the relevant data blocks where required records would be present

## Lakehouse Storage Components

The lakehouse storage layer consists of three main components:

- **Cloud object storage for storing the data**

- **Open file formats for compressing data and support distributed processing**

- **Open table formats for providing the transactional capabilities and efficient data retrieval**



## \[ Cloud Object Storage\]

Cloud object storage services like Amazon S3 and Azure Blob Storage use a similar hierarchical structure, though with some key differences in terminology and implementation:

- Core Structure

   - **Object**: The fundamental storage unit (a file with its data and metadata)

   - **Container/Bucket**: A top-level namespace that holds objects

   - **Optional logical hierarchy**: Using prefixes or virtual folders

- AWS S3 Structure

   - **Buckets**: The top-level containers

   - **Objects**: Files stored with unique keys inside buckets

   - **Keys**: Unique identifiers for objects (e.g., "photos/2023/beach.jpg")

   - **Prefixes**: Portions of keys that create logical hierarchies (e.g., "photos/2023/")

   - **Metadata**: System and user-defined key-value pairs attached to objects

- Azure Blob Storage Structure

   - **Storage Account**: The top-level resource (container for all services)

   - **Containers**: Similar to S3 buckets, but with different naming rules

   - **Blobs**: Objects/files (equivalent to S3 objects)

   - **Virtual directories**: Similar to S3 prefixes, creating a logical hierarchy

![image 127.png](./Cloud%20Storage-assets/image%20127.png)



## \[**File Formats**\]

![image 128.png](./Cloud%20Storage-assets/image%20128.png)

### **Parquet (**[ASF documentation](https://oreil.ly/mM2TT)**)**

- Created in 2013, an open source file format that uses columnar storage

- Has been adopted by many organizations for big data workloads. 

- Much better compression ratios than CSV and JSON file formats

- Enhanced performance for handling complex data






