# Databricks Cert Agent Repo (GitHub Copilot + Agent Skills) 專案規格書

## 1. 規劃目的

建立一個基於 GitHub Copilot 的團隊協作框架，將 Databricks 認證考試轉化為「可版本化」、「可複習」且「可持續迭代」的知識資產。透過 Agent Skills 規範輸出品質，達成團隊內部「輸出一致、弱點共享、自動化訓練」的目標。

## 2. 核心原則

* **輸出一致性**：所有題目解析需符合統一模板，確保邏輯排除、術語口徑一致。
* **知識資產化**：題庫與解析透過 Git 管理，利用 PR 流程進行內容審核（Review），形成方法論。
* **自動化閉環**：建立「解析 → 標籤 → 統計 → 衝刺」的自動化路徑，降低人工整理負擔。

---

## 3. Repo 資料夾結構

```text
databricks-cert-agent/
├── README.md                   # 專案說明與快速上手指南
├── docs/                       # 核心知識庫
│   ├── 00-start-here.md        # 學習路徑與進度導引
│   ├── exam-map/               # 考綱與考點映射表
│   ├── core-knowledge/         # 主題式速查表 (Cheatsheets)
│   └── mistakes/               # 錯誤模式與常見陷阱庫
├── question-bank/              # 標準化題庫
│   ├── by-topic/               # 按技術標籤分類 (e.g., Delta, Streaming)
│   ├── by-mock/                # 按模擬試卷分類
│   └── _template/              # 題目與解析 Markdown 標準模板
├── prompts/                    # Agent 指令集
│   ├── copilot/                # 個人日常練習 Prompts
│   └── team/                   # 團隊規範與風格 Prompts
├── skills/                     # Agent 核心技能
│   ├── no-script/              # 基於 Prompt 的邏輯技能 (Markdown 產出)
│   └── scripted/               # 基於 Script 的自動化技能 (Python/Bash)
├── progress/                   # 進度追蹤
│   ├── individuals/            # 個人錯題紀錄與學習日誌
│   └── team-dashboard.md       # 團隊整體弱點分析報表
└── tooling/                    # 工具配置
    ├── contribution-guide.md   # PR 與貢獻規範
    └── tagging-schema.md       # 標籤規則 (Topic/Trap/Level)

```

---

## 4. Agent 主要功能 (Roadmap)

### 第一階段：知識與題庫體系化

* **Exam Map**: 建立考綱到具體考點的雙向索引。
* **Standardized Q&A**: 每一題解析必須包含：考點、關鍵字、正解說明、排除理由、記憶法、官方文件引用。

### 第二階段：個人化訓練與衝刺

* **弱點雷達**: 透過錯題標籤統計，識別個人與團隊的技術盲區。
* **變形題訓練**: 針對高頻錯題，利用 Agent 自動生成情境變體，防止死背答案。

### 第三階段：團隊協作與自動化

* **Peer Review**: 解析需經過 PR Review 確保品質。
* **Auto-Grader**: 腳本化批改模擬卷並自動更新進度報表。

---

## 5. Prompt 指令集規劃

### Copilot Prompts (個人日常)

* **`solve-question`**: 依照標準模板解析題目，著重「逐項排除邏輯」。
* **`generate-variants`**: 選定考點，產出 3-5 題情境變形題與解析。
* **`note-to-exam`**: 將散亂的技術筆記轉換為 MCQ 考題與 Flashcards。
* **`sprint-mode`**: 根據弱點標籤，生成 7 天考前衝刺菜單。

### Team Prompts (團隊規範)

* **`style-check`**: 檢查解析內容是否符合 `answer-style-guide.md` 規範。
* **`tag-standardizer`**: 確保標籤命名符合 `tagging-schema.md`，避免標籤發散。

---

## 6. Skills 核心技能定義

### A. 邏輯型技能 (No-Script)

* **`explain-why-not`**: 深度拆解錯誤選項的混淆點。
* **`wrong-answer-review`**: 將錯題轉化為「可執行的補強規則」。
* **`flashcards-generator`**: 產出結構化 Q&A 卡片。

### B. 自動化型技能 (Scripted)

* **`mock-exam-grader`**: 讀取答案檔，產出得分率與弱點排序路徑。
* **`tag-and-file`**: 自動識別題目內容，上標籤並搬移至正確資料夾。
* **`team-weakness-dashboard`**: 彙整所有成員的錯題標籤，生成團隊補坑指南。
* **`anki-exporter`**: 將 Flashcards 轉換為 Anki 或 Quizlet 可匯入格式。

---

## 7. 建議落地優先序

1. **Phase 1 (MVP)**:
* 完成資料夾結構與 `_template`。
* 部署核心 `solve-question` 與 `explain-why-not` 技能。
* 手動建立第一批 Core Knowledge 骨架。


2. **Phase 2 (Efficiency)**:
* 實作 `mock-exam-grader` 與 `team-weakness-dashboard`。
* 導入 PR Review 流程，累積高品質解析。


3. **Phase 3 (Automation)**:
* 開發 `tag-and-file` 自動整理腳本。
* 串接 `anki-exporter` 達成跨平台複習。