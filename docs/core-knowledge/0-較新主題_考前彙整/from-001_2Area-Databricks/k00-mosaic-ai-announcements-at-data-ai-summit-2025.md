---
tags:
  - databricks
  - llm-application
---
# Mosaic AI Announcements at Data + AI Summit 2025

<https://www.databricks.com/blog/mosaic-ai-announcements-data-ai-summit-2025?hl=en-US>

這篇 **Databricks Data + AI Summit 2025 的 Mosaic AI 新功能公告**，可以歸納成幾個重點方向：



---

### **1\. Agent Bricks（Beta）**

- 只要描述任務 + 連結企業資料，就能自動生成高品質 Agent。

- 支援 **資訊抽取、知識助理、文字轉換、多 Agent 系統**。

- 自動建立測試與優化成本/品質。



---

### **2\. MLflow 3.0（為 GenAI 重構）**

- 新版專為 **生成式 AI 與 Agent 管理**打造。

- **跨平台監控**：能觀測部署在 AWS、GCP、On-Prem 的 Agent。

- **Prompt Registry**：註冊、版本化、測試與部署 LLM Prompt。





---

### **3\. AI Functions in SQL（更快且支援多模態）**

- 效能提升：**速度提升 3 倍，成本降 4 倍**。

- 新增 **文件解析（ai_parse_document）**，從複雜文件中萃取結構化資訊。

- 支援 **跨文字、圖片等多模態數據**。





---





### **4\. Storage-Optimized Vector Search（Public Preview）**

- 架構重寫：**計算與儲存分離**。

- 成本降低 **7 倍**，可支援數十億向量。

- 更適合 **RAG 應用、語義搜尋、文件探索**。





---





### **5\. Serverless GPU Compute（Beta）**

- Databricks Serverless 平台新增 GPU。

- 不需管理基礎設施即可使用 GPU 做 **訓練 / 推理 / 大規模轉換**。

- 支援 **A10g (Beta)**，即將支援 **H100**。





---





### **6\. High-Scale Model Serving**

- 模型服務效能提升：可支援 **25 萬 QPS**。

- 新自研推理引擎，Meta Llama 等模型推理可快 **1\.5 倍**。

- 讓 LLM 部署更快、更便宜、更易於維運。





---





### **7\. MCP Support in Databricks**

- 內建 **Anthropic Model Context Protocol (MCP)** 支援。

- 可在 Databricks App 裡快速部署 **MCP Server**，並在 Playground 測試。

- 已支援 UC Functions、Genie、Vector Search。





---





### **8\. AI Gateway（正式 GA）**

- **AI 服務統一入口**，提供治理、使用監控、安全控制。

- 功能包含 **多供應商自動 fallback、PII 安全防護、Rate Limit 政策**。

- 支援 Databricks 內外部 AI 服務。





---



👉 總結來說，這些更新的方向是：



- **建 Agent 更簡單**（Agent Bricks, MLflow 3.0）

- **AI 效能更快更便宜**（AI Functions, Vector Search, Serverless GPU, Model Serving）

- **跨平台治理與安全更完整**（MLflow observability, AI Gateway, MCP support）





---