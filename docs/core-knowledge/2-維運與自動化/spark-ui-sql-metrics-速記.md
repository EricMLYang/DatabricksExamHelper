# Spark UI SQL Metrics 速記（Query-level vs Operator-level）

## 一句話
SQL Metrics 是 **operator-level**；Duration/Jobs 是 **query-level**。

---

## 層級結構（考試必記）
```
SQL Tab
- Query List Page: Query ID, Description, Submitted Time, Duration, Succeeded Jobs
- Query Details Page: DAG / Physical Plan / SQL Metrics (per operator)
```

---

## 正解核心
- SQL metrics 會出現在 **Query Details Page 的 Physical Plan**
- **Spill size** 是典型的 operator-level SQL metric

---

## 錯誤選項的共同點
- Succeeded Jobs / Query duration / Execution time 都是 **query-level**
- 顯示在 Query List 或查詢概要區，不是算子旁的 metric

---

## 常見 SQL Metrics（operator-level）
- number of output rows
- data size
- spill size
- time in aggregation
- shuffle records written

---

## 10 秒記憶法
```
Query 看 Duration/Jobs
Details 看 Metrics 在算子
Spill 一出現，記憶體要調
```

---

## 速判模板（Q-035 類型）
- 題目問「SQL metrics」或「operator-level」→ 直接找 **spill size** 這種算子指標
- 題目出現 Duration/Jobs/Submitted Time → 一律是 query-level（非正解）
