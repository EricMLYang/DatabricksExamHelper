# **Databricks 認證讀書計畫** 



## **A. 概覽**

### **Why**

通過考試證明具備「設計、建立、並維護可營運 (Production-grade) 的 Databricks 數據系統」的專業能力。

考試的重點不在於背誦 API，而在於評估在真實營運環境中的「權衡 (Trade-off)」能力：面對問題時，哪個選項最可靠、最省錢、最安全、效能最高。

### **What (要學什麼)**

依 80/20 原則，將 10 個考綱主題重組為 7 個「作戰集群」:

1. **核心開發與轉換 (32%):** + \[數據轉換、清洗和品質 (10%)\]

2. **維運與自動化 (20%):** \[監控與警報 (10%)\] + \[除錯與部署 (10%)\]

3. **安全與治理 (17%):** \[確保數據安全與合規 (10%)\] + \[數據治理 (7%)\]

4. **成本與效能優化 (13%):** \[成本與性能優化 (13%)\]

5. **數據攝取 (7%):** \[數據攝取與獲取 (7%)\]

6. **數據建模 (6%):** \[數據建模 (6%)\]

7. **數據共享 (5%):** \[數據共享與聯邦 (5%)\]

真正的拉分差距在於「維運 (20%)」、「安全 (17%)」和「優化 (13%)」。這三塊（總計 50%）是區分「工程師」與「*專業*工程師」的關鍵。

### **How (怎麼學)**

一次只專注於一個最小學習單元，依循以下三步驟，攻克一個特定主題

1. 學習：花 20-30 分鐘閱讀文章或觀看影片，理解概念。

2. 實作：花 30-60 分鐘直接在 Databricks 中針對該概念進行動手編碼或解決問題。

3. 回想與測驗 (Recall & Quiz)：花 10 分鐘透過自製閃卡或自我提問進行主動回憶，鞏固關鍵知識。

---



## **B. Concepts (概念地圖)**

### **B0. 整體**

- **Medallion Architecture** 

   - 將資料組織成銅（原始）、銀（清理）和金（業務），每階段逐步提升資料品質。

   - 是 Databricks 最佳實踐基礎，確保資料從攝取到分析的流程中，職責劃分清晰。

- **模組化 ETL 與管線設計**

   - **原則**: 將資料管線**分階段**建構（例如獎牌分層），並撰寫模組化程式碼（函式、notebooks）以提高可讀性與重用性。例如，將攝取、轉換和載入的步驟分開。

   - **陷阱**: 建立一個包山包海的巨大 notebook 或 job。這種作法難以維護和偵錯（就像一團亂麻的義大利麵）。你應該將你的管線想像成一條有明確定義步驟的裝配線。

- **Spark 轉換 (Transformations) 與動作 (Actions)**

   - **原則**: 利用 Spark 的分散式 DataFrame 操作來處理繁重的工作（joins, aggregations, filtering），只在必要時才使用 actions (collect, output)。熟悉**寬轉換 vs. 窄轉換**（例如 `map` vs. `join`）以及 Spark 的延遲評估 (lazy evaluation) 和 Catalyst 優化器如何為你所用。

   - **陷阱**: 使用 Python 迴圈或 Pandas 處理大數據——這會扼殺效能。永遠將大型資料操作「委派」給 Spark（例如，使用 `df.groupBy().agg()` 而不是在 Python 中累積結果）。

- **Delta Lake 的可靠性**

   - **原則**: Delta Lake 中的 **ACID 交易**和結構強制 (schema enforcement) 確保了可靠的資料更新和版本控制（時間旅行 Time Travel）。對於可變的資料集（updates/deletes）以及處理並行寫入，應使用 Delta。**刪除向量 (Deletion Vectors)** 等功能可以在不重寫整個檔案的情況下標記已刪除的資料列，以提高效率。

   - **陷阱**: 忽略表格優化。隨著時間推移，小檔案和多個版本會拖慢查詢速度。記得定期對 Delta 表格執行 `OPTIMIZE` 和 `VACUUM`（但**切勿過早執行 vacuum**——預設的 7 天保留期可防止意外的資料遺失）。

