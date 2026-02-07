# Delta Lake DEEP CLONE / 增量同步 速記（考前複習）

## 這題在考什麼
你先做了：
```
CREATE TABLE orders_archive
DEEP CLONE orders
```
來源表 `orders` 持續有新變更，想把**新變更同步**到 `orders_archive`。

**重點：** deep clone 是獨立副本（資料 + transaction log），**不會自動跟著來源變動**。

---

## 正解（必記）
✅
```
CREATE OR REPLACE TABLE orders_archive
DEEP CLONE orders
```

### 為什麼是它？
1. 對既有 clone 目標表「再次 clone」
2. **增量同步**：只套用**自上次 clone 之後的差異**，不是全量重拷

> 關鍵字：**REPLACE + existing Delta target = incremental clone**

---

## 快速記憶法
- **DEEP CLONE** = 獨立完整副本（資料 + metadata + log）
- **要同步** = 再跑一次 clone（搭配 `CREATE OR REPLACE`）
- **增量同步關鍵字** = `REPLACE` + 已存在的 Delta target

---

## 其他選項為什麼是陷阱
- `SYNC orders_archive` ❌
  - SYNC 是 HMS/UC 同步的用途，不是 clone 的資料同步
- `INSERT OVERWRITE orders_archive SELECT * FROM orders` ❌
  - 變成 ETL 覆寫，不是 clone 的增量機制，也可能破壞 clone 語意
- `REFRESH orders_archive` ❌
  - 只刷新 metadata/cache，不會同步來源變更

---

## 實務案例：DR / 備援副本
**情境**：跨區域/跨環境保留備援表（非近即時）

**做法（排程每 30 分鐘/每小時）**
```
CREATE OR REPLACE TABLE orders_archive
DEEP CLONE orders;
```

**為什麼適合**
- deep clone 不依賴來源資料檔（不像 shallow clone 會引用來源檔案）
- `REPLACE ... CLONE` 對既有 target 會走增量 commit，效率高
- 適合作為**週期性快照/備援**，不是近即時 replication

---

## 一句話考前作答
Delta 的 deep clone 是獨立副本，不會自動同步；要把新變更同步進 clone，需對目標表再執行 `CREATE OR REPLACE ... [DEEP] CLONE source`，且對既有 Delta target 會以**增量 commit**套用上次 clone 後的變更。
