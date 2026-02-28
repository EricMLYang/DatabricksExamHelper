# Databricks 認證準備資訊



Databricks Certified Data Engineer Professional ( 3星 )

<https://www.databricks.com/learn/certification/data-engineer-professional> 



## \[簡介\]

- 這不是一張「專家級」**認證，證明你**不只是「會用」Databricks，而是能「精通」

- 需要有能力在 Databricks 平台上，建立、優化並維護一個「真正能上線營運 (Production-grade)」**的數據系統。官方**強烈建議**至少有**一年以上實際經驗再來考。

---

###  需要會的關鍵能力

- 全面評估從「設計」到「部署」的整個數據工程生命週期能力。

#### 1\. 核心重點：建立可靠的數據管線 (ETL)

- **懂設計：** 你要能設計出**安全、可靠、又省錢**的數據處理流程 (ETL)。

- **懂處理：** 能用 **Python** 和 **SQL** 這兩個主要語言，處理來自各種不同地方的「複雜」或「髒」的資料。

- **懂架構：** 必須熟悉 **Medallion Architecture** ，也就是 Databricks 推薦的「銅、銀、金」資料分層處理方法。



#### 2\. 必備工具：熟悉 Databricks

你必須對 Databricks Lakehouse 平台的核心功能瞭若指掌：

- **Delta Lake**

- **Unity Catalog：** 這是「資料治理」工具。管理資料權限、看資料血緣 (data lineage)、確保數據安全。

- **Auto Loader：** 「自動載入器」，當有新檔案丟進雲端儲存時，它能自動、有效率地幫你讀取資料。

- **Lakeflow Pipelines (可能指 DLT)：** 這是建立「穩定」數據管線的工具 (例如 Delta Live Tables)，它能自動化處理很多麻煩事。

- **Compute & Jobs：** 知道如何設定「運算資源」(Cluster)，包含 **Serverless (無伺服器)** 模式，並使用「工作 (Jobs)」來排程執行你的數據任務。



#### 3\. 進階能力：維運、優化、自動化

這就是「專家」和「新手」的差別：

- **效能調校 (Optimization)：** 你要會讓系統跑得快，知道如何優化查詢、管理儲存。

- **系統管理 (Governance)：** 除了 Unity Catalog，還要懂「綱要管理 (Schema Management)」(當資料欄位變動時怎麼辦)，以及「可觀測性 (Observability)」(系統出包時，你找得到問題出在哪)。

- **處理即時資料 (Streaming)：** 不只會處理「一批一批」的資料 (Batch)，也要會處理「即時進來」的串流資料。

- **專業部署 (DevOps & CI/CD)：** 你不能只在筆記本 (Notebook) 上手動執行。

   - 你要知道如何「編排工作流程」(Orchestration)，讓任務 A 跑完再跑 B。

   - **理解 CI/CD**，也就是讓程式碼的測試和上版「自動化」。

   - 用 **CLI** (命令列)、**REST API** 或 **Asset Bundles** 來部署你程式碼。

---

## \[考試內容\]

1. Developing Code for Data Processing using Python and SQL – 22%

2. Data Ingestion & Acquisition – 7%

3. Data Transformation, Cleansing, and Quality – 10%

4. Data Sharing and Federation – 5%

5. Monitoring and Alerting – 10%

6. Cost & Performance Optimisation – 13%

7. Ensuring Data Security and Compliance – 10%

8. Data Governance – 7%

9. Debugging and Deploying – 10%

10. Data Modelling – 6%

## \[考試方式\]

- 計分題數：59 (選擇題)

- 120 分鐘、線上、不允許使用輔助工具

- 語言：英語、日語、巴西葡萄牙語、韓語

- 註冊費：200 美元

- 先決條件：無，但強烈建議接受相關培訓

- 有效期限：2 年

- 非計分內容：考試可能包含非計分題，用於收集統計資料以供將來使用。這些項目不會在表格中列出，也不會影響您的分數。考試時間已預留額外時間以涵蓋這些內容



## 