- **效能調校與資料跳過 (Data Skipping)**

   - **原則**: 透過減少掃描的資料量來提升查詢速度。技巧包括：**分區 (Partitioning)**（按資料夾進行粗略裁剪）、**Z-Ordering**（在檔案內按鍵值對資料進行叢集化，以利資料跳過索引），以及較新的**液態叢集 (Liquid Clustering)**，它能**自動**取代手動分區/Z-order，按指定鍵值對資料進行叢集。此外，利用快取 (in-memory) 處理重複存取，並使用 **Photon**（Databricks 的向量化引擎）來加速執行。

   - **陷阱**: 對高基數 (high-cardinality) 欄位進行過度分區，會導致過多的小檔案和開銷。在這種情況下，使用 Liquid Clustering 或 Z-Order 通常比建立數千個分區要好。同樣地，小心使用 `shuffle()` 操作——資料傾斜（某個分區獲得大部分資料）會悄悄地損害效能，所以要監控並緩解（例如使用加鹽或增加 shuffle 分區數）。

- **串流 vs. 批次處理**

   - **原則**: 使用**結構化串流 (Structured Streaming)** 處理近乎即時的管線（低延遲、持續處理），而批次處理則用於週期性的大量作業。理解**事件時間 (event time)** vs. 處理時間 (processing time)，並使用浮水印 (watermarks) 來處理延遲資料。像 **Auto Loader** 這樣的工具，透過自動發現新檔案，讓將新檔案作為串流攝取變得更容易。

   - **陷阱**: 將串流當作批次處理——例如，不設定檢查點 (checkpointing) 或忽略輸出模式。在串流作業中，務必指定一個檢查點位置並選擇正確的輸出模式（append, complete 等），否則在發生故障時可能會出現重複資料或進度遺失。

- **資料品質與治理**

   - **原則**: 「垃圾進，垃圾出」。在每個階段強制執行品質：例如，使用 **Delta Live Tables (DLT) 的期望 (expectations)** 來驗證資料（確保主鍵不為空、數值在範圍內等），並決定對無效記錄是**拋棄 (drop)**、**隔離 (quarantine)** 或**失敗 (fail)**。同時應用**治理**控制：使用 **Unity Catalog** 進行權限管理（誰能看到哪些表格），並對敏感資料使用**列級安全性 (Row-Level Security)** 和**欄位遮罩 (Column Masking)**。Unity Catalog 的權限會**向下繼承**（在綱要或目錄層級授權，即可涵蓋其下的所有表格），簡化了管理。

   - **陷阱**: 讓「髒」資料通過——例如，直到下游出現問題才處理空值、重複值或結構變更。最好在銀層就捕捉到問題（例如，為有問題的記錄建立一個 `_quarantine` 表格），而不是讓壞資料悄悄地污染金層。同樣，避免違反**最小權限原則**的臨時授權——不要給分析師廣泛的管理員角色，當他們只需要對特定表格的 `SELECT` 權限時。

- **任務調度 & CI/CD**

   - **原則**: 將管線視為生產程式碼：使用 **Jobs** 來排程具有依賴關係的 notebooks/scripts（任務 A -> B -> C），並實作 CI/CD 以可靠地部署更新。Databricks Repos 允許 Git 整合，而 **Asset Bundles** 讓你將管線基礎設施定義為程式碼，以便在不同環境中進行一致的部署。將工作流程參數化（例如，使用任務參數或 widgets）以提高在開發/測試/生產環境中的靈活性。

   - **陷阱**: 以臨時方式手動運行 notebooks——這無法規模化。與其為每個步驟點擊「運行」，不如將你的程式碼打包並使用自動化的作業觸發器（並在失敗時設定警報）。忽略測試是另一個陷阱：如果沒有至少一些單元測試或作業層級的錯誤處理，你可能會部署在邊界情況下會出錯的管線。務必使用樣本資料進行測試，並納入回滾或修復流程。



後續依 10 大考綱主題，建立核心原理與直覺。

### **B.1: 開發使用 Python 和 SQL 進行數據處理 (22%)**

- **Spark 是「延遲執行 (Lazy Evaluation)」的：** 您寫的 PySpark 程式碼只是在建構一個「執行計畫 (Plan)」，直到您呼叫 .write(), .show() 或 .collect() 這樣的「動作 (Action)」時，它才會真正開始運算。

- **DataFrame API vs. Spark SQL：** 兩者效能完全相同。Catalyst Optimizer 會將它們轉譯為相同的底層執行計畫。選擇標準：SQL 適合「聲明式」的業務邏輯；DataFrame API 適合「程式化」的動態建構與單元測試。

- **UDF (自訂函數) 是最後的手段：** UDF (User-Defined Functions) 對 Spark 而言是「黑盒子」，會破壞 Catalyst Optimizer 的優化（如謂詞下推），且涉及 Python <-> JVM 序列化/反序列化，成本極高。

