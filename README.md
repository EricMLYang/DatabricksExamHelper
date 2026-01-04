## 📖 專案目的

本專案建立一個基於 **GitHub Copilot** 與 **Agent Skills** 的團隊協作框架，目標是：

1. **知識資產化** - 透過 Git 管理題庫與解析，利用 PR 流程確保內容品質
2. **輸出一致性** - 所有題目解析符合統一模板，邏輯排除清晰、術語一致
3. **自動化閉環** - 建立「解析 → 標籤 → 統計 → 衝刺」的自動化訓練路徑

### 核心原則

| 原則 | 說明 |
|------|------|
| **輸出一致性** | 所有題目解析需符合統一模板，確保邏輯排除、術語口徑一致 |
| **知識資產化** | 題庫與解析透過 Git 管理，利用 PR 流程進行內容審核 (Review)，形成方法論 |
| **自動化閉環** | 建立「解析 → 標籤 → 統計 → 衝刺」的自動化路徑，降低人工整理負擔 |

---

## 🚀 快速開始

### 前置需求
- Git 已安裝並設定好
- （選填）GitHub Copilot 訂閱（用於 Agent Skills）
- （選填）Python 3.8+ （用於自動化腳本）

### 1. 建立第一個題目

複製模板並填寫題目：

```bash
# 複製題目模板
cp question-bank/_template/question-template.md \
   question-bank/by-topic/Q-PRACTICE-001-question.md

# 複製解析模板
cp question-bank/_template/analysis-template.md \
   question-bank/by-topic/Q-PRACTICE-001-analysis.md
```

使用編輯器開啟檔案，依照模板中的註解說明填寫內容。

### 2. 檢視模板結構

```bash
# 檢視題目模板
cat question-bank/_template/question-template.md

# 檢視解析模板
cat question-bank/_template/analysis-template.md
```

### 3. 提交變更

```bash
git add question-bank/by-topic/Q-PRACTICE-001-*.md
git commit -m "Add: Q-PRACTICE-001 Delta Lake VACUUM 題目與解析"
git push origin main
```

### 4. 檢視標籤規範

```bash
# 查看標籤命名規則
cat tooling/tagging-schema.md

# 查看貢獻指南
cat tooling/contribution-guide.md
```

---

## 📁 資料夾結構

```text
databricks-cert-agent/
├── README.md                   # 📘 專案說明與快速上手指南
├── dev-spec.md                 # 📐 專案規格書（技術規劃）
├── dev-tasks.md                # ✅ 開發任務追蹤
│
├── docs/                       # 📚 核心知識庫
│   ├── exam-map/               #    考綱與考點映射表
│   ├── core-knowledge/         #    主題式速查表 (Cheatsheets)
│   └── mistakes/               #    錯誤模式與常見陷阱庫
│
├── question-bank/              # 📝 標準化題庫
│   ├── by-topic/               #    按技術標籤分類 (e.g., Delta, Streaming)
│   ├── by-mock/                #    按模擬試卷分類
│   └── _template/              #    題目與解析 Markdown 標準模板
│       ├── question-template.md   # 題目模板
│       └── analysis-template.md   # 解析模板
│
├── prompts/                    # 💬 Agent 指令集
│   ├── copilot/                #    個人日常練習 Prompts
│   └── team/                   #    團隊規範與風格 Prompts
│
├── skills/                     # 🤖 Agent 核心技能
│   ├── no-script/              #    基於 Prompt 的邏輯技能 (Markdown 產出)
│   └── scripted/               #    基於 Script 的自動化技能 (Python/Bash)
│
├── progress/                   # 📊 進度追蹤
│   └── individuals/            #    個人錯題紀錄與學習日誌
│
└── tooling/                    # 🛠️ 工具配置
    ├── contribution-guide.md   #    PR 與貢獻規範
    └── tagging-schema.md       #    標籤規則 (Topic/Trap/Level)
```

---

## 🎯 使用場景

### 場景 1: 新增題目與解析

**目標:** 將練習遇到的題目標準化，建立可複習的知識資產

**步驟:**
1. 複製 `question-bank/_template/question-template.md`
2. 填寫題目內容、選項、標籤
3. 複製 `question-bank/_template/analysis-template.md`
4. 逐項分析正解與錯誤選項
5. 提交 PR，經團隊 Review 後合併

**範例指令:**
```bash
# 建立新題目（Delta Lake 相關）
cp question-bank/_template/question-template.md \
   question-bank/by-topic/Q-DELTA-015-question.md

# 建立對應解析
cp question-bank/_template/analysis-template.md \
   question-bank/by-topic/Q-DELTA-015-analysis.md

# 編輯後提交
git add question-bank/by-topic/Q-DELTA-015-*.md
git commit -m "Add: Q-DELTA-015 Delta Lake MERGE 指令題目"
git push origin feature/q-delta-015
```

---

### 場景 2: 檢視特定主題的所有題目

**目標:** 針對弱點主題（如 Streaming）集中複習

**步驟:**
1. 使用 `grep` 搜尋特定標籤
2. 開啟相關題目與解析
3. 記錄錯題至個人進度追蹤

**範例指令:**
```bash
# 搜尋所有 Streaming 相關題目
grep -r "Streaming" question-bank/by-topic/ | grep "Topics:"

# 列出所有 L3-Advanced 難度題目
grep -r "L3-Advanced" question-bank/by-topic/
```

---

### 場景 3: 團隊弱點分析

**目標:** 識別團隊整體的技術盲區，規劃補強計畫

