# Development Tasks Tracker

## Phase 1: Project Foundation

### Task 1.1: Folder Structure Setup
建立完整的目錄結構，參考 dev-spec.md 第 3 節。

**Requirements:**
- [ ] 建立 docs/ 及其子目錄 (exam-map/, core-knowledge/, mistakes/)
- [ ] 建立 question-bank/ 及其子目錄 (by-topic/, by-mock/, _template/)
- [ ] 建立 prompts/ 及其子目錄 (copilot/, team/)
- [ ] 建立 skills/ 及其子目錄 (no-script/, scripted/)
- [ ] 建立 progress/ 及其子目錄 (individuals/, team-dashboard.md)
- [ ] 建立 tooling/ 目錄
- [ ] 在所有空目錄中加入 .gitkeep 檔案

**Deliverables:**
- 完整的資料夾樹狀結構
- 可透過 `tree -L 3` 驗證結構正確性

---

### Task 1.2: Template Files Creation
建立標準化的題目與解析模板。

**Requirements:**
- [ ] question-bank/_template/question-template.md
  - 欄位：題目編號、來源、描述、選項、標籤
- [ ] question-bank/_template/analysis-template.md
  - 區塊：考點識別、正解說明、錯誤選項排除、記憶法、官方文件引用

**Deliverables:**
- 2 個模板檔案
- 每個模板包含詳細欄位說明與填寫範例

---

### Task 1.3: Core Documentation
建立專案核心文件。

**Requirements:**
- [ ] README.md
  - 專案目的與核心原則（參考 dev-spec.md 第 1-2 節）
  - 快速開始指南（實際可執行的指令）
  - 資料夾結構說明
  
- [ ] tooling/contribution-guide.md
  - PR 提交規範
  - 內容審核標準
  - 範例 PR 描述模板
  
- [ ] tooling/tagging-schema.md
  - Topic tags 命名規則
  - Trap tags 定義
  - Level tags 分級標準

**Deliverables:**
- 3 個文件檔案
- README 包含至少 1 個完整的使用範例

---

## Acceptance Criteria (Phase 1)
- [ ] 所有資料夾結構符合 dev-spec.md 第 3 節定義
- [ ] 模板檔案可直接複製使用（包含範例內容）
- [ ] README 可讓新成員在 5 分鐘內理解專案目的
- [ ] 所有變更已提交至 Git

---

## Next Phase Preview
Phase 2 將包含：
- No-Script Skills 開發（Prompt 檔案）
- Scripted Skills 開發（Python 腳本）
- 範例題目與解析