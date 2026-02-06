# Databricks Delta Sharing 深度解析

根據你的題目，讓我詳細說明 Databricks 的分享機制，特別是 Delta Sharing 的運作原理。

---

## 🎯 Delta Sharing 核心概念

### 1. 兩種 Delta Sharing 模式

```
Delta Sharing 架構
├── Open Delta Sharing (開放式)
│   ├── 基於開源協議
│   ├── 支援非 Databricks 客戶端
│   ├── 只能分享 Tables
│   └── 使用 REST API 存取
│
└── Databricks-to-Databricks (D2D)
    ├── Databricks 原生整合
    ├── 雙方都必須是 Databricks 客戶
    ├── 支援 Tables、Notebooks、Volumes、ML Models
    └── 原生 Unity Catalog 整合
```

### 2. 為什麼題目選 A？

**關鍵資訊識別：**
- ✅ "external analytics vendor" → 外部供應商
- ✅ "who is a Databricks client" → **也是 Databricks 用戶**
- ✅ "does not have access to the company Databricks account" → 不同 account

**結論：** 符合 **Databricks-to-Databricks** Delta Sharing 使用場景

---

## 📐 Delta Sharing 架構詳解

### 核心組件

```python
# Delta Sharing 的三大核心物件

Unity Catalog 架構
├── Share（分享）
│   ├── 定義：要分享的資源集合
│   ├── 包含：tables、notebooks、volumes、models
│   └── 授權：控制誰可以存取
│
├── Recipient（接收者）
│   ├── 定義：接收分享的外部實體
│   ├── 認證：使用 activation link 或 token
│   └── 權限：READ ONLY（唯讀）
│
└── Provider（提供者）
    ├── 定義：分享資源的擁有者
    ├── 控制：管理 share 和 recipient
    └── 監控：追蹤存取使用情況
```

### 實際操作流程

```sql
-- 步驟 1: 建立 Share
CREATE SHARE IF NOT EXISTS vendor_analytics_share;

-- 步驟 2: 加入 Tables 到 Share
ALTER SHARE vendor_analytics_share 
ADD TABLE logistics_catalog.shipment_data.delivery_tracking;

ALTER SHARE vendor_analytics_share 
ADD TABLE logistics_catalog.shipment_data.route_optimization;

-- 步驟 3: 加入 Notebooks 到 Share (D2D only)
ALTER SHARE vendor_analytics_share 
ADD NOTEBOOK /Shared/Analytics/Delivery_Analysis;

-- 步驟 4: 建立 Recipient
CREATE RECIPIENT IF NOT EXISTS analytics_vendor
COMMENT 'External analytics vendor access';

-- 步驟 5: 授權 Share 給 Recipient
GRANT SELECT ON SHARE vendor_analytics_share 
TO RECIPIENT analytics_vendor;

-- 步驟 6: 取得 Activation Link
DESCRIBE RECIPIENT analytics_vendor;
-- 會返回 activation_link，傳送給供應商
```

---

## 🔄 D2D vs Open Delta Sharing 比較

### 功能矩陣

| 功能特性 | Open Delta Sharing | Databricks-to-Databricks |
|----------|-------------------|-------------------------|
| **分享 Tables** | ✅ | ✅ |
| **分享 Notebooks** | ❌ | ✅ |
| **分享 Volumes** | ❌ | ✅ |
| **分享 ML Models** | ❌ | ✅ |
| **即時更新** | ✅ | ✅ |
| **需求條件** | REST API client | 雙方都是 Databricks |
| **安全性** | Token-based | Native UC integration |
| **存取方式** | REST API / pandas | Native Spark / SQL |

### 使用場景選擇

```
選擇決策樹
├── 接收方是否為 Databricks 客戶？
│   ├── 是 → 使用 D2D Delta Sharing
│   │   ├── 需要分享 notebooks？ → D2D
│   │   ├── 需要分享 volumes？ → D2D
│   │   └── 需要分享 ML models？ → D2D
│   │
│   └── 否 → 使用 Open Delta Sharing
│       └── 只能分享 tables
│           ├── 使用 delta-sharing Python library
│           ├── 使用 pandas connector
│           └── 或其他支援的工具
```

---

## 🔐 安全性與權限控制

### 1. Recipient 認證流程

```
Databricks-to-Databricks 認證
Provider (你的公司)
├── 建立 Recipient
├── 生成 Activation Link
└── 傳送給 Vendor
        │
        ▼
Vendor (供應商)
├── 點擊 Activation Link
├── 授權連接自己的 Databricks account
└── Share 自動出現在 Unity Catalog
        │
        ▼
存取資源
├── 透過 Catalog Browser 查看
├── 使用 SQL 查詢 tables
└── 執行分享的 notebooks
```

### 2. 權限特性

```python
# Delta Sharing 權限特性

權限模型
├── 唯讀存取（READ ONLY）
│   ├── 無法修改原始資料
│   ├── 無法看到底層儲存位置
│   └── 無法存取 metadata schema
│
├── 資料隔離
│   ├── 只能看到被分享的 tables/columns
│   ├── 支援 row-level filtering
│   └── 支援 column masking
│
└── 即時撤銷
    ├── Provider 可隨時撤銷存取
    ├── Recipient 立即失去存取權
    └── 不需要刪除資料副本
```

### 3. 進階安全功能

```sql
-- Row-level security (動態資料過濾)
CREATE SHARE vendor_share;

-- 只分享特定區域的資料
ALTER SHARE vendor_share 
ADD TABLE logistics_catalog.shipment_data.deliveries
WITH ROW FILTER region = 'APAC';

-- Column masking (欄位遮罩)
ALTER SHARE vendor_share 
ADD TABLE logistics_catalog.customer_data.contacts
WITH COLUMN MASK email = 'REDACTED';
```

