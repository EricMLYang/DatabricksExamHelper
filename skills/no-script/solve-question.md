# Solve Question - 題目解析技能

> 依照標準模板解析 Databricks 認證考試題目，著重「逐項排除邏輯」

---

## 🎯 技能目的

此技能用於將單一考試題目轉化為符合 `analysis-template.md` 格式的完整解析，確保：
1. **邏輯清晰** - 每個錯誤選項都有明確的排除理由
2. **結構一致** - 輸出符合專案標準模板
3. **可複習性** - 包含記憶法與解題技巧

---

## 📥 輸入格式

### 必要資訊
```markdown
**題目 ID:** Q-XXX-XXX
**題幹:** [題目描述]
**選項:**
- A. [選項 A]
- B. [選項 B]
- C. [選項 C]
- D. [選項 D]
**正確答案:** [A/B/C/D]
```

### 選填資訊
- **來源:** 題目來源（Mock Exam / Official / Community）
- **難度:** 預估難度等級
- **相關文件:** 已知的官方文件連結

---

## 📤 輸出結構

輸出必須符合 `question-bank/_template/analysis-template.md` 的完整結構：

### 核心區塊（必須包含）
1. **📍 考點識別** - 主要與次要考點
2. **✅ 正解說明** - 為什麼正確答案是對的
3. **❌ 錯誤選項排除** - 逐一拆解每個錯誤選項
4. **🧠 記憶法與解題技巧** - 記憶口訣、解題步驟、陷阱警示
5. **📚 官方文件與延伸閱讀** - 至少 1 個官方文件連結
6. **🏷️ 標籤與分類** - Topic Tags, Trap Tags, Level Tags

---

## 🔑 核心原則：逐項排除邏輯

### 排除邏輯的四個層次

#### 1. 語法錯誤排除
指出選項的語法、拼寫、參數順序等明顯錯誤。

**範例:**
```markdown
### 選項 A - `VACCUM table_name RETAIN 30 HOURS`
**錯誤原因:** 語法錯誤

**詳細分析:**
指令拼寫錯誤，正確應為 `VACUUM`（有 U），而非 `VACCUM`。
這是典型的「拼寫陷阱」，測試是否熟悉正確語法。
```

---

#### 2. 概念混淆排除
指出選項混淆了不同概念或功能。

**範例:**
```markdown
### 選項 B - `OPTIMIZE table_name ZORDER BY (date_column)`
**錯誤原因:** 指令用途錯誤

**詳細分析:**
OPTIMIZE 用於合併小檔案與重新排序資料，**不會刪除舊版本檔案**。
此選項混淆了 OPTIMIZE（效能優化）與 VACUUM（空間清理）的用途。

**易混淆點:**
兩者都是 Delta Lake 維護指令，但目的完全不同：
- OPTIMIZE: 提升查詢效能
- VACUUM: 釋放儲存空間
```

---

#### 3. 參數錯誤排除
指出選項的參數值、單位、或條件設定錯誤。

**範例:**
```markdown
### 選項 C - `VACUUM table_name RETAIN 30 HOURS`
**錯誤原因:** 時間單位換算錯誤

**詳細分析:**
題目要求「刪除超過 30 天的舊版本」，30 天 = 30 × 24 = **720 小時**。
此選項僅保留 30 小時（約 1.25 天），與需求不符。

**易混淆點:**
數字陷阱 - 題目中的「30 天」與選項中的「30」數字相同，但單位不同。
VACUUM 只接受 HOURS 作為單位，需自行換算。
```

---

#### 4. 行為誤解排除
指出選項對指令執行行為、副作用、或結果的誤解。

**範例:**
```markdown
### 選項 D - `DELETE FROM table_name WHERE _commit_timestamp < current_date() - 30`
**錯誤原因:** 混淆邏輯刪除與實體刪除

**詳細分析:**
DELETE 只會**標記資料為刪除**（邏輯刪除），不會實際釋放儲存空間。
舊版本檔案仍保留在儲存層，需配合 VACUUM 才能真正清理。

**易混淆點:**
- DELETE: 邏輯刪除，資料仍可透過 Time Travel 復原
- VACUUM: 實體刪除，永久釋放空間
```

---

## 📋 完整使用範例

### 輸入

```markdown
**題目 ID:** Q-MOCK01-023
**題幹:** 在 Delta Lake 中，您需要永久刪除超過 30 天的舊版本資料以節省儲存空間。以下哪個指令可以達成此目的？
**選項:**
- A. VACUUM table_name RETAIN 30 HOURS
- B. VACUUM table_name RETAIN 720 HOURS
- C. DELETE FROM table_name WHERE _commit_timestamp < current_date() - 30
- D. OPTIMIZE table_name ZORDER BY (date_column)
**正確答案:** B
```

---

### 輸出

