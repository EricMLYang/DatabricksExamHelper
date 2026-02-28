---
tags:
  - databricks
---
# 【用 Databricks Auto Loader 處理秒級通知】

最近有一個數據量偏大的數據分析案



提出有 10% 數據需要在幾秒內做出異常通知



因為 10% 已經是每天幾千萬等級，而且逐年累積增長



所以花時間思考是否需要用特定服務來特別處理這秒級需求



以下說明:

．現況主架構說明

．AWS 服務方案

．Databricks Auto Loader 方案

．從功能面的說明什麼是 Databricks Auto Loader

．Databricks Auto Loader 底層概要

．最後選擇與考量因素







▋原本主架構說明

原本 Data Pipeline 主流程都是透過 Databricks 處理。



主要是因為我們後續需要處理大量數據的各種分析。



而 Databricks 的 Spark Base 和運算資源管理機制是主要特點。



更重要當然是成員比較熟悉 Databricks 以及分析人員可用 PySpaark 接手分析。



數據量每天預估破億，頻率是 1-10 秒間產出一筆。



但因為不太要求即時性，因此為了成本考量，我們打算批次處理。



到時候可以調整出每個 Job 的最佳費用。



而影響費用的直接變數就是你所選取的資源和計算時間。



直到客戶提出有可能部分數據要有異常通知的功能，且功能希望 10 秒內達成。



因為 10 秒包含終端取數據、解譯的時間，後續才是傳給我們處理。



因此概估我們從收到數據到完成通知動作，大概只能 5 秒內完成。



這讓我們開始考量是否要搭配其他服務來處理。







▋AWS 服務方案

我們初步想到用即時資料串流服務 + serverless 計算服務處理。



在 AWS 上就是 Kinesis + Lambda，有 Rule-Base 異常就傳到應用後端做通知。



上述不管有沒有異常，我數據都還是要回到 Databricks 主 Pipeline 做分析。



當然有異常的數據會做標註，當做後續分析的重點資訊。



這個方案我們是希望確保即時通知的功能不會被延遲。



而且當即時通知的量變大的時候有足夠的因應機制。



但這樣的機制最大的壞處就是讓架構變複雜以及成本考量。



因為會多一組服務，來處理同一批數據(只是即時性要求不同)。



而且當規格變多， Lambda 的程式效能和成本會不好控制，而且變的不好維護。



因此我們就思考 Databricks 的 Auto Loader 機制是否可以滿足需求。







▋Databricks Auto Loader 方案

Databricks Auto Loader 可以開啟一個常開的運算資源。



並且監控雲端儲存裝置(AWS S3、Azure Blob) 、串流服務、資料庫…等。



一旦有新的檔案，可以細粒度的控制批次量，把你的數據放進 Delta Table。



而我們其他單位有嘗試過較小的 Databricks 運算資源監聽 Kafka。



一天可以處理約幾億筆數據。



時間延遲上雖然較不穩定，但大致上 3-5 秒內會把數據清理好放到 Delta Table。



而我們需求而言，就只需要多加測試用 Databricks call 後端 API 這一段會不會延遲。



如果符合需求，這樣最大的好處是在計算費用可控、統一維護的情況下完成秒級即時通知。







▋從功能面的說明什麼是 Databricks Auto Loader

Auto Loader incrementally and efficiently processes new data files as they arrive in cloud storage without any additional setup.



白話一點說，就像在一個大資料匣插上一個監聽機制，只要新檔案一出現，就會按照你在 jupyter notebook 寫的 code 去處理數據。



他有先來後到的順序，當量大時，就會排隊等著，或是你用 Databricks 的 autoscaling 去增加運算資源處理。



而如果只是要把數據進 Delta Table，你寫的 Code 可以很簡潔，甚至就像 SQL 一樣。



大資料匣可以是:

．Amazon S3

．Azure Data Lake Storage

．Google Cloud Storage

．Azure Blob Storage

．Databricks File System



但除了以上來源，Spark 原生就有串流的連接器，因此可以直接處理像 Kafka 的串流服務數據，使用上非常方便。







▋Databricks Auto Loader 底層概要

Auto Loader 主要是透過 Spark Structured Streaming 的模組來實現。



大家都知道 Spark 是一大數據處理引擎。



其主要核心就是圍繞在怎麼處理分布式運算，像是：

\-主要資料結構 RDD, 

\-各種分布式需要的運算規劃： DAG Scheduler, Task Scheduler

\-運算資源管理：Memory Management, Cluster Manager



而基於 Spark Core 會有不同模組像是 Spark SQL / MLlib / GraphX …等。



而 Structured Streaming 就是其中一個模組。



Structured Streaming 本身就有:

\-scalable stream processing engine 

\-querying of infinite data sources

\-automatically detecting new data as it arrives

\-persisting results into target data sinks



而他進一步引用其他模組引入 SQL queries, DataFrame operations, and Spark SQL functions。



使用上非常的便利。





▋最後選擇與考量因素

基於以下考量，我們最後採用 Auto Loader 為主軸來進行。

．架構越單純越好

．雲端服務的成本較低或可控性

．足夠用的即時性



雖然 AWS 顧問不太開心，因為錢都被 Databricks 賺走了。



但 Databricks 的服務對於我們這種分析為主軸的小團隊，真的非常的便利。


