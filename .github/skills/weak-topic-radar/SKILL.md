---
name: weak-topic-radar
description: 弱點雷達報告技能，從練習紀錄與錯題本生成主題弱點、陷阱雷達、到期複習與新舊題池表現分析。
allowed-tools: Read, Write, Bash, Grep
---

# Weak Topic Radar

> 根據你的作答歷史，產生可執行的複習優先順序。

## 何時使用

- 每週回顧學習進度
- 考前確認弱點主題與陷阱類型
- 檢視 `v1`（舊題）與 `b1-b4`（新題）表現差異

## 執行方式

```bash
# 輸出到預設路徑 docs/reports/weak-topic-radar.md
python .github/skills/weak-topic-radar/scripts/weak_topic_radar.py

# 指定輸出路徑
python .github/skills/weak-topic-radar/scripts/weak_topic_radar.py \
  --output docs/reports/weekly-weak-topic-radar.md

# 自訂分析窗口
python .github/skills/weak-topic-radar/scripts/weak_topic_radar.py \
  --lookback-days 14 --min-attempts 5
```

## 輸入資料來源

- `~/.claude-exam-helper/user_data/practice_history.json`
- `~/.claude-exam-helper/user_data/mistakes.json`
- `question-bank/by-order_v1`
- `question-bank/by-order_b1~b4`

## 規則來源

- 實作腳本：`.github/skills/weak-topic-radar/scripts/weak_topic_radar.py`
