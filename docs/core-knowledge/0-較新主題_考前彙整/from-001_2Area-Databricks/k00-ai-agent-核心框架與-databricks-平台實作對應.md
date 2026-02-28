# AI Agent 核心框架與 Databricks 平台實作對應

---



本文檔旨在將 AI Agent 的八大核心抽象框架，與 Databricks 平台上對應的具體服務和工具進行映射，以利於在該平台上構建企業級 AI Agent 系統。



#### 1\. 推理引擎 (Reasoning Engine) - Agent 的大腦



- **核心 Databricks 服務**:

   - **Foundation Model API**: 提供對 Llama 3, Claude 等頂級模型的統一、按用量付費的 API 接口。

   - **Model Serving**: 用於部署自訂或開源的 LLM，提供高吞吐量的即時推理端點。

- **主要功能**: 作為 Agent 的決策核心，負責理解指令、規劃步驟和生成回應。



#### 2\. 工具 (Tools / Function Calling) - Agent 的雙手



- **核心 Databricks 服務**:

   - **Unity Catalog (UC) Functions ⭐**: 將 SQL 查詢和 Python 程式碼註冊為受治理、可重用的工具，是連接 Agent 與數據的關鍵。

   - **MCP (Model Context Protocol) Servers**: 提供標準化的工具接口，用於連接向量搜尋、UC Functions、Genie (結構化查詢) 和外部 API。

- **主要功能**: 讓 Agent 從「只能說」變成「能做事」，能夠查詢數據、執行計算、調用外部系統。



#### 3\. 記憶 (Memory) - Agent 的知識庫與經驗



- **核心 Databricks 服務**:

   - **Mosaic AI Vector Search ⭐**: (長期向量記憶) 將文件、知識庫等非結構化數據索引化，為 Agent 提供 RAG (檢索增強生成) 的能力。

   - **Delta Lake / Unity Catalog Tables**: (長期結構化記憶) 儲存對話歷史、用戶偏好、歷史指標等結構化數據。

   - **Feature Serving**: 提供毫秒級的即時上下文查詢。

- **主要功能**: 賦予 Agent 持久的記憶，使其能夠聯繫上下文、實現個人化並從歷史中學習。



#### 4\. 規劃與控制流 (Planning & Control Flow) - Agent 的策略與執行緒



- **核心 Databricks 服務**:

   - **Databricks Workflows ⭐**: 用於編排複雜、多步驟的任務，管理任務依賴、條件分支和失敗重試。

   - **Agent Frameworks (如 LangGraph)**: 在 Agent 內部管理狀態和決策流程。

   - **Delta Live Tables / Streaming**: 用於事件驅動和即時數據管道的控制流。

- **主要功能**: 確保 Agent 能夠可靠、穩定地執行複雜任務，是系統穩定性的基石。



#### 5\. 感知 (Perception) - Agent 的感官



- **核心 Databricks 服務**:

   - **Unity Catalog Metadata**: 讓 Agent 能夠自動理解數據庫的 Schema、欄位和關聯。

   - **多模態模型支持**: 處理文字、圖像等多種類型的輸入。

   - **DLT 資料品質監控**: 感知數據的品質狀態。

- **主要功能**: 使 Agent 能夠理解其所處的環境和接收到的各類資訊。



#### 6\. 行動 (Action) - Agent 的實際操作



- **核心 Databricks 服務**:

   - **Lakeguard**: 提供沙箱化的安全代碼執行環境。

   - **Notebooks / Jobs**: 提供互動式或排程化的執行環境。

   - **Delta Lake ACID Transactions**: 確保數據操作的可靠性。

- **主要功能**: 提供 Agent 執行決策所需的安全、可靠的計算與數據操作環境。



#### 7\. 評估與反思 (Evaluation & Reflection) - Agent 的自我進化機制



- **核心 Databricks 服務**:

   - **Mosaic AI Agent Evaluation ⭐**: 提供 AI 輔助評分、專家反饋 App 等工具，系統性地評估和衡量 Agent 的回應品質。

   - **MLflow Tracing**: 記錄 Agent 的每一步推理和工具調用，實現完整的可觀測性。

   - **Agent Monitoring & Inference Tables**: 在生產環境中持續監控 Agent 品質並記錄所有請求，用於稽核和持續改進。

- **主要功能**: 建立一個完整的反饋閉環，讓 Agent 的表現可以被量化、監控和持續優化。



#### 8\. 治理層 (Governance) - 貫穿所有環節的基礎



- **核心 Databricks 服務**:

   - **Unity Catalog**: 提供統一的數據和 AI 資產治理，包括權限管理 (ACLs)、數據血緣 (Lineage) 和稽核日誌 (Audit Logs)。

- **主要功能**: 確保 Agent 系統的開發與運行在一個安全、合規、可控的環境中。

---



### 場景應用實例




| 場景 | 核心框架元件 | 對應 Databricks 服務 | 
|---|---|---|
| **每日報表生成** | 推理、工具、記憶、控制流 | Foundation Model API, UC Function (SQL), Vector Search, Databricks Workflow | 
| **異常檢測與通知** | 推理、工具、記憶、控制流 | Foundation Model API, UC Function (Python), MCP (通知), Delta Table, Streaming | 
| **互動式資料查詢** | 推理、工具、記憶、規劃 | Foundation Model API, Genie MCP, UC Functions, Vector Search, Feature Serving, LangGraph | 



### 總結



Databricks 平台為 AI Agent 核心框架的每一個元件都提供了原生、深度整合的解決方案。從底層的數據治理 (Unity Catalog)、記憶儲存 (Delta Lake, Vector Search)，到核心的工具執行 (UC Functions) 和推理 (Model Serving)，再到上層的流程編排 (Workflows) 與品質評估 (Agent Evaluation)，構成了一個端到端、生產級的 AI Agent 開發與部署平台。


