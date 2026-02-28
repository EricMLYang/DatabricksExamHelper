# 題目模板

<!--
此模板用於建立標準化的 Databricks 認證考試題目。
每個欄位都有明確的用途，請確保完整填寫以利後續檢索與分析。
-->

---

## 題目資訊

### 題目編號
<!--
格式：Q-{來源}-{序號}
範例：Q-MOCK01-015, Q-OFFICIAL-042
用途：唯一識別題目，方便引用與追蹤
-->
**ID:** `Q-XXX-XXX`

### 來源
<!--
說明題目的來源，可能的值：
- Official Practice Exam (官方模擬試題)
- Mock Exam (第三方模擬試題)
- Community Contributed (社群貢獻)
- Real Exam Recall (實際考試回憶)
-->
**來源:**

### 難度等級
<!--
根據 .github/skills/tagging-schema/references/tagging-schema.md 的 Level Tags 定義
- L1-Basic: 基礎概念題
- L2-Intermediate: 中階應用題
- L3-Advanced: 進階情境題
-->
**難度:** `L1-Basic` / `L2-Intermediate` / `L3-Advanced`

---

## 題目內容

### 題幹
<!--
清楚描述問題情境，包含：
1. 背景說明（若有）
2. 核心問題
3. 任何必要的技術細節或限制條件
-->

```
[在此填寫題目描述]
```

### 選項

<!--
列出所有選項，使用 A/B/C/D 標記
建議格式：每個選項獨立一行，方便閱讀
-->

- **A.** [選項 A 內容]
- **B.** [選項 B 內容]
- **C.** [選項 C 內容]
- **D.** [選項 D 內容]

<!-- 如果是多選題，請在此註明 -->
<!-- 📌 此題為多選題 (Multiple Choice) -->

---

## 標籤系統

### Topic Tags (技術主題標籤)
<!--
根據 .github/skills/tagging-schema/references/tagging-schema.md 定義的 Topic Tags
可多選，用逗號分隔
範例：Delta-Lake, Streaming, Performance-Tuning
-->
**Topics:** `[Tag1]`, `[Tag2]`, `[Tag3]`

### Trap Tags (陷阱類型標籤)
<!--
標記此題容易混淆的陷阱類型
範例：Syntax-Confusion, Parameter-Order, Similar-Function
參考 .github/skills/tagging-schema/references/tagging-schema.md 的 Trap Tags 定義
-->
**Traps:** `[Trap1]`, `[Trap2]`

### Knowledge Domain (知識領域)
<!--
對應 Databricks 官方考綱的知識領域
範例：Data Engineering, Lakehouse Architecture, Delta Lake
-->
**Domain:** `[Knowledge-Domain]`

---

## 答案與解析連結

### 正確答案
<!--
僅列出正確選項字母，不在此處說明原因
詳細解析請見對應的 analysis-template.md
-->
**正解:** `[A/B/C/D 或 A,B,C 若為多選]`

### 解析檔案
<!--
連結到對應的解析檔案
命名規則：與題目檔案同名，但位於 analysis 資料夾
-->
**詳細解析:** [點此查看解析](../analysis/[對應檔名].md)

---

## 相關資源

### 官方文件
<!--
列出與此題相關的 Databricks 官方文件連結
建議至少提供 1 個主要參考文件
-->
- [官方文件標題](https://docs.databricks.com/...)

### 相關題目
<!--
若有類似或相關的題目，可在此交叉引用
格式：[題目 ID] 簡短描述
-->
- `Q-XXX-XXX` - [相關題目簡述]

---

## 範例：完整填寫示範

```markdown
## 題目資訊
**ID:** `Q-MOCK01-023`
**來源:** Mock Exam - Databricks Certified Data Engineer Associate
**難度:** `L2-Intermediate`

## 題目內容

### 題幹
在 Delta Lake 中，您需要永久刪除超過 30 天的舊版本資料以節省儲存空間。以下哪個指令可以達成此目的？

### 選項
- **A.** `VACUUM table_name RETAIN 30 HOURS`
- **B.** `VACUUM table_name RETAIN 720 HOURS`
- **C.** `DELETE FROM table_name WHERE _commit_timestamp < current_date() - 30`
- **D.** `OPTIMIZE table_name ZORDER BY (date_column)`

## 標籤系統
**Topics:** `Delta-Lake`, `Data-Retention`, `Storage-Management`
**Traps:** `Unit-Confusion`, `Command-Purpose`
**Domain:** `Delta Lake`

## 答案與解析連結
**正解:** `B`
**詳細解析:** [點此查看解析](../analysis/Q-MOCK01-023-analysis.md)

## 相關資源
- [VACUUM | Databricks Documentation](https://docs.databricks.com/sql/language-manual/delta-vacuum.html)
```

---

## 使用指南

### 建立新題目的步驟
1. 複製此模板至適當的分類資料夾 (by-topic/ 或 by-mock/)
2. 依據題目來源命名檔案 (例如：`Q-MOCK01-023-question.md`)
3. 填寫所有必要欄位
4. 使用 .github/skills/tagging-schema/references/tagging-schema.md 確保標籤符合規範
5. 建立對應的 analysis 檔案 (使用 analysis-template.md)

### 欄位填寫優先順序
必填欄位 (🔴)：
- 題目編號 (ID)
- 題幹 (Question Description)
- 選項 (Options)
- 正確答案 (Correct Answer)
- Topic Tags

建議填寫 (🟡)：
- 來源 (Source)
- 難度等級 (Level)
- Trap Tags
- 官方文件連結

選填欄位 (🟢)：
- 相關題目
- Knowledge Domain (可從 Topic Tags 推導)
