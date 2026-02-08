# 深度解析：Unity Catalog Row-Level Security

## ✅ 你的解析正確性確認

你的解析**完全正確**！邏輯清晰、說明到位。我基於實務經驗和考試重點，補充更多細節。

---

## 🎯 實務應用場景補充

### 典型使用案例

```sql
-- 案例 1: 多層級權限控制
CREATE FUNCTION region_filter(region STRING, account_manager STRING)
RETURN CASE
  WHEN IS_ACCOUNT_GROUP_MEMBER('admin') THEN true
  WHEN IS_ACCOUNT_GROUP_MEMBER('manager') THEN account_manager = current_user()
  WHEN IS_ACCOUNT_GROUP_MEMBER('regional_team') THEN region IN ('US', 'CA')
  ELSE false
END;

-- 案例 2: 結合敏感資料遮罩
CREATE FUNCTION pii_filter(department STRING)
RETURN IF(
  IS_ACCOUNT_GROUP_MEMBER('compliance_team'), 
  true, 
  department = current_user_department()
);

-- 案例 3: 時間範圍限制
CREATE FUNCTION time_based_filter(created_date DATE)
RETURN IF(
  IS_ACCOUNT_GROUP_MEMBER('finance_team'),
  true,
  created_date >= date_sub(current_date(), 90)  -- 非財務只能看 90 天內
);
```

---

## 🔍 考試必考陷阱加強

### 陷阱 1: IF vs CASE 的條件順序混淆

```sql
-- ❌ 常見錯誤：把「特權用戶」寫在 ELSE 分支
CREATE FUNCTION wrong_filter(region STRING)
RETURN CASE
  WHEN region='US' THEN true
  WHEN IS_ACCOUNT_GROUP_MEMBER('finance') THEN true  -- ❌ 邏輯多餘且易錯
END;

-- ✅ 正確寫法：特權用戶優先判斷
CREATE FUNCTION correct_filter(region STRING)
RETURN CASE
  WHEN IS_ACCOUNT_GROUP_MEMBER('finance') THEN true  -- ✅ 先放行特權
  ELSE region='US'
END;
```

**實務經驗：**
- Unity Catalog 按**從上到下**執行 CASE 分支
- 永遠先檢查「特權條件」，避免被後續條件覆蓋
- 在我們 AUO 的 VMS 系統中，我們先檢查 `admin` 群組，再檢查車隊管理員

### 陷阱 2: 返回值類型錯誤

```sql
-- ❌ 錯誤：返回 STRING
CREATE FUNCTION bad_filter(region STRING)
RETURN region;  -- 返回 'US', 'EU' 等字串

-- ❌ 錯誤：返回 NULL
CREATE FUNCTION bad_filter2(region STRING)
RETURN IF(region='US', true, NULL);  -- NULL 會導致該行被過濾

-- ✅ 正確：必須返回 BOOLEAN
CREATE FUNCTION good_filter(region STRING)
RETURN region='US';  -- 返回 true/false
```

**關鍵點：**
- Row Filter 函數**必須**返回 `BOOLEAN`
- `NULL` 被視為 `false`，該行會被過濾掉
- 考試常見陷阱：`ELSE region` 看起來合理，但類型錯誤

### 陷阱 3: IS_ACCOUNT_GROUP_MEMBER 的大小寫敏感性

```sql
-- ⚠️ 群組名稱大小寫敏感
IS_ACCOUNT_GROUP_MEMBER('Finance_Team')  -- ❌ 如果實際是 'finance_team'
IS_ACCOUNT_GROUP_MEMBER('finance_team')  -- ✅ 必須完全匹配

-- 實務建議：使用統一命名規範
CREATE FUNCTION robust_filter(region STRING)
RETURN IF(
  IS_ACCOUNT_GROUP_MEMBER('finance_team') OR 
  IS_ACCOUNT_GROUP_MEMBER('Finance_Team'),  -- 防禦性編程
  true,
  region='US'
);
```

---

## 🏗️ 實務部署完整流程

### Step 1: 建立 Unity Catalog 群組

```sql
-- 在 Account Console 或使用 SQL
CREATE GROUP IF NOT EXISTS finance_team;
CREATE GROUP IF NOT EXISTS regional_managers;

-- 添加用戶到群組
ALTER GROUP finance_team ADD USER 'eric.yang@auo.com';
```

