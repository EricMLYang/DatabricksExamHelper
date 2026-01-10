1.核心開發與轉換 (32%): + [數據轉換、清洗和品質 (10%)]

1. Python 和 SQL 進行數據處理（22%）

考察用 Python（特別是 PySpark）和 SQL 來處理大數據的能力。

在 Databricks 環境中，資料工程師需要撰寫程式碼來讀取、轉換及寫入資料，例如使用 Spark DataFrame API 或 Spark SQL 查詢來實現 ETL 工作流。

重點在於能夠撰寫高效、可維護的程式碼來處理各種資料。

範圍: 涵蓋在 Databricks 平臺上開發 ETL 管道所需的技能

基本:

包括使用 PySpark 進行資料轉換

在 Notebook 或檔案中組織程式碼

運用 SQL 查詢 進行資料處理

設計模組化的專案結構:

例如 Databricks Asset Bundles

如何管理第三方函式庫和相依性

撰寫自訂函式（UDF）

使用 Databricks 提供的工作流程（Jobs）、排程批次或串流任務。

可能包括比較串流處理與批次處理的差異（例如結構化串流 vs. 物化檢視）

需要的知識：gp6ak

Python 編程和 Spark 框架

理解資料框操作、Spark SQL 語法、Window 函數、連接（Join）等進階轉換操作

Databricks 開發工具:  Notebook 環境、Jobs 介面、Databricks CLI/API，用於自動化 ETL 工作流的建立與部署。

單元測試與整合測試方法，確保程式碼正確性（Databricks 提供了諸如 assertDataFrameEqual 等函式來協助測試

特別注意：考試中的程式碼範例主要使用 Python 和 SQL，不需要掌握 Scala

準備方式：

實作一個簡單的資料管道。例如，使用 PySpark 讀取不同格式的檔案，對資料進行轉換，然後寫入 Delta Lake。

嘗試撰寫 UDF 來處理自訂邏輯，並使用 Spark SQL 實現相同功能以了解兩者差異。

'熟悉 Databricks Notebook 環境，學習如何透過 Jobs 排程 Notebook 或 Python 腳本執行批次任務。

閱讀官方文件關於 Lakehouse 平臺的開發最佳實踐，瞭解如何組織專案程式碼、管理套件相依性（例如使用 %pip 安裝依賴或在叢集上預先安裝庫），

使用 Databricks Repos 進行原始碼管理。

考試注意事項：

務必理解 PySpark DataFrame API 和 Spark SQL 常見功能的等價關係，例如 DataFrame 的操作如何用 SQL 實現，反之亦然。

當遇到程式碼題時，注意觀察縮排與語法細節，以避免陷入陷阱（如 UDF 的使用限制或 join 操作可能導致的資料傾斜）。

對於給定場景，要能判斷使用批次處理還是串流處理，更佳的答案通常涉及性能與可靠性的考量。例如，要知道 Autoloader 適合持續監控目錄以攝取新檔案

何時應該使用 Delta Live Tables 或 Lakeflow Pipeline 來簡化工作流開發。

3.數據轉換、清洗和品質（Transformation, Cleansing, and Quality，10%）

關注將原始資料轉換為有用資訊的能力，以及確保資料質量達到要求。

評估對清理髒資料、標準化欄位值、處理遺漏值和異常值，以及應用各種轉換邏輯的掌握程度。

範圍：

使用 Spark SQL 和 PySpark 進行進階資料轉換的技巧，例如窗口函數、複雜的 JOIN 和彙總查詢等

資料清洗的策略，例如設計流程將不符合品質的資料隔離（quarantine）。

考題可能涉及如何在串流管道中處理壞資料（例如使用 Autoloader 在經典 Jobs 模式中將不良資料寫到另一個路徑）或在 Lakeflow 宣告式管道中跳過/標記髒資料。

資料品質可能問到如何實現 資料驗證（例如檢查欄位格式、值範圍）以及採取措施保證最終資料的可信度。

需要的知識：

理解 Spark 中的轉換操作，如 groupBy、agg 聚合、各種 join 類型（inner, left, semi 等）對結果和性能的影響。

熟悉 窗口函數 的用途，例如根據時間或分類計算移動平均、排名等。

如何在 Spark 結構化串流中處理延遲到達的資料（watermark）以及去除重複資料（去重）。

資料清洗要知道偵測異常和錯誤值的方法，可能使用 Spark 條件語句過濾或額外建立一個「隔離區」資料表存放問題記錄。

瞭解 Delta Lake 提供的約束（Constraints）或期望（Expectations，例如利用 Delta Live Tables 的 EXPECT 命令）來自動驗證資料品質的功能。

準備方式：練習撰寫複雜查詢來轉換資料，例如：給定使用者行為記錄資料集，使用 Spark SQL 窗口函數計算每個使用者過去7天的平均活動數。嘗試用 PySpark 實現相同邏輯，加深對資料框操作的理解。製造一些「髒」資料（如缺值、明顯異常值），練習編寫程式將其過濾或隔離出去。熟悉 Delta Lake 在資料品質方面的特性，例如在建立表時設定NOT NULL或 CHECK 條件，以及違反時系統的行為。也可閱讀關於 Delta Live Tables 的資料品質管控（如自動中斷管道或將問題資料寫入錯誤表）的內容。

考試注意事項：

考題涉及效能時，考慮資料轉換寫法的優化。例如避免不必要的重複掃描資料，適當使用快取（cache），以及瞭解 Catalyst Optimizer 如何優化查詢。

SQL 題中，注意 WHERE 與 HAVING 的區別、窗口函數的 PARTITION BY 和 ORDER BY 用法。

資料品質題，要能識別題目描述的問題類型（例如重複資料、缺失值、格式錯誤）並選出對應的解決方案，如使用 DROP/FILTER 刪除、FILL 填補缺失值，或正則表達式檢查格式。

題目提到隔離壞資料，聯想到在串流處理中可以將不合格資料分流到另一Delta表保存，以免影響主管道的完整性。