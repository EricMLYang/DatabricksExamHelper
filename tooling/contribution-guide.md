# 貢獻指南 (Contribution Guide)

> 確保團隊協作品質與知識資產一致性的規範文件

---

## 🎯 貢獻原則

本專案遵循以下核心原則：

1. **品質優先** - 解析必須清晰、正確、可複習
2. **模板一致** - 所有內容符合標準模板格式
3. **審核機制** - 透過 PR Review 確保內容品質
4. **知識共享** - 歡迎所有形式的貢獻與改進建議

---

## 📝 貢獻類型

### 1. 新增題目與解析 (最常見)

**適用情境:**
- 練習遇到有價值的題目
- 模擬試卷題目整理
- 實際考試回憶題（需遵守保密協議，以變形題呈現）

**提交前檢查清單:**
- [ ] 使用 `question-bank/_template/question-template.md` 建立題目
- [ ] 使用 `question-bank/_template/analysis-template.md` 建立解析
- [ ] 檔案命名符合規範：`Q-{來源}-{序號}-{question|analysis}.md`
- [ ] 標籤符合 `tooling/tagging-schema.md` 規範
- [ ] 解析包含至少 1 個官方文件引用
- [ ] 每個錯誤選項都有明確的排除理由

---

### 2. 修正現有內容

**適用情境:**
- 發現解析有錯誤或不清楚之處
- 技術細節需要更新（如 Databricks 新版本變更）
- 標籤分類不正確

**提交前檢查清單:**
- [ ] 在 PR 描述中說明修正原因
- [ ] 提供正確資訊的來源（官方文件連結）
- [ ] 若影響標籤，同步更新相關檔案

---

### 3. 新增核心知識文件

**適用情境:**
- 建立主題式速查表 (Cheatsheets)
- 整理錯誤模式與陷阱庫
- 更新考綱映射表

**提交前檢查清單:**
- [ ] 內容結構清晰，適合快速查閱
- [ ] 包含實際範例程式碼或指令
- [ ] 引用官方文件作為權威來源

---

### 4. 開發 Agent Skills

**適用情境:**
- 建立新的 Prompt 檔案 (No-Script Skills)
- 開發自動化腳本 (Scripted Skills)

**提交前檢查清單:**
- [ ] Skills 有明確的使用情境說明
- [ ] 提供實際執行範例
- [ ] 腳本包含錯誤處理與使用說明

---

## 🔀 Pull Request (PR) 流程

### 步驟 1: Fork 或建立分支

```bash
# 方法 A: 建立功能分支 (團隊成員)
git checkout -b feature/q-delta-023

# 方法 B: Fork 專案 (外部貢獻者)
# 在 GitHub 上點擊 Fork 按鈕
```

---

### 步驟 2: 進行變更

```bash
# 建立新題目與解析
cp question-bank/_template/question-template.md \
   question-bank/by-topic/Q-DELTA-023-question.md

cp question-bank/_template/analysis-template.md \
   question-bank/by-topic/Q-DELTA-023-analysis.md

# 編輯檔案內容
# ...

# 提交變更
git add question-bank/by-topic/Q-DELTA-023-*.md
git commit -m "Add: Q-DELTA-023 Delta Lake MERGE 語法題目"
```

---

### 步驟 3: 推送變更

```bash
# 推送至遠端分支
git push origin feature/q-delta-023
```

---

### 步驟 4: 建立 Pull Request

在 GitHub 上建立 PR，使用以下範本：

---

## 📋 PR 描述範本

### 新增題目 PR 範本

