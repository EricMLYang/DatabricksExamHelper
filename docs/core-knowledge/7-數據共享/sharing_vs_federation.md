# Databricks Sharing 機制完整筆記

> **快速索引:** [Delta Sharing](#delta-sharing) | [Lakehouse Federation](#lakehouse-federation) | [比較對照](#比較對照) | [選擇決策](#選擇決策)

---

## 🎯 核心概念速覽

### 一句話總結

| 技術 | 核心概念 | 類比 |
|------|---------|------|
| **Delta Sharing** | 我分享資料給你 | 分享 Google Drive 檔案 |
| **Lakehouse Federation** | 我查詢你的資料庫 | 資料庫的 Foreign Data Wrapper |

### 資料流向對比

```
Delta Sharing (資料分享)
Provider ──┐
           ├─→ Share (資料副本存取權) ──→ Recipient
           └─→ 資料留在 Provider

Lakehouse Federation (統一查詢)
Databricks ←─ Query ─→ MySQL
           ←─ Query ─→ PostgreSQL  
           ←─ Query ─→ Snowflake
           └─→ 統一 SQL 介面查詢外部系統
```

---

## Delta Sharing

### 📋 基本定義

**作用：** 安全地分享 Delta Lake 資料給外部組織或系統  
**方向：** Databricks → 外部（資料提供者）  
**特性：** 唯讀、即時、零資料複製

### 🔧 兩種模式

#### 1. Open Delta Sharing
```
特點：
├── 開源協議
├── 支援非 Databricks 客戶端
├── 只能分享 Tables
└── 使用 REST API

支援工具：
├── Pandas
├── Power BI
├── Tableau
└── 任何支援 Delta Sharing protocol 的工具
```

#### 2. Databricks-to-Databricks (D2D)
```
特點：
├── Databricks 原生整合
├── 雙方都必須是 Databricks 用戶
├── 支援更多資源類型
└── 更好的整合體驗

可分享資源：
├── Tables ✅
├── Notebooks ✅ (D2D only)
├── Volumes ✅ (D2D only)
└── ML Models ✅ (D2D only)
```

### 🏗️ 核心架構

```sql
-- 三大核心物件

Unity Catalog
├── Share (分享)
│   └── 定義要分享的資源集合
│
├── Recipient (接收者)
│   └── 接收分享的外部實體
│
└── Provider (提供者)
    └── 分享資源的擁有者
```

### 💻 實作範例

```sql
-- === Provider 端設定 ===

-- 1. 建立 Share
CREATE SHARE vendor_analytics_share;

-- 2. 加入 Tables
ALTER SHARE vendor_analytics_share 
ADD TABLE logistics_catalog.deliveries.tracking_info;

-- 3. 加入 Notebooks (D2D only)
ALTER SHARE vendor_analytics_share 
ADD NOTEBOOK /Shared/Analytics/Delivery_Analysis;

-- 4. 建立 Recipient
CREATE RECIPIENT analytics_vendor
COMMENT 'External analytics vendor';

-- 5. 授權
GRANT SELECT ON SHARE vendor_analytics_share 
TO RECIPIENT analytics_vendor;

-- 6. 取得 Activation Link
DESCRIBE RECIPIENT analytics_vendor;
-- 傳送 activation_link 給供應商


-- === Recipient 端使用 ===

-- 1. 使用 activation link 連接

-- 2. 建立 Catalog
CREATE CATALOG logistics_shared
USING SHARE `provider_name`.vendor_analytics_share;

-- 3. 查詢分享資料
SELECT * 
FROM logistics_shared.deliveries.tracking_info
WHERE delivery_date >= current_date() - 7;

-- 4. JOIN 自己的資料
SELECT 
    o.order_id,
    o.customer_name,
    t.delivery_status
FROM my_catalog.orders o
JOIN logistics_shared.deliveries.tracking_info t
    ON o.order_id = t.order_id;
```

### 🔐 安全功能

```sql
-- Row-level filtering
ALTER SHARE vendor_share 
ADD TABLE deliveries
WITH ROW FILTER region = 'APAC';

-- Column masking
ALTER SHARE vendor_share 
ADD TABLE contacts
WITH COLUMN MASK email = 'REDACTED';
```

### ✅ 優勢

- ✅ 零資料複製（資料留在 Provider）
- ✅ 即時資料更新
- ✅ 細粒度權限控制（row/column level）
- ✅ 可隨時撤銷存取
- ✅ 統一的 Unity Catalog 管理
- ✅ 支援跨雲、跨區域

### ⚠️ 限制

- ❌ 唯讀存取（無法寫入）
- ❌ Notebooks 分享僅限 D2D
- ❌ 大量資料查詢有網路延遲
- ❌ Recipient 需要 Databricks（D2D）或支援的工具（Open）

### 📊 使用場景

```
適用情境：
├── 跨組織資料分享
│   ├── 供應商資料交換
│   ├── 客戶資料提供
│   └── 合作夥伴協作
│
├── 資料產品化
│   ├── 資料市集 (Data Marketplace)
│   ├── 資料即服務 (DaaS)
│   └── 開放資料計畫
│
└── 分析資料分發
    ├── BI 工具存取
    ├── ML 訓練資料集
    └── 報表資料來源
```

---

## Lakehouse Federation

### 📋 基本定義

**作用：** Databricks 作為統一查詢引擎，連接並查詢外部資料系統  
**方向：** Databricks ← → 外部系統（雙向查詢）  
**特性：** 即時查詢、統一 SQL 介面、零資料遷移

### 🔌 支援的資料源

```
支援的外部系統：
├── 關聯式資料庫
│   ├── MySQL ✅
│   ├── PostgreSQL ✅
│   ├── SQL Server ✅
│   ├── Oracle ✅
│   └── MariaDB ✅
│
├── 雲端資料倉儲
│   ├── Snowflake ✅
│   ├── BigQuery ✅ (preview)
│   ├── Redshift ✅
│   └── Azure Synapse ✅
│
└── 其他
    ├── MongoDB ✅
    └── 更多持續增加...
```

### 🏗️ 核心架構

```
統一查詢介面概念：

你的 Spark SQL
      ↓
Databricks Query Engine
      ├── MySQL Connector ──→ MySQL DB
      ├── PostgreSQL Connector ──→ PostgreSQL DB
      ├── Snowflake Connector ──→ Snowflake
      └── 自動翻譯 SQL 方言
```

### 💻 實作範例

```sql
-- === 設定 Connections ===

-- 1. 建立 MySQL Connection
CREATE CONNECTION mysql_erp_connection
TYPE mysql
OPTIONS (
    host 'erp-db.company.internal',
    port '3306',
    user secret('mysql_user'),
    password secret('mysql_password')
);

-- 2. 建立 Federated Catalog
CREATE FOREIGN CATALOG mysql_erp
USING CONNECTION mysql_erp_connection
OPTIONS (database 'production_db');

-- 3. 建立 PostgreSQL Connection
CREATE CONNECTION postgres_crm_connection
TYPE postgresql
OPTIONS (
    host 'crm-db.company.internal',
    port '5432',
    user secret('pg_user'),
    password secret('pg_password')
);

-- 4. 建立另一個 Federated Catalog
CREATE FOREIGN CATALOG postgres_crm
USING CONNECTION postgres_crm_connection
OPTIONS (database 'crm_production');


-- === 統一查詢 ===

-- 跨系統 JOIN 查詢
SELECT 
    -- Delta Lake (本地)
    s.sale_id,
    s.sale_date,
    s.amount,
    
    -- MySQL ERP
    p.product_name,
    i.stock_level,
    
    -- PostgreSQL CRM
    c.customer_name,
    c.customer_segment
    
FROM delta_catalog.sales.transactions s
JOIN mysql_erp.products p ON s.product_id = p.product_id
JOIN mysql_erp.inventory i ON p.product_id = i.product_id
JOIN postgres_crm.customers c ON s.customer_id = c.customer_id

WHERE s.sale_date >= '2024-01-01'
    AND i.stock_level < 100
    AND c.customer_segment = 'Premium';
```

### ⚡ Query Pushdown 機制

```sql
-- Databricks 會自動優化查詢

-- 你寫的 SQL:
SELECT customer_name, COUNT(*) 
FROM mysql_catalog.orders
WHERE order_date >= '2024-01-01'
    AND status = 'completed'
GROUP BY customer_name;

-- Databricks 自動做的事:
┌─────────────────────────────────┐
│ Query Optimizer                 │
├─────────────────────────────────┤
│ 1. 推送 WHERE 到 MySQL          │
│    WHERE order_date >= ...      │
│    AND status = 'completed'     │
│                                 │
│ 2. 推送 SELECT 欄位             │
│    只取 customer_name           │
│                                 │
│ 3. 部分 GROUP BY 可能推送       │
│                                 │
│ 4. 在 Databricks 完成最終聚合  │
└─────────────────────────────────┘

優點：
├── 減少網路傳輸
├── 利用外部系統的索引
└── 更快的查詢速度
```

### ✅ 優勢

- ✅ 統一 SQL 介面（只需要會 Spark SQL）
- ✅ 零資料複製（資料留在原處）
- ✅ 即時資料存取（無 ETL 延遲）
- ✅ Query Pushdown 優化
- ✅ 部分支援寫入操作
- ✅ Unity Catalog 統一治理

### ⚠️ 限制

- ❌ 效能受限於外部系統
- ❌ 跨系統 JOIN 可能較慢
- ❌ 需要網路連接穩定
- ❌ 不支援所有 SQL 功能（取決於外部系統）
- ❌ 只能在 Databricks 內使用

### 📊 使用場景

```
適用情境：
├── Legacy 系統整合
│   ├── 現有 MySQL/PostgreSQL/Oracle
│   ├── 企業 ERP/CRM 系統
│   └── 傳統資料倉儲
│
├── 多雲資料存取
│   ├── Snowflake 資料
│   ├── BigQuery 資料
│   └── Redshift 資料
│
├── 統一查詢介面
│   ├── 避免資料重複
│   ├── 即時資料存取
│   └── 減少 ETL 複雜度
│
└── POC 快速驗證
    └── 無需資料遷移即可測試
```

---

## 比較對照

### 📊 功能矩陣

| 維度 | Delta Sharing | Lakehouse Federation |
|------|--------------|---------------------|
| **主要目的** | 資料分享 | 資料整合 |
| **資料方向** | Databricks → 外部 | Databricks ↔ 外部 |
| **資料位置** | Delta Lake | 外部系統 |
| **資料格式** | Delta tables only | 多種資料庫 |
| **支援系統** | Databricks + 開源工具 | 僅 Databricks |
| **寫入支援** | ❌ 唯讀 | ✅ 部分支援 |
| **分享對象** | 跨組織 | 內部整合 |
| **網路需求** | 資料傳輸 | 查詢推送 |
| **效能** | 優秀 (Delta 優化) | 取決於外部系統 |
| **權限控制** | Row/Column level | Unity Catalog + 外部 |

### 🔄 資料流對比

```
Delta Sharing
═══════════════════════════════════════
Provider Databricks
├── Delta Tables (原始資料)
├── Share Objects
└── Delta Sharing Server
        │
        │ (透過 Delta Sharing Protocol)
        │ 資料以 Parquet 傳輸
        ▼
Recipient
├── Databricks / Pandas / BI Tools
└── 虛擬副本存取


Lakehouse Federation
═══════════════════════════════════════
Databricks (統一查詢引擎)
        │
        ├── Connector → MySQL (即時查詢)
        ├── Connector → PostgreSQL (即時查詢)
        ├── Connector → Snowflake (即時查詢)
        └── 統一 Spark SQL 介面
        
資料永遠留在原始系統
```

### 🎯 適用場景對比

| 需求 | Delta Sharing | Lakehouse Federation |
|------|--------------|---------------------|
| 供應商資料交換 | ✅ 最佳選擇 | ❌ |
| 整合 Legacy MySQL | ❌ | ✅ 最佳選擇 |
| 資料市集 | ✅ 最佳選擇 | ❌ |
| 多雲統一查詢 | ❌ | ✅ 最佳選擇 |
| BI 工具存取 | ✅ Open Sharing | ❌ |
| 即時 OLTP 查詢 | ❌ | ✅ 最佳選擇 |
| 大規模分析 | ✅ (需 ETL) | ⚠️ (效能考量) |
| POC 驗證 | ⚠️ | ✅ 快速驗證 |

---

## 選擇決策

### 🌳 決策樹

```
資料整合/分享需求
│
├─ 是否跨組織？
│  ├─ 是 → Delta Sharing
│  │      ├─ 對方是 Databricks 用戶？
│  │      │  ├─ 是 → D2D Delta Sharing
│  │      │  │      └─ 可分享 tables/notebooks/models
│  │      │  └─ 否 → Open Delta Sharing
│  │      │         └─ 只能分享 tables
│  │      │
│  │      └─ 需要嚴格權限控制？
│  │         └─ 是 → Delta Sharing (row/column filter)
│  │
│  └─ 否 (內部整合) → 繼續評估
│     │
│     ├─ 資料在哪裡？
│     │  ├─ Delta Lake → 直接用 Unity Catalog
│     │  ├─ 外部系統 → Lakehouse Federation
│     │  └─ 需遷移？ → 評估 ETL vs Federation
│     │
│     ├─ 查詢頻率？
│     │  ├─ 高頻 → ETL 到 Delta (更好效能)
│     │  ├─ 低頻 → Federation (避免重複)
│     │  └─ 即時 → Federation (無延遲)
│     │
│     └─ 資料量？
│        ├─ 大型 → ETL 到 Delta
│        ├─ 中小型 → Federation
│        └─ 混合 → Federation + 選擇性 ETL
```

### ✅ 快速檢查清單

**選 Delta Sharing 當：**
- ✅ 需要分享給外部組織
- ✅ 需要分享 notebooks/models (D2D)
- ✅ 需要嚴格存取控制
- ✅ 對方沒有 VPN 存取權
- ✅ 資料已經在 Delta Lake

**選 Lakehouse Federation 當：**
- ✅ 內部系統整合
- ✅ 資料在 MySQL/PostgreSQL/Snowflake
- ✅ 需要即時查詢
- ✅ 避免資料重複
- ✅ POC 快速驗證

---

## 混合使用範例

### 🔄 Federation + Sharing 組合

```sql
-- 實際企業場景：
-- 1. 用 Federation 整合內部系統
-- 2. 用 Delta Sharing 分享給外部夥伴

-- === Step 1: Federation 整合內部資料 ===
CREATE VIEW unified_catalog.analytics.customer_360 AS
SELECT 
    c.customer_id,
    c.customer_name,
    o.total_orders,
    o.total_revenue,
    s.satisfaction_score
FROM postgres_crm.customers c
LEFT JOIN mysql_erp.order_summary o ON c.customer_id = o.customer_id
LEFT JOIN postgres_crm.support_metrics s ON c.customer_id = s.customer_id;

-- === Step 2: 物化到 Delta table ===
CREATE TABLE delta_catalog.analytics.customer_360_gold
AS SELECT * FROM unified_catalog.analytics.customer_360;

-- === Step 3: Delta Sharing 分享給外部 ===
CREATE SHARE partner_analytics_share;

ALTER SHARE partner_analytics_share 
ADD TABLE delta_catalog.analytics.customer_360_gold;

GRANT SELECT ON SHARE partner_analytics_share 
TO RECIPIENT marketing_agency;
```

---

## 實務最佳實踐

### Delta Sharing 最佳實踐

```sql
-- 1. 使用 partition 減少傳輸
CREATE TABLE analytics.sales_partitioned
PARTITIONED BY (year, month)
AS SELECT * FROM sales;

-- 2. 只分享必要欄位（用 view）
CREATE VIEW analytics.sales_shared AS
SELECT sale_id, sale_date, amount
FROM analytics.sales_partitioned;

ALTER SHARE partner_share ADD TABLE analytics.sales_shared;

-- 3. 使用 row filter 限制資料
ALTER SHARE partner_share 
ADD TABLE analytics.sales
WITH ROW FILTER region = 'APAC';

-- 4. 監控使用
SELECT share_name, recipient_name, action, event_time
FROM system.access.audit
WHERE action LIKE '%SHARE%'
ORDER BY event_time DESC;
```

### Lakehouse Federation 最佳實踐

```sql
-- 1. 建立 view 簡化存取
CREATE VIEW unified.customer_orders AS
SELECT c.*, o.order_id, o.amount
FROM postgres_crm.customers c
LEFT JOIN mysql_erp.orders o ON c.customer_id = o.customer_id;

-- 2. 定期物化常用查詢
CREATE TABLE delta_catalog.customer_orders_cache
AS SELECT * FROM unified.customer_orders;

-- 3. 設定 connection pool
ALTER CONNECTION mysql_connection
SET max_connections = 50,
    connection_timeout = 30;

-- 4. 監控效能
SELECT query_text, execution_duration, external_table_name
FROM system.query.history
WHERE external_table_name IS NOT NULL
ORDER BY execution_duration DESC;
```

---

## 效能優化

### Delta Sharing 優化

```sql
-- 1. Z-Ordering 優化
OPTIMIZE sales_table ZORDER BY (customer_id, date);

-- 2. Partition pruning
SELECT * FROM shared_table
WHERE year = 2024 AND month = 2;  -- 只掃描特定 partition

-- 3. 使用 Change Data Feed 增量傳輸
ALTER TABLE sales_table
SET TBLPROPERTIES (delta.enableChangeDataFeed = true);
```

### Lakehouse Federation 優化

```sql
-- 1. 利用 pushdown (自動)
SELECT * FROM mysql_catalog.orders
WHERE date >= '2024-01-01'  -- 推送到 MySQL
    AND amount > 1000;      -- 推送到 MySQL

-- 2. 只選擇需要的欄位
SELECT order_id, amount  -- 減少傳輸
FROM mysql_catalog.orders;

-- 3. 建立索引在外部系統
-- 在 MySQL 上建立索引加速查詢
CREATE INDEX idx_order_date ON orders(order_date);
```

---

## 考試重點

### ⚡ 快速記憶

**Delta Sharing 記憶點：**
- 🔑 **D2D** = Delta-to-Databricks = 可分享 notebooks/models
- 🔑 **Open** = 開放協議 = 只能分享 tables
- 🔑 資料分享 ≠ 資料移動（零複製）
- 🔑 唯讀存取（READ ONLY）

**Lakehouse Federation 記憶點：**
- 🔑 **統一介面** = 一個 SQL 查所有系統
- 🔑 **Connector** = 萬用轉接頭
- 🔑 **Query Pushdown** = 減少網路傳輸
- 🔑 資料留在原處（零遷移）

### 📝 題目識別關鍵字

| 關鍵字 | 答案方向 |
|--------|---------|
| external vendor, partner | → Delta Sharing |
| Databricks client | → D2D Delta Sharing |
| MySQL, PostgreSQL, legacy | → Federation |
| unified query, single SQL | → Federation |
| notebooks sharing | → D2D only |
| cross-organization | → Delta Sharing |
| real-time, no ETL | → Federation |

---

## 實際應用場景

### 你的 AUO 專案應用

```
VMS (Vehicle Management System)
├── Federation 整合
│   ├── Legacy ERP (MySQL) - 車輛主檔
│   ├── Fleet DB (PostgreSQL) - 即時位置
│   └── Client DW (Snowflake) - 客戶資料
│
└── Delta Sharing 分享
    ├── 分享車隊分析給客戶
    └── 分享效能報告給供應商

SmartSignage DataHub
├── Federation 整合
│   ├── Retail POS (MySQL) - 銷售資料
│   ├── CRM (PostgreSQL) - 顧客資料
│   └── Ad Platform (API) - 廣告數據
│
└── Delta Sharing 分享
    ├── 分享廣告成效給廣告主
    └── 分享 BI 資料給零售商
```

---

## 總結對照表

| 需求 | 推薦方案 | 原因 |
|------|---------|------|
| 供應商資料交換 | Delta Sharing | 跨組織、安全隔離 |
| 整合 Legacy MySQL | Federation | 避免重複、即時存取 |
| 資料市集 | Delta Sharing | 資料產品化、易管理 |
| 多雲統一查詢 | Federation | 統一 SQL 介面 |
| BI 工具存取 | Open Delta Sharing | 廣泛支援 |
| 即時 OLTP | Federation | 直接查詢來源 |
| 大規模分析 | ETL → Delta + Sharing | 最佳效能 |
| POC 驗證 | Federation | 快速、無需遷移 |

---

**🎓 認證考試口訣：**
- **Delta Sharing** = "分享我的 Delta 給你"
- **Lakehouse Federation** = "我查詢你的資料庫"
- **D2D** = "Databricks 對 Databricks，功能最完整"
- **Open** = "開放協議，只能分享表格"

---

**📚 延伸閱讀：**
- [Delta Sharing 官方文件](https://docs.databricks.com/data-sharing/index.html)
- [Lakehouse Federation 官方文件](https://docs.databricks.com/query-federation/index.html)
- [Unity Catalog 文件](https://docs.databricks.com/data-governance/unity-catalog/index.html)