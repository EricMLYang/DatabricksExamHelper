# 近期 Commit 變更整理（DatabricksExamHelper）

## 範圍
整理最近 5 筆 commit 的變更重點（2026-02-06 ～ 2026-02-07）。

---

## 主要新增/更新

### 1) 核心知識速記文件擴充
- Auto Loader schema evolution / schema location
- Auto Loader bad records 處理
- availableNow vs batch 模式對比
- Structured Streaming 非時間視窗限制
- Delta CDC + MERGE 語法
- Delta deep clone incremental 方法
- System billing usage 查詢
- Spark UI SQL metrics
- PySpark window functions
- Unity Catalog 權限與遮罩語法
- Delta Sharing 認證機制
- Delta Time Travel 語法
- 高頻 CLI 指令補充

### 2) 題目解析與不熟題目清單
- 更新 Q-009、Q-011、Q-020、Q-033、Q-044 等題目
- 維護不熟題目清單（b4 Q-028 ~ Q-042）

### 3) 文章與心得整理
- 新增「考試複習系統化方法論分享」
- 精簡「考試複習工具心得」內容，聚焦 Databricks 考試準備

## 近期重點方向
- 持續把題目解析沉澱成速記筆記，降低重複學習成本
- 針對考點高頻區域（Streaming、Auto Loader、Delta、UC）加密整理
- 建立可複用的學習資產與整理流程

---

## 近期變更聚焦的 Databricks 主題
- **Streaming / Structured Streaming**：trigger、availableNow、非時間視窗限制、資料品質隔離
- **Auto Loader / Schema 管理**：schemaLocation、schemaEvolution、badRecordsPath
- **Delta Lake 核心能力**：Time Travel、DEEP CLONE 增量同步、MERGE CDC
- **Delta Sharing / CDF**：分享歷史、增量變更存取
- **Unity Catalog / 權限治理**：權限與遮罩語法、UC Sharing 認證
- **效能與成本監控**：`system.billing.usage` 的 DBU 解析