---

## 📊 實際使用範例

### Provider 端（你的公司）

```python
# 使用 Python 管理 Delta Sharing

from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

# 建立 share
share = w.shares.create(name="vendor_analytics_share")

# 加入 tables
w.shares.update(
    name="vendor_analytics_share",
    updates=[
        {
            "action": "ADD",
            "data_object": {
                "name": "logistics_catalog.shipment_data.deliveries",
                "data_object_type": "TABLE"
            }
        },
        {
            "action": "ADD",
            "data_object": {
                "name": "/Shared/Analytics/Delivery_Report",
                "data_object_type": "NOTEBOOK"
            }
        }
    ]
)

# 建立 recipient
recipient = w.recipients.create(
    name="analytics_vendor",
    authentication_type="DATABRICKS"
)

# 授權
w.grants.update(
    securable_type="SHARE",
    full_name="vendor_analytics_share",
    updates=[
        {
            "principal": "analytics_vendor",
            "add": ["SELECT"]
        }
    ]
)

# 取得 activation link
print(recipient.activation_url)
```

### Recipient 端（供應商）

```sql
-- 供應商完成 activation 後

-- 1. 查看可用的 shares
SHOW SHARES;

-- 2. 查看 share 內容
SHOW ALL IN SHARE `provider_name`.vendor_analytics_share;

-- 3. 建立 catalog 存取 shared data
CREATE CATALOG IF NOT EXISTS shared_logistics
USING SHARE `provider_name`.vendor_analytics_share;

-- 4. 查詢 shared tables
SELECT * 
FROM shared_logistics.shipment_data.deliveries
WHERE delivery_date >= '2024-01-01';

-- 5. 執行 shared notebooks
-- 透過 Workspace UI 直接開啟執行
```

---

## ⚠️ 常見陷阱與限制

### 1. 功能限制

```
Delta Sharing 限制
├── Notebooks 分享
│   ├── ❌ 無法編輯（唯讀）
│   ├── ❌ 無法看到執行歷史
│   └── ✅ 可以複製到自己 workspace 修改
│
├── Tables 分享
│   ├── ❌ 無法寫入
│   ├── ❌ 無法執行 MERGE/UPDATE/DELETE
│   └── ✅ 可以讀取並寫入自己的 tables
│
└── 效能考量
    ├── 大量資料傳輸會有網路成本
    ├── 建議使用 partition pruning
    └── 考慮使用 change data feed
```

### 2. 為什麼其他選項錯誤？

#### 選項 B - Notebook 內建協作功能
```
Notebook 協作功能限制
├── 需要在同一個 workspace
│   ├── 共享相同的 compute resources
│   ├── 共享相同的 Unity Catalog
│   └── 供應商無法存取你的 workspace
│
└── 適用場景
    ├── 團隊內部協作
    └── 不適合跨組織分享
```

#### 選項 C - HTML 發布
```
HTML 發布的問題
├── 靜態內容
│   ├── 無法執行程式碼
│   ├── 無法互動查詢
│   └── 無法存取最新資料
│
└── 維護困難
    ├── 資料更新需要重新發布
    └── 沒有版本控制
```

#### 選項 D - DBC 檔案
```
DBC 檔案的缺點
├── 手動傳輸
│   ├── 需要 export/import
│   ├── 無法自動同步
│   └── 安全性風險
│
└── 沒有存取控制
    ├── 無法撤銷
    └── 無法追蹤使用情況
```

---

## 🎓 最佳實踐建議

### 1. 建立 Share 的策略

```sql
-- 按業務領域組織
CREATE SHARE analytics_share;  -- 分析用途
CREATE SHARE ml_share;          -- ML 模型用途
CREATE SHARE reporting_share;  -- 報表用途

-- 使用命名規範
-- 格式: {purpose}_{recipient}_{env}_share
CREATE SHARE analytics_vendor_prod_share;
```

### 2. 監控與稽核

```sql
-- 查看所有 shares
SHOW SHARES;

-- 查看 share 的 recipients
SHOW GRANT ON SHARE vendor_analytics_share;

-- 查看存取日誌
SELECT * FROM system.access.audit
WHERE request_params.share_name = 'vendor_analytics_share'
ORDER BY event_time DESC;
```

### 3. 資料治理

```python
# 實施資料分類標籤
ALTER TABLE logistics_catalog.shipment_data.deliveries
SET TAGS ('classification' = 'confidential', 
          'department' = 'logistics');

# 設定資料保留政策
ALTER SHARE vendor_analytics_share
SET TBLPROPERTIES (
    'delta.logRetentionDuration' = '30 days',
    'delta.deletedFileRetentionDuration' = '7 days'
);
```

---

## 📈 效能優化

### 1. 使用 Change Data Feed

```sql
-- 啟用 CDF 只傳輸變更資料
ALTER TABLE logistics_catalog.shipment_data.deliveries
SET TBLPROPERTIES (delta.enableChangeDataFeed = true);

-- Recipient 端只讀取變更
SELECT * 
FROM table_changes('shared_logistics.shipment_data.deliveries', 2, 10)
WHERE _change_type IN ('insert', 'update_postimage');
```

### 2. Partition Pruning

```sql
-- Provider 端確保良好的 partition 設計
CREATE TABLE logistics_catalog.shipment_data.deliveries
USING DELTA
PARTITIONED BY (delivery_date)
AS SELECT * FROM source;

-- Recipient 端利用 partition filter
SELECT * 
FROM shared_logistics.shipment_data.deliveries
WHERE delivery_date = '2024-02-06';  -- partition pruning
```