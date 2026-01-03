# Development Tasks Tracker

## Phase 1: Project Foundation

### Task 1.1: Folder Structure Setup
建立完整的目錄結構，參考 dev-spec.md 第 3 節。

**Requirements:**
- [x] 建立 docs/ 及其子目錄 (exam-map/, core-knowledge/, mistakes/)
- [x] 建立 question-bank/ 及其子目錄 (by-topic/, by-mock/, _template/)
- [x] 建立 prompts/ 及其子目錄 (copilot/, team/)
- [x] 建立 skills/ 及其子目錄 (no-script/, scripted/)
- [x] 建立 progress/ 及其子目錄 (individuals/, team-dashboard.md)
- [x] 建立 tooling/ 目錄
- [x] 在所有空目錄中加入 .gitkeep 檔案

**Deliverables:**
- 完整的資料夾樹狀結構
- 可透過 `tree -L 3` 驗證結構正確性

---

### Task 1.2: Template Files Creation
建立標準化的題目與解析模板。

**Requirements:**
- [x] question-bank/_template/question-template.md
  - 欄位：題目編號、來源、描述、選項、標籤
- [x] question-bank/_template/analysis-template.md
  - 區塊：考點識別、正解說明、錯誤選項排除、記憶法、官方文件引用

**Deliverables:**
- 2 個模板檔案
- 每個模板包含詳細欄位說明與填寫範例

---

### Task 1.3: Core Documentation
建立專案核心文件。

**Requirements:**
- [x] README.md
  - 專案目的與核心原則（參考 dev-spec.md 第 1-2 節）
  - 快速開始指南（實際可執行的指令）
  - 資料夾結構說明

- [x] tooling/contribution-guide.md
  - PR 提交規範
  - 內容審核標準
  - 範例 PR 描述模板

- [x] tooling/tagging-schema.md
  - Topic tags 命名規則
  - Trap tags 定義
  - Level tags 分級標準

**Deliverables:**
- 3 個文件檔案
- README 包含至少 1 個完整的使用範例

---

## Acceptance Criteria (Phase 1)
- [x] 所有資料夾結構符合 dev-spec.md 第 3 節定義
- [x] 模板檔案可直接複製使用（包含範例內容）
- [x] README 可讓新成員在 5 分鐘內理解專案目的
- [ ] 所有變更已提交至 Git

---

## Next Phase Preview
Phase 2 將包含：
- No-Script Skills 開發（Prompt 檔案）
- Scripted Skills 開發（Python 腳本）
- 範例題目與解析



## Phase 2: Core Skills Development

### Task 2.1: No-Script Skills - Prompt Files
建立基於 Prompt 的邏輯技能定義。

**Requirements:**
- [x] skills/no-script/solve-question.md
  - 功能：解析單一題目，產出符合 analysis-template 的內容
  - 包含：輸入格式、輸出結構、使用範例
  - 重點：逐項排除邏輯的 Prompt 示範

- [x] skills/no-script/explain-why-not.md
  - 功能：深度拆解錯誤選項的迷惑點
  - 包含：輸入（題目 + 錯誤選項編號）、輸出（拆解分析）

- [x] skills/no-script/generate-variants.md
  - 功能：產生情境變形題
  - 包含：輸入（原題 + 考點）、輸出（3-5 題變形 + 解析）

**Deliverables:**
- 3 個 Markdown Prompt 檔案
- 每個檔案包含至少 1 個完整使用範例

---

### Task 2.2: Scripted Skills - Python Scripts
建立自動化處理腳本。

**Requirements:**
- [x] skills/scripted/mock_exam_grader.py
  - 功能：批改模擬卷，產出錯題報告
  - CLI: `--input <yaml> --user <name> --output <path>`
  - 錯誤處理：YAML 格式異常、檔案不存在

- [x] skills/scripted/tag_and_file.py
  - 功能：自動分類題目到 by-topic/ 目錄
  - CLI: `--source <dir> --dry-run`
  - 邏輯：基於題目內容的關鍵字匹配

- [x] skills/scripted/team_weakness_dashboard.py
  - 功能：彙整團隊弱點分析
  - CLI: `--individuals-dir <path> --output <file>`
  - 輸出：Markdown 格式的統計報表

**Deliverables:**
- 3 個 Python 腳本檔案
- 每個腳本包含：
  - 完整的 docstring 與型別提示
  - argparse CLI 介面
  - 基本錯誤處理
- 至少 1 個腳本有對應的 pytest 測試檔

---

### Task 2.3: Example Content
建立範例內容供參考使用。

**Requirements:**
- [x] question-bank/by-topic/delta-lake/example-001.md
  - 實際展示如何使用 question-template
  - 包含完整的解析內容

- [x] docs/core-knowledge/delta-lake-cheatsheet.md
  - Delta Lake 核心概念速查表
  - 以表格呈現關鍵 API 與配置

**Deliverables:**
- 1 個範例題目（含解析）
- 1 個技術 Cheatsheet

---

## Acceptance Criteria (Phase 2)
- [x] 所有 Prompt 檔案清晰易懂，可直接使用
- [x] Python 腳本可獨立執行（含 --help）
- [x] 至少有 1 個測試檔案且測試通過
- [x] 範例內容品質符合實際使用需求
- [ ] 所有變更已提交至 Git