- **比喻：** UDF 就像在高速公路（Spark 優化）上突然下交流道去便利商店（Python 解譯器）買東西，再繞回高速公路。請 99% 的時間都使用 spark.sql.functions 內的內建函數。

- **串流 (Streaming) vs. 批次 (Batch)：** 它們在 Databricks 中共享幾乎一樣的 API (Structured Streaming)，但心智模型不同。批次是「處理 *已存在* 的資料」；串流是「處理 *將抵達* 的資料」，需要額外考慮「狀態 (State)」、「浮水印 (Watermark)」與「觸發間隔 (Trigger)」。

- **模組化 (Modularity) 是專業級要求：** 考試會鄙視「把所有邏輯寫在一個 Notebook」的做法。專業級的做法是使用 %run 呼叫共用函式庫、使用 Databricks Repos，或最終使用 Databricks Asset Bundles (DABs) 來封裝。

### **B.2: 數據攝取與獲取 (7%)**

- **Auto Loader 是增量攝取的標準答案：** 它是 Databricks 提供的最佳工具，用於「增量」且「冪等」地處理雲端儲存上的新檔案。

- **Auto Loader 的核心是「狀態管理」：** 它透過 schemaLocation 選項，自動追蹤哪些檔案已被處理，確保檔案不會被重複讀取。

- **Auto Loader 處理 Schema 演進：** 原始資料的欄位會改變。Auto Loader 能自動偵測這些變更（schemaEvolutionMode），並優雅地合併新欄位，而不會中斷管線。

- **COPY INTO 是手動的替代方案：** 它也具備冪等性，適合「手動觸發」或「小型」的批次載入，但 Auto Loader（cloud_files）才是用於建立「自動化」管線的首選。

- **比喻：** COPY INTO 像是一次性的「匯入」按鈕；Auto Loader 像是一個「永久訂閱」，持續監控新郵件的收件匣。

### **B.3: 數據轉換、清洗和品質 (10%)**

- **Lakehouse 採用 ELT 模式：** 在現代數據架構中，我們不再是 ETL (Extract, Transform, Load)，而是 ELT。先用 Auto Loader (E) 和 DLT (L) 把原始資料 (Bronze) 載入，然後才用 SQL/PySpark (T) 轉換為 Silver/Gold 層。

- **Delta Live Tables (DLT) 的核心是「資料流管理」：** DLT 是一個「聲明式」框架。您只需定義「資料的終態」，DLT 會自動處理任務編排、錯誤重試、日誌記錄、以及基礎設施的啟動與關閉。

- **DLT 的「期望 (Expectations)」是內建的資料品質防火牆：** EXPECT... ON VIOLATION... 語法讓您能在資料流「之中」定義品質規則，而不必等資料落地後才「事後」檢查。

- **處理延遲資料 (Late-arriving data) 是串流必考題：** Watermarking (浮水印) 是 Spark 告訴自己「我願意等多久」的機制，用以關閉舊的狀態窗口。

- **隔離 (Quarantine) 髒資料：** 專業的管線不會因為髒資料就停擺。在 DLT 中，這對應 ON VIOLATION DROP ROW 或 RETAIN 策略。在 Auto Loader 中，這對應 \_rescued_data 欄位。

### **B.4: 數據共享與聯邦 (5%)**

- **Delta Sharing 的核心是「不複製」：** 它是唯一安全的、原生的方式，能將 Lakehouse 中的「即時」資料分享給外部，而無需複製或移動資料。

- **Delta Sharing 的原理：** 它透過一個安全的開放協議，分享「預簽署的 URL (Pre-signed URL)」給 Parquet 檔案。接收方（D2O）甚至不需要是 Databricks 用戶。

- **比喻：** Delta Sharing 不是「寄送 Email 附件」（複製資料），而是「分享一個 Google Doc 的唯讀連結」（分享存取權）。

- **Lakehouse Federation 是「查詢」外部：** 這功能讓您在 Databricks (Unity Catalog) 中註冊「外部」資料庫（如 MySQL, Postgres），並直接用 Databricks 查詢它們，實現「聯邦查詢」。

### **B.5: 監控與警報 (10%)**

- **監控工具的職責劃分是必考點：**

- **Spark UI：** 用於「即時」或「事後」深入除錯*單一 Spark Job*。看 DAG、Stages、Shuffle、Spill。

- **Query Profile：** 用於除錯 *Databricks SQL Warehouse* 上的「SQL 查詢」。它更直觀地顯示哪個環節耗時最長。

- **System Tables：** 用於「全帳戶」的「長期」監控與審計。是 SQL 介面，用來查 system.billing.usage (成本)、system.access.audit (審計)。

