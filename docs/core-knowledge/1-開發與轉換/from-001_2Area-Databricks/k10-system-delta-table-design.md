---
tags:
  - vms
  - data-platform
  - databricks
---
# **System - Delta Table Design** 

## \[ Best Practice\]

### **Star Schema** ( [Doc. link](https://www.databricks.com/blog/five-simple-steps-for-implementing-a-star-schema-in-databricks-with-delta-lake?utm_source=chatgpt.com), )

- Most data warehouse developers are very familiar with the ever-present star schema

- 5 step:

   1. Use Delta Tables to create your fact and dimension tables

   2. Use Liquid Clustering to provide the best file size

   3. Use Liquid Clustering on your fact tables

   4. Use Liquid Clustering on your larger dimension table’s keys and likely predicates

   5. Leverage Predictive Optimization to maintain tables and gather statistics

- Feature tables are like a dimension tables ?

   - main different is dimension table is a description of fact table, but feature table take part of fact table data to transformance to another format

   - Star Schema Example :

![image 100.png](./System%20-%20Delta%20Table%20Design%20-assets/image%20100.png)

![image 101.png](./System%20-%20Delta%20Table%20Design%20-assets/image%20101.png)



### **Schema Evolution**

- Start with a **Main Table** (Fact Table) and Reference Tables (Dimension Tables)

- Design your schema with future changes in mind. Delta Lake allowing you to add, delete, or modify columns without rewriting the entire table.



### Liquid Clustering

- for dynamic data layout optimization, improving query performance and reducing maintenance overhead

- replaces traditional partitioning and Z-ordering

- enabled on a table by specifying the **CLUSTER BY** command when creating the table

   - `CREATE EXTERNAL TABLE taxidb.tripDataClustered ``CLUSTER BY`` (VendorId) LOCATION '/mnt/datalake/book/chapter05/YellowTaxisLiquidClusteringDelta' AS SELECT * FROM taxiDb.tripData LIMIT 1000;`

- particularly beneficial for tables with high cardinality columns, skewed data distribution, or changing access patterns

- Liquid clustering is not compatible with partitioning or ZORDER BY, and requires Databricks Runtime 13.2 and above to run. Additionally, it may require regular scheduling of OPTIMIZE jobs to ensure data is properly clustered.



### OPTIMIZE

- The ` OPTIMIZE your_table`  rewrites data files to improve data layout for Delta tables.

- For tables with liquid clustering enabled, `OPTIMIZE` rewrites data files to group data by liquid clustering keys. 



### **Predictive optimization** ([doc.1 link](https://docs.databricks.com/en/optimizations/predictive-optimization.html), [doc. 2 link](https://www.databricks.com/blog/predictive-optimization-automatically-delivers-faster-queries-and-lower-tco))

- Predictive optimization is a feature that runs VACUUM and OPTIMIZE for you, allowing you to focus on other tasks.

- This feature is enabled by setting the enableDeletionVectors table property in the DLT table definition.



### **OTHERS**

- Hundreds of columns might be fine, but thousands could impact performance

- **Column order:** Place frequently queried columns earlier in the schema for potential performance gains.

- 



## **\[ 統一  vs  分表 \]**

- Design:

   - 初期先用統一表簡化數據存儲與管理

   - 隨數據規模與業務增長，對高頻數據切出專表

   - 提前設計好數據分區與訪問層架構，讓切出專表過程可以平滑過渡

- **統一管理：**

   - 數據存儲在一張統一的 Delta Table 中。

   - 方便整體數據的統計分析，減少表的數量。

   - 可能因表過於龐大影響查詢性能

- **統一表的欄位定義**：

   - 包含 vehicle_id、timestamp、subsystem_type、data_key、data_value 等欄位。

- **分表管理：**

   - 為每個子系統建立獨立的 Delta Table

   - 針對不同子系統優化結構，提高查詢效率

   - 增加維護成本，跨子系統分析需要聯合查詢



## **\[ 分區與分表的區別 \]**

- **分區（Partitioning）：**

   - 在同一張表內進行數據的物理存儲劃分

   - 提高大表的查詢性能，避免全表掃描。

   - 不等於設置另一張表。

- **分表：**

   - 將數據邏輯上分開存放到多張表中。

   - 適合子系統業務完全獨立的情況。

   - 增加了表的數量，導致需要更多的維護和管理。

#### **從統一表切出專表的策略**

- **實施方式：**

   - **設置統一表：**

      - 初期將所有數據存儲在統一表中，簡化管理。

   - **監控查詢負載：**

      - 當特定子系統的查詢需求變高時，考慮切出專表。

   - **切出專表的步驟：**

      - 建立專表，從統一表遷移數據。

      - 更新應用層邏輯，確保查詢不受影響。

- **執行上的挑戰與解決方案：**

   - **數據一致性與同步：**

      - 在數據遷移期間，暫時停止對統一表的更新。

      - 統一配置數據接收邏輯，確保新數據進入正確的表。

   - **查詢邏輯切換的影響：**

      - 使用抽象的數據訪問層，隱藏底層數據存儲結構變化。

#### **拆出專表與設置分區的比較**

