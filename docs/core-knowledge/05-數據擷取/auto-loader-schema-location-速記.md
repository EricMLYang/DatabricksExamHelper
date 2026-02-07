# Auto Loader Schema 推論 速記（實戰速成）

## 一句話
**`schemaLocation` = schema 記憶體**，存一次、後續免重推論。

---

## 核心結論
- 不想每次重掃 50GB / 1000 檔 → 一定要設 `cloudFiles.schemaLocation`
- 仍可追蹤 schema 變更（版本會存到 `_schemas/`）

---

## 沒設 vs 有設
### 沒設（每次都推論）
- 每次啟動都重新掃描前 50GB/1000 檔
- 成本高、時間長

### 有設（只推論一次）
- 第一次推論後寫入 `schemaLocation`
- 後續直接讀 schema 檔
- 成本大幅下降

---

## 題目速判（Q-041 類型）
```
需求: avoid re-sampling + reduce cost + track schema changes
答案: .option("cloudFiles.schemaLocation", "/path/to/checkpoint")
```

---

## 常見陷阱
- `schemaEvolutionMode`：只管「新欄位怎麼處理」
- `checkpointLocation`：只管「進度」
- `mergeSchema`：Delta 寫入用，不是 Auto Loader

---

## 生產建議標配
```python
spark.readStream.format("cloudFiles") \
  .option("cloudFiles.format", "json") \
  .option("cloudFiles.schemaLocation", "/schema/xxx") \
  .option("cloudFiles.schemaEvolutionMode", "addNewColumns") \
  .option("checkpointLocation", "/checkpoint/xxx") \
  .load("/raw/xxx")
```

---

## 口訣
```
schemaLocation = schema 記憶體
checkpointLocation = 進度記錄器
```