- **SQL Alerts：** 用於「數據指標」的警報。它會定期執行一個 SQL 查詢，當「結果」滿足特定條件時（e.g., count > 100），觸發警報。

### **B.6: 成本與性能優化 (13%)**

- **優化的第一原則：不做重複的工作。** Databricks 的核心優化（如 Data Skipping, File Pruning）都是基於這個原則。

- **Delta Lake 優化 (OPTIMIZE) 的本質是「解決小檔案問題」：** 它把一堆碎的 Parquet 小檔案「合併 (Compaction)」成較大的檔案（e.g., 1GB），提升讀取時的吞吐量 (Throughput)。

- **Z-Order 是「多欄位」的 Data Skipping：** 如果您經常 WHERE a=1 AND b=2，單純的 Partitioning 幫不了你。Z-Order 是一種「多維空間填充曲線」，會把相關的資料區塊「物理上」排在一起。

- **比喻：** Partitioning 是「按州分檔案櫃」(e.g., CA, NY)；Z-Order 是「在 CA 櫃子裡，把『城市』和『郵遞區號』相近的檔案夾放在一起」。

- **Liquid Clustering (LC) 是優化的未來：** LC 是 Databricks 對 Partitioning + Z-Order 的現代答案。它「自動」且「增量」地管理資料佈局，避免了手動選擇「分區欄位」的詛咒（例如，選了高基數欄位導致百萬個小檔案）。

- **Photon 引擎是「硬體加速」：** 它是一個 C++ 寫的向量化執行引擎，專門用來取代 Spark 的 JVM 引擎。只要您的 ETL 是 SQL 或 DataFrame 為主（非 UDF），開啟 Photon 幾乎總是能同時「加速」並「降本」。

### **B.7: 確保數據安全與合規 (10%)**

- **Unity Catalog (UC) 是所有安全題的唯一答案：** 考試中任何關於權限、安全、治理的問題，答案 100% 與 Unity Catalog 相關。

- **UC 的三層命名空間：** Catalog.Schema.Table (或 Catalog.Database.Table)。所有權限都在這三層級上管理。

- **權限是繼承的：** 在 Catalog 層級授予的權限，會自動繼承到其下的所有 Schema 和 Table。**最小權限原則 (PoLP)** 是設計核心。

- **行級安全 (Row-level Security) 與列級遮罩 (Column Masking)：** 這是 UC 提供的「數據級」安全。

- Row Filter：動態過濾數據（e.g., 經理 A 只能看到部門 A 的行）。

- Column Mask：動態遮蔽數據（e.g., PII 欄位顯示為 \*\*\*\*）。

- **PII（個人身份資訊）處理：** 合規性要求您必須知道如何使用 Column Masking 或在 Silver 層就使用 SHA2() 等函數對 PII 進行雜湊 (Hash) 處理。

### **B.8: 數據治理 (7%)**

- **UC 不只是安全，它還是「治理」平台：**

- **Data Catalog (數據目錄)：** UC 提供了一個可搜尋的目錄。您可以使用 COMMENT ON TABLE 和 Tags 來豐富中繼資料 (Metadata)，讓數據「可被發現」。

- **Data Lineage (數據血緣)：** UC「自動」捕獲所有透過 SQL 和 PySpark 執行的查詢血緣，精確到「欄位級」。您可以看到 Gold 層的某個欄位是從哪些 Silver/Bronze 層欄位計算來的。

- **Tags (標籤)：** Tags 是實現治理分類的工具。您可以標記 PII: True 或 Department: Sales，並基於 Tag 進行搜索或套用策略。

### **B.9: 除錯與部署 (10%)**

- **專業級的部署不是「手動」：** 在 Notebook 點擊 "Run" 不是部署。

- **Databricks Repos：** 這是實現 Git 整合的第一步。它將您的 Git 儲存庫 (e.g., GitHub)「同步」到 Databricks Workspace，實現程式碼版控。

- **Databricks Asset Bundles (DABs)：** 這是「部署」的標準答案。DABs 允許您使用一個 databricks.yml 檔案，將您的程式碼（Notebooks, Python scripts）和「基礎設施」（Jobs, Pipelines, Alerts）「打包」並「部署」到不同環境 (dev/staging/prod)。

- **比喻：** Repos 是把「樂高積木」(程式碼) 帶進來；DABs 是那張「說明書」(YAML)，告訴 Databricks 如何把這些積木「組裝」成一個「完整的城堡」(Job/Pipeline)。

