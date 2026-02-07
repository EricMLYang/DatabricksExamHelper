# PySpark Window Functions 考前速記版

## 核心概念速記

### Window Function 三大組成
```python
Window.partitionBy("col1")      # 分組依據 (類似 GROUP BY)
      .orderBy("col2")           # 排序依據 (決定累積順序)
      .rowsBetween(start, end)   # 框架範圍 (決定計算窗口)
```

---

## 必考語法對照表

### 1) Frame Boundary 邊界設定
| 語法 | 意義 | 使用情境 |
|------|------|---------|
| `Window.unboundedPreceding` | 從分組**最開始**到... | 累積計算(從頭算起) |
| `Window.currentRow` | ...到**當前列** | 累積計算(算到這筆) |
| `Window.unboundedFollowing` | ...到分組**最後面** | 全分組計算 |
| `-1` | 前一筆 | 移動平均/差分 |
| `1` | 後一筆 | 預測性計算 |

---

## 常見組合模式
```python
# 模式 A: 累積計算 (Cumulative) ⭐ 本題考點
.rowsBetween(Window.unboundedPreceding, Window.currentRow)
# 意義: 從分組開始累積到當前筆
# 例: 學生從第一次考試到本次的平均分數

# 模式 B: 全分組計算 (Overall)
.rowsBetween(Window.unboundedPreceding, Window.unboundedFollowing)
# 意義: 計算整個分組的統計值
# 例: 學生所有考試的總平均分數

# 模式 C: 移動窗口 (Sliding Window)
.rowsBetween(-2, 0)
# 意義: 前兩筆 + 當前筆
# 例: 最近三次考試的移動平均

# 模式 D: 前後對稱窗口
.rowsBetween(-1, 1)
# 意義: 前一筆 + 當前 + 後一筆
# 例: 平滑處理
```

---

## 本題解析速記
```python
window_spec = Window.partitionBy("student_id")\
                    .orderBy("exam_date")\
                    .rowsBetween(Window.unboundedPreceding,
                                 Window.currentRow)

df_new = df.withColumn("avg_score", avg("score").over(window_spec))
```

### 執行邏輯
1. `partitionBy` → 每個學生獨立計算
2. `orderBy` → 按時間順序排列考試
3. `rowsBetween` → 每次計算「從第一次到當前」的平均

### 數據示例
```
student_id | exam_date  | score | avg_score (計算範圍)
-----------|------------|-------|---------------------
A          | 2024-01-01 | 80    | 80        (只有第1次)
A          | 2024-02-01 | 90    | 85        (第1+2次)
A          | 2024-03-01 | 70    | 80        (第1+2+3次)
B          | 2024-01-01 | 75    | 75        (B的第1次)
```

---

## 考試陷阱辨識

### 陷阱類型對照
| 選項描述 | 關鍵字辨識 | 對應語法 |
|---------|-----------|---------|
| overall average | 全部平均 | `unboundedPreceding` to `unboundedFollowing` |
| cumulative average from first to current ✓ | 累積平均 | `unboundedPreceding` to `currentRow` |
| each exam (非 each student) | 錯誤分組 | 應該是 `partitionBy("exam_date")` |
| from first student to current student | 錯誤排序軸 | 應該是 `orderBy("student_id")` |

---

## 快速檢查清單
1. 先看 `partitionBy` → 確認分組單位
2. 再看 `orderBy` → 確認累積方向
3. 最後看 `rowsBetween` → 確認計算範圍
4. 關鍵字對照:
- cumulative → 看是否有 `currentRow`
- overall → 看是否有 `unboundedFollowing`
- each [分組欄位] → 檢查 `partitionBy`

---

## 補充: rowsBetween vs rangeBetween
```python
# rowsBetween: 按「實體列數」計算
.rowsBetween(-2, 0)  # 前2列 + 當前列 (共3列)

# rangeBetween: 按「邏輯值範圍」計算
.rangeBetween(-7, 0)  # 當前日期往前推7天內的所有列
```

考試提示: 題目若無特別說明,通常考 `rowsBetween`
