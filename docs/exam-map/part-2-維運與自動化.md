2.維運與自動化 (20%): [監控與警報 (10%)] + [除錯與部署 (10%)]

5.監控與警報（Monitoring and Alerting，10%）

專注於監控資料管道和工作負載的健康狀況，及在出現問題或特定狀況時發出警報（通知）。

工程師需持續追蹤 ETL 作業的執行情形、效能指標、資源使用情況，並設定自動告警機制，及時發現失敗或異常。

範圍：

涵蓋 Databricks 提供的各種監控工具與 通知機制。

監控: 使用系統資料表（system tables）或日誌來觀察資源使用、成本、審計紀錄，以及Spark UI、查詢分析 (Query Profiler) 來監視作業執行情況

監控: 涉及利用 Databricks CLI/REST API 獲取工作與管道的狀態資訊，或查詢 Lakeflow 管道日誌 了解每個步驟的執行情形

警報: 在 Databricks SQL 上設定查詢結果警示（SQL Alerts）（例如當某指標查詢結果超出閾值時發送通知）

警報: 透過工作流程設定任務失敗或延遲的通知（可經由工作流程UI直接設定，或使用 Jobs API 與第三方整合來通知)

需要的知識：

熟悉 Spark UI 中的指標，如Stage的執行時間、Task的Shuffle讀寫量等，以判斷瓶頸所在。

了解資源使用監控：例如叢集的 CPU/記憶體 使用率，可以從叢集事件日誌或 Ganglia (在舊版Spark UI) 中獲取。

知道 系統資料表（如 event_log 或 Databricks 資源用量表）的結構，可用 SQL 查詢近期所有作業的耗時與成本。

熟悉 Databricks SQL Alert 的配置，在 SQL編輯器中設置條件觸發郵件。

知道 Jobs 內建通知選項，例如在任務失敗、成功或長時間無響應時發郵件或Webhook通知。

準備方式：

在 Databricks 上執行一個長時間運行的 Spark 作業，打開 Spark UI 觀察整個執行情形，練習解讀執行計劃和各階段統計資料。查看 Databricks 的監控頁面或透過查詢系統資料表來了解叢集的資源用量情況。嘗試建立一個 SQL Alert：例如寫一個查詢監測Delta表的資料品質統計，如果發現不合格率超過閾值則觸發警報。也可以設定 Jobs 的通知，模擬一個故意會失敗的任務，確認是否收到警報電子郵件。透過這些實作來熟悉監控與警報的各項功能。

考試注意事項：

當題目提到效能調優或排解問題，往往隱含需要使用監控工具來找出問題根因。例如，面對一個執行緩慢的查詢，正確答案可能是「使用 Query Profile 或 Spark UI 尋找瓶頸」而不是盲目增加叢集規模。同樣地，若提及資料延遲增加或作業無故失敗，要聯想到設置警報機制。注意區分不同監控工具的用途：系統資料表適合長期趨勢和審計，Spark UI/日誌適合即時除錯，SQL Alert適合資料品質或商業指標監控。

9.除錯與部署（Debugging and Deploying，10%）

考察在 Databricks 平臺上偵錯資料管道問題以及將解決方案部署到生產環境的技能。

偵錯涵蓋如何診斷Spark作業或管道的失敗原因、性能瓶頸

部署則涉及使用 CI/CD 工具將開發完成的管道自動化推送到工作區。

簡言之就是要會找蟲（除錯），也要會推程式碼上線（部署）。

範圍：

能夠運用 Spark UI、叢集日誌、系統表、查詢 Profiler 等工具找出錯誤或性能問題的線索，例如考題可能給出一段錯誤日誌，問你哪裡出問題或下一步該看哪裡。

瞭解 Databricks jobs 提供的 Repair 功能，允許在失敗點重新執行，以及使用參數覆蓋（Parameter Override）調整重跑行為。

在 Lakeflow 管道的調試上，要知道怎麼查看其 事件記錄 (Event Logs) 來診斷問題。

部署重點是 Databricks Asset Bundles 和 Repos/Git 整合。涉及使用 Asset Bundle 將工作區資源（例如Notebook、工作流程定義）打包部署到另一環境，或如何把 Databricks 與 Git (如 GitHub/Azure DevOps) 結合實現 CI/CD。

瞭解使用 Databricks CLI 或 REST API 來自動化部署也是範疇之一。

需要的知識：

熟悉 Spark 常見錯誤訊息和排除方法，例如 OOM（記憶體不足）如何定位（Spark UI 的執行緒dump）、Shuffle read 超時該調哪些配置等。

了解 Databricks 上偵錯的特定工具，如叢集日誌可以在Driver/Executor Log找堆疊訊息，Spark UI 可以查看任務失敗在哪個Stage。

使用 系統表（如 SHOW JOBS 或查 pipeline 事件）來確認任務執行情形。

對 CI/CD 部署，需要知道 Databricks 提供的整合點：

Databricks Repos 用於將 Git 儲存庫內容同步到工作區；

Asset Bundles 允許以基礎碼+設定的方式打包所有資源，以便在不同環境重現。

熟悉 Asset Bundle 的 YAML 格式大概長什麼樣，以及如何用 CLI 將它部署。

了解 Jobs API 可用於程式化地建立、更新 Jobs，以及 Workspace API 匯入 Notebook 等操作，因為這些可以融入 CI/CD 腳本。

準備方式：

模擬失敗案例來練習偵錯：

例如資料轉換中引入除零錯誤，觀察 Spark 作業失敗日誌長什麼樣

引入結構不符的資料，查看 Spark UI 的錯誤訊息以及 Lakeflow pipeline 的 event log 是否提示問題所在。

練習使用 Databricks CLI：例如導出一個 Notebook 或啟動一個 Job，熟悉 CLI 參數。

建立簡單 CI/CD 流程: 將 Notebook 放入 Git 儲存庫，使用 Databricks Repos 同步，然後修改程式碼推送，再在 Databricks 上執行工作流程，確保改動順利部署。

了解 Asset Bundle，把數個Jobs和資源定義在一個 bundle 中部署到 workspace。

考試注意事項：

除錯題可能給你錯誤日誌片段，選項則是可能的原因或解決辦法，要能快速定位問題核心（例如 NullPointerException 通常跟資料schema或UDF有關；Stage hang 可能是資料倾斜）。

千萬注意關鍵字（比如 Broadcast, Shuffle 等）暗示了什麼問題。

部署題重在流程理解，如問「如何將Notebook自動部署到多個環境」，正確答案應包含使用 Repos 或 Bundles。

可能考對 Databricks 平臺特定CI/CD功能的了解，例如 Asset Bundle 相較手動配置的優點。答題時，條理清晰地選出既能解決問題又符合平臺最佳實踐的選項。