# Databricks 考試助手 - 技能使用指南

本目錄包含一套完整的 Databricks 認證考試準備技能，幫助您系統化地學習與複習。

---

## 📚 可用技能

### 📖 題目解析類

#### 1. **solve-question** - 題目解析
> 產出符合標準模板的完整題目解析，包含考點識別、正解說明、錯誤選項排除、記憶法與官方文件引用

**使用時機：** 初次接觸題目，需要完整解析時

**使用方式：**
```bash
# 提供題目 ID 和基本資訊
/solve-question Q-023
```

---

#### 2. **explain-why-not** - 錯誤選項深度拆解
> 深度拆解特定錯誤選項的混淆點，三層次分析（表面錯誤、概念對比、陷阱設計）與記憶強化方法

**使用時機：** 答錯題目後，想深入理解為什麼誤選某個選項

**使用方式：**
```bash
# 指定題目和錯誤選項
/explain-why-not Q-023 --wrong-option A
```

---

### 📝 練習與測驗類

#### 3. **practice-exam** ⭐ 新增 - 互動式練習考試
> 逐題顯示、收集答案、即時反饋、深度解析，提供真實考試般的互動體驗

**使用時機：** 日常練習、考前訓練、想要即時反饋

**使用方式：**
```bash
# 基本練習（預設 10 題）
python .github/skills/practice-exam/scripts/interactive_exam.py

# 指定題目數量
python .github/skills/practice-exam/scripts/interactive_exam.py --count 5

# 按主題篩選
python .github/skills/practice-exam/scripts/interactive_exam.py --topic Delta-Lake

# 按難度篩選
python .github/skills/practice-exam/scripts/interactive_exam.py --level L2-Intermediate

# 組合篩選
python .github/skills/practice-exam/scripts/interactive_exam.py \
    --topic Streaming --level L2-Intermediate --count 8
```

**特色功能：**
- ✅ 一次顯示一題，減少干擾
- ✅ 即時反饋（答對/答錯）
- ✅ 答錯時顯示解析提示與來源檔案
- ✅ 生成成績報告與建議
- ✅ 自動記錄到錯題本

---

### 📚 複習與分析類

#### 4. **review-mistakes** ⭐ 新增 - 錯題本管理
> 追蹤答錯的題目、分析錯題模式、生成專屬錯題測驗、標記已精通題目

**使用時機：** 複習錯題、分析弱點、追蹤進步

**使用方式：**
```bash
# 查看錯題統計
python .github/skills/review-mistakes/scripts/mistake_tracker.py --show-stats

# 列出所有錯題
python .github/skills/review-mistakes/scripts/mistake_tracker.py --list

# 按主題查看錯題
python .github/skills/review-mistakes/scripts/mistake_tracker.py --list --topic Delta-Lake

# 標記題目為已精通
python .github/skills/review-mistakes/scripts/mistake_tracker.py --mark-mastered Q-023

# 清除已精通的題目
python .github/skills/review-mistakes/scripts/mistake_tracker.py --clear-mastered

# 匯出錯題本（備份）
python .github/skills/review-mistakes/scripts/mistake_tracker.py --export my_mistakes.json

# 匯入錯題本（還原）
python .github/skills/review-mistakes/scripts/mistake_tracker.py --import my_mistakes.json
```

**特色功能：**
- ✅ 自動記錄答錯的題目
- ✅ 按主題、陷阱類型分組
- ✅ 追蹤複習次數與進度
- ✅ 連續答對 3 次自動標記為已精通
- ✅ 統計分析與建議

---

## 🔄 完整學習流程

### Phase 1: 初次學習
```bash
# 1. 使用 practice-exam 進行互動式練習
python .github/skills/practice-exam/scripts/interactive_exam.py --count 10

# 2. 答錯的題目自動加入錯題本
# 3. 系統會提示查看完整解析檔案
```

### Phase 2: 複習錯題
```bash
# 1. 查看錯題統計，了解弱點
python .github/skills/review-mistakes/scripts/mistake_tracker.py --show-stats

# 2. 列出錯題清單
python .github/skills/review-mistakes/scripts/mistake_tracker.py --list

# 3. 針對特定主題進行專項訓練
python .github/skills/practice-exam/scripts/interactive_exam.py --topic Delta-Lake
```

### Phase 3: 模擬考試
```bash
# 使用互動式模擬考（更真實）
python .github/skills/practice-exam/scripts/interactive_exam.py --count 20 --seed 42
```

---

## 📊 資料儲存位置

### 使用者個人資料
所有個人學習資料儲存在：
```
~/.claude-exam-helper/user_data/
├── practice_history.json    # 練習歷史記錄
└── mistakes.json             # 錯題本資料庫
```

**注意：** 這些檔案已加入 `.gitignore`，不會被提交到 Git

### 備份建議
定期備份您的學習資料：
```bash
# 備份錯題本
python .github/skills/review-mistakes/scripts/mistake_tracker.py \
    --export ~/backups/mistakes_$(date +%Y%m%d).json

# 備份練習歷史
cp ~/.claude-exam-helper/user_data/practice_history.json \
    ~/backups/practice_history_$(date +%Y%m%d).json
```

---

## 🎯 推薦使用順序

### 對於初學者
1. **practice-exam** - 先做互動式練習，快速建立題感
2. **solve-question** - 查看完整解析，理解考點
3. **explain-why-not** - 針對誤選選項深挖陷阱
4. **review-mistakes** - 定期複習錯題

### 對於準備考試者
1. **practice-exam** - 每天進行定量練習（10-20 題）
2. **review-mistakes** - 每 2-3 天複習錯題
3. **practice-exam** - 考前進行完整模擬測驗（20 題以上）
4. **explain-why-not** - 深入理解容易誤選的選項

---

## ⚙️ 系統需求

- Python 3.7+
- 題庫目錄完整（`question-bank/by-order_v1/` 或 `question-bank/by-topic/`）

---

## 🐛 疑難排解

### 問題 1: 找不到題庫目錄
**解決方案：**
確保在專案根目錄執行腳本，或使用絕對路徑

### 問題 2: 無法保存答題記錄
**解決方案：**
檢查 `~/.claude-exam-helper/user_data/` 目錄權限

### 問題 3: 腳本無法執行
**解決方案：**
```bash
# 賦予執行權限
chmod +x .github/skills/practice-exam/scripts/interactive_exam.py
chmod +x .github/skills/review-mistakes/scripts/mistake_tracker.py
```

---

## 📖 更多資訊

- [practice-exam 詳細文件](./practice-exam/SKILL.md)
- [review-mistakes 詳細文件](./review-mistakes/SKILL.md)
- [solve-question 詳細文件](./solve-question/SKILL.md)
- [explain-why-not 詳細文件](./explain-why-not/SKILL.md)

---

## 🚀 未來計劃

### Phase 2: 進階功能（規劃中）
- **spaced-review** - 間隔複習系統（基於艾賓豪斯遺忘曲線）
- **weak-topic-analysis** - 弱點主題分析與專項訓練

---

**祝您考試順利！🎓**
