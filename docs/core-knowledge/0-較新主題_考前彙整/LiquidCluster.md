## 用途與目的
Liquid Clustering 是 一種**資料組織方式**，用來自動（或半自動）重整 Delta 表檔案布局，改善查詢效能，並降低傳統 **Partition** 與 **Z-ORDER** 帶來的維運成本。

### 它在解決什麼問題
傳統 partitioning 需要你先猜好切分欄位與粒度，容易遇到過度分割、小檔案、資料傾斜等問題；
Z-ORDER 需要定期人工 OPTIMIZE 維護。
Liquid clustering 的設計方向是：用更彈性的 clustering keys + 增量重整檔案，讓表的布局更容易隨需求調整。

### 核心特性
1. 維運負擔更低：你不必長期維護複雜的 partition 策略，也不需要一直手動調 ZORDER。
2. keys 選擇更彈性：可以用高基數欄位作為 clustering keys（過去這常是 partition 的禁區），更貼近查詢的過濾條件。
3. keys 可調整：支援用 ALTER TABLE 調整 clustering keys；但既有資料不會立刻全部重寫，需要靠後續 OPTIMIZE 逐步把資料轉成新的布局。
4. 不相容限制：**Clustering 不可與 partitioning 共用，也不可再做 ZORDER**（二選一）。

### 適用情境（建議用法）
* 資料持續成長、常做篩選查詢、或希望避免 partition 失誤成本的表
* 過濾欄位高基數、partition 不適合，但仍想要類似資料局部性帶來的效能收益
* 希望後續能調整 keys，而不是一開始選錯就要大改表設計

---


## 怎麼啟用
用 SQL 在建表時指定 clustering keys，例如：

* 建表：`CREATE TABLE ... USING DELTA CLUSTER BY (col0);`
* 或 CTAS：`CREATE TABLE ... CLUSTER BY (col0) AS SELECT ...;`
* 觸發整理：`OPTIMIZE table_name;`

另外，若要談「會依查詢模式自動調整」這件事，要特別區分：

* 你手動指定 `CLUSTER BY (cols...)`：不會自己“發現新 keys”，要你自己改。
* 若使用 **AUTO / Predictive Optimization** 相關能力：才會根據工作負載（query history）自動選 key / 調整策略（版本與可用性依 workspace / DBR 而異）。

---

## 怎麼運作
Liquid clustering 的 OPTIMIZE 以「增量」方式處理：每次會找出尚未完成 clustering 的檔案，分組成一個邏輯單元（常被描述為 ZCube），再用類似空間填充曲線（常見提法是 Hilbert curve）的方式把資料重新排列、產生新的 clustered files。重點是：後續 OPTIMIZE 主要只處理新增或尚未分群的檔案，降低重寫量與 I/O。


### 白話概念版：
想像一張 Delta table 底下其實是一堆 Parquet 檔。你想做某個條件查詢或聚合時（例如 key 在 100～120），引擎最怕的是「很多檔看起來都有可能符合」，結果就得掃一堆檔。

Liquid Clustering 做的事可以分成兩層：

第一層：先把多維資料變成一個排序用的數字
它會用一個演算法，把你指定的多個欄位（clustering keys）的值，壓成「一個排序用的數字」。這個數字越接近，代表那些欄位的值越接近。接下來 OPTIMIZE 就會照這個數字把資料重新排隊，並重寫檔案。

第二層：不只檔案內整齊，還要讓檔案之間也有區間感
如果只做到「檔案內排序」，每個檔裡面都整齊了，但 A 檔、B 檔、C 檔 可能各自仍然混著很多 key 範圍。你查 key 在 100～120 時，很多檔的資料看起來都“可能有”，最後還是得掃很多檔。

做到「檔案間分布」則不同：重寫檔案時不是隨機切檔，而是照排序後的連續區間切成一個個檔案，於是檔案之間會自然呈現出「檔案1 大多是 key 0～50、檔案2 大多是 50～100、檔案3 大多是 100～150」這種分段感。你查 100～120 時，大部分前面的檔可以直接跳過，只需要讀後面少數檔案。

### 精準說法

每個 Parquet 檔（甚至每個 row group）都有欄位統計資訊，例如 min/max、null count。Delta 會利用這些統計做 data skipping（檔案剪枝與掃描量減少）。Liquid clustering 透過「重新排列 + 重寫檔案」同時改善兩件事：
	1.	檔案內分布（within-file）