```markdown
## 📝 變更類型
- [x] 新增題目與解析
- [ ] 修正現有內容
- [ ] 新增核心知識文件
- [ ] 開發 Agent Skills

## 📌 題目資訊
**題目 ID:** Q-DELTA-023
**主題標籤:** `Delta-Lake`, `MERGE`, `DML-Operations`
**難度等級:** L2-Intermediate
**來源:** Mock Exam - Data Engineer Associate

## 📚 變更摘要
新增 Delta Lake MERGE 指令的語法題目與詳細解析。

**考點:**
- MERGE 指令的 WHEN MATCHED / WHEN NOT MATCHED 語法
- 條件式更新與插入邏輯

**解析亮點:**
- 逐項排除錯誤選項的語法錯誤
- 提供記憶口訣："MERGE 三步驟 - ON 條件、MATCHED 更新、NOT MATCHED 插入"
- 引用官方文件與實務範例

## ✅ 檢查清單
- [x] 使用標準模板
- [x] 標籤符合 tagging-schema.md
- [x] 解析包含官方文件引用
- [x] 錯誤選項有明確排除邏輯
- [x] 檔案命名符合規範

## 🔗 相關資源
- [MERGE | Databricks Documentation](https://docs.databricks.com/sql/language-manual/delta-merge-into.html)
```

---

### 修正內容 PR 範本

```markdown
## 📝 變更類型
- [ ] 新增題目與解析
- [x] 修正現有內容
- [ ] 新增核心知識文件
- [ ] 開發 Agent Skills

## 🐛 修正說明
**修正檔案:** question-bank/by-topic/Q-STREAM-015-analysis.md

**問題描述:**
原解析中提到 `Trigger.Once` 會重複執行，但這是錯誤的。Trigger.Once 只會執行一次所有可用的資料後停止。

**修正內容:**
- 更正 Trigger.Once 的行為說明
- 補充與 Trigger.AvailableNow 的差異
- 更新官方文件連結

**參考來源:**
- [Triggers in Structured Streaming | Databricks Docs](https://docs.databricks.com/structured-streaming/triggers.html)

## ✅ 檢查清單
- [x] 提供正確資訊來源
- [x] 修正所有相關錯誤
- [x] 保持模板格式一致
```

---

## 🔍 內容審核標準

### Reviewer 檢查重點

當您擔任 Reviewer 時，請確認以下項目：

#### 1. 模板符合性 ✅
- [ ] 題目包含所有必填欄位（ID、來源、難度、題幹、選項、標籤、正解）
- [ ] 解析包含所有核心區塊（考點識別、正解說明、錯誤選項排除、記憶法、官方文件）

#### 2. 技術正確性 ✅
- [ ] 正確答案無誤
- [ ] 技術細節準確（指令語法、參數、行為等）
- [ ] 官方文件連結有效且相關

#### 3. 邏輯清晰性 ✅
- [ ] 錯誤選項的排除理由說服力足夠
- [ ] 解析邏輯連貫，易於理解
- [ ] 術語使用一致（如 "串流" vs "Streaming" 需統一）

#### 4. 標籤規範性 ✅
- [ ] Topic Tags 符合 `tooling/tagging-schema.md` 定義
- [ ] Trap Tags 正確標記混淆點
- [ ] 難度等級合理（L1/L2/L3）

#### 5. 可複習性 ✅
- [ ] 包含記憶口訣或解題技巧
- [ ] 提供實務應用情境或範例程式碼
- [ ] 交叉引用相關題目（若有）

---

### Review 意見範例

**✅ 批准範例:**
```
LGTM! 解析清晰且邏輯完整。

特別喜歡「VACUUM 吸塵器」的記憶口訣，非常實用。

建議微調：
- 考慮在「錯誤選項 C」中補充 DELETE 與 VACUUM 的差異表格，會更一目了然。

已批准合併。
```

**🔄 要求修改範例:**
```
感謝貢獻！內容整體不錯，但有幾處需要修正：

**必須修改:**
1. 正解說明中提到「RETAIN 預設 7 天」，但實際是 168 小時，建議統一使用「小時」避免混淆。
2. 官方文件連結失效，請更新為最新版本。

**建議改進:**
1. 錯誤選項 D 的排除理由稍嫌簡略，建議補充 OPTIMIZE 的實際用途。
2. 記憶法區塊可以更具體，例如提供「天數 × 24 = 小時數」的換算口訣。

請修改後再次提交 Review。
```