### **B.10: 數據建模 (6%)**

- **Medallion 架構是 Lakehouse 的建模基礎：**

- **Bronze (銅層)：** 原始、未經處理的資料。1:1 對應來源。

- **Silver (銀層)：** 經過清洗、驗證、去重、標準化的資料。

- **Gold (金層)：** 針對特定業務（BI/AI）進行「聚合 (Aggregate)」或「優化」的資料。

- **維度建模 (Dimensional Modeling) 仍然重要：** Gold 層通常會被建構成「星型模型 (Star Schema)」或「雪花模型 (Snowflake Schema)」，以優化 BI 工具（如 Power BI）的查詢效能。

- Fact Table (事實表)：儲存「指標」（e.g., 銷售額、數量）。

- Dimension Tables (維度表)：儲存「上下文」（e.g., 客戶、產品、日期）。

- **Lakehouse 簡化了建模：** 由於 Delta Lake 的存在，我們不再需要像傳統數倉那樣過度正規化。Gold 層的「寬表 (Wide Tables)」也是一種常見且高效的模型。



---



## **C. Facts (必背清單)**

以「Q → A」列出高頻且容易混淆的事實。

### **C.1: 開發 (Facts)**

- **Q: repartition() 和 coalesce() 的區別？**

- A: repartition() 會產生完整的 Shuffle，可增加或減少 Partitions；coalesce() 僅用於「減少」Partitions，它會合併現有的 Partitions，避免完整 Shuffle，速度較快。

- **Q: 為什麼 PySpark UDF 效能差？**

- A: 1. Python <-> JVM 序列化/反序列化成本。 2. 破壞 Catalyst Optimizer 優化（它對 UDF 內部是黑盒子）。

- **Q: PySpark Pandas UDF (Vectorized UDF) 為何快？**

- A: 它使用 Apache Arrow 在記憶體中傳輸數據，避免了序列化成本，並能利用向量化操作。

- **Q: spark.sql.shuffle.partitions 參數的作用？**

- A: 控制在 Shuffle 階段（如 JOIN, GROUP BY）後，輸出的 Partition 數量。預設 200，常需調高。



### **C.2: 攝取 (Facts)**

- **Q: Auto Loader 必須的兩個 cloudFiles 選項？**

- A: cloudFiles.format (e.g., "json", "csv") 和 cloudFiles.schemaLocation (用於儲存狀態和 Schema)。

- **Q: Auto Loader 的兩種檔案偵測模式？**

- A: Directory Listing (預設，適用百萬級檔案) 和 File Notification (使用雲端事件通知，如 SQS/Event Grid，適用上億檔案)。

- **Q: COPY INTO 和 Auto Loader 都能增量嗎？**

- A: 都是冪等的。但 COPY INTO 需要「手動觸發」（如 Jobs 排程），Auto Loader 是「持續的」（readStream）。

- **Q: Auto Loader 如何處理髒資料？**

- A: 欄位不符的資料會被存放在 \_rescued_data 欄位（如果啟用了）。

### **C.3: 轉換與品質 (Facts)**

- **Q: DLT 的 CREATE STREAMING LIVE TABLE 和 CREATE LIVE TABLE 區別？**

- A: STREAMING 用於增量/串流來源，僅處理新抵達的數據；LIVE 用於批次，每次更新都會重新計算整個表。

- **Q: DLT 的 EXPECT 規則三種 ON VIOLATION 模式？**

- A: FAIL (停止管線), DROP ROW (丟棄該筆髒資料), RETAIN (保留，但標記為違規，通常用於隔離)。

- **Q: MERGE INTO 指令的核心用途？**

- A: 實現 "Upsert"（Update + Insert）。WHEN MATCHED THEN UPDATE, WHEN NOT MATCHED THEN INSERT。

- **Q: 什麼是 Watermarking (浮水印)？**

- A: 在串流處理中，定義一個「可容忍的延遲時間」，讓 Spark 知道何時可以安全地關閉舊的窗口並清除狀態。

### **C.4: 共享 (Facts)**

- **Q: Delta Sharing 有哪兩種分享模式？**

- A: 1. Databricks-to-Databricks (D2D)：在 UC 中管理。 2. Open Sharing (D2O)：使用 datashare 協議，接收方可以是任何客戶端 (Power BI, Python)。

- **Q: 分享資料時，資料會被複製嗎？**

- A: 不會。Delta Sharing 只分享元數據和短期的預簽署 URL，接收方直接從您的雲端儲存讀取 Parquet 檔案。