同一個檔案內，資料在 clustering keys 的排序上更連續，所以每個 row group 的 min/max 範圍更窄、更集中，查詢時可以跳過更多 row group（或至少減少解壓與掃描量）。
	2.	檔案間分布（across-files）
新檔案的切分依排序鍵的連續區間來產生，讓不同檔案的 min/max 範圍更少重疊（overlap 下降），查詢時 Delta 能直接跳過整個檔案，I/O 明顯下降。這也是官方說 clustering 能改善 data skipping、提升效能的原因。


### 演算法：Hilbert curve扮演角色：
「把多維資料壓成一個排序用的數字」的演算法，Liquid clustering 用的就是 Hilbert curve 這類 space-filling curve 的概念：它會把多個欄位形成的多維座標映射成一個一維的順序（Hilbert ordering / index），目標是讓在多維空間彼此接近的資料，在一維排序上也盡量接近。換成你前面的描述：它就是用來產生那個「排序用的數字」，讓重寫檔案時能做出更好的檔案內連續性與檔案間分段。

簡單的商業數據分析例子（讓多維聚合更清楚）：

假設你在做零售的銷售分析表 sales，常見的聚合是：
	•	看某個「門市 + 商品類別」在一段時間內的銷售額、毛利、來客數
例如：store_id、category_id、event_date 是你最常 filter / group by 的維度。

如果資料檔案是亂的，你做「某門市、某類別、近 7 天」的聚合時，很多檔案的 min/max 都涵蓋很廣的 store/category/date，導致引擎必須掃大量檔案再進行聚合，聚合結果雖然正確，但計算成本很高。

把 clustering keys 設成 (store_id, category_id, event_date) 後，Hilbert ordering 會把在這三個維度上接近的資料排在一起，OPTIMIZE 重寫後通常會形成更清楚的檔案分布：
	•	某些檔案主要落在特定 store 的區段
	•	且在該 store 內又更集中於某些 category
	•	同時日期區間也更連續

於是你查「store=12、category=3、近 7 天」時，大量不相關檔案會因 min/max 不相交而被跳過，真正讀進來聚合的資料更聚焦，聚合的 I/O 與掃描量會明顯下降，查詢延遲更穩定。

（如果你把你實際常用的 2～4 個 filter/group 維度貼給我，我也可以把這個例子改成更貼你查詢模式的版本，甚至幫你判斷 keys 排序的優先順序。）
---


## 🆕 需要補充的功能

**1. Automatic Liquid Clustering**（DBR 15.4 LTS+）
```sql
-- 讓平台自動選擇最佳 clustering keys
CREATE TABLE t1 (...) CLUSTER BY AUTO;
ALTER TABLE t1 CLUSTER BY AUTO;
```
- 需啟用 Predictive Optimization
- 分析歷史查詢自動調整 keys，無需手動維護

**2. `OPTIMIZE FULL`**（DBR 16.0+）
```sql
-- 強制全表重新聚類（首次啟用或變更 keys 時使用）
OPTIMIZE table_name FULL;
```
- 一般 `OPTIMIZE` 是增量的，不會重寫已聚類資料

**3. Clustering on Write 有觸發門檻**

| Clustering Keys 數量 | UC Managed Tables | 其他 Delta Tables |
|---------------------|-------------------|------------------|
| 1 | 64 MB | 256 MB |
| 2 | 256 MB | 1 GB |
| 3 | 512 MB | 2 GB |
| 4 | 1 GB | 4 GB |

→ 小批次寫入不會自動觸發，仍需定期執行 `OPTIMIZE`

---

### 📌 實務建議更新

| 情境 | 建議 |
|-----|-----|
| Unity Catalog managed tables | 直接用 `CLUSTER BY AUTO` + Predictive Optimization |
| 小表（<10TB） | 限制 1-2 個 clustering keys |
| 首次啟用或變更 keys | 執行 `OPTIMIZE FULL` |
| 高頻 insert/update | 每 1-2 小時排程 `OPTIMIZE`（或啟用 Predictive Optimization） |

---

### 🔖 版本對照
| 功能 | 最低 DBR 版本 |
|-----|-------------|
| Liquid Clustering GA | 15.2 |
| Automatic Liquid Clustering | 15.4 LTS |
| Structured Streaming 建表 | 16.0 |
| `OPTIMIZE FULL` | 16.0 |
| Iceberg 支援（Preview） | 16.4 LTS |
| 大表 OPTIMIZE 效能優化 | 17.2（建議） |