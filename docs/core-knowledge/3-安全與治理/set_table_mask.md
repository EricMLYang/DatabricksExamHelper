# ALTER/SET 語法速記法 - 考試專用

## 🎯 核心口訣

```
改表用 ALTER TABLE
改欄用 ALTER COLUMN
設定用 SET
```

---

## 📝 Column Mask 語法記憶

### ✅ 正確格式（三層結構）
```sql
ALTER TABLE {table_name}
  ALTER COLUMN {column_name}
    SET MASK {function_name};
```

### 🧠 記憶技巧
**「表→欄→設」三步驟：**
1. **ALTER TABLE** - 先找到表
2. **ALTER COLUMN** - 再定位欄位  
3. **SET MASK** - 最後設定遮罩

---

## ⚡ 快速判斷法

看到題目關鍵字時的反應：

| 題目提到 | 立刻想到 |
|---------|---------|
| **column mask** | `ALTER COLUMN ... SET MASK` |
| **row filter** | `ALTER TABLE ... SET ROW FILTER` |
| **table property** | `ALTER TABLE ... SET TBLPROPERTIES` |
| **table constraint** | `ALTER TABLE ADD CONSTRAINT` |

---

## 🚫 常見錯誤語法（秒殺選項）

❌ `ALTER TABLE ... SET MASK card_mask ON (credit_card)`  
❌ `SET MASK ... ON TABLE ... TO COLUMN ...`  
❌ `ALTER TABLE ... SET MASK card_mask` (沒指定欄位)

**判斷原則：**
- Column-level 操作 → 必須有 `ALTER COLUMN`
- 看到 `ON (column)` → 錯誤語法
- 看到 `SET MASK` 卻沒 `ALTER COLUMN` → 錯誤

---

## 📋 Unity Catalog 常用 ALTER 語法對照表

```sql
-- Column Mask (欄位遮罩)
ALTER TABLE t ALTER COLUMN c SET MASK func;

-- Row Filter (列過濾)  
ALTER TABLE t SET ROW FILTER func;

-- Table Properties (表屬性)
ALTER TABLE t SET TBLPROPERTIES ('key'='value');

-- Add Constraint (新增約束)
ALTER TABLE t ADD CONSTRAINT name CHECK (condition);

-- Change Column (更改欄位)
ALTER TABLE t ALTER COLUMN c SET NOT NULL;
ALTER TABLE t ALTER COLUMN c COMMENT 'text';
```

---

## 🎓 考試口訣總結

```
欄位遮罩三層套：
ALTER TABLE 改表
ALTER COLUMN 改欄  
SET MASK 設遮罩

列過濾兩層夠：
ALTER TABLE 改表
SET ROW FILTER 設過濾
```

**秒殺技巧：**
- 選項有 `ALTER COLUMN` + `SET MASK` → 99% 正確
- 選項語法超過三層 → 錯誤
- 選項用 `ON (column)` 語法 → 錯誤


---

# TBLPROPERTIES 多個屬性設定

## ✅ 正確語法

```sql
ALTER TABLE table_name 
SET TBLPROPERTIES (
  'key1' = 'value1',
  'key2' = 'value2',
  'key3' = 'value3'
);
```

---

## 🧠 記憶口訣

**「括號內，逗號分隔，鍵值成對」**

```
SET TBLPROPERTIES (
  'k1'='v1',
  'k2'='v2',
  'k3'='v3'
)
```

---

## 📝 實際範例

### Example 1: Delta 表優化設定
```sql
ALTER TABLE customer_accounts 
SET TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true',
  'delta.deletedFileRetentionDuration' = 'interval 7 days'
);
```

### Example 2: 表描述與標籤
```sql
ALTER TABLE sales_data 
SET TBLPROPERTIES (
  'description' = 'Daily sales transactions',
  'owner' = 'data-team',
  'classification' = 'sensitive',
  'retention_days' = '365'
);
```

---

## ⚡ 考試快速判斷

### ✅ 正確格式特徵
- 單一 `TBLPROPERTIES` 關鍵字
- 單一括號 `( )`
- 逗號分隔多個 key-value pair
- 每個 key 和 value 都用單引號

### ❌ 錯誤格式（秒殺）
```sql
-- ❌ 多個 TBLPROPERTIES
SET TBLPROPERTIES ('k1'='v1')
SET TBLPROPERTIES ('k2'='v2')

-- ❌ 多個括號
SET TBLPROPERTIES ('k1'='v1') ('k2'='v2')

-- ❌ 沒有逗號分隔
SET TBLPROPERTIES ('k1'='v1' 'k2'='v2')

-- ❌ 沒有引號
SET TBLPROPERTIES (k1=v1, k2=v2)
```

---

## 📋 完整對照：單個 vs 多個

| 屬性數量 | 語法 |
|---------|------|
| **單個** | `SET TBLPROPERTIES ('key'='value')` |
| **多個** | `SET TBLPROPERTIES ('k1'='v1', 'k2'='v2', 'k3'='v3')` |

**核心原則：**
- 一個 `TBLPROPERTIES`
- 一對括號
- 逗號連接

---

## 🎯 秒記版本

```
單個：SET TBLPROPERTIES ('k'='v')
多個：SET TBLPROPERTIES ('k1'='v1', 'k2'='v2', ...)

記住：一個括號包全部，逗號分隔每一對
```

---

# Unity Catalog 欄位遮罩治理觀念

## 一句話
**遮罩函式集中管理 → 單一版本，避免各單位各自定義。**

---

## 核心概念
- Unity Catalog 提供**集中式**遮罩函式管理
- 所有團隊共用同一套遮罩定義，避免版本分裂
- 目標是**一致性與治理**，不是「各自管理」

---

## 題目關鍵字對照
| 題目說法 | 正確理解 |
|---|---|
| single source of truth | 遮罩規則集中管理 |
| inconsistent exposure | 透過集中遮罩避免不一致 |
| different teams each have policies | UC 的改善點就是統一版本 |

---

## 秒殺判斷
✅ 看見「各單位各自遮罩」→ 答案是 **集中定義**  
❌ 「讓各團隊自訂遮罩」→ 錯（違反 UC 目標）

---

# Unity Catalog 欄位遮罩治理觀念

## 一句話
