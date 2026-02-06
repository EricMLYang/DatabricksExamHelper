# 📦 Databricks Asset Bundles (DABs) 速記筆記

---

## 🎯 DABs 核心概念

**Databricks Asset Bundles (DABs)** = Infrastructure as Code for Databricks
- **目的**: 將 Databricks 資源(jobs, pipelines, dashboards)版本控制化
- **格式**: YAML 配置 + 程式碼檔案
- **優勢**: CI/CD 整合、多環境部署、團隊協作

---

## 🔄 DABs 完整生命週期

```
DAB 生命週期流程:
┌─────────────────────────────────────────────────────┐
│ 1. INIT/GENERATE → 2. DEVELOP → 3. VALIDATE → 4. DEPLOY → 5. RUN │
└─────────────────────────────────────────────────────┘
        ↓              ↓           ↓            ↓         ↓
   創建專案        開發階段     檢查設定      部署資源    執行任務
```

### 階段詳解

| 階段 | 命令 | 說明 | 使用時機 |
|------|------|------|----------|
| **1. 初始化** | `bundle init` | 從模板創建新 bundle | 全新專案開始 |
| | `bundle generate` | 從現有資源生成 bundle | 遷移現有資源到 DAB |
| **2. 開發** | 手動編輯 YAML | 修改配置檔 | 調整資源定義 |
| **3. 驗證** | `bundle validate` | 檢查 YAML 語法和配置 | 部署前檢查 |
| **4. 部署** | `bundle deploy` | 將 bundle 部署到 workspace | 發布到環境 |
| **5. 執行** | `bundle run` | 執行 bundle 中的 job | 觸發任務執行 |
| **管理** | `bundle destroy` | 刪除部署的資源 | 清理環境 |

---

## 📋 DABs 基本指令速查表

### 核心命令(考試必記!)

```bash
# 1️⃣ 初始化新專案
databricks bundle init [template-name]
# 產出: databricks.yml + 資料夾結構

# 2️⃣ 從現有資源生成 (⭐ 本題考點)
databricks bundle generate [resource-type] --existing-[resource]-id [ID]
# 支援: job, pipeline, dashboard, app
# 同時產出: YAML 定義 + artifacts

# 3️⃣ 驗證配置
databricks bundle validate
databricks bundle validate -e [environment]

# 4️⃣ 部署到環境
databricks bundle deploy
databricks bundle deploy -e dev
databricks bundle deploy -e prod -t

# 5️⃣ 執行資源
databricks bundle run [job-key]
databricks bundle run [job-key] -e prod

# 6️⃣ 銷毀資源
databricks bundle destroy
databricks bundle destroy -e dev --auto-approve
```

---

## 🗂️ DABs 專案結構

```
my-dab-project/
├── databricks.yml          # 主配置檔(必須)
├── resources/              # 資源定義
│   ├── jobs/
│   │   └── my_job.yml
│   ├── pipelines/
│   │   └── my_pipeline.yml
│   └── dashboards/
│       └── my_dashboard.yml
├── src/                    # 程式碼
│   ├── notebooks/
│   ├── python/
│   └── sql/
└── fixtures/               # 測試資料(可選)
```

---

## 🎓 考試重點速記

### 1️⃣ 命令辨識陷阱(Syntax Trap)

**❌ 不存在的命令(容易混淆!)**
```bash
databricks bundle clone      # ❌ 沒有 clone
databricks bundle get        # ❌ 沒有 get
databricks bundle download   # ❌ 沒有 download
databricks bundle sync       # ❌ 沒有 sync
databricks bundle pull       # ❌ 沒有 pull
```

**✅ 正確命令**
```bash
databricks bundle init       # ✅ 初始化
databricks bundle generate   # ✅ 生成(從現有資源)
databricks bundle validate   # ✅ 驗證
databricks bundle deploy     # ✅ 部署
databricks bundle run        # ✅ 執行
databricks bundle destroy    # ✅ 銷毀
```

### 2️⃣ generate vs init 差異

| 特性 | `bundle init` | `bundle generate` |
|------|---------------|-------------------|
| **用途** | 創建全新 bundle | 從現有資源生成 |
| **輸入** | 模板名稱 | 資源 ID |
| **輸出** | 空白模板結構 | YAML + artifacts |
| **使用場景** | 新專案 | 遷移現有資源 |

