# ✅ Databricks 認證考試高頻 CLI 指令 (官方驗證版)

## 🔥 1. Jobs 指令 (⭐⭐⭐ 最高頻)

### 查詢 Runs
```bash
# 列出 job 的所有 runs
databricks jobs list-runs --job-id <job-id>

# ✅ 只列出已完成的 runs (你的題目答案)
databricks jobs list-runs --job-id <job-id> --completed-only

# 只列出執行中的 runs
databricks jobs list-runs --job-id <job-id> --active-only

# 包含 task 詳細資訊
databricks jobs list-runs --job-id <job-id> --expand-tasks
```

### 執行與控制
```bash
# 立即執行 job
databricks jobs run-now <job-id>

# 取消執行中的 run
databricks jobs cancel-run <run-id>

# 取得 run 的輸出
databricks jobs get-run-output <run-id>

# 重新執行失敗的任務
databricks jobs repair-run <run-id>
```

### Job 管理
```bash
# 列出所有 jobs
databricks jobs list

# 取得 job 詳細資訊
databricks jobs get <job-id>

# 建立 job (使用 JSON)
databricks jobs create --json @config.json

# 更新 job 部分設定
databricks jobs update <job-id> --json '{"name":"new-name"}'

# 覆寫所有 job 設定
databricks jobs reset --json @config.json

# 刪除 job
databricks jobs delete <job-id>
```

---

## 📁 2. Workspace 指令 (⭐⭐⭐ 高頻)

```bash
# 列出目錄內容
databricks workspace ls /path/to/directory

# 匯出 notebook (4 種格式)
databricks workspace export /path/to/notebook -f SOURCE
databricks workspace export /path/to/notebook -f JUPYTER
databricks workspace export /path/to/notebook -f HTML
databricks workspace export /path/to/notebook -f DBC

# 匯入 notebook
databricks workspace import <local-file> /path/to/notebook -f SOURCE

# 刪除檔案或目錄
databricks workspace rm /path/to/file
databricks workspace rm -r /path/to/directory

# 建立目錄
databricks workspace mkdirs /path/to/directory
```

---

## 🗄️ 3. FS (File System) 指令 (⭐⭐⭐ 高頻)

### 基本操作
```bash
# 列出目錄內容
databricks fs ls dbfs:/path
databricks fs ls dbfs:/Volumes/main/default/my-volume

# 詳細列表 (包含大小、時間)
databricks fs ls dbfs:/path -l --absolute

# 查看檔案內容
databricks fs cat dbfs:/path/file.txt

# 建立目錄
databricks fs mkdir dbfs:/path/directory
```

### 檔案操作
```bash
# 複製檔案 (本地 → DBFS)
databricks fs cp <local-file> dbfs:/path/

# 複製檔案 (DBFS → 本地)
databricks fs cp dbfs:/path/file <local-path>

# 遞迴複製目錄
databricks fs cp -r <source> dbfs:/destination

# 覆寫現有檔案
databricks fs cp <source> dbfs:/destination --overwrite

# 刪除檔案
databricks fs rm dbfs:/path/file

# 遞迴刪除目錄
databricks fs rm -r dbfs:/path/directory
```

---

## 🔐 4. Secrets 指令 (⭐⭐⭐ 高頻)

### Scope 管理
```bash
# 列出所有 secret scopes
databricks secrets list-scopes

# 建立 Databricks-backed scope
databricks secrets create-scope <scope-name>

# 建立 scope (JSON 方式)
databricks secrets create-scope --json '{
  "scope": "my-scope",
  "initial_manage_principal": "users"
}'

# 刪除 scope
databricks secrets delete-scope <scope-name>
```

### Secret 管理
```bash
# 列出 scope 中的 secrets (僅元資料)
databricks secrets list-secrets <scope-name>

# 建立/更新 secret (互動式輸入)
databricks secrets put-secret <scope-name> <key-name>

# 建立/更新 secret (字串值)
databricks secrets put-secret --json '{
  "scope": "<scope-name>",
  "key": "<key-name>",
  "string_value": "<secret>"
}'

# 刪除 secret
databricks secrets delete-secret <scope-name> <key-name>
```

