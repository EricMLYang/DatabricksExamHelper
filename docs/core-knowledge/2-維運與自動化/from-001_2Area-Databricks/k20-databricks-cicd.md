# Databricks CICD

- Databricks Asset Bundles 是目前 Databricks **官方推薦**的 CI/CD 方式

- 這種方法將專案的所有元件（Jobs、Notebooks、Libraries 等）都視為「程式碼」（Infrastructure as Code），可以實現可重複、可審核、可回滾的自動化佈署。

---

## 流程

1. **原始碼**：將專案檔案放在 Git 倉庫中是所有 CI/CD 流程的起點。

2. **機密設定**：使用 Pipelines 變數庫來存放機密資訊（如 `DATABRICKS_HOST` 和 `DATABRICKS_TOKEN`），這是標準的安全做法。

3. **安裝 CLI**：在 Runner 上安裝 Databricks CLI 是執行任何 CLI 命令的必要前置步驟。

4. **建置/測試**：這是 CI/CD 流程中確保程式碼品質的關鍵步驟，建置 Wheel 並執行單元測試是常見的模式。

5. **佈署**：`databricks bundle deploy` 是使用 Bundles 進行佈署的標準命令。

---

# 1) 最簡 `databricks.yml`（含 Job、Dashboard、建表）

> 重點：
>
> - Job 先跑一個 **SQL 檔** 來 `CREATE TABLE IF NOT EXISTS`，再跑 **notebook**。
>
> - 用 **新叢集**（`new_cluster`）與 **Quartz Cron** 設排程。
>
> - Dashboard 用 **Lakeview JSON** 檔（`.lvdash.json`）+ **SQL Warehouse**。
>
> - 變數（`var.*`）集中設定，targets 可切換 dev/stg/prod。
>    參考：官方 bundle 設定/資源/任務型別文件與 Dashboard 範例。 ([Databricks Documentation](https://docs.databricks.com/aws/en/dev-tools/bundles/settings?utm_source=chatgpt.com "Databricks Asset Bundle configuration"), [Microsoft Learn](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/resources?utm_source=chatgpt.com "Databricks Asset Bundles resources - Azure ..."))

```yaml
# databricks.yml  —— 最小可行示例
bundle:
  name: mini-pipeline

variables:
  warehouse_id:
    description: SQL Warehouse ID for dashboard & SQL tasks
    default: "<PUT-YOUR-WAREHOUSE-ID>"
  node_type_id:
    description: Cluster node type
    default: "Standard_DS3_v2"
  spark_version:
    description: Runtime
    default: "13.3.x-scala2.12"

resources:
  jobs:
    mini_etl_job:
      name: mini_etl_job
      schedule:                   # Quartz Cron：每天 07:00 執行（台北時區）
        quartz_cron_expression: "0 0 7 * * ?"
        timezone_id: "Asia/Taipei"
      tasks:
        # 1) 先執行 SQL 以建立不存在的表
        - task_key: init_ddl
          sql_task:
            file:
              path: ./sql/01_init.sql     # 內含 CREATE TABLE IF NOT EXISTS ...
              source: WORKSPACE
            warehouse_id: ${var.warehouse_id}
        # 2) 執行 Notebook（PySpark）
        - task_key: run_notebook
          depends_on:
            - task_key: init_ddl
          notebook_task:
            notebook_path: ./src/etl_notebook.ipynb
          new_cluster:
            spark_version: ${var.spark_version}
            node_type_id: ${var.node_type_id}
            num_workers: 2

  dashboards:
    mini_dashboard:
      display_name: "Mini Demo Dashboard"
      file_path: ./dashboards/mini_demo.lvdash.json
      warehouse_id: ${var.warehouse_id}

targets:
  dev:
    default: true
```

- **Notebook 任務**與**SQL file 任務**在 Bundles 的 YAML 寫法如上（來源對應 Workspace 路徑，部署時會自動上傳），這些寫法與 Jobs API 對應，Schedule 使用 **Quartz Cron**。([Databricks Documentation](https://docs.databricks.com/aws/en/dev-tools/bundles/job-task-types "Add tasks to jobs in Databricks Asset Bundles | Databricks on AWS"), [quartz-scheduler.org](https://www.quartz-scheduler.org/documentation/quartz-2.3.0/tutorials/crontrigger.html?utm_source=chatgpt.com "Cron Trigger Tutorial"))

- **Dashboard 資源**用 `file_path` 指向 Lakeview 的 JSON 匯出檔，並指定 `warehouse_id`。([Microsoft Learn](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/resources?utm_source=chatgpt.com "Databricks Asset Bundles resources - Azure ..."))

### `sql/01_init.sql`（最簡 DDL；首次部署確保表存在）

> 請把 `catalog.schema.table` 換成你的 UC 名稱。

```sql
CREATE TABLE IF NOT EXISTS main.demo.people_counter (
  event_date DATE,
  cam_id     STRING,
  count      BIGINT
) COMMENT 'demo table for dashboard';
```

> 補充：若你要把表放在 UC（Unity Catalog）下，記得用三段名（`catalog.schema.table`）。若 Dashboard 的查詢會用到表，**JSON 內容本身**（`lvdash.json`）裡的查詢要引用同一個表名；Bundles 的 `dashboards` 區塊只負責把 JSON 上傳與綁定 Warehouse。([Microsoft Learn](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/resources?utm_source=chatgpt.com "Databricks Asset Bundles resources - Azure ..."))

---

# 2) 最簡 Azure DevOps Pipeline（`azure-pipelines.yml`）

> 重點：安裝 Databricks CLI → `bundle validate` → `bundle deploy`。`DATABRICKS_HOST / DATABRICKS_TOKEN` 放在 Pipeline 變數或 Variable Group。([Microsoft Learn](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/cli/bundle-commands?utm_source=chatgpt.com "bundle command group - Azure Databricks"))

```yaml
# azure-pipelines.yml —— 最小可行示例
trigger:
  - main

pool:
  vmImage: "ubuntu-latest"

steps:
  - script: python -m pip install --upgrade pip databricks-cli
    displayName: "Install Databricks CLI"

  - task: Bash@3
    displayName: "Validate & Deploy Bundle (dev)"
    env:
      DATABRICKS_HOST: $(DATABRICKS_HOST)
      DATABRICKS_TOKEN: $(DATABRICKS_TOKEN)
    inputs:
      targetType: inline
      script: |
        databricks -v
        databricks bundle validate --target dev
        databricks bundle deploy --target dev
```

- `databricks bundle` 指令是官方建議用於 CI/CD 的做法；適用 GitHub Actions 或 Azure DevOps。([Microsoft Learn](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/cli/bundle-commands?utm_source=chatgpt.com "bundle command group - Azure Databricks"))

- 若你想用 **不同環境 cron / 叢集大小**，可在 `targets` 下覆蓋參數或用 YAML 變數／管線替換策略（例如 Replace Tokens）。([Stack Overflow](https://stackoverflow.com/questions/77542813/how-can-i-pass-parameters-to-databricks-yml-in-databricks-asset-bundles?utm_source=chatgpt.com "How can I pass parameters to databricks.yml in ..."))

- Azure DevOps 端到端範例與教學可參考 Databricks/社群文章（步驟與範例 YAML）。([Microsoft Learn](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/ci-cd-bundles?utm_source=chatgpt.com "CI/CD using Databricks Asset Bundles - Azure ..."), [Databricks Community](https://community.databricks.com/t5/data-engineering/demo-deploy-a-databricks-asset-bundle-with-azure-devops/td-p/126585?utm_source=chatgpt.com "Demo Deploy a Databricks Asset Bundle with Azure D..."), [StefanKo.ch](https://stefanko.ch/posts/effortless-databricks-asset-bundle-deployments-with-azure-devops/?utm_source=chatgpt.com "Effortless Databricks Asset Bundle Deployments with Azure ..."), [Medium](https://stefanko-ch.medium.com/effortless-databricks-asset-bundle-deployments-with-azure-devops-262f530176cb?utm_source=chatgpt.com "Effortless Databricks Asset Bundle Deployments with Azure ..."))

---

# 3) 其他執行補充（易踩雷 → 快速說清）

- **Warehouse / Cluster ID 取得**

   - `warehouse_id`：到 SQL Warehouse 頁面「Name」後括號裡的 ID。([Databricks Documentation](https://docs.databricks.com/aws/en/dev-tools/bundles/job-task-types "Add tasks to jobs in Databricks Asset Bundles | Databricks on AWS"))

- **排程（Quartz Cron）**

   - Job `schedule.quartz_cron_expression` 使用 Quartz 語法；上例每日 07:00。需要複雜規則可參考 Quartz 文件。([Databricks Documentation](https://docs.databricks.com/api/workspace/jobs/create?utm_source=chatgpt.com "Create a new job | Jobs API | REST API reference"), [quartz-scheduler.org](https://www.quartz-scheduler.org/documentation/quartz-2.3.0/tutorials/crontrigger.html?utm_source=chatgpt.com "Cron Trigger Tutorial"))

- **Dashboard JSON**

   - Lakeview 儀表板可以匯出為 `.lvdash.json`；JSON 裡的查詢要直接讀你建立的表（例如 `main.demo.people_counter`）。Bundles 只負責把檔案與 Warehouse 綁上。([Microsoft Learn](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/resources?utm_source=chatgpt.com "Databricks Asset Bundles resources - Azure ..."))

- **資源定義來源**

   - 所有 `resources`（jobs、dashboards…）都以 Bundles YAML 宣告；你也可以用 `bundle generate` 從現有工作區資源反向產生配置，再精簡成你的最小案。([Databricks Documentation](https://docs.databricks.com/aws/en/dev-tools/bundles/migrate-resources?utm_source=chatgpt.com "Migrate existing resources to a bundle | Databricks on AWS"))

- **專案骨架 / 範例**

   - 官方提供 **Examples**（含 dashboard + job 的 NYC Taxi 範例）與 **Templates** 可直接對照。([Microsoft Learn](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/examples?utm_source=chatgpt.com "Bundle configuration examples - Azure Databricks"), [Databricks Documentation](https://docs.databricks.com/aws/en/dev-tools/bundles/examples?utm_source=chatgpt.com "Bundle configuration examples | Databricks on AWS"))

- **認證與 CLI 版本**

   - 建議使用新版 Databricks CLI（0.218+）；Pipeline 內以 `DATABRICKS_HOST` 與 `DATABRICKS_TOKEN` 環境變數認證最單純。([Databricks Documentation](https://docs.databricks.com/aws/en/dev-tools/bundles/settings?utm_source=chatgpt.com "Databricks Asset Bundle configuration"))

---

如果你把上面三個檔案放好（`databricks.yml`、`sql/01_init.sql`、`azure-pipelines.yml`），再把一個最簡的 `src/etl_notebook.ipynb` 與 `dashboards/mini_demo.lvdash.json` 放進 repo，**就能跑完整 flow**：
**DevOps 觸發 → 部署 bundle → 建表（若不存在）→ 跑 notebook → 上傳/更新 Dashboard**。這組合是官方文件支援、實務最常見的最小集。([Databricks Documentation](https://docs.databricks.com/aws/en/dev-tools/bundles/settings?utm_source=chatgpt.com "Databricks Asset Bundle configuration"))

<https://learn.microsoft.com/en-us/azure/databricks/dev-tools/ci-cd/azure-devops?utm_source=chatgpt.com> 