# 深度解析：PySpark Pandas UDF 與 applyInPandas

## ✅ 你的解析正確性確認

你的解析**完全正確**！特別是執行流程圖和 API 對照表非常清晰。我補充實務應用和考試陷阱。

---

## 🎯 實務應用場景補充

### 我們在 SmartSignage 的真實案例

```python
# 場景：計算每個廣告位的 7 天滾動 CTR（點擊率）
# 原始資料：每天的曝光和點擊數

from pyspark.sql.functions import col
import pandas as pd

# 定義輸出 schema
output_schema = StructType([
    StructField("ad_slot_id", StringType()),
    StructField("date", DateType()),
    StructField("impressions", LongType()),
    StructField("clicks", LongType()),
    StructField("rolling_ctr_7d", DoubleType()),
    StructField("rolling_impressions_7d", DoubleType())
])

def calculate_rolling_metrics(pdf: pd.DataFrame) -> pd.DataFrame:
    """
    計算滾動視窗指標
    - 7 天滾動 CTR
    - 7 天滾動總曝光數
    """
    # 確保按日期排序
    pdf = pdf.sort_values("date")
    
    # 計算滾動視窗
    pdf["rolling_impressions_7d"] = pdf["impressions"].rolling(
        window=7, min_periods=1
    ).sum()
    
    pdf["rolling_clicks_7d"] = pdf["clicks"].rolling(
        window=7, min_periods=1
    ).sum()
    
    # 計算 CTR（避免除以零）
    pdf["rolling_ctr_7d"] = (
        pdf["rolling_clicks_7d"] / pdf["rolling_impressions_7d"]
    ).fillna(0)
    
    # 移除中間計算欄位
    pdf = pdf.drop(columns=["rolling_clicks_7d"])
    
    return pdf

# 應用到每個廣告位
result_df = (
    raw_df
    .groupBy("ad_slot_id")
    .applyInPandas(calculate_rolling_metrics, schema=output_schema)
)

# 結果可以直接寫入 Delta Lake
result_df.write.format("delta").mode("overwrite").save("/mnt/analytics/ad_metrics")
```

---

## 🔍 三種 Pandas 整合 API 深度對比

### 1. pandas_udf - 欄位級別操作

```python
from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import DoubleType

# ❌ 錯誤理解：以為可以處理 DataFrame
@pandas_udf(DoubleType())
def calculate_sales(pdf: pd.DataFrame) -> pd.DataFrame:  # ❌ 類型錯誤
    return pdf["sales_amount"].rolling(7).mean()

# ✅ 正確用法：處理 Series
@pandas_udf(DoubleType())
def multiply_by_two(s: pd.Series) -> pd.Series:
    return s * 2

df.select(multiply_by_two(col("value")))

# ✅ Grouped Map UDF（已棄用，被 applyInPandas 取代）
@pandas_udf(schema, PandasUDFType.GROUPED_MAP)  # 舊版 API
def old_style(pdf):
    return pdf
```

**pandas_udf 的侷限：**
- 只能處理單一欄位（Series）
- 無法直接存取同組的其他欄位
- 不適合需要「整組資料」的計算（如滾動視窗）

### 2. applyInPandas - 分組 DataFrame 操作 ⭐

```python
# ✅ 完美適用場景
def calculate_per_store(pdf: pd.DataFrame) -> pd.DataFrame:
    """
    每個 store_id 分組內的複雜計算
    - 可以存取該組的所有欄位
    - 可以新增/刪除欄位
    - 可以改變行數（過濾、擴展）
    """
    pdf = pdf.sort_values("date")
    
    # 滾動視窗
    pdf["ma_7"] = pdf["sales"].rolling(7).mean()
    
    # 移動標準差
    pdf["std_7"] = pdf["sales"].rolling(7).std()
    
    # Z-score（異常檢測）
    pdf["z_score"] = (pdf["sales"] - pdf["ma_7"]) / pdf["std_7"]
    
    # 過濾異常值
    pdf = pdf[abs(pdf["z_score"]) < 3]
    
    return pdf

result = df.groupBy("store_id").applyInPandas(calculate_per_store, schema)
```

**applyInPandas 的優勢：**
- 完整的 Pandas API 可用（rolling, resample, pivot, merge）
- 可以改變 DataFrame 結構
- 自動並行處理各分組
- 保持 Spark 的分散式優勢

### 3. mapInPandas - 全表 DataFrame 操作

```python
# ✅ 適用場景：不需要分組，但需要 Pandas API
def normalize_columns(iterator):
    """
    對整個 DataFrame 做標準化
    注意：iterator 是為了處理大數據，逐批讀取
    """
    for pdf in iterator:
        # 每批次的處理
        pdf["sales_normalized"] = (
            pdf["sales"] - pdf["sales"].mean()
        ) / pdf["sales"].std()
        yield pdf

result = df.mapInPandas(normalize_columns, schema)

# ❌ 常見錯誤：混淆 mapInPandas 和 applyInPandas
df.mapInPandas("store_id", func, schema)  # ❌ mapInPandas 沒有分組參數
df.groupBy("store_id").mapInPandas(func, schema)  # ❌ groupBy 後不能用 mapInPandas
```

