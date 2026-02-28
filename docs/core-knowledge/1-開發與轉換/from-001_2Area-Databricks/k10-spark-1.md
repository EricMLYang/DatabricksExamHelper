# Spark

\
**High Performance Spark, 2nd Edition**



What:

-  high-performance, general-purpose distributed computing system

- most active ASF(Apache Software Foundation) open source project

- more than 1,000 active contributors



What Spark can do:

- process large quantities of data, beyond what can fit on a single machine

- have high-level, relatively easy-to-use API.

- design and interface are unique,

- one of the fastest systems of its kind

- allows us to write the logic of data transformations and machine learning algorithms in a parallelizable way

- relatively system-agnostic



挑戰 - 需要知識才能用的好：

- 最直覺簡單實現的常見資料科學任務可能會比較慢，且穩定性較差

- 大規模資料處理的挑戰： 儘管查詢可能在較小資料集（如幾GB）上失敗，優化後可以在更大資料集（如TB級）上成功運行。

- 效能提升的實際經驗：實踐中，透過適當的優化，任務的運行速度能提升 100 倍。

- 並非所有效能優化技術對每個使用案例都適用。Spark 是一個高度可配置的框架，因此我們可以通過更了解資料的結構來獲得巨大的效益

- 依據資料結構選擇技術：

   - 有些技術在特定的資料大小或資料分佈情況下表現得很好，但並不是每次都有效。

   - 例如 groupByKey 可能會導致記憶體溢出（out-of-memory）錯誤，但對於資料中重複項目很少的情況，這個操作的效能可以和其他替代方法一樣快。



Scala is Needed?

- In the first edition, we said that we believed most users seeking high performance Spark would have to use some Scala. However improvements in Spark’s Python integrations mean this assertion is no longer correct.

- To Be a Spark Expert You Have to Be Able to Read a Little Scala Anyway

- learning **to read** Scala is a worthwhile investment for anyone interested in delving deep into Spark development

- the advantages of cultivating a sophisticated understanding of the Spark codebase is integral to the advanced Spark user. Because Spark is written in Scala, it will be difficult to interact with the Spark source code without the ability, at least, to read Scala code.







ETL + 秒級串流 + ML，其實就是 Spark Structured Streaming 的甜蜜區。

- 大量歷史資料清理、轉換（batch / ETL）

- 秒級 \~ 十秒級的串流處理（near real-time）

- 後面接 ML / 特徵工程 / 模型線上推論



### **1\. Spark Structured Streaming（你現在的基準）**



- 模型：**micro-batch**，幾百毫秒～數秒一批

- 優點：

   - 和 batch 完全同一套 API（Spark SQL / DataFrame），**lambda 架構很自然**

   - 生態最完整：MLlib、Graph、Delta Lake、Databricks 整合

   - 對「先有大量 batch，再加上一點 streaming」的團隊非常友善

   

- 缺點：

   

   - 不是真·逐筆 streaming，超低延遲（幾十毫秒級）的場景會輸給 Flink 類

   - JVM GC、shuffle、狀態管理在極端低延遲／超大 state 場景需要小心

   



---



### **2\. Apache Flink**





- 模型：**true streaming（event-by-event）** + 很強的 event-time & window

- 優點：

   

   - 可以做到**更低延遲、細粒度控制**，很多金融、IoT、風控都用它做「硬即時」

   - 狀態管理、exactly-once 語義做得很好（RocksDB state backend 等）

   - 對複雜 window / CEP（Complex Event Processing）非常強

   

- 缺點：

   

   - 學習曲線比 Spark 陡，API 思維也不太一樣

   - 批處理雖然有，但整體生態（尤其 ML）不如 Spark 完整

   

- 什麼時候會考慮 Flink > Spark？

   

   - 你真的需要 **< 1 秒**、甚至數十毫秒級延遲

   - streaming 是「主角」，batch 是附屬，而不是反過來

   - 例如：實時風控、交易撮合、即時推薦、IoT 控制迴路

   



## **二、為什麼 Databricks 做 Photon，而不是「繼續只優化 Spark」？**





先把概念拆開：



- **Apache Spark**：開源專案，主要是 Scala/Java + JVM，上面有 Catalyst optimizer + Spark 執行引擎。

