```markdown
# CDF / CDC 說明文件（以目的與作用說清楚）

## 1) 目的與作用差異（先用一句話分開）
- **CDF (Change Data Feed)**：讓你可以「讀到某張 Delta 表的變更事件」。（insert / update / delete）
- **CDC (Change Data Capture)**：一套「把變更套用到目標表」的做法；常見落地方式就是 **`MERGE INTO`**。

---

## 2) CDF（Change Data Feed）

### 2.1 CDF 在做什麼
CDF 會讓 Delta 表能提供「這段期間有哪些列被改了」的資料輸出；你下游就能只處理變更，而不是每次重掃全表。

### 2.2 開啟 CDF（表層級設定）
```sql
ALTER TABLE my_table
SET TBLPROPERTIES (delta.enableChangeDataFeed = true);
```

（也可在建立表時用 TBLPROPERTIES 開啟）

### 2.3 讀 CDF：最常用的兩種「簡易語法」

#### A) SQL：`table_changes`（批次查變更）

```sql
-- 讀取從 version 0 到 10 的變更
SELECT * FROM table_changes('my_table', 0, 10);

-- 只給起點：從 version 0 一路讀到最新
SELECT * FROM table_changes('my_table', 0);
```

回傳會包含原表欄位 + CDF 3 個欄位：
- `_change_type`（insert / delete / update_preimage / update_postimage）
- `_commit_version`
- `_commit_timestamp`

#### B) Streaming：讀變更（readChangeFeed）

```python
df = (spark.readStream
  .option("readChangeFeed", "true")
  .table("my_table")
)
```

**重要：首次啟動行為**  
首次啟動時，Streaming 會先回傳整個表的當前 snapshot（全部標記為 INSERT），之後才開始回傳增量變更。如果目標表已經有完整資料，可用 `startingVersion` 跳過初始 snapshot。

```python
# 從特定版本開始讀取（跳過初始 snapshot）
df = (spark.readStream
  .option("readChangeFeed", "true")
  .option("startingVersion", 5)
  .table("my_table")
)
```

### 2.4 CDF 重要限制（實務必知）

#### 1. 只記錄啟用後的變更
CDF 不是追溯性的，只會記錄「啟用 CDF 之後」發生的變更。啟用前的歷史版本無法透過 CDF 查詢。

#### 2. 受 VACUUM 影響
變更檔案會跟隨表的 retention policy。執行 `VACUUM` 時，舊的變更檔案會被刪除。

如果需要長期保留變更記錄（如稽核用途），務必調整 `delta.logRetentionDuration` 設定：

```sql
ALTER TABLE my_table 
SET TBLPROPERTIES (
  delta.logRetentionDuration = '30 days',
  delta.deletedFileRetentionDuration = '30 days'
);
```

#### 3. 部分操作不產生變更檔案
某些操作（insert-only、全分區刪除）不會產生獨立的變更檔案，Databricks 會直接從 transaction log 計算 CDF。

#### 4. 儲存成本增加
啟用 CDF 會增加少量儲存成本，因為變更可能記錄在獨立的檔案中（存放在 `_change_data` 目錄）。

#### 5. 指定的 version 必須存在
如果指定的 `startingVersion` 已被 VACUUM 清理，串流會無法啟動並報錯。

---

## 3) CDC（Change Data Capture）

### 3.1 CDC 在做什麼

CDC 的重點不是「讀變更」，而是「把變更正確套用到目標表」：
- source 來了新資料 → 插入
- source 有更新 → 更新目標
- source 告訴你刪除 → 刪除目標

### 3.2 CDC 常見落地：`MERGE INTO`（用一段 SQL 同時做 insert / update / delete）

`MERGE INTO` 的核心是：用 `ON` 定義「同一筆資料怎麼對齊」，再用三種分支決定要做什麼。

#### MERGE 的基本骨架

```sql
MERGE INTO target_table AS t
USING source_table AS s
ON t.id = s.id

WHEN MATCHED THEN
  UPDATE SET *

WHEN NOT MATCHED THEN
  INSERT *

WHEN NOT MATCHED BY SOURCE THEN
  DELETE;
```

**三種分支說明：**
- **WHEN MATCHED**：target & source 都找到同一筆（通常做 UPDATE / DELETE）
- **WHEN NOT MATCHED**：source 有、target 沒有（做 INSERT）
- **WHEN NOT MATCHED BY SOURCE**：target 有、source 沒有（常用於同步時清掉目標多出來的資料）

> 注意：`WHEN NOT MATCHED BY SOURCE` 需要 **Databricks Runtime 12.2 LTS 以上**才完整支援。

#### 常見 CDC（帶操作類型）的寫法

```sql
MERGE INTO target_table AS t
USING source_changes AS s
ON t.id = s.id