- **Q: Lakehouse Federation 的用途？**

- A: 讓 UC 成為一個「聯邦」查詢引擎，可以直接查詢外部資料庫（如 MySQL, Postgres, Redshift）中的數據，無需 ETL。



### **C.5: 監控 (Facts)**

- **Q: 如何監控 Databricks 成本？**

- A: 查詢 System Table system.billing.usage。

- **Q: 如何審計誰存取了哪個表？**

- A: 查詢 System Table system.access.audit。

- **Q: SQL Alerts 如何設定？**

- A: 在 SQL 編輯器中寫一個查詢，點擊 "Alerts" 設定，定義一個「觸發條件」（e.g., Value > X）和「通知目的地」。

- **Q: Spark UI 預設在哪個 port？**

- A: Driver node 上的 4040 port。

### **C.6: 優化 (Facts)**

- **Q: OPTIMIZE 指令的 ZORDER BY 和 Liquid Clustering 可以同時使用嗎？**

- A: 不行。一個 Delta 表要麼使用 Z-Order，要麼使用 Liquid Clustering。LC 是新表的建議做法。

- **Q: Deletion Vectors (刪除向量) 是什麼？**

- A: 一種 Delta Lake 功能，它將刪除標記為「元數據」，而不是立即重寫 Parquet 檔案。這極大加速了 DELETE 和 UPDATE 操作。

- **Q: Photon 引擎在哪種情境下「無效」？**

- A: 當您的程式碼大量依賴 RDD API 或 Python UDF 時，Photon 無法介入優化。

- **Q: Adaptive Query Execution (AQE) 的三大功能？**

- A: 1. 動態合併 Partitions (解小檔案) 2. 動態切換 Join 策略 (e.g., SortMerge to Broadcast) 3. 動態處理 Skew Join (資料傾斜)。

### **C.7: 安全 (Facts)**

- **Q: UC 的三層命名空間是什麼？**

- A: Catalog.Schema.Table (或 Catalog.Database.Table)。

- **Q: UC 中最小的授權單位是什麼？**

- A: SELECT, MODIFY, USE CATALOG, USE SCHEMA 等。

- **Q: 建立 Row Filter Function 時，函數必須返回什麼？**

- A: BOOLEAN (布林值)。True 表示該行可見，False 表示不可見。

- **Q: 如果我在 Catalog 層級 GRANT SELECT，但在 Schema 層級 DENY SELECT，結果是什麼？**

- A: DENY 優先。使用者將無法存取該 Schema。



### **C.8: 治理 (Facts)**

- **Q: UC 的 Data Lineage (數據血緣) 支援哪些語言？**

- A: SQL, PySpark, Scala。

- **Q: UC Lineage 是即時的嗎？**

- A: 不是，通常需要幾分鐘的延遲來捕獲和顯示。

- **Q: 如何為表格添加註解？**

- A: COMMENT ON TABLE my_table IS 'This is a comment.'。

- **Q: Tags (標籤) 可以應用在哪些 UC 物件上？**

- A: Catalog, Schema, Table, Column (欄位級標籤)。

### **C.9: 除錯與部署 (Facts)**

- **Q: Databricks Asset Bundles (DABs) 的核心設定檔是什麼？**

- A: databricks.yml。

- **Q: databricks.yml 中的 targets 區塊作用？**

- A: 定義您的部署「環境」（e.g., dev, staging, prod）及其特定配置（如 Job Cluster ID, Workspace URL）。

- **Q: Databricks Repos 和 DABs 的關係？**

- A: Repos 用於將 Git 程式碼「同步」到 Workspace。DABs 是 CI/CD 工具，用於將這些程式碼和相關資源「部署」為 Job 或 Pipeline。

- **Q: Job 失敗時，如何從失敗的 Task 繼續？**

- A: 使用 Repair and Rerun 功能（如果 Job 是 DLT 或有 Task-level 依賴）。

### **C.10: 建模 (Facts)**

- **Q: Medallion (銅銀金) 架構的三層各自職責？**

- A: Bronze (原始資料), Silver (清洗、標準化), Gold (業務聚合)。

- **Q: 星型模型 (Star Schema) 是什麼？**

- A: 一個大型的「事實表 (Fact Table)」在中心，周圍環繞著多個「維度表 (Dimension Tables)」。

- **Q: 為什麼 Lakehouse 適合星型模型？**

- A: Delta Lake 的高效能 Join（特別是 Broadcast Join）和 Photon 引擎，使得 Fact 和 Dimension 表之間的 Join 非常快。