### Step 2: 建立並測試 Row Filter 函數

```sql
-- 建立函數（必須在 Unity Catalog schema 中）
CREATE OR REPLACE FUNCTION main.security.us_filter(region STRING)
RETURN IF(IS_ACCOUNT_GROUP_MEMBER('finance_team'), true, region='US');

-- 測試函數（在套用前先驗證）
SELECT 
  region,
  main.security.us_filter(region) as filter_result
FROM transactions
LIMIT 10;
```

### Step 3: 應用 Row Filter

```sql
-- 套用到表格
ALTER TABLE main.analytics.transactions 
SET ROW FILTER main.security.us_filter ON (region);

-- 驗證：以不同身份查詢
-- Finance team 成員會看到所有 region
-- 其他用戶只看到 region='US'
SELECT region, COUNT(*) FROM main.analytics.transactions GROUP BY region;
```

### Step 4: 監控與審計

```sql
-- 查看哪些表有 Row Filter
SHOW TBLPROPERTIES main.analytics.transactions;

-- 查看 Row Filter 定義
DESCRIBE FUNCTION main.security.us_filter;

-- 查看用戶群組成員
SHOW GROUPS;
SHOW GROUP MEMBERS finance_team;

-- 審計日誌（Unity Catalog 自動記錄）
SELECT * FROM system.access.audit 
WHERE table_name = 'transactions' 
  AND action_name = 'SELECT'
ORDER BY event_time DESC;
```

---

## 📊 SmartSignage 實務案例

### 我們的廣告平台權限設計

```sql
-- 場景：廣告數據平台
-- 需求：
-- 1. 內部分析師看所有廣告主數據
-- 2. 廣告主只能看自己的數據
-- 3. 區域經理只能看負責區域

CREATE FUNCTION main.smartsignage.advertiser_filter(
  advertiser_id STRING,
  region STRING
)
RETURN CASE
  WHEN IS_ACCOUNT_GROUP_MEMBER('analytics_team') THEN true
  WHEN IS_ACCOUNT_GROUP_MEMBER('regional_manager_north') THEN region = 'North'
  WHEN IS_ACCOUNT_GROUP_MEMBER('regional_manager_south') THEN region = 'South'
  ELSE advertiser_id = current_user()  -- 廣告主只看自己
END;

-- 套用到廣告效果表
ALTER TABLE main.smartsignage.campaign_performance
SET ROW FILTER main.smartsignage.advertiser_filter 
ON (advertiser_id, region);
```

### Column Masking 搭配使用

```sql
-- Row Filter + Column Mask 組合拳
-- Row Filter: 控制「看哪些行」
ALTER TABLE transactions 
SET ROW FILTER us_filter ON (region);

-- Column Mask: 控制「看哪些列的完整內容」
CREATE FUNCTION mask_amount(amount DECIMAL(10,2))
RETURN IF(
  IS_ACCOUNT_GROUP_MEMBER('finance_team'),
  amount,
  NULL  -- 非財務人員看不到金額
);

ALTER TABLE transactions 
ALTER COLUMN amount 
SET MASK mask_amount;
```

---

## 🎓 考試答題技巧

### 快速判斷法（30 秒內解題）

```
Step 1: 找關鍵字「Finance team 看所有」
       → 特權群組返回 true

Step 2: 找關鍵字「其他用戶只看 US」
       → 非特權群組返回 region='US'

Step 3: 套用 IF 模板
       IF(是特權, true, 限制條件)
       IF(IS_ACCOUNT_GROUP_MEMBER(...), true, region='US')
       
答案：A
```

### 排除法加速

```
看到 ELSE region → 立刻排除（類型錯誤）
看到條件反轉 → 立刻排除（邏輯錯誤）
剩下的檢查 IF 參數順序
```

---

## 🔒 安全性最佳實務

### 1. 最小權限原則

```sql
-- ❌ 避免：過於寬鬆
CREATE FUNCTION lazy_filter(region STRING)
RETURN true;  -- 所有人都能看

-- ✅ 推薦：明確限制
CREATE FUNCTION secure_filter(region STRING)
RETURN IF(
  IS_ACCOUNT_GROUP_MEMBER('approved_users'),
  region IN ('US', 'CA'),  -- 即使批准用戶也只能看北美
  false  -- 其他人完全看不到
);
```