- **Databricks Photon**：Databricks 自家開發的 **C++ 原生 vectorized 引擎**，接到 Spark 的 logical plan 後，負責真正執行 SQL / DataFrame 的物理運算。





你可以把它想成：



> Spark = 「編譯器 + JVM 引擎」

> Photon = 把原本 JVM 部分換成「原生 C++ 引擎」，且只在 Databricks 平台上跑





### **1\. JVM 已經到瓶頸，Photon 是「換整個引擎」**





Spark 原本靠 JVM + whole-stage codegen 來生成 Java/Scala 程式，再執行分散式計算。這個架構有幾個硬傷：



- JVM 物件開銷和 GC（Garbage Collection），在超大數據、長時間任務、shuffle 很重的時候會變成瓶頸

- 對 CPU cache / SIMD 指令集的掌控比較有限

- 很多底層最佳化不容易在 JVM 上做到極限





Photon 用 C++ 把 operator 寫成 **向量化（vectorized）、欄式（columnar）的原生 kernel**，用批次處理 column 的方式吃資料，盡量吃滿 CPU 管線與 cache。



實際結果：官方與社群測試大多看到 **數倍加速、shuffle 延遲大幅下降**，尤其在 100GB 級以上、很多 join/agg 的 SQL 工作負載上。



這種程度的改變，已經不是「再調一調 JVM 上的 Spark」可以做到的，而是：



> **重寫核心引擎，只沿用 Spark 的 API & optimizer。**



---





### **2\. 開源節奏 vs 商業產品節奏**





Databricks 是 Spark 的主要貢獻者之一，當然有持續在優化開源 Spark；

但：



- 開源 Spark 要顧慮整個社群、所有部署型態，**變太大會破壞相容性**

- Databricks 想做很多跟硬體、雲平台特化的優化（例如 cache、shuffle、storage layout），不一定適合直接放進 OSS Spark





Photon 作為 Databricks 專用引擎，可以：



- 不破壞 Spark 原本的開源設計／相容性

- 又可以在自己平台上**大膽試驗、快速演進**，例如新的 vectorized shuffle、cache 策略等





對使用者來說，體感就是：



- 你還是寫 Spark SQL / DataFrame / PySpark

- Databricks 在背後決定哪些 operator 交給 Photon 跑，哪些還是交給原本 Spark 引擎





---





### **3\. 「不重寫你的程式碼」是關鍵產品策略**





Photon 官方一再強調：**不用改任何程式碼**，你只要把 cluster 換成 Photon runtime 就能吃到加速



如果他們只是去「優化 Spark」，你很難：



- 在不破壞別人 on-prem / 其他雲上的 Spark 的前提下，做這麼激進的改動

- 也比較難把「我們家 Databricks 比別人家的 Spark 快很多」講得那麼清楚





現在的策略是：



- 上層：大家都用 Apache Spark API（不鎖死生態）

- 下層：在 Databricks 上，你可以選擇「Spark 原生引擎」或「Photon 引擎」

- 商業價值：

   

   - SQL Warehouse 已預設用 Photon，賣「5x performance」的 story

   - Data Engineering cluster 上 Photon 當成進階選項（多付一點 DBU，換更多吞吐）

   





---





### **4\. 所以，他們不是「不優化 Spark」，而是「兩條線一起走」**





整理一下：



- Databricks **繼續優化 Apache Spark 本體**：Catalyst、API、新功能（Structured Streaming、Delta、Lakehouse pattern …）

- 同時為自己平台做一個**專屬、硬體級優化的 C++ 執行引擎 Photon**：

   

   - 更極致地吃 CPU / cache / SIMD

   - 對大型 SQL / DataFrame 工作負載給出顯著加速

   - 保留 Spark API 相容性

   





把這兩個放在一起看：



> Spark = 生態 + 抽象 + 可攜性

> Photon = Databricks 上的「超級引擎」，把這些抽象轉成更快的機器碼



---



如果要用一句話幫你記：



- **Spark 的主要競品是 Flink / Kafka Streams（在 streaming 的不同側重點）**，但 Spark 仍是「batch + streaming + ML 大一統」最穩的選項。

- **Photon 不是 Spark 的替代品，而是 Databricks 幫 Spark API 接上「更狠的底層引擎」。**


