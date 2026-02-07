# Auto Loader Schema Evolution 速記（考前速讀版）

## 一句話
需求「新欄位偵測就失敗、但 schema 仍要更新」→ **`addNewColumns`**。

---

## 四大模式行為對照表
| 模式 | 偵測新欄位時 | Schema 是否更新 | 資料處理方式 | 典型場景 |
|---|---|---|---|---|
| **addNewColumns** ⭐ | 立即失敗該批次 | ✅ 會更新 | 重啟後用新 schema | 需人工審核新欄位 |
| **failOnNewColumns** | 立即失敗該批次 | ❌ 不更新 | 一直卡住 | 嚴格禁止 schema 變更 |
| **rescue** | 不失敗 | ❌ 不更新 | 新欄位進 `_rescued_data` | 容錯優先 |
| **none** (預設) | 不失敗 | ❌ 不更新 | 新欄位忽略 | schema 固定 |

---

## 題目需求拆解（Q-039 類型）
```
需求 1: 新欄位偵測就失敗 → 排除 rescue / none
需求 2: schema 還要更新 → 排除 failOnNewColumns
結論: addNewColumns ✅
```

---

## 速記口訣
```
addNewColumns = 先炸一次，schema 會長大
failOnNewColumns = 一直炸，不會長大
rescue = 不炸，把新欄塞垃圾桶
none = 不炸，當沒看到
```

---

## 重要參數位置
```python
.option("cloudFiles.schemaEvolutionMode", "addNewColumns")
.option("cloudFiles.schemaLocation", "s3://.../checkpoints/...")
.option("checkpointLocation", "s3://.../checkpoints/...")
```

---

## 常見陷阱
- 看到「fail」就選 `failOnNewColumns` → 錯（不更新 schema）
- 把 `rescue` 當「更新 schema」→ 錯（只塞 `_rescued_data`）
- 忘記 `none` 是預設 → 仍然不更新 schema