### 2. 防禦性編程

```sql
-- 處理 NULL 值
CREATE FUNCTION null_safe_filter(region STRING)
RETURN IF(
  IS_ACCOUNT_GROUP_MEMBER('finance_team'),
  true,
  COALESCE(region, 'UNKNOWN') = 'US'  -- 防止 NULL 值異常
);
```

### 3. 審計與合規

```sql
-- 記錄誰在何時看了什麼
-- Unity Catalog 自動記錄，但可以建立自定義視圖
CREATE VIEW audit_summary AS
SELECT 
  user_name,
  table_name,
  COUNT(*) as access_count,
  MAX(event_time) as last_access
FROM system.access.audit
WHERE action_name = 'SELECT'
GROUP BY user_name, table_name;
```

---

## 📝 考試常見變形題

### 變形 1: 多條件組合

```sql
-- 題目：Finance 看全部，Manager 看自己管理的，其他人看 US
CREATE FUNCTION multi_level_filter(region STRING, manager STRING)
RETURN CASE
  WHEN IS_ACCOUNT_GROUP_MEMBER('finance') THEN true
  WHEN IS_ACCOUNT_GROUP_MEMBER('manager') THEN manager = current_user()
  ELSE region = 'US'
END;
```

### 變形 2: 使用 IS_MEMBER (Workspace-level)

```sql
-- Unity Catalog: IS_ACCOUNT_GROUP_MEMBER (Account-level)
-- Workspace: IS_MEMBER (Workspace-level, legacy)

-- ⚠️ 考試可能混用，注意區分
CREATE FUNCTION workspace_filter(region STRING)
RETURN IF(
  IS_MEMBER('finance'),  -- Workspace 群組
  true,
  region='US'
);
```

### 變形 3: 動態參數

```sql
-- 使用 current_user() 動態判斷
CREATE FUNCTION owner_filter(owner STRING)
RETURN IF(
  IS_ACCOUNT_GROUP_MEMBER('admin'),
  true,
  owner = current_user()  -- 只能看自己的記錄
);
```

---

## 🚨 實務常見問題排查

### 問題 1: Filter 未生效

```sql
-- 檢查清單：
-- 1. 函數是否在正確的 catalog.schema
DESCRIBE FUNCTION EXTENDED main.security.us_filter;

-- 2. 用戶是否在群組中
SHOW GROUP MEMBERS finance_team;

-- 3. Row Filter 是否正確應用
SHOW CREATE TABLE transactions;  -- 查看 DDL

-- 4. 權限是否正確
SHOW GRANTS ON TABLE transactions;
```

### 問題 2: 性能問題

```sql
-- ❌ 避免：複雜子查詢
CREATE FUNCTION slow_filter(id INT)
RETURN id IN (SELECT id FROM authorized_ids);  -- 每次都執行子查詢

-- ✅ 推薦：簡單條件
CREATE FUNCTION fast_filter(region STRING)
RETURN region = 'US';  -- 可以利用分區剪枝

-- ✅ 更好：預先計算
-- 使用 Delta Cache 緩存群組成員信息
```

### 問題 3: 更新 Filter 邏輯

```sql
-- 修改函數
CREATE OR REPLACE FUNCTION us_filter(region STRING)
RETURN IF(IS_ACCOUNT_GROUP_MEMBER('finance_team'), true, region IN ('US', 'CA'));

-- 變更立即生效，無需重新應用
-- Unity Catalog 自動重新編譯查詢計畫
```

---

## 🎯 總結：考試必記

| 概念 | 關鍵點 | 記憶提示 |
|------|--------|----------|
| **返回值** | 必須是 BOOLEAN | `region='US'` ✅  `region` ❌ |
| **IF 順序** | `IF(條件, 真, 假)` | 特權在前：`IF(is_admin, true, ...)` |
| **CASE 順序** | 特權條件寫最上面 | 從上到下執行，優先放行 |
| **群組函數** | `IS_ACCOUNT_GROUP_MEMBER()` | Account-level，大小寫敏感 |
| **NULL 處理** | NULL = false | 使用 `COALESCE` 防禦 |

你的解析已經很完整，這些補充會讓你在實務和考試中更加無敵！💪