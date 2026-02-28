# 標籤規範 (Tagging Schema)

> 統一的標籤系統，確保題庫可檢索、可統計、可分析

---

## 🎯 標籤系統概覽

本專案使用三層標籤系統：

| 標籤類型 | 用途 | 數量限制 | 範例 |
|---------|------|---------|------|
| **Topic Tags** | 技術主題分類 | 1-3 個 | `Delta-Lake`, `Streaming`, `Unity-Catalog` |
| **Trap Tags** | 陷阱類型標記 | 0-2 個 | `Syntax-Confusion`, `Parameter-Order` |
| **Level Tags** | 難度等級 | 必須 1 個 | `L1-Basic`, `L2-Intermediate`, `L3-Advanced` |

---

## 📚 Topic Tags (技術主題標籤)

### 使用原則
- **核心為主** - 選擇最核心的技術主題，最多 3 個
- **一致性** - 嚴格使用下列標準標籤，避免自創標籤
- **層級關係** - 優先使用細分標籤（如 `Delta-Lake`），而非廣泛標籤（如 `Storage`）

---

### 標準 Topic Tags 清單

#### 1. Delta Lake 相關
| 標籤 | 說明 | 適用題型範例 |
|------|------|-------------|
| `Delta-Lake` | Delta Lake 核心功能 | VACUUM, OPTIMIZE, Time Travel |
| `Delta-MERGE` | MERGE 指令 | MERGE INTO 語法、條件式更新 |
| `Delta-CDC` | Change Data Capture | CDF (Change Data Feed) 功能 |
| `Delta-Constraints` | 約束條件 | CHECK constraints, NOT NULL |
| `Delta-Schema-Evolution` | Schema 演化 | mergeSchema, overwriteSchema |
| `Delta-Optimization` | 效能優化 | ZORDER, OPTIMIZE, 檔案管理 |

---

#### 2. Structured Streaming 相關
| 標籤 | 說明 | 適用題型範例 |
|------|------|-------------|
| `Streaming` | 串流處理核心概念 | Trigger, Checkpoint, Watermark |
| `Streaming-Sources` | 串流資料來源 | Kafka, Event Hubs, Auto Loader |
| `Streaming-Sinks` | 串流輸出目標 | Delta, Parquet, Console |
| `Streaming-Windowing` | 視窗函數 | Tumbling, Sliding, Session Windows |
| `Streaming-Stateful` | 狀態管理 | mapGroupsWithState, flatMapGroupsWithState |
| `Auto-Loader` | Auto Loader 功能 | cloudFiles, schema inference |

---

#### 3. Unity Catalog 相關
| 標籤 | 說明 | 適用題型範例 |
|------|------|-------------|
| `Unity-Catalog` | Unity Catalog 核心概念 | Metastore, Catalog, Schema 三層架構 |
| `UC-Permissions` | 權限管理 | GRANT, REVOKE, 權限繼承 |
| `UC-Data-Governance` | 數據治理 | Lineage, Audit Logs, Tags |
| `UC-External-Locations` | 外部位置 | External Locations, Storage Credentials |
| `UC-Sharing` | Delta Sharing | 跨組織資料共享 |

---

#### 4. Databricks 平台相關
| 標籤 | 說明 | 適用題型範例 |
|------|------|-------------|
| `Databricks-SQL` | Databricks SQL | SQL Warehouse, Query History |
| `Databricks-Workflows` | 工作流程 | Jobs, Tasks, Orchestration |
| `Databricks-Repos` | Git 整合 | Repos, Notebooks 版本控制 |
| `Databricks-Secrets` | 密鑰管理 | Secret Scopes, dbutils.secrets |
| `Databricks-CLI` | 命令列工具 | Databricks CLI 指令 |
| `Cluster-Management` | 叢集管理 | Cluster 類型、配置、Auto-scaling |

---

#### 5. Spark 核心與 PySpark/SQL
| 標籤 | 說明 | 適用題型範例 |
|------|------|-------------|
| `PySpark` | PySpark 語法 | DataFrame API, transformations |
| `Spark-SQL` | Spark SQL 語法 | SELECT, JOIN, Window Functions |
| `DataFrames` | DataFrame 操作 | select, filter, groupBy, agg |
| `Spark-UDF` | 使用者自訂函數 | UDF, Pandas UDF |
| `Spark-Performance` | Spark 效能調校 | Partitioning, Caching, Broadcast |
| `Spark-Joins` | Join 操作 | Inner, Left, Right, Anti, Semi |

