# 第一篇 - 什麼是 Lakehouse？



在進入一些技術或操作細節前，

我希望同仁先理解 Databricks 的出現是想解決什麼問題，

**因為操作 (How)** 是基礎，

但**概念 (Why)** 決定了技術上限，

**Lakehouse** 就是 Databricks 的 **Why**，

所以從「Lakehouse」簡介開始講起，

並很簡單的介紹競品與定位。



---



▋傳統架構的兩難：倉儲 vs. 湖泊

簡單來說 Lakehouse 是一種現代的資料平台架構，

它的出現是為了解決過去兩種傳統架構的根本性缺陷。

過去，企業在建構資料平台時，主要有兩種選擇，

#### Data Warehouse 或是 Data Lake。



▋資料倉儲概述 

#### 第一是資料倉儲 (Data Warehouse)

#### 專為 **BI 商業智慧** 和報表分析而設計，

**優點可**針對 BI 查詢優化，

支援 **ACID** 確保資料一致性與可靠性，

結構化、高品質的資料。

**但最致命缺點就是本質上還是用 SQL DB，**

**處理非結構化資料** (如影像、Logs、串流資料)的難度較高，

因此不適用於 AI / ML (機器學習) 工作。

**儲存與運算緊密耦合**，導致擴展彈性差且成本高昂。

採用「**Schema-on-Write**」(寫入時定義結構)，彈性低。



▋大數據興起 - Data Lake

#### 後來資料湖 (Data Lake) 盛行，

其彈性讓需求高漲的 AI / ML 分析便利很多，

儲存**所有類型**的原始資料，

可說是專為 AI / ML 和資料科學而生。

**彈性就是最大的好處了，**

採用「**Schema-on-Read**」(讀取時定義結構)，彈性極高，

支援所有資料格式 (結構化、半結構化、非結構化)，

**儲存與運算分離**，擴展性高、成本低 (使用 S3, ADLS 等雲端儲存)。

**但不支援 ACID 交易**，資料**可靠性差是致命缺點，**

BI 報表效能較差，

缺乏有效的資料管理和治理，

容易變成「**資料沼澤 (Data Swamp)**」。

---



### ▋Lakehouse：兩全其美的解決方案

最一開始，

企業被迫採用「倉儲 + 湖泊」的**混合架構**，

但這導致系統變得**極度複雜**，

資料在兩個系統中**重複儲存**、且管理困難。

**Lakehouse 架構的核心理念是：**

> 直接在 Data Lake (如 S3, ADLS) 的低成本儲存之上，提供 Data Warehouse 等級的資料可靠性 (ACID) 與高效能 (BI)。

它結合了兩者的最大優點，實現了「**一個平台，支援所有資料工作**」。





#### ▋重要技術 - 開放式資料表格式 (Open Table Formats)

Lakehouse 是如何做到的？

關鍵在於它在「開放檔案格式 (如 Parquet)」之上，

增加了一層「**交易層 (Transactional Layer)**」。

這層「交易層」就是所謂的 **Open Table Formats**，

它是一種中介資料 (Metadata) 層，

為底層的資料湖檔案提供了 Data Warehouse 的關鍵功能：

**1\.ACID 交易**：確保資料寫入的原子性、一致性。

**2\.支援更新和刪除**：這是傳統 Data Lake 做不到的。

**3\.效能優化**：如資料索引、分區 (Partitioning) 等，提升 BI 查詢速度。

**4\.精細的存取控制**。

---





### ▋Lakehouse 與 Databricks 的關鍵關係

目前市場上主流的 Open Table Formats 有三種，

Apache Iceberg、Apache Hudi，以及 **Delta Lake**，

Delta Lake 正是由 Databricks 的創辦團隊所開發，

並將其開源 (目前由 Linux 基金會管理)。

Databricks 平台就是基於 Lakehouse 架構打造的，

而 Delta Lake 則是其預設且深度整合的核心儲存格式。



Databricks 利用 **Delta Lake** 作為技術核心，

在 Data Lake 上實現了 Lakehouse 架構，

這使得 Databricks 成為一個**統一的平台**，

能讓資料工程師、資料科學家和 BI 分析師在同一份資料上協同工作，

同時處理 BI、SQL、Streaming、AI 和 ML 等所有類型的任務。





### ▋主競品定位差異

Databricks 算是  **Lakehouse 概念的開創者與領導者**，

從 Data Lake (Spark 巨量資料處理) 出發，

透過其核心技術 **Delta Lake** 補強了 Data Warehouse 的能力（ACID、效能），

是「從湖到倉」的代表。



Snowflake 是雲端資料倉儲霸主，

強項一直是 SQL 分析與 BI 效能，

為了應對 AI/ML 需求反向擁抱 Lakehouse，

主要推動的是另一個開放格式 **Apache Iceberg**。



#### AWS Lake Formation **核心是「治理」**，

#### 幫你管理 S3 上的資料權限、目錄 (Catalog) 和安全性。

#### 需要自己組合 AWS Glue (ETL)、Athena (Query)、EMR (Spark)，

####  等服務來實現完整的 Lakehouse 功能。



#### Azure Synapse Analytics 是**整合式分析平台**，

試圖將「SQL 資料倉儲」和「Spark 巨量資料」兩套獨立的引擎，

整合在同一個 UI 介面下，

更像前面到的「混合架構」。



### ▋總結：Lakehouse 的核心特性

**\-單一儲存層**：不再有倉儲和湖泊兩個獨立系統，資料不再重複。

**\-儲存與運算分離**：繼承 Data Lake 的優勢，具備高彈性與低成本。

**\-支援所有資料類型**：結構化與非結構化資料並存。

**\-支援所有工作負載**：同時支援 BI 報表與 AI/ML 任務。

**\-開放架構**：基於開放標準 (如 Parquet 和 Delta Lake)，避免被單一廠商鎖定 