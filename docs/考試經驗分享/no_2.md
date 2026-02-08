

<重新彙整內容>

## 📊 考試成績分布

| 科目 | 得分 | 狀態 |
|------|------|------|
| Developing Code (Python/SQL) | 61% | ⚠️ 加強 |
| **Data Ingestion & Acquisition** | 75% | ✅ |
| Data Transformation & Quality | 66% | 💪 |
| **Data Sharing and Federation** | 100% | 🎯 |
| **Monitoring and Alerting** | 100% | 🎯 |
| **Cost & Performance Optimisation** | 37% | ❌ 重點弱項 |
| Security and Compliance | 66% | 💪 |
| **Data Governance** | 75% | ✅ |
| **Debugging and Deploying** | 100% | 🎯 |
| **Data Modelling** | 75% | ✅ |

---

## 🎯 核心考點整理

### 1️⃣ SCD (Slowly Changing Dimension) - 必考！

| 類型 | 更新方式 | 歷史保留 | 使用場景 |
|------|---------|---------|---------|
| **Type 0** | ❌ 不更新 | ❌ 不維護 | 固定屬性（如出生日期、ID） |
| **Type 1** | ✅ 直接 UPDATE 覆蓋 | ❌ 只保留最新值 | 不需歷史的屬性（如地址） |
| **Type 2** | ✅ 新增一列 | ✅ 完整歷史 | 保留所有變更記錄（標記 current, end_date） |
| **Type 3** | ✅ 更新欄位 | ⚠️ 有限歷史 | 同列多欄位（current_value, previous_value） |

**實作方式**：Delta Lake `MERGE INTO` + `WHEN MATCHED ... UPDATE` + `WHEN NOT MATCHED ... INSERT`

---

### 2️⃣ 視圖與快取

#### Materialized View
- **特性**：將 View 查詢結果**實際儲存成實體資料**
- **優勢**：查詢速度快，不需重新計算
- **注意**：需手動或自動 REFRESH

---

### 3️⃣ Delta Lake 進階特性

#### Deletion Vectors
- **定義**：Delta Lake 的 **metadata 結構**
- **作用**：標記 data file 中哪些列「邏輯上被刪除」
- **優勢**：**不需立刻重寫整個檔案**，提升刪除效能

#### Auto Optimize
- **組成**：**Optimized Writes + Auto Compaction**
- **觸發**：寫入時自動執行
- **目標**：減少小檔案數量

---

### 4️⃣ CDC (Change Data Capture)

#### Lakeflow Declarative Pipelines with AUTO CDC
```sql
CREATE FLOW cdc_flow AS AUTO CDC INTO target_table
FROM stream(source_table)
KEYS (primary_key)
SEQUENCE BY timestamp_column
```
- **用途**：自動處理 INSERT、UPDATE、DELETE 操作
- **關鍵**：需指定 KEYS (主鍵) 和 SEQUENCE (排序依據)

---

### 5️⃣ Unity Catalog 權限管理

#### Secrets 管理
```bash
# 建立 Scope
databricks secrets create-scope api_scope

# 儲存 Secret
databricks secrets put-secret api_scope api_key

# 讀取 Secret
api_key = dbutils.secrets.get("api_scope", "api_key")
```

#### 資料權限
- **Row Filter**：`ALTER TABLE ... SET ROW FILTER ...`
- **Column Mask**：`ALTER TABLE ... ALTER COLUMN ... SET MASK ...`
- **權限層級**：Catalog → Schema → Table → Column

---

### 6️⃣ 效能優化

#### Broadcast Join
- **用途**：避免大表 shuffle
- **條件**：小表可放入記憶體
- **語法**：`SELECT /*+ BROADCAST(small_table) */ ...`

#### 視窗函數差異
| 函數 | 相同排名處理 | 下一排名 | 使用場景 |
|------|-------------|---------|---------|
| `rank()` | 相同排名 | 跳號 (1,2,2,4) | 競賽排名 |
| `dense_rank()` | 相同排名 | 連續 (1,2,2,3) | 分組排名 |
| `row_number()` | 唯一編號 | 連續 (1,2,3,4) | 唯一識別 |

---

### 7️⃣ System Tables - 計費分析

#### `system.billing.usage` 關鍵欄位
```sql
SELECT 
    identity_metadata.run_as AS user,           -- 使用者
    sku_name,                                   -- 計算資源類型 (JOBS_COMPUTE, ALL_PURPOSE_COMPUTE)
    SUM(usage_quantity) AS total_dbu,          -- DBU 用量
    usage_date                                  -- 日期
FROM system.billing.usage
WHERE usage_unit = 'DBU'                       -- 只看 DBU
GROUP BY user, sku_name, usage_date
ORDER BY total_dbu DESC;
```

**重要欄位**：
- `identity_metadata.run_as` → 按使用者分析
- `sku_name` → 按計算類型分析
- `usage_quantity` → DBU 消耗量
- `usage_date` → 按日期分析

---

### 8️⃣ Databricks Jobs CLI