---

#### 6. 資料工程通用概念
| 標籤 | 說明 | 適用題型範例 |
|------|------|-------------|
| `ETL-Patterns` | ETL 設計模式 | Incremental load, SCD Type 2 |
| `Data-Quality` | 資料品質 | Validation, Expectations, Testing |
| `Data-Modeling` | 資料建模 | Star Schema, Snowflake Schema |
| `File-Formats` | 檔案格式 | Parquet, JSON, CSV, Avro |
| `Partitioning` | 資料分割 | Partition columns, bucketing |
| `Schema-Management` | Schema 管理 | Schema inference, evolution |

---

#### 7. 安全性與治理
| 標籤 | 說明 | 適用題型範例 |
|------|------|-------------|
| `Security` | 安全性通用概念 | Authentication, Authorization |
| `Access-Control` | 存取控制 | ACLs, Table ACLs, Row/Column level |
| `Encryption` | 加密機制 | At-rest, In-transit encryption |
| `Audit-Logging` | 稽核日誌 | Audit logs, Compliance |

---

## ⚠️ Trap Tags (陷阱類型標籤)

### 使用原則
- **標記易錯點** - 標記此題容易誤選的原因
- **最多 2 個** - 選擇最主要的陷阱類型
- **選填欄位** - 若無明顯陷阱，可不標記

---

### 標準 Trap Tags 清單

#### 語法與指令相關
| 標籤 | 說明 | 範例 |
|------|------|------|
| `Syntax-Confusion` | 語法混淆 | MERGE 與 UPDATE 語法相似 |
| `Parameter-Order` | 參數順序錯誤 | groupBy vs partitionBy 順序 |
| `Command-Purpose` | 指令用途混淆 | VACUUM vs OPTIMIZE vs DELETE |
| `Case-Sensitivity` | 大小寫敏感 | SQL 關鍵字、欄位名稱 |
| `Keyword-Typo` | 關鍵字拼寫 | DISTICT vs DISTINCT |

---

#### 概念與邏輯相關
| 標籤 | 說明 | 範例 |
|------|------|------|
| `Concept-Confusion` | 概念混淆 | Watermark vs Window |
| `Similar-Function` | 相似功能混淆 | cache() vs persist() |
| `Logical-Trap` | 邏輯陷阱 | 否定邏輯、條件判斷錯誤 |
| `Scope-Misunderstanding` | 作用域誤解 | 變數作用域、權限範圍 |

---

#### 數值與單位相關
| 標籤 | 說明 | 範例 |
|------|------|------|
| `Unit-Confusion` | 單位混淆 | 天 vs 小時, MB vs GB |
| `Number-Trap` | 數字陷阱 | 30 天 ≠ 30 小時 |
| `Default-Value` | 預設值誤解 | VACUUM RETAIN 預設 168 小時 |

---

#### 行為與執行相關
| 標籤 | 說明 | 範例 |
|------|------|------|
| `Execution-Behavior` | 執行行為誤解 | Lazy evaluation vs eager |
| `Side-Effect` | 副作用誤解 | 指令是否會修改原始資料 |
| `Performance-Misconception` | 效能認知錯誤 | 以為某操作會自動優化 |

---

## 📊 Level Tags (難度等級標籤)

### 使用原則
- **必填欄位** - 每題必須標記難度
- **只能選一個** - L1 / L2 / L3 三選一
- **客觀評估** - 基於考點複雜度，而非個人主觀感受

---

### 難度定義

#### L1-Basic (基礎題)
**特徵:**
- 官方文件直接查得到答案
- 考核單一概念或指令
- 語法直觀，無複雜邏輯

**範例題型:**
- Delta Lake 的預設保留期限是多少天？
- 如何使用 DESCRIBE DETAIL 查看表格資訊？
- Spark DataFrame 的 select() 方法用途是什麼？

**佔比建議:** 30-40%

---

#### L2-Intermediate (中階題)
**特徵:**
- 需理解多個概念的組合
- 涉及參數選擇或條件判斷
- 需比較類似功能的差異

**範例題型:**
- 在何種情況下應使用 MERGE 而非 UPDATE？
- Structured Streaming 的三種 Trigger 模式差異是什麼？
- Unity Catalog 的三層權限繼承規則如何運作？

**佔比建議:** 40-50%

---

#### L3-Advanced (進階題)
**特徵:**
- 需深入理解運作原理
- 涉及效能優化或最佳實踐
- 複雜情境題，需綜合判斷

