# Delta CDC + MERGE 速記（考前必讀）

## 一句話
**CDC 先去重保最新 → 再 MERGE**（INSERT/UPDATE/DELETE 三種情況）。

---

## 核心語法 1：Window 去重（保留最新）
```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, col

window_spec = Window.partitionBy("customer_id") \
                    .orderBy(col("update_time").desc())

cdc_latest = (cdc_df
  .withColumn("rn", row_number().over(window_spec))
  .filter("rn = 1")
  .drop("rn")
)
```

為什麼不用 `dropDuplicates`？
- `dropDuplicates("customer_id")` **不保證留下最新**，可能保留舊資料

---

## 核心語法 2：MERGE INTO（標準 Delta）
```sql
MERGE INTO target_table t
USING cdc_latest s
ON t.customer_id = s.customer_id

WHEN MATCHED AND s.operation = 'DELETE' THEN DELETE
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED AND s.operation != 'DELETE' THEN INSERT *
```

三種情況記憶：
- MATCHED + DELETE → DELETE
- MATCHED → UPDATE
- NOT MATCHED → INSERT

---

## DLT 專用：APPLY CHANGES INTO
```sql
APPLY CHANGES INTO target_table
FROM cdc_stream
KEYS (customer_id)
SEQUENCE BY update_time
STORED AS SCD TYPE 1
```

對比：
- `MERGE INTO` → 標準 Spark/Delta，**需手動去重**
- `APPLY CHANGES INTO` → DLT 專用，**SEQUENCE BY 自動時序處理**

---

## 考試陷阱
- `MERGE INTO ... SEQUENCE BY` ❌（MERGE 不支援）
- `dropDuplicates` ❌（隨機保留）
- CDF ❌（方向相反，是**輸出變更**不是消費 CDC）

---

## 考前速記卡
```
Window 去重保最新
MERGE 合併分三種
SEQUENCE 只能在 APPLY CHANGES
CDF 是輸出，不是接收
```
