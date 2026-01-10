5.數據攝取 (7%): [數據攝取與獲取 (7%)]

2.數據攝取與獲取（Data Ingestion & Acquisition，7%）

評估如何將外部來源的資料匯入 Databricks Lakehouse 平臺。

需要能夠從各種資料來源（如檔案系統、串流訊息匯流排、資料庫等）讀取和匯入資料，

並確保延展性和可靠性。

範圍：不同類型和格式資料攝取方法，設計高效的批次與串流資料管道

涉及讀取多種常見資料格式（例如 Delta Lake 表、Parquet、ORC、Avro、JSON、CSV、XML 等）

多樣化來源取得資料（如雲端儲存、消息佇列系統Kafka或類似message bus）以及使用 Auto Loader 進行持續資料攝取。

建立追加模式（append-only）的資料管道，可同時處理批次和串流資料更新，例如使用 Delta Lake 的功能來讓批次處理和串流處理共存。

需要的知識：

熟悉 Apache Spark 如何讀取各種檔案格式的資料，例如使用 [spark.read](spark.read)``.format("json")... 讀取 JSON，

從 雲端物件儲存（如 S3/ADLS） 加載資料

理解 Autoloader（Spark Structured Streaming + File Notification）的機制，知道如何設定監控一個雲端儲存路徑自動匯入新檔案

了解 Delta Lake 在處理串流和批次資料時的特性，例如 Delta 表的寫入可以被即時查詢，以及如何利用寫前鏡像（CDC/Change Data Capture）或Change Data Feed來處理變更資料。

準備方式：

練習建立幾種簡單的資料攝取工作流。

設定一個 Autoloader 從雲端儲存（例如 AWS S3）持續讀取新增的JSON檔案，將資料寫入Delta表；同時模擬每日批次批量匯入CSV檔案的流程。比較兩種方式在實作上的差異。

閱讀官方文件瞭解 Delta Live Tables 或 Lakeflow Declarative Pipeline 如何簡化資料攝取流程。

嘗試不同資料來源：例如用 Spark 直連一個 JDBC 資料庫，或透過 Kafka 連接器取得串流資料，以熟悉各種來源的整合方法。

考試注意事項：

注意模式推斷與模式演進（Schema Inference/Evolution）在資料匯入時的處理。例如，使用 Autoloader 時如何處理新出現的欄位。

了解處理大型檔案與小檔案的差異：許多小檔案可能導致效能問題，而 Delta 的 Auto Optimize 可以減緩這種問題。

當題目提到Append-Only或增量載入，聯想 Delta Lake 如何保證資料不重複攝取（例如依賴文件目錄結構或檔名）。

場景涉及即時串流資料（如即時Log、IoT資料），要能識別需要用Structured Streaming方案而非僅批次Spark作業。