### ACL 權限管理
```bash
# 列出 scope 的 ACLs
databricks secrets list-acls <scope-name>

# 授予權限 (READ, WRITE, MANAGE)
databricks secrets put-acl <scope-name> <principal> <permission>
# 範例:
databricks secrets put-acl my-scope data-engineers READ

# 取得特定 principal 的權限
databricks secrets get-acl <scope-name> <principal>

# 刪除 ACL
databricks secrets delete-acl <scope-name> <principal>
```

---

## 🖥️ 5. Clusters 指令 (⭐⭐ 中高頻)

```bash
# 列出所有 clusters
databricks clusters list

# 取得 cluster 詳細資訊
databricks clusters get --cluster-id <cluster-id>

# 建立 cluster
databricks clusters create --json @cluster-config.json

# 啟動 cluster
databricks clusters start --cluster-id <cluster-id>

# 重啟 cluster
databricks clusters restart --cluster-id <cluster-id>

# 終止 cluster
databricks clusters delete --cluster-id <cluster-id>

# 永久刪除 cluster
databricks clusters permanent-delete --cluster-id <cluster-id>
```

---

## 📚 6. Libraries 管理 (⭐⭐ 中頻)

```bash
# 列出 cluster 上的 libraries
databricks libraries cluster-status --cluster-id <cluster-id>

# 安裝 PyPI package
databricks libraries install --cluster-id <cluster-id> \
  --json '{"pypi": {"package": "pandas==2.0.0"}}'

# 安裝 JAR
databricks libraries install --cluster-id <cluster-id> \
  --json '{"jar": "dbfs:/path/to/library.jar"}'

# 卸載 library
databricks libraries uninstall --cluster-id <cluster-id> \
  --json '{"pypi": {"package": "pandas"}}'
```

---

## 🎯 考試陷阱總整理

### ❌ 常見錯誤 vs ✅ 正確語法

| 錯誤寫法 | 正確寫法 | 說明 |
|---------|---------|------|
| `--success-only` | `--completed-only` | 參數名稱錯誤 |
| `--success` | `--completed-only` | 參數不存在 |
| `/dbfs/path` | `dbfs:/path` | 路徑前綴錯誤 |
| `databricks fs rm dbfs:/dir` | `databricks fs rm -r dbfs:/dir` | 刪除目錄需要 -r |
| `-f PYTHON` | `-f SOURCE` | 格式參數錯誤 |
| `secrets list <scope>` | `secrets list-secrets <scope>` | 子指令名稱錯誤 |
| `clusters get <id>` | `clusters get --cluster-id <id>` | 缺少參數旗標 |

---

## 📝 記憶技巧

### 1️⃣ Jobs Runs 過濾
- **completed-only**: 已完成的 (正確 ✅)
- **active-only**: 執行中的 (正確 ✅)
- **success-only**: 不存在 (錯誤 ❌)

### 2️⃣ 路徑規則
- **DBFS 路徑**: `dbfs:/path` (必須有 `dbfs:/` 前綴)
- **Workspace 路徑**: `/Workspace/path` (用於 workspace 指令)
- **Volumes 路徑**: `dbfs:/Volumes/catalog/schema/volume`

### 3️⃣ Notebook 匯出格式
記憶口訣：**「SOURCE JUPYTER HTML DBC」**
- `SOURCE`: 原始程式碼
- `JUPYTER`: Jupyter notebook 格式
- `HTML`: 網頁格式
- `DBC`: Databricks 封存格式

### 4️⃣ Secrets 權限層級
從低到高：**READ → WRITE → MANAGE**
- `READ`: 只能讀取 secrets
- `WRITE`: 可新增/更新 secrets
- `MANAGE`: 完整控制 (ACL 管理)

---

## 🔥 必背指令 Top 15

1. `databricks jobs list-runs --job-id <id> --completed-only`
2. `databricks fs cp -r <source> dbfs:/target`
3. `databricks fs rm -r dbfs:/path`
4. `databricks workspace export /path -f SOURCE`
5. `databricks secrets create-scope <scope>`
6. `databricks secrets put-secret <scope> <key>`
7. `databricks secrets put-acl <scope> <principal> READ`
8. `databricks secrets list-scopes`
9. `databricks clusters start --cluster-id <id>`
10. `databricks jobs run-now <job-id>`
11. `databricks jobs get-run-output <run-id>`
12. `databricks fs ls dbfs:/path -l --absolute`
13. `databricks jobs repair-run <run-id>`
14. `databricks workspace mkdirs /path`
15. `databricks clusters list`

---
