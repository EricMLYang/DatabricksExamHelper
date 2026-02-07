# Auto Loader Bad Records 速記

## 一句話
`badRecordsPath` = **解析/Schema 錯誤資料的隔離區**，串流不中斷。

---

## 正解觀念（Q-013 類型）
- JSON 無法解析 → 寫進 `badRecordsPath`
- JSON 可解析但 schema 不符 → 也寫進 `badRecordsPath`

```python
df = (spark.readStream
  .format("cloudFiles")
  .option("cloudFiles.format", "json")
  .option("badRecordsPath", "s3://project/quarantine")
  .schema("id int, value double")
  .load("s3://project/source/")
)
```

---

## 常見陷阱
- `pathGlobFilter`：只負責**選檔**，不是隔離路徑
- `cloudFiles.schemaLocation`：只存 schema 推論結果
- `schemaEvolutionMode`：只管**新欄位**策略，不是錯誤隔離
- `.rescue()`：不存在的 API

---

## 口訣
```
badRecordsPath = 壞資料隔離區
schemaLocation = schema 記憶體
checkpointLocation = 進度記錄器
```