#### 常用指令
```bash
# 列出特定 Job 的執行記錄（指定時間起）
databricks jobs list-runs --job-id <job-id> --start-time-from <time-value>

# 只列出已完成的執行
databricks jobs list-runs --job-id <job-id> --completed-only
```

---

### 9️⃣ Auto Loader 控制參數

#### `cloudFiles.maxBytesPerTrigger`
- **作用**：控制每個 micro-batch 處理的最大資料量
- **優勢**：
  - 漸進式處理大檔案
  - 保持批次處理時間可預測
  - 避免單次處理過多資料導致 OOM

---

### 🔟 DLT 資料品質監控

#### Event Log 查詢 - Expectations 結果
```sql
SELECT details:flow_progress.data_quality.expectations
FROM event_log('pipeline_id')
WHERE event_type = 'flow_progress'
```
- **用途**：查詢 DLT pipeline 的資料品質檢查結果
- **位置**：`details:flow_progress.data_quality.expectations`

---

## ⚠️ 考試重點提醒

1. **題目複雜度高**：常將 2-3 個概念混合考
2. **程式碼選項相似**：每個選項都很像，要仔細比對語法差異
3. **觀念要清楚**：不只背語法，要理解原理與使用場景
4. **弱點科目**：
   - **Cost & Performance Optimisation (37%)** - 需大量加強
   - **Developing Code (61%)** - 語法細節要熟練

---

## 💡 快速記憶法

### 數字記憶
- **500 毫秒** = 預設 Streaming trigger
- **128 MB** = Auto Compaction 目標檔案大小
- **DBU** = Databricks Unit (計費單位)

### 語法模式
- **SCD Type 2** = 新增列 + current flag
- **Broadcast Join** = 小表 + /*+ BROADCAST() */
- **Secrets** = create-scope → put-secret → get()

### 概念對比
- **Materialized View** (儲存結果) vs **Normal View** (動態查詢)
- **Deletion Vectors** (標記刪除) vs **實際刪除** (重寫檔案)
- **rank()** (跳號) vs **dense_rank()** (連續) vs **row_number()** (唯一)

</重新彙整內容>


考試小筆記:
出了bob上週說到的那些都要記，再額外補充以下給大家~
另外有些題目會把兩三個概念放一起考，重要觀念要記清楚
很多是考code 每個選項都很像要看仔細!
 
*每個都要知道
SCD Type 0（Slowly Changing Dimension Type 0）
原始值不變（Fixed Dimension）；不更新、不維護歷史，多用於不應被變更的屬性。
SCD Type 1
直接 UPDATE 覆蓋舊值，不保留歷史；只有一個最新版本。
SCD Type 2
每次變更都 新增一列，並把舊列標記為非 current（例如 current=false, end_date 設為結束時間）；
可完整保留所有歷史版本。
SCD Type 3
在同一列中保存現在值與有限數量的舊值（例如 current_address、previous_address），
不是多列歷史，而是「多欄位歷史」。
Delta Lake MERGE for SCD
常用 MERGE INTO + WHEN MATCHED ... UPDATE + WHEN NOT MATCHED ... INSERT
來實作各種型別的 SCD（尤其 Type 1, Type 2）。
 
*Materialized view 會將 view 的查詢結果 實際儲存成實體資料。
 
*Lakeflow Declarative Pipelines 中使用 AUTO CDC
 
*Databricks Unity Catalog權限
 
*使用 broadcast join 來避免大表 shuffle
 
*Deletion vectors 是 Delta Lake 的一種 metadata 結構，用來標記 data file 中哪些列「邏輯上被刪除」，而不需要立刻重寫整個檔案
 
*databricks secrets create-scope api_scope
databricks secrets put-secret api_scope api_key
api_key = dbutils.secrets.get("api_scope", "api_key")
 
*rank /dense rank/row number
 
*Auto optimize=Optimized+ Auto compaction:
 
*系統計費資料表 system.billing.usage 裡幾個重要欄位、以及怎麼用它們來看 DBU 使用量。逐項對應說明如下：
system.billing.usage: This is a system table that tracks billable usage in detail.
usage_unit = 'DBU': This explicitly filters the records to only show consumption measured in Databricks Units (DBUs), the standard unit of consumption for compute.
identity_metadata.run_as: This column logs the user or service principal (identity) who ran the workload. This is the per user component.
sku_name: This column identifies the specific type of computing resource (e.g., ALL_PURPOSE_COMPUTE, JOBS_COMPUTE, SERVERLESS_SQL) that consumed the DBUs. This gives the type of computing resource detail.
usage_quantity: This is the actual DBU consumption amount.
usage_date: This provides the daily temporal detail.
 
*兩個一起考
databricks jobs list-runs --job-id <job-id> --start-time-from <time-value>
databricks jobs list-runs --job-id <job-id> --completed-only
 
*In Auto Loader, “cloudFiles.maxBytesPerTrigger” controls the maximum amount of data to process in each micro-batch, allowing the stream to handle large files incrementally and keep batch processing times predictable.
* details:flow_progress:data_quality.expectations: specifically holds the expectation results。