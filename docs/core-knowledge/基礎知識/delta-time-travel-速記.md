# Delta Lake Time Travel 速記（考前速讀版）

## 1) 一句話
- **版本號**：`@v{version}` 或 `VERSION AS OF {version}`
- **時間點**：`TIMESTAMP AS OF '{timestamp}'`
- 差集比對用 **EXCEPT**（不是 MINUS）

---

## 2) 核心語法總覽
| 方式 | 語法 | 範例 | 適用場景 |
|---|---|---|---|
| 版本號（簡寫） | `@v{version}` | `SELECT * FROM table@v5` | 知道版本號 |
| 版本號（完整） | `VERSION AS OF {version}` | `SELECT * FROM table VERSION AS OF 5` | 同上（正式） |
| 時間戳 | `TIMESTAMP AS OF '{timestamp}'` | `SELECT * FROM table TIMESTAMP AS OF '2024-01-01'` | 以時間點查 |

---

## 3) 常見錯誤語法（秒殺）
```sql
-- ❌ 錯誤
AS VERSION = 5
@VERSION 5
VERSION = 5
AS OF VERSION 5
MINUS

-- ✅ 正確
@v5
VERSION AS OF 5
TIMESTAMP AS OF '2024-01-01'
EXCEPT
```

---

## 4) 版本差異比對（常考）
```sql
-- 新增的資料
SELECT * FROM table@v10
EXCEPT
SELECT * FROM table@v9

-- 刪除的資料
SELECT * FROM table@v9
EXCEPT
SELECT * FROM table@v10

-- 變更的資料（對稱差）
(SELECT * FROM table@v10 EXCEPT SELECT * FROM table@v9)
UNION
(SELECT * FROM table@v9 EXCEPT SELECT * FROM table@v10)
```

---

## 5) 版本資訊查詢
```sql
-- 查看版本歷史
DESCRIBE HISTORY my_table

-- 最近 N 筆
DESCRIBE HISTORY my_table LIMIT 5

-- 取得最新版本號
SELECT max(version) FROM (DESCRIBE HISTORY my_table)
```

---

## 6) Time Travel 限制與注意
- **VACUUM** 會刪除舊版本檔案 → 可能無法回查
- 預設保留期 **30 天**（可透過表屬性調整）

```sql
ALTER TABLE my_table
SET TBLPROPERTIES (
  'delta.logRetentionDuration' = '365 days',
  'delta.deletedFileRetentionDuration' = '365 days'
)
```

---

## 7) 10 秒記憶法
```
@v = at version
VERSION AS OF = 完整版本語法
TIMESTAMP AS OF = 時間點
差集用 EXCEPT，不是 MINUS
```
