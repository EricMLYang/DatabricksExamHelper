# Structured Streaming Trigger 速記

## 一句話
`.trigger(參數名="值")` 是唯一固定格式。

---

## 核心結論
### 唯一正確語法（固定間隔）
```
.trigger(processingTime="2 minutes")
```

---

## 快速對照表
| 需求關鍵字 | 正確語法 | 記憶點 |
|---|---|---|
| 每 N 分鐘/秒 | `.trigger(processingTime="N minutes")` | 定時跑 = processingTime |
| 只跑一次 | `.trigger(once=True)` | once 只有 True |
| 全部可用資料 | `.trigger(availableNow=True)` | availableNow = 一次吃完 |
| 超低延遲連續 | `.trigger(continuous="1 second")` | continuous = 連續 |
| 預設 | 不寫 `.trigger()` | 盡快處理 |

---

## 必背口訣
```
定期跑：processingTime
跑一次：once=True
全處理：availableNow=True
超低延：continuous
格式：.trigger(參數名="值")
```

---

## 秒殺判斷
### 題目說 -> 直接選
| 題目說 | 答案必是 |
|---|---|
| every X minutes/seconds | `trigger(processingTime="X minutes")` |
| once / one-time | `trigger(once=True)` |
| all available data | `trigger(availableNow=True)` |
| low latency / continuous | `trigger(continuous="...")` |

---

## 常見陷阱（看起來合理但錯）
- `trigger("2 minutes")`：缺參數名
- `processingTime("2 minutes")`：不是獨立方法
- `trigger(once="2 minutes")`：once 只接受 True

---

## 記憶技巧
### 三秒反射
看到「每 X 分鐘」只記兩件事：
- `trigger()` 一定要寫
- `processingTime` 一定要當參數名

### 反例記憶法
把錯的背起來更快：
- 不能省參數名
- 不能把參數當方法
- once 不吃時間
