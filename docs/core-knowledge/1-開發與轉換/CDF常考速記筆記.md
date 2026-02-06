我來幫你設計一個 Change Data Feed (CDF) 的速記快覽筆記，涵蓋常考情境和對應語法。# 📘 Databricks CDF 常考速記筆記

## 📊 核心概念對照表

| 特性 | spark.read (Batch) | spark.readStream (Streaming) |
|------|-------------------|------------------------------|
| **處理模式** | 批次/靜態 | 串流/增量 |
| **版本範圍** | 固定範圍 (startingVersion → ending) | 從起點持續處理新變更 |
| **進度追蹤** | ❌ 無 checkpoint | ✅ checkpoint 自動記錄 |
| **重複執行** | 每次讀取完整範圍 | 只處理新增變更 |
| **適用場景** | 一次性歷史分析 | 持續 CDC 管道 |
| **資源效率** | 重複處理歷史數據 | 只處理增量 |

---

## 🎯 常考情境與語法

### 情境 1: Batch 讀取完整歷史 (考試高頻)

**題型特徵:**
- 使用 `spark.read`
- `startingVersion: 0` 固定起點
- `mode("overwrite")` 覆蓋模式

```python
# ⚠️ 危險模式：每次執行都讀取完整歷史
spark.read \
    .option("readChangeFeed", "true") \
    .option("startingVersion", 0) \  # 從版本 0 開始
    .table("customers") \
    .filter(col("_change_type").isin(["update_postimage"])) \
    .write \
    .mode("overwrite") \  # 覆蓋目標表
    .table("customers_updates")

# 執行行為：
# 第1次執行: 讀取 v0→v10 的所有 update → 覆蓋目標表
# 第2次執行: 讀取 v0→v15 的所有 update → 再次覆蓋目標表
# ❌ 問題：重複讀取歷史，無增量處理
```

**記憶口訣:** 「Batch 讀全量，overwrite 蓋全表」

---

### 情境 2: Streaming 增量處理 (生產最佳實踐)

**題型特徵:**
- 使用 `spark.readStream`
- 有 `checkpointLocation`
- 自動追蹤進度

```python
# ✅ 正確模式：串流增量處理
spark.readStream \
    .option("readChangeFeed", "true") \
    .table("customers") \
    .filter(col("_change_type").isin(["update_postimage"])) \
    .writeStream \
    .option("checkpointLocation", "/checkpoint/customers_cdc") \
    .outputMode("append") \
    .table("customers_updates")

# 執行行為：
# 第1次執行: 讀取完整快照為 INSERT → 寫入
# 第2次執行: 只讀取新變更 (自動從 checkpoint 記錄處繼續)
# ✅ 優點：增量處理，不重複讀取
```

---

### 情境 3: 指定版本範圍讀取

```python
# 讀取特定版本區間
df = spark.read \
    .format("delta") \
    .option("readChangeFeed", "true") \
    .option("startingVersion", 5) \
    .option("endingVersion", 10) \
    .table("customers")

# 使用時間戳
df = spark.read \
    .format("delta") \
    .option("readChangeFeed", "true") \
    .option("startingTimestamp", "2024-01-01 00:00:00") \
    .option("endingTimestamp", "2024-01-31 23:59:59") \
    .table("customers")
```

---

### 情境 4: CDF 元數據欄位

```python
# CDF 自動提供 3 個元數據欄位
df = spark.read \
    .option("readChangeFeed", "true") \
    .option("startingVersion", 0) \
    .table("customers")

df.select("id", "name", "_change_type", "_commit_version", "_commit_timestamp").show()

# 輸出範例:
# +---+-------+------------------+---------------+-------------------+
# | id| name  | _change_type     |_commit_version|_commit_timestamp  |
# +---+-------+------------------+---------------+-------------------+
# |  1| Alice | insert           |             0 | 2024-01-01 10:00  |
# |  1| Alice | update_preimage  |             5 | 2024-01-02 14:30  |
# |  1| Alice2| update_postimage |             5 | 2024-01-02 14:30  |
# |  2| Bob   | delete           |             8 | 2024-01-03 09:15  |
# +---+-------+------------------+---------------+-------------------+
```

**元數據欄位說明:**
- `_change_type`: `insert`, `update_preimage`, `update_postimage`, `delete`
- `_commit_version`: 變更發生的 Delta 版本號
- `_commit_timestamp`: 變更提交時間戳

---

### 情境 5: 啟用 CDF

```python
# 方法 1: 建表時啟用
spark.sql("""
    CREATE TABLE customers (
        id INT,
        name STRING,
        email STRING
    )
    TBLPROPERTIES (delta.enableChangeDataFeed = true)
""")

# 方法 2: 既有表格啟用
spark.sql("""
    ALTER TABLE customers 
    SET TBLPROPERTIES (delta.enableChangeDataFeed = true)
""")

# 方法 3: Python API
from delta.tables import DeltaTable

DeltaTable.createIfNotExists(spark) \
    .tableName("customers") \
    .addColumn("id", "INT") \
    .addColumn("name", "STRING") \
    .property("delta.enableChangeDataFeed", "true") \
    .execute()
```

