# Databricks SOP

## Dev/Prod.

- Architecture
   

   ![](https://hackmd.io/_uploads/HJZV6ssnlg.png)

- 報告

   - 

      ![](https://hackmd.io/_uploads/HJ8m6N0sxx.png)

- Workspace： 

   - S4M 會提供三個環境

      1. 開發(Dev)

         - Azure name:(待補上)

         - MongoDB: 

            - 與測試用DB一致

      2. 測試(Testing)

         - Azure name:([databricks_testing](https://adb-2468759545490070.10.azuredatabricks.net/?o=2468759545490070&l=zh-hant))

         - MongoDB: 

            - 測試用DB

            - 沒使用時須關閉

      3. 模擬(Staging)

         - Azure name:(待補上)

         - CosmosDB: 模擬用

      4. 正式(Prod)

         - Azure name:(待補上)

         - CosmosDB: 正式用

      5. 正式(Family)

         - Azure name:(待補上)

         - MongoDB: 正式用

- Catalog: Dev/ Prod. 一模一樣的命名

   - 全家

      - catalog name: family-report-prod

      - schema name: family-mart

      - schema name (archive):family-mart-archive

   - S4M-Dev

      - catalog name: impress-report-dev 

      - schema name: impress-mart-dev 

      - schema name (archive):impress-mart-dev-archive

   - S4M-Testing

      - catalog name: impress-report-testing

      - schema name: impress-mart-testing

      - schema name (archive):impress-mart-testing-archive

   - S4M-Staging

      - catalog name: impress-report-Staging

      - schema name: impress-mart-Staging

      - schema name (archive):impress-mart-Staging-archive

   - S4M-Prod

      - catalog name: impress-report-prod

      - schema name: impress-mart-prod

      - schema name (archive):impress-mart-prod-archive

## 存封

- family-mart-archive 要連接最便宜的 storage

   - storage 有存取層級 (Access Tiers)，就挑延遲最高、價格最低的

## 計算資源

- prod：成本為主要考量的話就先開 4 核最小的，不開 auto scaling 

   - 暫定:

      - Compute Cluster: 

         - 

            ![](https://hackmd.io/_uploads/S10S4VRoee.png)

      - SQL warehouse

         - 

            ![](https://hackmd.io/_uploads/r13gs_QTlx.png)

   - 執行時間:

      - 原則都是批次啟動 Job (每 4 – 8 - 12 hr 開一次都可以考量，會分散到很多 Job， 每次執行含開機應該會在 10 分鐘內)

      - 估計每天啟動約 1.5 小時 \* 30 天來算

      - SQL warehouse 用 20 小時每月估計

## 費用:



![](https://hackmd.io/_uploads/Bkmpqd76ee.png)

## 問題：

- To Eric

   - Q1: 存封等級的 Blob 建議儲存多久?

   - Q2: 銅質資料預計會存多久?

   - Q3: Databricks 程式碼是否會儲存在我們環境?

   - Q4: 有無測試流程?如何在全家端測試?

## 時程

- Dev databricks 建置 -> 已建置完成 -> <https://adb-712494778862333.13.azuredatabricks.net/>

- testing databricks 環境 -> 已有

- Pord databricks 建置 -> 待定

- Family databricks 建置 -> 待定

- Azure DevOps for S4M -> 9/24 前

## \[SOP\]

### MongoDB 數據擷取 UC 與 MongoDB Spark Connector 相容性指南

#### 基礎知識

spark 

mongo-spark-connector

---

## 解決方案（二選一，沒其他原因的話以 B 為主）

### 方案 A：純 UC 環境 + v3.x 連接器

**適用場景**：環境必須使用 UC，且可接受 v3.x 功能
**架構圖**：

```
UC 叢集 (v3.x) → MongoDB → UC Delta 表
```

**實作**：

```python
# 安裝套件：org.mongodb.spark:mongo-spark-connector_2.12:3.x

df = spark.read.format("mongo") \
    .option("uri", connection_string) \
    .option("database", "db_name") \
    .option("collection", "collection_name") \
    .load()

# 寫入 UC 管理的表
df.write.saveAsTable("catalog.schema.table_name")
```

**優點**：

- v3.x 基於 **DataSource V1**，與 UC 完全相容

- 最小變更，配置簡單

- 資料直接受 UC 治理

**限制**：

- 無法使用 v10.x 的新功能（如增強的 Structured Streaming、更好的效能優化）

---

### 方案 B：分離架構 (v10.x 抽取 + UC 治理)

**適用場景**：需要 v10.x 新功能，同時需要 UC 治理
**架構圖**：

```
非 UC 叢集 (v10.x) → MongoDB → 物件儲存 (Delta) → UC 叢集 → 受治理的表
```

**實作步驟**：
**Step 1：建立非 UC 叢集並安裝 v10.x**

```
套件：org.mongodb.spark:mongo-spark-connector_2.12:10.x
Access Mode：任意（建議 Single User 以避免限制）
```

**Step 2：在非 UC 叢集抽取資料**

```python
df = spark.read.format("mongodb") \
    .option("connection.uri", connection_string) \
    .option("database", "db_name") \
    .option("collection", "collection_name") \
    .load()

# 寫入物件儲存（S3/ADLS/GCS）
df.write.format("delta") \
    .mode("overwrite") \
    .save("s3://bucket/path/mongo_data")
```

**Step 3：在 UC 叢集建立受治理的表**

```python
# 在 UC 叢集執行
spark.sql("""
CREATE TABLE IF NOT EXISTS catalog.schema.mongo_table 
USING DELTA 
LOCATION 's3://bucket/path/mongo_data'
""")

# 設定權限
spark.sql("GRANT SELECT ON TABLE catalog.schema.mongo_table TO `data_analysts`")
```

**Step 4：使用者透過 UC 存取**

```python
# 所有存取都受 UC 權限控管、稽核、血緣追蹤
df = spark.sql("SELECT * FROM catalog.schema.mongo_table")
```

**優點**：

- 可使用 v10.x 所有新功能和效能優化

- 最終資料仍完整受 UC 治理（權限、稽核、血緣）

- 清晰的責任分離：抽取層 vs 治理層

- 適合企業級長期架構

**限制**：

- 需要維護兩種叢集配置 

- 資料流程多一個步驟（抽取 → 落地 → 註冊）

- 即時性稍差（需要排程或觸發抽取作業）

---

#### Access Mode 選擇指南

##### UC 叢集的 Access Mode

| Mode | 說明 | 建議使用時機 | 
|---|---|---|
| **Standard**<br>(前稱 Shared) | 多人共用資源<br>Databricks 官方推薦 | **預設優先選擇**<br>適用多數工作負載 | 
| **Dedicated**<br>(前稱 Single-user) | 單一使用者或群組<br>完整環境控制 | Standard 不支援的功能<br>部分第三方連接器需求 | 

> **實務提醒**：部分 DataSource V2 連接器在 Standard 模式會失敗，但在 Dedicated 模式可運行。建議先嘗試 Standard，遇到問題再切換。

##### 非 UC 叢集的 Access Mode

- 無 UC 限制，選擇任意 Access Mode 即可

- 建議使用 **Single User** 以簡化配置

---

#### 名詞速查表

| 術語 | 說明 | 
|---|---|
| **UC 叢集** | 啟用 Unity Catalog 的計算環境<br>提供集中式資料治理（權限、稽核、血緣追蹤） | 
| **非 UC 叢集** | 傳統叢集，使用 Hive Metastore<br>對第三方連接器限制較少 | 
| **DataSource V1** | Spark 舊版資料源 API<br>相容性廣，但功能較少 | 
| **DataSource V2** | Spark 新版資料源 API<br>效能更好，但需平台端支援與整合 | 
| **v3.x** | MongoDB Connector 舊版<br>使用 `format("mongo")`，基於 V1 API | 
| **v10.x** | MongoDB Connector 新版<br>使用 `format("mongodb")`，基於 V2 API | 
| **Standard Mode** | 前稱 Shared Access Mode<br>UC 叢集的推薦模式 | 
| **Dedicated Mode** | 前稱 Single-user Access Mode<br>特殊需求時使用 | 

---

#### 快速決策流程

```
需要 Unity Catalog 資料治理？
│
├─ 是 → 能接受 v3.x 功能限制？
│      │
│      ├─ 是 → 方案 A
│      │       純 UC 環境 + v3.x
│      │       ✓ 最簡單
│      │       ✗ 功能受限
│      │
│      └─ 否 → 方案 B
│              分離架構 (非 UC v10.x + UC 治理)
│              ✓ 完整功能 + 完整治理
│              ✗ 架構較複雜
│
└─ 否 → 直接使用非 UC 叢集 + v10.x
        (不在本文討論範圍)
```

---

#### 方案比較總表

| 比較項目 | 方案 A | 方案 B | 
|---|---|---|
| **連接器版本** | v3.x | v10.x | 
| **叢集類型** | UC 叢集 | 非 UC + UC | 
| **架構複雜度** | ⭐ 簡單 | ⭐⭐⭐ 較複雜 | 
| **UC 治理** | ✅ 完整 | ✅ 完整 | 
| **v10.x 新功能** | ❌ 不支援 | ✅ 完整支援 | 
| **維運成本** | ⭐ 低 | ⭐⭐ 中等 | 
| **適用場景** | 一般批次抽取 | 需要新功能或高效能 | 
| **長期推薦** | 短期快速方案 | 企業級長期架構 | 

---

#### 常見問題 FAQ

### Q1：為什麼不直接在 UC 叢集上用 v10.x？

**A**：UC 為確保資料治理一致性，對未完成 UC 整合的 DataSource V2 連接器實施限制。這是安全策略，非技術問題。

### Q2：方案 B 會失去即時性嗎？

**A**：是的，資料需先抽取到物件儲存。可透過以下方式優化：

- 使用 Databricks Workflows 定期排程

- 實作 Change Data Capture (CDC) 機制

- 根據業務需求調整抽取頻率

### Q3：v3.x 和 v10.x 功能差異大嗎？

**A**：主要差異：

- **Structured Streaming**：v10.x 提供更好的整合

- **效能優化**：v10.x 有更好的 filter pushdown 和 partition 支援

- **API 設計**：v10.x 採用更現代的設計

如果只是一般批次讀寫，v3.x 通常足夠。

### Q4：可以同時安裝 v3.x 和 v10.x 嗎？

**A**：技術上可以（它們使用不同的 namespace），但不建議，容易造成混淆和版本衝突。