- **Q: Liquid Clustering (LC) 如何簡化建模？**

- A: LC 自動管理資料佈局，您不再需要為「分區策略」而過度煩惱，降低了物理建模的複雜性。

### **C.11: 關鍵數值索引 (Numerical Index)**

- **Q: Delta Lake Time Travel 預設保留多久？**

- A: 30 天 (可透過 logRetentionDuration 調整)。

- **Q: VACUUM 指令的預設保留門檻？**

- A: 7 天 (168 小時)。VACUUM 會「永久刪除」早於此門檻的舊資料檔案，使 Time Travel 失效。

- **Q: VACUUM 的 RETAIN 0 HOURS 為什麼危險？**

- A: 它會立即刪除所有非最新版本的檔案，如果此時有長時間執行的查詢正在讀取舊檔案，該查詢會失敗。

- **Q: Spark UI 預設 port？**

- A: 4040

- **Q: spark.sql.shuffle.partitions 預設值？**

- A: 200



---

## **D. Procedures (程序/解題術)**

"Professional" 級考試不考「指令」，考「策略」。您需要的是「作戰手冊 (Playbook)」。

### **D.1: 關鍵任務標準流程 (Key Task Playbooks)**

#### **Playbook 1: 效能調校 SOP (Performance Tuning SOP)**

1. **症狀 (Symptom):** Job / SQL 查詢執行緩慢或 OOM (記憶體不足)。

2. **診斷 (Diagnose):**

   - *SQL Warehouse:* 使用 **Query Profile** (查詢分析器)。

   - *Job Cluster:* 使用 **Spark UI**。

3. **定位 (Locate):** 查看「執行計畫 (DAG)」和「Stages」：

   - (a) 尋找「執行時間最長」的 Stage。

   - (b) 檢查 Shuffle Read/Write (資料重組) 或 Spill (Disk) (記憶體溢出到硬碟) 的數據量。

4. **歸因 (Identify Cause) & 開藥 (Prescribe):**

   - **IF** (a) Shuffle 量極大，且 (b) 某幾個 Task 特別慢 -> **病因：Data Skew (資料傾斜)**。

      - *處方：* 啟用 AQE (Adaptive Query Execution)。或手動 salting (加鹽) 傾斜的 key。

   - **IF** (a) Spill (Disk) 量大 -> **病因：記憶體不足 / Partition太大**。

      - *處方：* 換用「記憶體優化」的節點類型。或在程式碼中用 repartition() 增加 Partition 數量，分散壓力。

   - **IF** (a) 掃描檔案 (File Scan) 時間過長，且 (b) files read 數量極大 -> **病因：小檔案問題 (Small File Problem)**。

      - *處方：* 執行 OPTIMIZE 合併小檔案。或（更推薦）改用 Liquid Clustering。

   - **IF** (a) files read 數量不大，但 (b) 掃描時間仍長 -> **病因：Data Skipping 失效**。

      - *處方：* 檢查 WHERE 條件欄位。如果該欄位是高基數欄位，使用 ZORDER BY 或 Liquid Clustering 優化它。

   - **IF** (a) 看到 BroadcastJoin -> **這是好事！** (AQE 自動將小表廣播，避免 Shuffle)。如果沒看到，但你知道有一張是小表，可手動 /\*+ BROADCAST(table_name) \*/ 提示。

#### **Playbook 2: CI/CD 部署流程 (使用 Databricks Asset Bundles - DABs)**

1. **本地開發 (Local Dev):** 在 VS Code (或您偏好的 IDE) 中開發。

2. **定義 Bundle:** 在根目錄建立 databricks.yml 檔案。

3. **定義資源 (Artifacts):** 在 databricks.yml 中定義：

   - artifacts: (例如：my\_[notebook.py](notebook.py))

   - targets: (您的環境，如 dev, staging, prod)

   - resources: (您要部署的 Databricks 物件，如 jobs, pipelines)

4. **部署 (Deploy):**

   - (首次) databricks bundle init (建立模板)

   - databricks bundle validate (驗證 YAML)

   - databricks bundle deploy -t dev (部署到 dev 環境)

5. **測試 (Test):** databricks bundle run my_job -t dev (在 dev 環境觸發 job)

6. **整合 (Integration):** 在您的 CI/CD 平台 (e.g., GitHub Actions) 中，安裝 Databricks CLI，並呼叫 databricks bundle deploy -t prod。

#### **Playbook 3: Unity Catalog 最小權限原則 (PoLP) 設計流程**

1. **定義角色 (Roles):** 建立 Group，例如 data_analysts, data_engineers, data_scientists。**永遠不對「單一使用者」授權**。