WHEN MATCHED AND s.op = 'UPDATE' THEN
  UPDATE SET *

WHEN MATCHED AND s.op = 'DELETE' THEN
  DELETE

WHEN NOT MATCHED AND s.op = 'INSERT' THEN
  INSERT *;
```

這種寫法的意思很直白：source 先把每筆變更標成 INSERT/UPDATE/DELETE，MERGE 只負責照規則把變更套到 target。

### 3.3 處理 CDF 多筆匹配問題（實務最佳做法）

當使用 CDF 作為 source 時，UPDATE 操作會產生兩筆記錄：
- `update_preimage`（更新前）
- `update_postimage`（更新後）

如果直接把 CDF 當作 source 進行 MERGE，會因為「多筆 source 匹配同一筆 target」而報錯：

```
錯誤訊息：DELTA_MULTIPLE_SOURCE_ROW_MATCHING_TARGET_ROW_IN_MERGE
```

#### 解決方法：先對 source 去重，只保留最新版本

**方法 1：使用 ROW_NUMBER 去重**

```sql
-- 先對 CDF 結果去重
WITH deduped_source AS (
  SELECT * FROM (
    SELECT *, 
           ROW_NUMBER() OVER (
             PARTITION BY id 
             ORDER BY _commit_version DESC, _commit_timestamp DESC
           ) as rn
    FROM table_changes('source_table', 0)
  ) WHERE rn = 1
)
MERGE INTO target_table AS t
USING deduped_source AS s
ON t.id = s.id

WHEN MATCHED AND s._change_type = 'delete' THEN
  DELETE

WHEN MATCHED AND s._change_type IN ('update_postimage', 'insert') THEN
  UPDATE SET *

WHEN NOT MATCHED AND s._change_type IN ('update_postimage', 'insert') THEN
  INSERT *;
```

**方法 2：只取 update_postimage（忽略 preimage）**

```sql
-- 過濾掉 update_preimage
WITH latest_changes AS (
  SELECT *
  FROM table_changes('source_table', 0)
  WHERE _change_type != 'update_preimage'  -- 過濾掉更新前的狀態
)
MERGE INTO target_table AS t
USING latest_changes AS s
ON t.id = s.id

WHEN MATCHED AND s._change_type = 'delete' THEN
  DELETE

WHEN MATCHED THEN
  UPDATE SET *

WHEN NOT MATCHED THEN
  INSERT *;
```

**關鍵要點：**
1. UPDATE 操作一定會產生兩筆記錄，必須先處理
2. 通常只需要 `update_postimage`（更新後的值）
3. 使用 `ROW_NUMBER` 或過濾 `_change_type` 來去重
4. DELETE 要優先處理（放在第一個 WHEN MATCHED）

### 3.4 新工具：AUTO CDC API（Databricks 推薦）

Databricks 現在提供 **AUTO CDC API**（原名 APPLY CHANGES），可以自動處理亂序資料、去重和 SCD Type 1/2 操作，不需要手寫複雜的 MERGE 邏輯。

#### Python 語法（Delta Live Tables）

```python
import dlt
from pyspark.sql.functions import col

dlt.create_auto_cdc_flow(
    target = "my_target_table",
    source = "my_cdf_stream",
    keys = ["id"],
    sequence_by = col("_commit_version"),  # 用來判斷記錄順序
    stored_as_scd_type = 1  # 或 2（SCD Type 2 會保留歷史版本）
)
```

#### 優勢
- 自動處理亂序資料（late-arriving data）
- 自動去重（不需要手寫 ROW_NUMBER）
- 支援 SCD Type 1 和 Type 2
- 效能比手寫 MERGE 更好

#### 適用場景
- 需要處理即時串流 CDC 資料
- 資料可能亂序到達
- 需要 SCD Type 2 歷史版本追蹤

---

## 4) 總結：CDF vs CDC 怎麼選

| 面向 | CDF | CDC (MERGE INTO) | AUTO CDC API |
|------|-----|------------------|--------------|
| 用途 | 讀取變更事件 | 套用變更到目標表 | 自動化 CDC 處理 |
| 適用場景 | 稽核、下游系統同步 | 手動控制合併邏輯 | 即時串流、SCD |
| 複雜度 | 低 | 中（需處理去重） | 低（自動化） |
| 效能 | 高（只讀變更） | 中（需要 MERGE） | 高（優化過） |
| 亂序處理 | 不處理 | 需手動處理 | 自動處理 |

**建議做法：**
1. 使用 CDF 讀取變更
2. 如需自己控制邏輯，用 MERGE INTO（記得去重）
3. 如需自動化且高效能，優先考慮 AUTO CDC API
```