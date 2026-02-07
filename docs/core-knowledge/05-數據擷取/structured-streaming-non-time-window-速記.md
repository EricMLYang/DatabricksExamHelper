# Structured Streaming 非時間視窗限制 速記

## 一句話
**Non-time-based window functions（rank/row_number/lead/lag）在 streaming DataFrame 上不支援**。

---

## 為什麼不支援
- Streaming 是無界資料流
- 排名類函數需要完整 partition 才能計算
- 狀態會無限膨脹 → 記憶體不可控

---

## 典型錯誤訊息
```
AnalysisException: Non-time-based windows are not supported on streaming DataFrames
```

---

## 正確解法：foreachBatch
用 micro-batch 的批次語意執行非時間視窗：
```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window

def process_batch(batch_df, batch_id):
    w = Window.partitionBy("item_id").orderBy(F.col("item_time").desc())
    result_df = (batch_df
        .withColumn("rank", F.rank().over(w))
        .filter("rank = 1")
        .drop("rank")
    )
    result_df.write.mode("append").saveAsTable("sales_latest")

(spark.readStream
  .table("sales")
  .writeStream
  .foreachBatch(process_batch)
  .outputMode("update")
  .start()
)
```

---

## Streaming 支援矩陣（考點）
| 操作類型 | Streaming 支援 | 說明 |
|---|---|---|
| Selection/Projection | ✅ | select/filter/where |
| Aggregation | ✅ | groupBy + agg（需 watermark） |
| Time-based Window | ✅ | window(event time) |
| Non-time-based Window | ❌ | rank/row_number/lead/lag |
| Joins | ⚠️ | stream-stream / stream-static |
| Distinct/dropDuplicates | ⚠️ | 需 watermark |