2. **定義資源 (Resources):**

   - bronze_catalog: 僅 data_engineers 有 SELECT + MODIFY。

   - silver_catalog: data_engineers 有 MODIFY；data_scientists 有 SELECT。

   - gold_catalog: data_engineers 有 MODIFY；data_analysts 有 SELECT。

3. **授權 (Grant):**

   - **在「最高層級」授權。** *IF* data_analysts 需要 gold_catalog 下的所有表，**就在 Catalog 層級 GRANT SELECT ON CATALOG gold_catalog TO data_analysts\`\`**。

      - *IF* data_analysts 只需要 gold_catalog.sales_schema -> 就在 Schema 層級授權。

      - *IF* 有 PII 資料 (e.g., [gold.users.email](gold.users.email)) -> 使用 Column Masking (欄位遮罩)。

      - *IF* 需依「部門」限制存取 (e.g., 銷售經理只能看自己區域) -> 使用 Row-level Security (行級安全性)。



### D.2 實戰單元

手冊 1: 優化有許多小檔案的慢速 Delta 表格

- 評估表格狀態: 使用 DESCRIBE DETAIL table（或在 Data Explorer UI 中查看）來檢查檔案數量、平均檔案大小和碎片化程度。如果你看到成千上萬個小檔案或許多未優化的分區，這就是優化的目標。

- 壓縮小檔案: 執行 OPTIMIZE tableName; 命令（在大型表格上，請在離峰時段執行）。這會將小檔案壓縮成較大的檔案。如果某些查詢會按特定欄位過濾（例如 date 或 userId），請使用 OPTIMIZE tableName ZORDER BY (col) 來共同定位該謂詞的資料，從而改善資料跳過的效果。

- 啟用自動優化: 在較新的 DBR 版本中，你可以在叢集或表格上啟用自動優化 (Auto Optimize) 和自動壓縮 (Auto Compaction)。這將使未來的寫入操作在背景自動壓縮小檔案。

- 驗證效能: 優化後，使用 Spark UI 或對代表性查詢執行 EXPLAIN。你應該會看到掃描的分區變少了。檢查查詢運行時間是否縮短。同時，確保 Z-Ordering 確實減少了檔案掃描（EXPLAIN 或 Query Profile 中的 Data Skipping 部分可以顯示跳過了多少檔案）。

- 必要時執行 Vacuum: 如果表格有大量過期檔案（例如，經過大量更新/刪除後），並且已超過保留期，請執行 VACUUM tableName RETAIN 168 HOURS; 來刪除舊的 Parquet 檔案並釋放儲存空間。請小心：只有當你確定不需要早於 7 天的時間旅行時才這樣做（或相應地調整小時數）。





手冊 2: Unity Catalog 權限鎖定 (最小權限原則)

- 用目錄/綱要組織: 假設你有一個財務資料集。在 Unity Catalog 中創建一個新的目錄（例如 Finance）和綱要（例如 Finance.Default）來存放這些表格。這提供了一個頂層容器，可以一次性管理權限。

- 為角色定義群組: 使用身份管理創建群組，如 finance_analysts, finance_engineers 等。（Databricks 可以與 Azure AD/Google IAM 群組同步）。根據用戶的職位將他們分配到適當的群組。

- 授予最小權限: 首先，將 Finance 目錄的 USAGE 權限授予需要任何存取權限的群組（這讓他們能看到該目錄）。接下來，授予綱要級和表格級的權限：例如 GRANT SELECT ON TABLE Finance.Default.Transactions TO finance_analysts; 讓分析師可以讀取資料。執行管線的工程師可能會獲得特定表格的 MODIFY 權限，但避免給予任何不需要的人廣泛的寫入權限。

列/欄位控制 (若需要): 如果表格包含敏感資訊（例如 PII 或不同區域的資料），請實作列過濾器和欄位遮罩。例如，添加一個列過濾器，讓每個分析師只看到 WHERE Region = 'APAC' 的資料（如果他們在亞太團隊），或為不應看到薪資等欄位的角色將其遮罩為 NULL。這確保即使他們有 SELECT 權限，也只能獲取適當的資料。

審核與迭代: 使用 Unity Catalog 的審計日誌或資料血緣 UI 來驗證誰在查詢這些表格。定期用 SHOW GRANTS 檢閱授權，確保沒有出現過度的權限。根據需要進行調整，撤銷任何不必要的權限。這使你的 Lakehouse 既易於存取又安全，遵循最小權限原則。