---

## 🚨 考試常見陷阱加強

### 陷阱 1: API 名稱相似性混淆

```python
# 這些 API 名稱太像了，考試最愛考！

# ✅ 分組處理
df.groupBy("key").applyInPandas(func, schema)
df.groupBy("key").applyInArrow(func, schema)  # Arrow 格式，更快

# ✅ 全表處理
df.mapInPandas(func, schema)
df.mapInArrow(func, schema)

# ❌ 不存在的組合
df.groupBy("key").mapInPandas(func, schema)  # ❌ 沒有這個 API
df.applyInPandas(func, schema)  # ❌ 必須先 groupBy
```

**記憶口訣：**
- `apply` = 對分組**應用**（需要先 groupBy）
- `map` = 對整表**映射**（不需要 groupBy）
- `InPandas` = 使用 Pandas DataFrame
- `InArrow` = 使用 PyArrow（更快，但 API 較少）

### 陷阱 2: Schema 定義錯誤

```python
# ❌ 錯誤 1：Schema 與實際輸出不符
def bad_func(pdf: pd.DataFrame) -> pd.DataFrame:
    pdf["new_col"] = 1  # 新增欄位
    return pdf

# Schema 沒有包含 new_col → 執行失敗
schema = StructType([
    StructField("store_id", StringType()),
    StructField("sales", DoubleType())
    # 缺少 new_col 定義
])

# ✅ 正確：Schema 必須完整定義所有輸出欄位
schema = StructType([
    StructField("store_id", StringType()),
    StructField("sales", DoubleType()),
    StructField("new_col", IntegerType())  # 加上新欄位
])

# ❌ 錯誤 2：欄位順序不一致
def func(pdf):
    return pdf[["date", "store_id", "sales"]]  # 順序：date, store_id, sales

schema = StructType([
    StructField("store_id", StringType()),  # 順序：store_id, date, sales
    StructField("date", DateType()),
    StructField("sales", DoubleType())
])
# ⚠️ 可能導致資料錯位

# ✅ 正確：確保順序一致
def func(pdf):
    return pdf[["store_id", "date", "sales"]]  # 與 schema 順序相同
```

### 陷阱 3: 忽略排序需求

```python
# ❌ 錯誤：未排序就計算滾動視窗
def bad_rolling(pdf: pd.DataFrame) -> pd.DataFrame:
    # 如果資料未排序，rolling 結果會錯誤
    pdf["ma_7"] = pdf["sales"].rolling(7).mean()
    return pdf

# ✅ 正確：先排序再計算
def good_rolling(pdf: pd.DataFrame) -> pd.DataFrame:
    pdf = pdf.sort_values("date")  # ⭐ 必須先排序
    pdf["ma_7"] = pdf["sales"].rolling(7).mean()
    return pdf

# 💡 實務技巧：在 Spark 層面預先排序
result = (
    df
    .orderBy("store_id", "date")  # Spark 預先排序
    .groupBy("store_id")
    .applyInPandas(good_rolling, schema)
)
```

---

## 📊 VMS 系統實務案例

### 車輛異常行為檢測

```python
# 場景：檢測每輛車的異常駕駛行為
# 需求：計算速度、加速度的滾動統計，標記異常

from scipy import stats

output_schema = StructType([
    StructField("vehicle_id", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("speed", DoubleType()),
    StructField("acceleration", DoubleType()),
    StructField("speed_ma_5min", DoubleType()),
    StructField("speed_std_5min", DoubleType()),
    StructField("is_anomaly", BooleanType())
])

def detect_anomalies(pdf: pd.DataFrame) -> pd.DataFrame:
    """
    對每輛車的時序資料檢測異常
    """
    pdf = pdf.sort_values("timestamp")
    
    # 計算加速度（如果沒有的話）
    pdf["acceleration"] = pdf["speed"].diff() / pdf["timestamp"].diff().dt.total_seconds()
    
    # 5 分鐘滾動視窗（假設每秒一筆資料，300 個點）
    window_size = 300
    pdf["speed_ma_5min"] = pdf["speed"].rolling(window_size, min_periods=10).mean()
    pdf["speed_std_5min"] = pdf["speed"].rolling(window_size, min_periods=10).std()
    
    # Z-score 異常檢測
    pdf["z_score"] = (
        (pdf["speed"] - pdf["speed_ma_5min"]) / 
        pdf["speed_std_5min"].replace(0, 1)  # 避免除以零
    )
    
    # 標記異常（Z-score > 3 或急加速 > 10 m/s²）
    pdf["is_anomaly"] = (
        (abs(pdf["z_score"]) > 3) | 
        (abs(pdf["acceleration"]) > 10)
    )
    
    return pdf[output_schema.fieldNames()]

# 處理所有車輛資料
anomaly_results = (
    vehicle_telemetry_df
    .groupBy("vehicle_id")
    .applyInPandas(detect_anomalies, schema=output_schema)
)

# 只保留異常記錄
alerts = anomaly_results.filter(col("is_anomaly") == True)
```

