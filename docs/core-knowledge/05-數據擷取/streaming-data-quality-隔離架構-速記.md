# 串流資料品質隔離架構｜考前速讀版

## 一句話
**主線保乾淨，壞資料旁路存。**

---

## 需求拆解（四句話）
- 即時儀表板要**持續更新**
- 只能用**乾淨資料**
- 壞資料要**保留可追查**
- **資源最小化**

---

## 正確架構（A）
```
Streaming Source
   ↓
Schema Validation
 ↙             ↘
Valid           Corrupted
 ↓                ↓
Production      Quarantine
Delta Table     (lightweight)
 ↓
Dashboard
```

---

## Databricks 速記做法（Auto Loader）
```python
# 主流程：只寫有效資料
valid_stream = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.schemaLocation", schema_path)
    .load(source_path)
    .filter("_rescued_data IS NULL")
    .writeStream
    .format("delta")
    .option("checkpointLocation", checkpoint_path)
    .table("production.sensor_readings")
)

# 旁路：保留壞資料（低頻）
corrupted_stream = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.schemaLocation", schema_path)
    .load(source_path)
    .filter("_rescued_data IS NOT NULL")
    .writeStream
    .format("delta")
    .option("checkpointLocation", corrupted_checkpoint_path)
    .trigger(processingTime="5 minutes")
    .table("quarantine.corrupted_records")
)
```

---

## 為什麼其他選項錯
- B/C：把壞資料混入主表 → 污染即時分析，增加下游負擔
- D：schema 失敗通常是**資料本身錯**，重試只是浪費資源

---

## 10 秒記憶
```
Fail Fast
Clean Pipeline
Side Channel
Low Cost
```
