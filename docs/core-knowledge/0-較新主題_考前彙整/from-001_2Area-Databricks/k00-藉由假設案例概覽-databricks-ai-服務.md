# 藉由假設案例概覽 Databricks AI 服務

用最小可行的 RAG 問答機器人為起點，逐步把 AI 服務在 Databricks 上建好、上線、並可持續監控與優化

全程以步驟呈現；每一步只要提到 Databricks 服務，就補充它是什麼、解決什麼問題。



# **假設場景**

- 目標：「公司產品 FAQ」的 RAG 問答機器人，回答內部同仁與一線客服的常見問題，並附上來源段落

- 成功指標: 

   - 答案可追溯來源

   - 平均延遲 < 2 秒

   - 前 30 天無 PII (Personally Identifiable Information) 外洩

   - Top-k=3  ( 被挑出來過 LLM ) ，Top-1( 最終回覆 ) 命中率 ≥ 70%

      - 衡量 RAG「答案品質」的技術指標

---





## **步驟 0｜定義邊界與成功指標**

- 定義了這個系統「如何被治理」以及「如何可持續」

- 產出：

   - 功能邊界（只回答產品 FAQ）

   - 允許的資料範圍（內部 PDF 與 Wiki 匯出）

   - 禁止主題（如：法律/投資建議）

- 指標：

   - 品質:

      - 命中率: 衡量答案「正確與否」

      - 忠實度: 衡量答案是否「忠於原文」

   - 效能（P50/P95 延遲、錯誤率）

      - P50 (中位數)： 代表你 50% 的使用者所體驗到的「典型速度」

      - P95 (95百分位)： 代表你 95% 的使用者所體驗到的「最差速度」。這才是真正決定使用者「體感」和「挫折感」的指標

   - 成本: 每百次請求成本 ( 控制 Token, 換模型 ...)

---



## **步驟 1｜建立專案治理基礎（Unity Catalog）**

- 動作：在 UC 建立 catalog.schema 作為專案命名空間；建立群組與物件層級 ACL；限制誰能讀寫資料/模型/索引。

- 用到的服務

   - **Unity Catalog（UC）**：Databricks 的統一治理層。集中管理資料、檔案、向量索引、模型的權限、稽核與血緣。

   - **UC Volumes**：在 UC 下管理非結構化檔案（PDF、TXT、HTML 匯出）。所有 RAG 原始檔案放這裡，統一受 UC 控制。

   - ACL 是「**存取控制列表**」(Access Control List) 的縮寫

   

---



## **步驟 2｜上傳原始文件到 UC Volumes（資料進來）**

- 動作：將產品手冊、FAQ、內部知識文件（PDF/TXT/HTML）存到 UC Volumes；建立最基本的檔名與類別目錄結構；禁止含 PII 的檔案上傳。

- 用到的服務

   - **UC Volumes**：統一存放原始文件的位置，後續 Parser 直接讀這裡。

---





## **步驟 3｜文件解析、分塊、寫入 Delta 表（資料準備）**

- 動作：Notebook 內用 parser（如 unstructured/beautifulsoup4 等）把 PDF/HTML 轉文字 → 依段落/標題規則「分塊」→ 生成「一塊一列」的結構化資料，包含 doc_id、chunk_id、text、metadata(page/section/path) → 寫成 **Delta Table**（例：genai_docs_chunked）。

- 用到的服務

   - **Delta Lake（Delta Table）**：Databricks 的湖倉表格格式。提供交易一致性、快照、快讀快寫，做為之後向量索引的來源表。

   

---



## **步驟 4｜建立向量索引（Vector Search + Delta Sync Index）**

- 動作：建立 **Vector Search Endpoint**，針對 genai_docs_chunked 建 **Delta Sync Index**，指定 Embedding 模型；設定要同步的欄位（文字與必要的 metadata）；打開自動同步。

- 用到的服務

   - **Vector Search**：Databricks 內建的向量資料庫與搜尋服務，用來儲存/查詢 Embeddings。

   - **Delta Sync Index**：Vector Search 的自動增量同步模式。來源 Delta 表一更新，索引自動更新，無需手動 ETL。

> 重點：用 Delta Sync，而不是手動把 Embeddings push 進索引，減少維運。

---



## **步驟 5｜原型檢索鍊（RAG 棧：檢索 → 重組 → 生成）**

- 動作：寫一段最小的 RAG 程式：

   1. 根據使用者問題查 Vector Search（top-k=3）

   2. 將問題 + 檢索到的 chunks 組成 Prompt

   3. 呼叫基礎模型生成回答，附上來源標註

   4. 先在 Notebook 互動測試（幾組真實問題）

   

- 用到的服務

   - **Vector Search**：提供近似度檢索 API，回傳最相關的文本塊與 metadata。

   - **（可選）Databricks Foundation Models / 外部模型**：在 Notebook 內先用 Serverless 模型端點或外部 API 測試生成效果。

---





## **步驟 6｜提示工程與結構化輸出（Application Development）**

- 動作：把 Prompt 模板化；要求模型輸出固定 JSON（answer、citations\[\]、confidence 等）；加入「不得回覆未授權主題」等系統提示；調整 few-shot 範例讓輸出更穩定。

- 用到的服務

   - **MLflow Tracking**：把每次實驗的 Prompt 版本、top-k、chunk 大小、模型名稱、評分結果記錄下來，便於回溯與比較。

---





## **步驟 7｜封裝為 MLflow PyFunc（可部署單元）**