---

## 🔧 進階技巧與最佳實務

### 技巧 1: 使用 Arrow 加速（Databricks Runtime 優化）

```python
# applyInArrow 比 applyInPandas 快 3-5 倍
# 但 API 略有不同（使用 PyArrow Table）

def calculate_sales_arrow(table: pa.Table) -> pa.Table:
    """
    PyArrow Table 處理
    - 零拷貝轉換
    - 更高效的序列化
    """
    # 轉換為 Pandas（零拷貝）
    pdf = table.to_pandas()
    
    # 計算
    pdf = pdf.sort_values("date")
    pdf["rolling_avg"] = pdf["sales"].rolling(7).mean()
    
    # 轉回 PyArrow
    return pa.Table.from_pandas(pdf)

# 使用 applyInArrow（Databricks 推薦）
result = (
    df
    .groupBy("store_id")
    .applyInArrow(calculate_sales_arrow, schema)
)
```

### 技巧 2: 處理記憶體限制

```python
# ❌ 問題：某些分組資料量過大，單個 partition 記憶體不足
df.groupBy("store_id").applyInPandas(func, schema)  # 可能 OOM

# ✅ 解法 1：增加分區數
df.repartition(200, "store_id").groupBy("store_id").applyInPandas(func, schema)

# ✅ 解法 2：處理前先過濾
df.filter(col("date") >= "2024-01-01").groupBy("store_id").applyInPandas(func, schema)

# ✅ 解法 3：分批處理大組
def chunked_process(pdf: pd.DataFrame) -> pd.DataFrame:
    """逐塊處理避免記憶體爆炸"""
    chunk_size = 10000
    results = []
    
    for i in range(0, len(pdf), chunk_size):
        chunk = pdf.iloc[i:i+chunk_size]
        processed = process_chunk(chunk)  # 你的處理邏輯
        results.append(processed)
    
    return pd.concat(results, ignore_index=True)
```

### 技巧 3: 除錯與測試

```python
# 開發階段：先在小樣本測試
sample_df = df.filter(col("store_id").isin(["S001", "S002"]))

# 收集單組資料測試函數
test_pdf = (
    sample_df
    .filter(col("store_id") == "S001")
    .toPandas()
)

# 直接測試函數
result_pdf = calculate_sales(test_pdf)
print(result_pdf.head())

# 確認無誤後再跑全量
full_result = df.groupBy("store_id").applyInPandas(calculate_sales, schema)
```

---

## 📚 官方文件與延伸閱讀

### 重要文件連結
- [PySpark Pandas UDF](https://spark.apache.org/docs/latest/api/python/user_guide/sql/arrow_pandas.html)
- [Grouped Map](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.GroupedData.applyInPandas.html)

---

## 🎓 考試答題速記卡

### 30 秒判斷法

```
題目關鍵字識別：
├─ "input and output are DataFrame" → applyInPandas 或 mapInPandas
├─ "each group" / "per store" → applyInPandas ✅
├─ "rolling window" / "within group" → applyInPandas ✅
└─ "entire DataFrame" → mapInPandas

排除法：
├─ pandas_udf → 只處理 Series ❌
├─ selectExpr → SQL 表達式，不能用 Python 函數 ❌
└─ mapInPandas("store_id", ...) → 語法錯誤 ❌

答案：B
```

### API 速查表（考試可心算）

| 需求 | API 選擇 | 關鍵特徵 |
|------|---------|---------|
| 單欄位轉換 | `pandas_udf` | 輸入輸出都是 Series |
| 分組 + DataFrame | `applyInPandas` | groupBy + 整組資料 |
| 全表 + DataFrame | `mapInPandas` | 無 groupBy + iterator |
| 分組 + 高效能 | `applyInArrow` | groupBy + PyArrow |

---

## 🎯 總結：必記重點

| 概念 | 關鍵點 | 陷阱預防 |
|------|--------|---------|
| **applyInPandas** | 分組後用 | 必須先 `groupBy()` |
| **mapInPandas** | 全表用 | 不能先 `groupBy()` |
| **Schema** | 必須完整定義 | 包含所有輸出欄位+正確順序 |
| **排序** | rolling 前必須排序 | `sort_values("date")` |
| **記憶體** | 大分組會 OOM | `repartition()` 增加分區 |

### 實務經驗總結

在 AUO 的項目中，我們：
1. **SmartSignage**: 用 `applyInPandas` 計算每個廣告位的滾動 CTR
2. **VMS**: 用 `applyInPandas` 檢測每輛車的異常行為
3. **通用原則**: 
   - 需要 Pandas 複雜操作 → applyInPandas
   - 需要分組內上下文 → applyInPandas
   - 簡單欄位轉換 → pandas_udf 就夠

你的解析已經很完整，加上這些實務案例和陷阱提醒，絕對能拿下這題！💪