**步驟:**
1. 收集所有成員的錯題標籤
2. 執行 `team-weakness-dashboard` 技能（Phase 2 開發）
3. 產出團隊補坑指南

**預期輸出 (Phase 2):**
```bash
python skills/scripted/team-weakness-dashboard.py

# 輸出範例：
# Top 3 Team Weaknesses:
# 1. Streaming (18 errors across 5 members)
# 2. Unity Catalog Permissions (12 errors across 4 members)
# 3. Delta Lake Optimization (9 errors across 3 members)
```

---

## 🧩 模板說明

### 題目模板 (question-template.md)

包含以下欄位：
- **題目編號** - 唯一識別碼 (格式: `Q-{來源}-{序號}`)
- **來源** - Official / Mock / Community / Real Exam Recall
- **難度等級** - L1-Basic / L2-Intermediate / L3-Advanced
- **題幹與選項** - 清楚描述問題與所有選項
- **標籤系統** - Topic Tags, Trap Tags, Knowledge Domain
- **答案與解析連結** - 正確答案與對應解析檔案

**範例:**
```markdown
**ID:** `Q-MOCK01-023`
**來源:** Mock Exam - Databricks Certified Data Engineer Associate
**難度:** `L2-Intermediate`
**Topics:** `Delta-Lake`, `Data-Retention`, `Storage-Management`
**正解:** `B`
```

---

### 解析模板 (analysis-template.md)

包含以下區塊：
- **📍 考點識別** - 主要與次要考點
- **✅ 正解說明** - 技術原理、符合需求、實務應用
- **❌ 錯誤選項排除** - 逐一拆解每個錯誤選項
- **🧠 記憶法與解題技巧** - 記憶口訣、解題步驟、陷阱警示
- **📚 官方文件與延伸閱讀** - 權威參考來源

**範例:**
```markdown
## 🧠 記憶法與解題技巧
### 記憶口訣
"VACUUM 吸塵器，清理舊檔案；RETAIN 加小時，天數要乘 24"

### 常見陷阱警示
⚠️ **陷阱 1:** 時間單位混淆 - VACUUM 只接受 HOURS，需自行換算
```

---

## 🤝 貢獻指南

我們歡迎所有形式的貢獻！請遵循以下規範：

### 提交 PR 前檢查
- [ ] 題目與解析使用標準模板
- [ ] 標籤符合 `tooling/tagging-schema.md` 規範
- [ ] 解析包含官方文件引用
- [ ] 錯誤選項有明確的排除邏輯
- [ ] 通過團隊 Review

### PR 命名規則
- **新增題目:** `Add: Q-{ID} {簡短描述}`
- **修正解析:** `Fix: Q-{ID} {修正內容}`
- **更新文件:** `Docs: {文件名稱} {更新內容}`

**詳細規範請參閱:** [tooling/contribution-guide.md](./tooling/contribution-guide.md)

---

## 📊 專案進度

### Phase 1: Project Foundation ✅ (已完成)
- [x] 建立資料夾結構
- [x] 建立題目與解析模板
- [x] 撰寫核心文件 (README, contribution-guide, tagging-schema)

### Phase 2: Skills Development (進行中)
- [ ] 開發 No-Script Skills (Prompt 檔案)
- [ ] 開發 Scripted Skills (Python 腳本)
- [ ] 建立範例題目與解析

### Phase 3: Automation (規劃中)
- [ ] 實作 `mock-exam-grader` 自動批改
- [ ] 實作 `team-weakness-dashboard` 團隊分析
- [ ] 實作 `anki-exporter` 匯出功能

---

## 📚 相關資源

### Databricks 官方資源
- [Databricks Certified Data Engineer Associate](https://www.databricks.com/learn/certification/data-engineer-associate)
- [Databricks Documentation](https://docs.databricks.com/)
- [Databricks Academy](https://www.databricks.com/learn/training)

### 社群資源
- [Databricks Community Forums](https://community.databricks.com/)
- [Stack Overflow - Databricks Tag](https://stackoverflow.com/questions/tagged/databricks)

---

## 📄 授權

本專案採用 [MIT License](LICENSE)

---

## 🙋 常見問題

### Q: 如何決定題目的難度等級？
A: 參考 `tooling/tagging-schema.md` 中的 Level Tags 定義：
- **L1-Basic:** 基礎概念題（官方文件直接查得到）
- **L2-Intermediate:** 中階應用題（需理解多個概念的組合）
- **L3-Advanced:** 進階情境題（需深入理解運作原理與最佳實踐）

### Q: 題目來源是 Real Exam Recall，可以分享嗎？
A: 請遵守 Databricks 考試保密協議。建議以「類似情境題」或「變形題」方式呈現，避免直接揭露考題內容。

### Q: 如何使用 GitHub Copilot Skills？
A: 詳見 Phase 2 開發文件（開發中）。Skills 將提供 `solve-question`、`explain-why-not` 等 Agent 指令。

### Q: 可以用其他語言撰寫嗎？
A: 本專案使用繁體中文撰寫，以利華語團隊協作。若需其他語言版本，請開 Issue 討論。

---

## 📮 聯絡方式

有任何問題或建議，歡迎：
- 開 [GitHub Issue](https://github.com/your-org/databricks-cert-agent/issues)
- 提交 [Pull Request](https://github.com/your-org/databricks-cert-agent/pulls)
- 聯絡專案維護者: [your-email@example.com](mailto:your-email@example.com)

---

**Happy Learning! 🎓**