- **效果類似但應用場景不同：**

   - **拆出專表：**

      - 適合某些子系統有極高查詢需求或特殊處理邏輯。

      - 可單獨優化，性能隔離。

   - **設置分區：**

      - 適合查詢量適中，子系統數據關聯性高的情況。

      - 簡化管理，降低維護成本。

- **建議策略：**

   - 初期採用分區設置簡化管理。

   - 根據業務增長和查詢負載，逐步拆出高頻子系統的專表。

## \[ 數據對齊策略 \]

### **1\. 統一表與專表的欄位結構設計**

#### **統一表的欄位設計**

統一表用於存儲所有子系統的數據，需包含以下幾類欄位：

1. **主鍵欄位**：

   - \*\*`vehicle_id`\*\*（車輛 ID）：標識車輛，唯一標識每輛車的數據。

   - \*\*`timestamp`\*\*（時間戳）：數據記錄的時間，用於時間序列對齊。

2. **子系統識別欄位**：

   - \*\*`subsystem_type`\*\*（子系統類型）：標識數據來自哪個子系統（例如 VCU、BMS、PCU）。

   - \*\*`subsystem_id`\*\*（子系統 ID，可選）：進一步標識具體的子系統（適用於一輛車有多個相同子系統的情況）。

3. **數據值欄位**：

   - \*\*`data_key`\*\*（數據名稱）：標識數據的類型，例如 "battery_voltage"（電壓）、"motor_speed"（馬達轉速）。

   - \*\*`data_value`\*\*（數據值）：存儲具體的數據值。

4. **元數據欄位**（可選）：

   - \*\*`data_quality_flag`\*\*（數據質量標記）：標識該條數據的可靠性（如是否有缺失或異常）。

#### **專表的欄位設計**

專表用於特定子系統（如 BMS、PCU）數據的高效查詢，可以針對該子系統的數據特性進行優化。

1. **主鍵欄位**：

   - \*\*`vehicle_id`\*\*（車輛 ID）。

   - \*\*`timestamp`\*\*（時間戳）。

2. **子系統特定欄位**：

   - 為該子系統設計專用的結構化欄位，例如：

      - BMS 表：`battery_voltage`, `battery_temperature`, `battery_current`。

      - PCU 表：`motor_speed`, `torque`, `inverter_temperature`。

### **2\. 數據時間序列的對齊方法**

數據從不同子系統以非同步方式到達，需要對時間序列進行對齊，以下是實現方法：

#### **2\.1. 基於時間戳的對齊邏輯**

1. **選擇基準時間間隔**：

   - 根據業務需求選擇時間間隔（例如 1 秒、5 秒、1 分鐘），用於將數據聚合到統一的時間軸上。

2. **對數據進行插值或補插**：

   - 當某些子系統的數據沒有在基準時間點到達時，可以進行插值補全。例如：

      - 使用前後兩條數據進行線性插值。

      - 如果不能插值，則用最近的數據（Last Observation Carried Forward, LOCF）。

3. **同步多個子系統數據**：

   - 使用 JOIN 或 Window 函數，根據 `timestamp` 和 `vehicle_id` 匹配多個子系統數據。

#### **2\.2. 統一處理時間序列的 Pipeline**

1. **標準化數據時間軸**：將所有數據按照基準時間進行分桶（Bucketing）

2. **對缺失數據進行標記**：

   - 為每個子系統數據添加標記，標識哪些時間段數據缺失，後續分析時可以自動處理。

---

### **3\. 優化時間序列對齊的性能**

1. **索引與分區**：

   - 為統一表與專表設置分區（Partition）和 Z-Order Clustering，根據 `vehicle_id` 和 `timestamp` 優化存取性能。

2. **分層處理**：

   - 使用兩級處理流程：

      - **第一級**：將所有數據對齊到統一表，完成基本時間序列聚合。

      - **第二級**：對專表數據進行深度處理（如補插或進一步分析）。

3. **實時與批量結合**：

   - 使用 Delta Table 的 **流批一體化** 功能，實現數據即時處理與定期對齊的結合。

## \[ **分區的概念** \]

分區（Partitioning）並不等於設置另一張表，而是一種優化數據存儲與查詢的方式，特別是在處理大數據時。分區是在**同一張表內進行數據的物理存儲劃分**，以提高性能和效率。

---

### **分區的概念**

在 **Delta Table** 中，分區是將一張表的數據按照某個或多個欄位的值，劃分成邏輯上獨立的子集合，這些子集合在底層存儲為獨立的文件或目錄。

- **分區不是另一張表**，而是同一張表的數據在存儲層的組織方式。

- 查詢時，分區能幫助 Spark 或其他引擎快速定位需要的數據，避免全表掃描。

---

### **分區的具體設置方式**

#### **1\. 在 Delta Table 中使用分區**

假設我們的統一表 `unified_table` 需要按車輛 ID（`vehicle_id`）和日期（`date`）進行分區。

##### **示例建表語句：**

```sql
CREATE TABLE unified_table (
    vehicle_id STRING,
    timestamp TIMESTAMP,
    subsystem_type STRING,
    data_key STRING,
    data_value DOUBLE,
    date DATE
)
USING DELTA
PARTITIONED BY (date);
```

- **`PARTITIONED BY (date)`** 指定了按 `date` 字段分區。

- 當查詢只針對某個日期的數據時，Spark 會自動過濾其他分區，僅掃描相關日期的數據，極大提高性能。