---

## 🏷️ Commit Message 規範

使用清楚的 Commit Message 有助於追蹤變更歷史。

### 格式
```
<類型>: <簡短描述>

<詳細說明> (選填)
```

### 類型標籤

| 類型 | 說明 | 範例 |
|------|------|------|
| `Add` | 新增題目、文件、Skills | `Add: Q-DELTA-023 MERGE 語法題目` |
| `Fix` | 修正錯誤內容 | `Fix: Q-STREAM-015 Trigger.Once 行為說明` |
| `Update` | 更新文件或改進內容 | `Update: README 快速開始指南` |
| `Refactor` | 重構檔案結構或格式 | `Refactor: 統一 by-topic 資料夾命名` |
| `Docs` | 純文件變更 | `Docs: 補充 contribution-guide 範例` |
| `Chore` | 維護性任務 | `Chore: 清理空目錄與測試檔案` |

### 良好範例
```bash
Add: Q-UNITY-042 Unity Catalog 權限管理題目

新增 Unity Catalog GRANT/REVOKE 指令題目，考點包含：
- Metastore、Catalog、Schema 三層權限模型
- USAGE 與 SELECT 權限差異
- 權限繼承規則

相關標籤: Unity-Catalog, Security, Permissions
```

---

## 🚫 常見錯誤與避免方法

### ❌ 錯誤 1: 標籤不符合規範
**問題:** 使用 `delta` 而非 `Delta-Lake`

**正確做法:**
- 參考 `tooling/tagging-schema.md` 的標準標籤清單
- 使用一致的大小寫與連字符

---

### ❌ 錯誤 2: 缺少官方文件引用
**問題:** 解析沒有提供任何官方文件連結

**正確做法:**
- 至少提供 1 個 Databricks 官方文件連結
- 確保連結有效且直接相關

---

### ❌ 錯誤 3: 錯誤選項排除理由不足
**問題:** 只寫「此選項錯誤」，沒有說明原因

**正確做法:**
- 明確指出錯誤原因（語法錯誤、概念混淆、參數錯誤等）
- 解釋為何容易混淆
- 提供正確的對比說明

---

### ❌ 錯誤 4: 檔案命名不一致
**問題:** 題目檔名為 `delta-023.md`，解析檔名為 `Q-DELTA-023-ans.md`

**正確做法:**
```
question-bank/by-topic/Q-DELTA-023-question.md
question-bank/by-topic/Q-DELTA-023-analysis.md
```

---

## 🎓 最佳實踐建議

### 1. 撰寫解析的黃金法則
- **邏輯優先** - 說服自己為何選這個答案，再撰寫解析
- **逐項排除** - 每個錯誤選項都要有明確的排除理由
- **可複習性** - 寫完後隔天再讀，看是否能快速理解

### 2. 標籤使用技巧
- **Topic Tags** - 最多 3 個，選最核心的技術主題
- **Trap Tags** - 標記容易誤選的陷阱類型
- **難度判斷** - L1 直接查文件可解 / L2 需理解組合 / L3 需深入原理

### 3. 團隊協作建議
- **小批量提交** - 一次 PR 不超過 5 題，方便 Review
- **及時回應** - Reviewer 提出問題後，24 小時內回應
- **互相學習** - Review 他人 PR 時，也是自己學習的機會

---

## 📞 需要協助？

如有任何疑問，請：
1. 查閱 [README.md](../README.md) 快速開始指南
2. 參考 [tooling/tagging-schema.md](./tagging-schema.md) 標籤規範
3. 開 [GitHub Issue](https://github.com/your-org/databricks-cert-agent/issues) 提問
4. 聯絡專案維護者

---

**感謝您的貢獻！每一個高品質的題目與解析，都是團隊共同的知識資產。🎉**
