


## Lakeflow 定義
Lakeflow 是 Databricks 提供的原生服務層，是一套「Declarative Data Pipeline Runtime + 管線管理服務」。
使用者只需要用 SQL 或 Python decorator 以宣告式方式定義 pipeline，平台就會自動負責：
( SQL：CREATE LIVE TABLE ..., Python：@dlt.table, @dlt.expect...)
* 管線依賴解析與宣告式定義
* 自動增量處理與狀態管理（state + checkpoint）
* 內建資料品質規則（expectations）
* 原生 lineage、受控的 schema evolution、版本回溯 / pipeline recovery
* 與 Unity Catalog 深度整合的治理與稽核能力

```
應用 / Agent / BI
───────────────
Lakeflow（資料流控制層 / 管線服務層）
───────────────
Spark + Delta Lake（計算與儲存引擎）
───────────────
Cloud Infra
```


## Delta Live Tables (DLT) vs. 一般 Delta Table
一般 Delta Table：
* 只是 storage + metadata

DLT 管的 Delta Table：多了一層「管線身分」：
* 屬於哪個 pipeline
* 上游是誰
* 下游是誰
* 最新成功版本是哪次 run
* 品質規則結果
* expectation pass / fail
這些資訊：存在在 Lakeflow / DLT 的 control plane metadata



## 快速複習 python decorators
```
def my_decorator(func):
    def wrapper():
        print("--- 執行前：準備工作 ---")
        func()  # 執行原本的函數
        print("--- 執行後：清理工作 ---")
    return wrapper

@my_decorator
def say_hello():
    print("你好，世界！")

say_hello()
```
```@my_decorator``` 只是一個簡寫，
它的效果等同於： ```say_hello = my_decorator(say_hello)```

## 最簡單範例
```
@dlt.table
@dlt.expect_or_drop("positive_price", "price > 0")
def silver_products():
    return spark.readStream.table("bronze_products")
```

有個模組叫 `dlt`，它有個 decorator 叫   `table` 和 `expect_or_drop`，
這段做了三件事：
	1.	定義一張 DLT/Lakeflow 的表：@dlt.table 把 silver_products 這個函數註冊成 pipeline 會產出的「silver_products」表（結果會被物化成 Delta table）。
	2.	加一條資料品質規則：@dlt.expect_or_drop("positive_price", "price > 0") 規定 price 必須大於 0，不符合的資料列會被丟掉（drop），同時系統會記錄這條規則的品質統計。
	3.	資料來源是串流讀取：函數本體用 spark.readStream.table("bronze_products") 從 bronze_products 這張表以 Structured Streaming 的方式讀資料，持續處理新進資料。




假想 decorator（示意用）
```
REGISTRY = {}   # 用來記住「有哪些 table 定義」
METRICS  = {}   # 用來記錄「跑完的統計」

def expect_or_drop(rule_name, rule_expr):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 1) 先執行原本的資料定義（拿到 DataFrame / Streaming DF）
            df = func(*args, **kwargs)

            # 2) 把 rule_expr 轉成 Spark SQL filter（示意）
            #    e.g. "price > 0" -> df.filter("price > 0")
            df_after = df.filter(rule_expr)

            # 3) 記錄品質指標（示意）
            #    - 總筆數、被丟掉筆數、丟掉比例
            #    - 寫到 event log / expectation metrics
            # (真實 DLT 會有更完整的 metrics 與 lineage)
            METRICS.setdefault(func.__name__, {})
            METRICS[func.__name__][rule_name] = {
                "rule": rule_expr,
                "action": "drop",
                "note": "count dropped/kept rows (simulated)"
            }

            # 4) 回傳套用規則後的 df
            return df_after
        return wrapper
    return decorator


def table(func):
    def wrapper(*args, **kwargs):
        # 執行時（runtime）做的事（示意清單）：
        # - 讀取/解析這個 dataset 的定義（呼叫原本 func 拿 df）
        # - 自動推斷依賴（看 df 讀了哪些上游表 / LIVE / dlt.read）
        # - 把計算交給 Spark 執行（Streaming / Batch）
        # - 管理 checkpoint / state（若是 streaming）
        # - 控制重試、錯誤處理、寫入 Delta、更新 table metadata
        # - 記錄 lineage、品質指標、執行時間、輸出資料量
        df = func(*args, **kwargs)

        # 這裡示意「把結果寫成 Delta table」
        # df.write.format("delta").mode("append").saveAsTable(f"LIVE.{func.__name__}")
        print(f"[DLT] materialize table: {func.__name__} (simulated)")

        return df

    # 註冊時（definition time）做的事（示意清單）：
    # - 把 func 註冊成 pipeline 裡的一個 table 節點（名稱、schema、註解、properties）
    # - 建立/更新 pipeline DAG 的節點資訊
    # - 讓 orchestration 知道「要產出這張表」
    REGISTRY[func.__name__] = {
        "type": "table",
        "definition": func,
        "note": "registered in pipeline graph (simulated)"
    }

    return wrapper
```