- 動作：把「前處理（查向量/組 Prompt）＋ 模型呼叫 ＋ 後處理（解析 JSON、裁切超長輸出）」封裝成 **MLflow PyFunc 模型**；mlflow.log_model() 記錄版本；mlflow.register_model() 註冊到 UC Model Registry。

- 用到的服務

   - **MLflow Models / Registry（UC）**：標準化打包與版本管理。之後就能一鍵部署到 Serving，並用 Staging/Production 階段切換。

---





## **步驟 8｜上線服務（Model Serving）**

- 動作：從 UC Registry 指定版本，一鍵建立 **Model Serving Endpoint**；低流量先採 **Pay-per-token（Serverless）**，量大或嚴格延遲再評估 **Provisioned Throughput**。

- 選項：開啟回應截斷、請求大小限制、超時；設定並發與速率限制；必要時做輸入/輸出遮罩（移除 PII）。

- 用到的服務

   - **Model Serving**：把模型變成可擴展的 REST API。支援 Serverless（按用量計費）與預留吞吐（低延遲、固定成本）。

---





## **步驟 9｜啟用自動監控（Inference Tables + Tracing）**

- 動作：在 Endpoint 上打開 **Inference Tables**；所有請求/回應、延遲、錯誤會自動寫到 UC 管控的 Delta 表。開啟 **MLflow Tracing** 以追蹤每次請求內部的檢索/生成步驟。用 SQL 建簡單 Dashboard（流量、延遲、錯誤率、成本估算）。

- 用到的服務

   - **Inference Tables**：Model Serving 的原生記錄功能，無需自寫 logging。

   - **MLflow Tracing**：把一次推論的內部步驟（檢索的內容、模型回合）具體化，利於除錯與品質分析。

---





## **步驟 10｜離線評估（品質保證）**

- 動作：建立離線評測集（真實問題、標準答案、允許參考來源）；對「檢索器」與「生成器」分別評測：

   - 檢索：是否取回正確 chunk（Recall@k，MRR）

   - 生成：忠實度/相關性（可用 LLM-as-a-Judge 自動評分）

   

- 用到的服務

   - **MLflow Tracking**：紀錄每次離線評測的指標與參數；比較不同設定（chunk 大小、重疊、top-k、prompt 版本、模型版本）。

---





## **步驟 11｜治理強化（安全護欄與權限）**

- 動作：

   - UC 權限最小化：Volumes、Delta 表、向量索引、模型皆用群組授權；稽核可查。

   - **Safety/Guardrails**：在系統提示與中介層做輸入/輸出過濾（禁止主題、敏感字詞、拒答策略）。

   - 機密管理：API Keys 與連線字串放雲端祕密管控（依組織做法）。

> 用到的服務：**Unity Catalog**（物件權限與稽核）；Guardrails 可在應用層/Serving 前置邏輯落實。

---





## **步驟 12｜迭代優化（效能、成本、品質）**

- 動作：

   - 依 Inference Tables 的真實流量調整 Serving 模式與並發；必要時改成 Provisioned Throughput 降 P95 延遲。

   - 針對常見查詢加 metadata filter（產品線、版本、語言）降低無關檢索。

   - 調整 Chunk 策略與 top-k；加重排序（re-ranking）提高命中。

   - Prompt 版本化；Few-shot 以實際錯題集更新。

   - 觀測成本/請求，設計快取（對重複問題回應快取）。

> 用到的服務：**Vector Search**（metadata filter、索引重建）、**MLflow**（實驗對照）、**Model Serving**（配額/並發/模式切換）。

---





## **步驟 13｜擴充到「即時資料」與「更高階任務」（選做）**

- 需求一：答案需結合即時庫存或定價

   - **Feature Serving**：以極低延遲讀取 Delta 表中的即時特徵（如庫存/價格），在 PyFunc 前處理階段合併進 Prompt。

   

- 需求二：跨工具多步任務（發 Ticket、查 API、貼 Slack）

   - **Agent（在應用層）**：用工具調用把 RAG 納入多步流程。Serving 仍用 PyFunc 打包，維持治理與監控一致。

---





# **最小資料與物件清單（可直接照做）**

- UC 名稱空間：genai_prod.catalog / genai_prod.schema

- UC Volumes：genai_prod.schema:/volumes/docs_raw

- Delta 表：genai\_[prod.schema.docs](prod.schema.docs)\_chunked

   - 必要欄位：doc_id, chunk_id, text, page_no, section, source_path, created_at

- Vector Search

   - Endpoint：vs-faq

   - Delta Sync Index：來源 docs_chunked，同步欄位 text + metadata，metadata 含 doc_id/page_no/source_path

- MLflow Model（PyFunc）：genai_prod.schema.rag_faq:1（UC Registry）

- Model Serving Endpoint：rag-faq-endpoint（先用 Pay-per-token）

- Inference Tables：對 rag-faq-endpoint 啟用

- Dashboards：延遲/錯誤率/成本與品質趨勢（讀 Inference Tables + 評測結果表）

---



# **驗收檢查表（上線前後各一次）**

- 功能：Top-1 命中率 ≥ 70%，回答均附來源；禁止主題已生效。

- 效能：P95 < 2s，錯誤率 < 0.5%。

- 成本：單次請求成本在預算內；高峰不超限。

- 治理：UC 權限與稽核 OK；Inference Tables 寫入正常；Secrets 不落盤。

- 可維運：MLflow 版本可回滾；向量索引自動同步正常；Dashboard 能反映最新流量與品質。

---



這份步驟清單可直接作為你們的「最小可行路徑」。先完成 0–9 就能有一個穩定可監控的 RAG 問答服務；之後再逐步做 10–13，把品質、成本與功能往上推。