```markdown
# 題目解析

## 題目回顧
**題目 ID:** Q-MOCK01-023
**正解:** B

---

## 📍 考點識別

### 主要考點
**核心技術:** Delta Lake VACUUM 指令
**知識領域:** Delta Lake - Data Retention
**關鍵概念:**
- VACUUM 的預設保留期限
- 時間單位換算 (HOURS)
- 儲存空間管理

### 次要考點
- VACUUM 與 DELETE、OPTIMIZE 的差異
- Delta Lake 版本管理機制

---

## ✅ 正解說明

### 為什麼 B (VACUUM table_name RETAIN 720 HOURS) 是正確的？

**技術原理:**
VACUUM 會永久刪除不再被任何版本參照的舊資料檔案。RETAIN 參數指定要保留的最小時間閾值，預設為 168 小時（7 天）。

**符合需求:**
題目要求「刪除超過 30 天的舊版本」，30 天 = 30 × 24 = 720 小時，因此 `RETAIN 720 HOURS` 正確。

**實務應用:**
\`\`\`sql
VACUUM my_table RETAIN 720 HOURS;  -- 保留 30 天內的資料
\`\`\`

執行後，30 天前的舊版本檔案將被永久刪除，無法透過 Time Travel 復原。

---

## ❌ 錯誤選項排除

### 選項 A - VACUUM table_name RETAIN 30 HOURS
**錯誤原因:** 時間單位換算錯誤

**詳細分析:**
此選項僅保留 30 小時（約 1.25 天）的資料，而非 30 天。
這是典型的「數字陷阱」，誤將天數直接當作小時數使用。

**易混淆點:**
- 題目中的「30 天」數字與選項中的「30」數字相同，但單位不同
- VACUUM 只接受 HOURS 作為單位，需自行換算天數

---

### 選項 C - DELETE FROM table_name WHERE _commit_timestamp < current_date() - 30
**錯誤原因:** 混淆邏輯刪除與實體刪除

**詳細分析:**
1. DELETE 只會標記資料為刪除（邏輯刪除），**不會實際釋放儲存空間**
2. `_commit_timestamp` 不是標準欄位，無法直接使用
3. 即使刪除成功，舊版本檔案仍保留，需配合 VACUUM 才能清理

**易混淆點:**
- DELETE: 邏輯刪除，資料仍可透過 Time Travel 復原
- VACUUM: 實體刪除，永久釋放空間

---

### 選項 D - OPTIMIZE table_name ZORDER BY (date_column)
**錯誤原因:** 指令用途錯誤

**詳細分析:**
OPTIMIZE 用於合併小檔案與重新排序資料（Z-Order），**不會刪除舊版本檔案**。
此選項混淆了 OPTIMIZE（效能優化）與 VACUUM（空間清理）的用途。

**易混淆點:**
兩者都是 Delta Lake 維護指令，但目的完全不同：
- OPTIMIZE: 提升查詢效能（合併檔案、重新排序）
- VACUUM: 釋放儲存空間（刪除舊版本）

---

## 🧠 記憶法與解題技巧

### 記憶口訣
"**VACUUM 吸塵器，清理舊檔案；RETAIN 加小時，天數要乘 24**"

### 解題步驟
1. **識別關鍵字「永久刪除」** → 想到 VACUUM
2. **排除明顯錯誤** → DELETE (邏輯刪除) 和 OPTIMIZE (效能優化)
3. **計算時間** → 30 天 × 24 小時 = 720 小時
4. **選擇正解** → VACUUM ... RETAIN 720 HOURS

### 常見陷阱警示
⚠️ **陷阱 1:** 時間單位混淆 - VACUUM 只接受 HOURS，需自行換算
⚠️ **陷阱 2:** 指令用途混淆 - DELETE、VACUUM、OPTIMIZE 功能完全不同
⚠️ **陷阱 3:** 數字陷阱 - 題目中的數字可能與選項數字相同但單位不同

---

## 📚 官方文件與延伸閱讀

### 官方文件
1. **[VACUUM | Databricks Documentation](https://docs.databricks.com/sql/language-manual/delta-vacuum.html)** - VACUUM 指令的完整說明與參數
2. **[Delta Lake Data Retention](https://docs.databricks.com/delta/history.html)** - Delta Lake 版本管理機制

### 延伸閱讀
- [Delta Lake Best Practices](https://docs.databricks.com/delta/best-practices.html)

### 相關題目
- `Q-DELTA-018` - Delta Lake Time Travel 功能
- `Q-DELTA-031` - OPTIMIZE 與 ZORDER 效能調校

---

## 🏷️ 標籤與分類

**Topics:** `Delta-Lake`, `Data-Retention`, `Storage-Management`
**Traps:** `Unit-Confusion`, `Number-Trap`
**Difficulty:** `L2-Intermediate`
```

---

## 💡 使用技巧

### 1. 按順序分析
先識別考點 → 說明正解 → 逐項排除錯誤選項 → 總結技巧

### 2. 重視排除邏輯
每個錯誤選項都要回答：
- **為什麼錯？** （錯誤原因）
- **錯在哪裡？** （詳細分析）
- **為什麼容易誤選？** （易混淆點）

### 3. 提供實務價值
- 記憶口訣要具體可用
- 解題步驟可套用同類題目
- 陷阱警示幫助避開常見錯誤

---

## 🔍 品質檢查清單

在完成解析前，請確認：
- [ ] 所有錯誤選項都有明確的排除理由
- [ ] 至少提供 1 個官方文件連結
- [ ] 包含記憶口訣或解題技巧
- [ ] 標籤符合 `tooling/tagging-schema.md` 規範
- [ ] 輸出結構符合 `analysis-template.md`

---

## 📞 相關資源

- [analysis-template.md](../../question-bank/_template/analysis-template.md) - 標準解析模板
- [tagging-schema.md](../../tooling/tagging-schema.md) - 標籤規範
- [contribution-guide.md](../../tooling/contribution-guide.md) - 貢獻指南

---

**透過逐項排除邏輯，將每個題目轉化為可複習的知識資產！🎓**