```bash
# init: 從零開始
databricks bundle init default-python
# 產出空白模板

# generate: 遷移現有資源 (⭐ Q-057 考點)
databricks bundle generate job --existing-job-id 12345
# 產出: 
# - resources/jobs/job_12345.yml
# - src/downloaded_notebook.py
```

### 3️⃣ 環境管理

```yaml
# databricks.yml
targets:
  dev:
    mode: development
    workspace:
      host: https://dev.cloud.databricks.com
  
  prod:
    mode: production
    workspace:
      host: https://prod.cloud.databricks.com
```

```bash
# 部署到不同環境
databricks bundle deploy -e dev
databricks bundle deploy -e prod
```

### 4️⃣ 支援的資源類型

```
DABs 支援資源:
├── Jobs                 (工作流程)
├── Pipelines            (Delta Live Tables)
├── Dashboards           (儀表板)
├── Apps                 (應用程式)
├── Models               (ML 模型)
└── Experiments          (ML 實驗)
```

---

## 🔍 考試陷阱辨識

### 陷阱類型 1: 命令拼寫
```bash
# ❌ 容易寫錯
databricks bundles deploy    # 多了 s
databrick bundle deploy      # 少了 s

# ✅ 正確
databricks bundle deploy
```

### 陷阱類型 2: 參數順序
```bash
# ❌ 錯誤順序
databricks bundle --existing-job-id 123 generate job

# ✅ 正確順序
databricks bundle generate job --existing-job-id 123
```

### 陷阱類型 3: 子命令混淆
```bash
# ❌ 混淆其他 CLI 工具
git clone                    # Git 命令
kubectl get                  # K8s 命令
docker pull                  # Docker 命令

# ✅ DABs 專屬
databricks bundle generate   # 唯一正確方式
```

---

## 💡 實戰記憶口訣

### 生命週期口訣
```
「初(init) 生(generate) 驗(validate) 部(deploy) 跑(run) 毀(destroy)」
```

### 命令功能記憶
```
init     → 「從零開始」創建專案
generate → 「反向工程」現有資源
validate → 「健康檢查」配置檔
deploy   → 「推上雲端」部署資源
run      → 「立即執行」觸發任務
destroy  → 「清理環境」刪除資源
```

### generate 特點記憶
```
「Generate 一石二鳥:
 ✓ YAML 定義拿到手
 ✓ Artifacts 自動 download」
```

---

## 📊 考試出題模式

### 模式 1: 命令語法題(如 Q-057)
**考點**: 正確的命令和參數
**解題關鍵**: 記住有效命令列表,排除不存在的命令

### 模式 2: 生命週期順序題
**考點**: 命令執行順序
**解題關鍵**: init/generate → validate → deploy → run

### 模式 3: 環境部署題
**考點**: 多環境管理
**解題關鍵**: `-e` 參數指定環境

### 模式 4: 資源遷移題
**考點**: 將現有資源轉為 DAB
**解題關鍵**: 使用 `generate` 而非 `init`

---

## ✅ 考前檢查清單

- [ ] 記住 6 個核心命令(init, generate, validate, deploy, run, destroy)
- [ ] 知道 generate 會同時產生 YAML 和下載 artifacts
- [ ] 理解 init(新專案) vs generate(遷移) 差異
- [ ] 記住不存在的命令(clone, get, download, sync, pull)
- [ ] 熟悉環境切換參數 `-e`
- [ ] 了解支援的資源類型(job, pipeline, dashboard, app)

---

## 🎯 Q-057 快速解題法

**題目關鍵字識別**:
1. "existing Databricks job" → 不是新建,是遷移
2. "get YAML definition" → 需要設定檔
3. "download artifacts" → 需要相關檔案

**答案推導**:
```
existing + YAML + artifacts 
    ↓
需要「反向工程」功能
    ↓
databricks bundle generate ✓
```

**排除法**:
- clone/get/download → 都不是有效命令 ❌
- init → 用於全新專案,不處理現有資源 ❌
- **generate → 唯一能從現有資源產生 YAML + artifacts** ✅

---

**記住**: DABs 的核心就是「把 Databricks 當程式碼管理」,所有命令都圍繞這個理念設計!