**⚠️ 重要限制:**
- CDF 是 **forward-looking**：只追蹤啟用後的變更
- 無法回溯啟用前的歷史
- 會被 `VACUUM` 清除

---

### 情境 6: SCD Type 1 vs Type 2

#### SCD Type 1: 直接更新 (不保留歷史)
```python
# 使用 AUTO CDC (Pipelines)
import dlt

@dlt.table
def customers_scd1():
    return spark.readStream.table("customers_cdf")

dlt.create_auto_cdc_flow(
    target="customers_current",
    source="customers_scd1",
    keys=["customer_id"],
    sequence_by="sequenceNum",
    scd_type="1"  # Type 1: 直接更新
)
```

#### SCD Type 2: 保留歷史版本
```python
# SCD Type 2: 新增有效期欄位
dlt.create_auto_cdc_flow(
    target="customers_history",
    source="customers_scd1",
    keys=["customer_id"],
    sequence_by="sequenceNum",
    scd_type="2",  # Type 2: 保留歷史
    track_history_column_list=["email", "address"]  # 追蹤這些欄位變更
)

# 產生的表結構會包含:
# - __START_AT: 記錄生效時間
# - __END_AT: 記錄失效時間
# - __IS_CURRENT: 是否為當前版本
```

---

### 情境 7: 使用 MERGE 處理 CDC (傳統方法)

```python
from delta.tables import DeltaTable

# 讀取變更
changes = spark.read \
    .option("readChangeFeed", "true") \
    .option("startingVersion", 5) \
    .table("customers")

# 手動 MERGE
target = DeltaTable.forName(spark, "customers_current")

target.alias("t").merge(
    changes.filter(col("_change_type") == "update_postimage").alias("s"),
    "t.id = s.id"
).whenMatchedUpdate(
    set={
        "name": "s.name",
        "email": "s.email",
        "updated_at": "s._commit_timestamp"
    }
).whenNotMatchedInsert(
    values={
        "id": "s.id",
        "name": "s.name",
        "email": "s.email",
        "updated_at": "s._commit_timestamp"
    }
).execute()
```

**⚠️ MERGE 的問題 (為何考試推薦 AUTO CDC):**
- 無法自動處理亂序記錄
- 需要手動編寫複雜 sequencing 邏輯
- 容易產生錯誤結果

---

## 🔥 常考陷阱總結

### 陷阱 1: Batch vs Streaming 混淆
```python
# ❌ 錯誤認知：認為 startingVersion 會「記住」進度
spark.read \
    .option("readChangeFeed", "true") \
    .option("startingVersion", 0) \  # 每次都從 0 開始！
    .table("source")

# ✅ 正確做法：使用 streaming + checkpoint
spark.readStream \
    .option("readChangeFeed", "true") \
    .option("checkpointLocation", "/checkpoint/path") \  # 自動記錄進度
    .table("source")
```

### 陷阱 2: Append vs Overwrite 誤判
```python
# 題目問：「會發生什麼？」
.write.mode("overwrite").table("target")

# ❌ 錯誤：認為是「增量 append」
# ✅ 正確：每次完全覆蓋目標表
```

### 陷阱 3: CDF 不是永久存儲
```python
# ❌ 錯誤：把 CDF 當作 audit log
# CDF 會被 VACUUM 清除

# ✅ 正確：需要寫入獨立 audit table
spark.readStream \
    .option("readChangeFeed", "true") \
    .table("source") \
    .writeStream \
    .option("checkpointLocation", "/checkpoint") \
    .trigger(availableNow=True) \  # 批次處理模式
    .table("audit_table")  # 永久保存變更歷史
```

---

## 📋 快速決策樹

```
需求：處理 Delta Lake 變更
    │
    ├─ 一次性歷史分析？
    │   └─ 使用 spark.read + startingVersion/endingVersion
    │
    ├─ 持續增量處理？
    │   └─ 使用 spark.readStream + checkpointLocation
    │
    ├─ 需要保留歷史？
    │   ├─ SCD Type 2 (保留所有版本)
    │   └─ 寫入獨立 audit table
    │
    └─ 只要最新狀態？
        └─ SCD Type 1 (直接更新)
```

---

## 🎓 考試答題技巧

1. **看到 `spark.read` + `startingVersion: 0`**
   - → 批次讀取完整歷史
   - → 配合 `mode("overwrite")` = 每次覆蓋全表

2. **看到 `spark.readStream` + `checkpointLocation`**
   - → 串流增量處理
   - → 只處理新變更

3. **看到 `_change_type`**
   - `insert`: 新增記錄
   - `update_preimage`: 更新前的舊值
   - `update_postimage`: 更新後的新值
   - `delete`: 刪除記錄

4. **版本 vs 時間戳**
   - 版本號優先用於精確控制
   - 時間戳用於時間範圍查詢

---

這份筆記涵蓋了 Databricks CDF 認證考試的所有高頻考點。需要我針對特定情境再深入解析嗎?