## Lakeflow/DLT 認證考試的核心重點。

---

## 表定義的兩種型態

DLT 中最基本的區分是 **Materialized Table** 和 **View**。`@dlt.table` 會將結果物化成實體 Delta Table，每次 pipeline 執行後資料會持久化保存。`@dlt.view` 則只是中間計算邏輯，不產生實體表，僅供 pipeline 內部其他表引用。

SQL 語法中要注意 `CREATE LIVE TABLE` 是批次處理的物化表，而 `CREATE STREAMING TABLE` 才支援增量串流處理。這個區分經常出現在考題中。

```python
@dlt.table
def silver_orders():
    return dlt.read_stream("bronze_orders")
```

```sql
CREATE OR REFRESH STREAMING TABLE bronze_events
AS SELECT * FROM cloud_files("/data/events", "json");
```

---

## 讀取資料的關鍵差異

Pipeline 內部表的讀取使用 `dlt.read()` 或 `dlt.read_stream()`，前者是批次、後者是串流。SQL 中則用 `LIVE.` 前綴表示 pipeline 內部表，用 `STREAM()` 函數包裝表示串流讀取。

```python
# 批次讀取 pipeline 內的表
dlt.read("bronze_orders")

# 串流讀取 pipeline 內的表
dlt.read_stream("bronze_orders")

# 讀取外部表（Unity Catalog）
spark.table("my_catalog.my_schema.external_table")
```

SQL 的對應寫法是 `SELECT * FROM LIVE.bronze_orders` 以及 `SELECT * FROM STREAM(LIVE.bronze_events)`。考試常考 `LIVE.` 前綴代表什麼意思，答案是「同一個 pipeline 內定義的表」。

---

## 資料品質 Expectations

這是 DLT 最重要的特色功能，考試必考。三種行為模式要背熟：

`@dlt.expect` 只記錄違規但保留資料，用於監控。`@dlt.expect_or_drop` 會丟棄不合格的資料列，Silver 層最常用。`@dlt.expect_or_fail` 會讓整個 pipeline 失敗停止，用於 Gold 層關鍵表。

```python
@dlt.table
@dlt.expect("valid_id", "id IS NOT NULL")
@dlt.expect_or_drop("positive_amount", "amount > 0")
@dlt.expect_or_fail("valid_date", "order_date <= current_date()")
def silver_orders():
    return dlt.read_stream("bronze_orders")
```

SQL 版本使用 `CONSTRAINT` 語法，`ON VIOLATION DROP ROW` 對應 expect_or_drop，`ON VIOLATION FAIL UPDATE` 對應 expect_or_fail。沒有 ON VIOLATION 子句就等同於 expect（只記錄）。

多條規則可以用 `@dlt.expect_all({...})`、`@dlt.expect_all_or_drop({...})` 一次定義多個。

---

## Auto Loader 資料擷取

Auto Loader 是從雲端儲存增量載入資料的標準方式，使用 `cloudFiles` format。

```python
@dlt.table
def bronze_events():
    return (
        spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "json")
            .option("cloudFiles.inferColumnTypes", "true")
            .option("cloudFiles.schemaLocation", "/schema/events")
            .load("/data/landing/events")
    )
```

SQL 使用 `cloud_files()` 函數。必考的選項包括 `cloudFiles.format` 指定來源格式、`cloudFiles.inferColumnTypes` 自動推斷型別、`cloudFiles.schemaLocation` 儲存 schema 演進歷史。沒有設定 schemaLocation 就無法追蹤 schema evolution。

---

## CDC 與 SCD Type 2

處理變更資料擷取（CDC）使用 `apply_changes` 函數。重點是必須先用 `dlt.create_streaming_table()` 建立目標表，然後才能套用變更。

```python
dlt.create_streaming_table("target_customers")

dlt.apply_changes(
    target="target_customers",
    source="cdc_source",
    keys=["customer_id"],
    sequence_by="event_timestamp",
    stored_as_scd_type=2
)
```

`stored_as_scd_type=1` 只保留最新值（直接覆蓋），`stored_as_scd_type=2` 保留完整歷史版本，系統會自動加入 `__START_AT` 和 `__END_AT` 欄位追蹤版本有效期間。

---

## 考試常見陷阱

第一個陷阱是混淆 `LIVE.table_name` 和完整路徑 `catalog.schema.table`，前者是 pipeline 內部表，後者是外部表。

第二個是 `STREAMING TABLE` 和 `LIVE TABLE` 的差異，前者支援增量串流處理，後者是批次物化視圖。

第三個是 Expectation 的預設行為，`@dlt.expect` 只記錄不會丟棄也不會失敗，很多人誤以為會自動丟棄資料。

第四個是 `apply_changes` 必須先建表，直接呼叫會報錯。

---

需要我針對這些內容出幾題模擬題讓你練習嗎？