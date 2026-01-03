# Delta Lake 核心概念速查表

> Databricks 認證考試必備：Delta Lake 核心 API 與配置快速參考

**最後更新:** 2024-01-15
**適用考試:** Data Engineer Associate / Professional

---

## 📋 目錄

1. [核心概念](#核心概念)
2. [資料表管理指令](#資料表管理指令)
3. [資料操作 (DML)](#資料操作-dml)
4. [Time Travel](#time-travel)
5. [資料表維護](#資料表維護)
6. [Schema 管理](#schema-管理)
7. [Change Data Feed (CDF)](#change-data-feed-cdf)
8. [配置參數](#配置參數)
9. [常見錯誤與排除](#常見錯誤與排除)

---

## 核心概念

### Delta Lake 是什麼？

Delta Lake 是建立在 Data Lake 之上的開源儲存層，提供 ACID 交易、可擴展的元資料處理、以及統一的批次與串流資料處理。

### 核心特性

| 特性 | 說明 | 考試重點 |
|------|------|---------|
| **ACID 交易** | 原子性、一致性、隔離性、持久性 | 多個寫入操作的一致性保證 |
| **Time Travel** | 查詢歷史版本資料 | VERSION AS OF 語法 |
| **Schema Evolution** | 動態調整 Schema | mergeSchema, overwriteSchema 選項 |
| **Upsert (MERGE)** | 合併插入/更新 | MERGE INTO 語法 |
| **DML 支援** | UPDATE, DELETE, MERGE | 與 Parquet 的差異 |

---

## 資料表管理指令

### 建立 Delta Table

| 方法 | 語法 | 使用時機 |
|------|------|---------|
| **SQL** | `CREATE TABLE table_name USING DELTA AS SELECT ...` | 從查詢結果建立 |
| **DataFrameWriter** | `df.write.format("delta").save("/path")` | PySpark 程式化建立 |
| **Convert Parquet** | `CONVERT TO DELTA parquet.\`/path\`` | 轉換現有 Parquet 資料 |

**範例:**
```sql
-- SQL 建立
CREATE TABLE events
USING DELTA
PARTITIONED BY (date)
AS SELECT * FROM raw_events;
```

```python
# PySpark 建立
df.write \
  .format("delta") \
  .partitionBy("date") \
  .save("/mnt/delta/events")
```

---

### 資料表屬性

| 屬性 | 說明 | 範例 |
|------|------|------|
| `LOCATION` | 實體儲存路徑 | `LOCATION '/mnt/delta/events'` |
| `PARTITIONED BY` | 分割欄位 | `PARTITIONED BY (date, region)` |
| `TBLPROPERTIES` | 自訂屬性 | `TBLPROPERTIES ('delta.autoOptimize.optimizeWrite' = 'true')` |

---

## 資料操作 (DML)

### UPDATE

```sql
UPDATE table_name
SET column = value
WHERE condition;
```

**考試重點:**
- Delta Lake 支援 UPDATE，Parquet 不支援
- WHERE 子句是選填的（但強烈建議使用）

---

### DELETE

```sql
DELETE FROM table_name
WHERE condition;
```

**考試重點:**
- DELETE 是**邏輯刪除**，不會立即釋放空間
- 需配合 VACUUM 才能實體刪除檔案

---

### MERGE (Upsert)

```sql
MERGE INTO target_table
USING source_table
ON target_table.id = source_table.id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

**完整語法結構:**
```sql
MERGE INTO target
USING source
ON merge_condition
WHEN MATCHED [AND condition] THEN UPDATE SET ...
WHEN MATCHED [AND condition] THEN DELETE
WHEN NOT MATCHED [AND condition] THEN INSERT ...
```

**考試重點:**
- `ON` 子句定義匹配條件
- 可組合多個 WHEN 子句
- `UPDATE SET *` 更新所有欄位
- 支援條件式更新/刪除

---

## Time Travel

### 查詢歷史版本

| 方法 | 語法 | 說明 |
|------|------|------|
| **版本號** | `SELECT * FROM table VERSION AS OF 42` | 查詢特定版本 |
| **時間戳記** | `SELECT * FROM table TIMESTAMP AS OF '2024-01-01'` | 查詢特定時間點 |
| **DataFrameReader** | `spark.read.format("delta").option("versionAsOf", 42)` | PySpark 寫法 |

**考試重點:**
- 版本號從 0 開始計數
- VACUUM 會刪除舊版本，影響 Time Travel 可用範圍
- Time Travel 依賴實體檔案，不僅僅是元資料

---

### 查詢版本歷史

```sql
DESCRIBE HISTORY table_name [LIMIT n];
```

**輸出欄位:**
- `version`: 版本號
- `timestamp`: 時間戳記
- `operation`: 操作類型 (WRITE, MERGE, DELETE等)
- `operationMetrics`: 操作統計資料

---

## 資料表維護

### VACUUM - 清理舊版本檔案

```sql
VACUUM table_name [RETAIN num HOURS];
```

| 參數 | 說明 | 預設值 | 考試陷阱 |
|------|------|--------|---------|
| `RETAIN` | 保留時間（小時） | 168 小時 (7 天) | **只接受 HOURS**，需換算天數 |
| `DRY RUN` | 預覽將刪除的檔案 | - | 不實際刪除，用於檢查 |

**重要提醒:**
- ⚠️ VACUUM 是**永久刪除**，無法復原
- ⚠️ 執行後會影響 Time Travel 可用範圍
- ⚠️ 預設保留 7 天，建議根據業務需求調整

**範例:**
```sql
-- 保留 30 天資料
VACUUM events RETAIN 720 HOURS;

-- 預覽將刪除的檔案（dry-run）
VACUUM events RETAIN 168 HOURS DRY RUN;
```

---

### OPTIMIZE - 合併小檔案

```sql
OPTIMIZE table_name [WHERE partition_filter]
[ZORDER BY (column1, column2, ...)];
```

| 功能 | 說明 | 使用時機 |
|------|------|---------|
| **合併小檔案** | 將小檔案合併為較大檔案 | 寫入頻繁導致大量小檔案 |
| **Z-Order** | 多維度聚集資料 | 多欄位篩選查詢 |

**考試重點:**
- OPTIMIZE **不會刪除舊版本**（與 VACUUM 的差異）
- ZORDER 最多建議 4 個欄位
- 執行後短期可能增加空間使用（需搭配 VACUUM）

**範例:**
```sql
-- 合併小檔案
OPTIMIZE events;

-- 針對特定分割區
OPTIMIZE events WHERE date >= '2024-01-01';

-- Z-Order 優化
OPTIMIZE events ZORDER BY (user_id, event_type);
```

---

### DESCRIBE DETAIL - 查看資料表詳細資訊

```sql
DESCRIBE DETAIL table_name;
```

**輸出關鍵欄位:**
- `format`: 資料格式（應為 `delta`）
- `location`: 儲存路徑
- `numFiles`: 檔案數量
- `sizeInBytes`: 資料大小
- `partitionColumns`: 分割欄位

---

## Schema 管理

### Schema Evolution 選項

| 選項 | 說明 | 使用時機 | 範例 |
|------|------|---------|------|
| `mergeSchema` | 合併新舊 Schema | 新增欄位 | `.option("mergeSchema", "true")` |
| `overwriteSchema` | 完全覆寫 Schema | 變更欄位型別或刪除欄位 | `.option("overwriteSchema", "true")` |

**範例:**
```python
# 新增欄位
df_with_new_column.write \
  .format("delta") \
  .mode("append") \
  .option("mergeSchema", "true") \
  .save("/mnt/delta/events")
```

**考試重點:**
- `mergeSchema` 只能**新增**欄位，不能刪除或變更型別
- `overwriteSchema` 會覆寫整個 Schema，需謹慎使用
- 預設不啟用，需明確指定

---

### Constraints (約束條件)

```sql
ALTER TABLE table_name ADD CONSTRAINT constraint_name CHECK (condition);
```

**範例:**
```sql
-- 檢查數值範圍
ALTER TABLE events ADD CONSTRAINT valid_age CHECK (age >= 0 AND age <= 120);

-- 檢查非空值
ALTER TABLE events ADD CONSTRAINT user_id_not_null CHECK (user_id IS NOT NULL);
```

---

## Change Data Feed (CDF)

### 啟用 CDF

```sql
ALTER TABLE table_name SET TBLPROPERTIES (delta.enableChangeDataFeed = true);
```

或在建立時啟用：
```sql
CREATE TABLE table_name
USING DELTA
TBLPROPERTIES (delta.enableChangeDataFeed = true)
AS SELECT ...;
```

### 查詢變更資料

```sql
SELECT * FROM table_changes('table_name', 2, 5);  -- 版本 2 到 5 的變更
SELECT * FROM table_changes('table_name', '2024-01-01', '2024-01-31');  -- 時間範圍
```

**輸出額外欄位:**
- `_change_type`: INSERT, UPDATE_PREIMAGE, UPDATE_POSTIMAGE, DELETE
- `_commit_version`: 變更發生的版本號
- `_commit_timestamp`: 變更時間

---

## 配置參數

### 常用 Table Properties

| 屬性 | 說明 | 預設值 | 建議值 |
|------|------|--------|--------|
| `delta.logRetentionDuration` | Log 保留時間 | 30 天 | 根據 Time Travel 需求調整 |
| `delta.deletedFileRetentionDuration` | 刪除檔案保留時間 | 7 天 | 與 VACUUM RETAIN 一致 |
| `delta.enableChangeDataFeed` | 啟用 CDF | false | 需要 CDC 功能時啟用 |
| `delta.autoOptimize.optimizeWrite` | 寫入時自動優化 | false | 寫入頻繁時啟用 |
| `delta.autoOptimize.autoCompact` | 自動合併小檔案 | false | 配合 optimizeWrite 使用 |

**設定範例:**
```sql
ALTER TABLE events SET TBLPROPERTIES (
  'delta.logRetentionDuration' = '90 days',
  'delta.deletedFileRetentionDuration' = '30 days',
  'delta.autoOptimize.optimizeWrite' = 'true'
);
```

---

## 常見錯誤與排除

### 錯誤 1: ConcurrentAppendException
**原因:** 多個寫入操作同時進行
**解決:** 使用 MERGE 或調整寫入策略

---

### 錯誤 2: ProtocolChangedException
**原因:** Delta Lake 版本不相容
**解決:** 升級 Delta Lake 版本或使用相容設定

---

### 錯誤 3: VACUUM 後無法 Time Travel
**原因:** VACUUM 刪除了需要的歷史檔案
**解決:** 調整 RETAIN 參數，確保大於 Time Travel 需求

---

## 🎯 考試高頻考點總結

### 必考觀念

1. **VACUUM vs OPTIMIZE vs DELETE 的差異**
   - VACUUM: 實體刪除舊版本檔案，釋放空間
   - OPTIMIZE: 合併小檔案，提升效能，**不刪除舊版本**
   - DELETE: 邏輯刪除資料，**不釋放空間**

2. **Time Travel 與 VACUUM 的關係**
   - VACUUM 會永久刪除檔案，影響 Time Travel 可用範圍
   - 需平衡儲存成本與資料復原需求

3. **MERGE 語法結構**
   - ON 條件、WHEN MATCHED、WHEN NOT MATCHED
   - 支援條件式更新與刪除

4. **Schema Evolution**
   - mergeSchema 只能新增欄位
   - overwriteSchema 完全覆寫

5. **單位陷阱**
   - VACUUM RETAIN 只接受 HOURS，需換算天數

---

## 📚 延伸閱讀

- [Delta Lake Official Documentation](https://docs.delta.io/)
- [Databricks Delta Lake Guide](https://docs.databricks.com/delta/index.html)
- [Delta Lake Best Practices](https://docs.databricks.com/delta/best-practices.html)

---

**快速複習完成！建議搭配實際練習題鞏固理解。** 🚀