**範例題型:**
- 如何設計 SCD Type 2 的 Delta Lake MERGE 邏輯？
- 在大規模資料集上，如何優化 Skewed Join？
- Structured Streaming 的 Stateful Operations 如何處理 Late Data？

**佔比建議:** 10-20%

---

## 🔍 標籤使用範例

### 範例 1: Delta Lake VACUUM 題目

```markdown
**Topics:** `Delta-Lake`, `Data-Retention`, `Storage-Management`
**Traps:** `Unit-Confusion`, `Number-Trap`
**Level:** `L2-Intermediate`
```

**說明:**
- **Topics:** 核心考點是 Delta Lake，涉及資料保留與儲存管理
- **Traps:** 陷阱在於時間單位換算（天 vs 小時）與數字混淆（30 天 ≠ 30）
- **Level:** 需理解 VACUUM 的參數與用途，屬中階題

---

### 範例 2: Structured Streaming Trigger 題目

```markdown
**Topics:** `Streaming`, `Streaming-Triggers`
**Traps:** `Execution-Behavior`, `Similar-Function`
**Level:** `L2-Intermediate`
```

**說明:**
- **Topics:** 核心考點是串流處理的 Trigger 模式
- **Traps:** 容易混淆 Once, Continuous, ProcessingTime 的執行行為
- **Level:** 需比較三種模式差異，屬中階題

---

### 範例 3: Unity Catalog GRANT 題目

```markdown
**Topics:** `Unity-Catalog`, `UC-Permissions`, `Security`
**Traps:** `Scope-Misunderstanding`
**Level:** `L3-Advanced`
```

**說明:**
- **Topics:** 核心考點是 Unity Catalog 的權限管理與安全性
- **Traps:** 容易誤解權限繼承的作用域（Metastore → Catalog → Schema）
- **Level:** 需深入理解三層架構與權限傳播規則，屬進階題

---

## 📏 標籤品質檢查

### 自我檢查清單
提交 PR 前，請確認：
- [ ] Topic Tags 數量為 1-3 個
- [ ] 所有 Topic Tags 都在標準清單中（無自創標籤）
- [ ] Level Tag 只有 1 個，且符合難度定義
- [ ] Trap Tags (若有) 準確標記易錯點
- [ ] 標籤使用連字符 `-` 而非底線 `_`（如 `Delta-Lake` 而非 `Delta_Lake`）

---

## 🆕 新增標籤流程

若現有標籤無法涵蓋新考點，請遵循以下流程：

### 步驟 1: 檢查是否真的需要新標籤
- 確認現有標籤確實無法涵蓋
- 避免過度細分（如不需要 `Delta-VACUUM` 標籤，用 `Delta-Lake` 即可）

### 步驟 2: 提出新標籤建議
在 PR 或 Issue 中說明：
- **建議標籤名稱**
- **適用範圍與定義**
- **範例題目**
- **與現有標籤的區別**

### 步驟 3: 團隊討論與批准
經團隊討論後，由專案維護者更新此文件。

### 步驟 4: 同步更新
- 更新 `.github/skills/tagging-schema/references/tagging-schema.md`
- 通知團隊成員新標籤可用
- 回溯標記相關題目（選填）

---

## 📊 標籤統計與分析

標籤系統的價值在於可統計與可分析。

### 個人弱點分析 (Phase 2 開發)
```bash
# 統計個人錯題的 Topic Tags 分佈
python skills/scripted/personal-weakness-analysis.py --user eric

# 輸出範例：
# Top 3 Weak Topics:
# 1. Streaming (5 errors)
# 2. Unity-Catalog (3 errors)
# 3. Delta-Optimization (2 errors)
```

### 團隊弱點儀表板 (Phase 2 開發)
```bash
# 產出團隊整體弱點報表
python skills/scripted/team-weakness-dashboard.py

# 輸出範例：
# Team Dashboard (2024-01-15)
# Total Questions: 120
# Average Accuracy: 78%
#
# Top Team Weaknesses:
# 1. Streaming (18 errors across 5 members)
# 2. UC-Permissions (12 errors across 4 members)
```

---

## 🔗 相關文件

- [contribution-guide.md](../../contribution-guide/references/contribution-guide.md) - PR 提交與 Review 規範
- [question-template.md](../../../../question-bank/_template/question-template.md) - 題目模板
- [analysis-template.md](../../../../question-bank/_template/analysis-template.md) - 解析模板

---

**標籤系統是知識資產化的基礎，請務必遵守規範，確保團隊協作品質！🏷️**
