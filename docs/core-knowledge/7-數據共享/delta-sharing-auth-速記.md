# Delta Sharing 認證機制差異｜考前速讀版

## 1) 一句話
- D2D（Databricks-to-Databricks）：**不需要 token-based credentials / credential file**（靠 Databricks/UC 內建 sharing 連線機制）
- D2O（Open Delta Sharing）：**一定需要外部認證**（Bearer token 或 OIDC federation）

---

## 2) D2D（Databricks-to-Databricks）

### 核心特徵（考點）
- Recipient 是 **UC-enabled Databricks**（對方也有 Unity Catalog / metastore）
- Provider 建 recipient 時，用 **DATABRICKS sharing identifier**（對方 metastore 的 identifier）
- **不需要 bearer token / 不需要 profile credential file**
- 權限仍由 UC 管：`CREATE SHARE` / `ADD TABLE` / `GRANT ... TO RECIPIENT`

### 考試安全用語
- ✅ built-in authentication
- ✅ no token-based credentials required（比 “no token exchange” 更不會被挑語病）

---

## 3) D2O（Open Delta Sharing）

### 核心特徵（考點）
- Recipient **不在 Databricks 生態內**（或非 UC-enabled）
- 需要「外部」方式向 Delta Sharing server 認證
- 兩條路：
  1. **Bearer token**（通常透過 credential/profile file 提供；可設定到期/撤銷/輪替）
  2. **OIDC federation**（用企業 IdP 取得 token；偏企業級整合/短期 token 流程）

---

## 4) 選項速判（Q-032 類型）
- A「兩者相同」❌
- B「D2D 用 OIDC、D2O 用 bearer」❌（搞反且 D2O 兩者都可）
- C「D2D 用 SSO、D2O 用 OIDC」❌（把登入 SSO 跟 sharing 認證混在一起）
- D ✅：D2D 內建認證、不需要 token-based credentials；D2O 需要外部認證（bearer 或 OIDC）

---

## 5) 10 秒類比記憶
- D2D = 內網：同一 Databricks/UC 生態內 → 免 token-based credentials
- D2O = VPN/外部 API：跨出生態 → 必須 bearer/OIDC

---

## 6) 三行版（超濃縮）
```
D2D：內建認證，不用 token-based credentials
D2O：外部認證，需要 bearer token 或 OIDC federation
題目問差異：就是「內建 vs 外部」
```
