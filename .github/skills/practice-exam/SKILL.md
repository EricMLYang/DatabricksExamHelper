---
name: practice-exam
description: 互動式練習考試模式，逐題顯示題目、收集答案、即時反饋，答錯時自動深度解析。支援按主題、難度篩選題目，並記錄答題歷史用於後續分析。適合日常練習與考前訓練。
allowed-tools: Read, Write, Bash, Grep
---

# Practice Exam - 互動式練習考試技能

> 提供真實考試般的互動式答題體驗，即時反饋與深度解析

---

## 🎯 技能目的

此技能用於提供**互動式答題練習**，模擬真實考試體驗，確保：
1. **逐題作答** - 一次顯示一題，避免干擾
2. **即時反饋** - 作答後立即顯示對錯與解析
3. **深度解析** - 答錯時自動調用 `explain-why-not` 深入講解
4. **記錄追蹤** - 保存答題歷史，供後續分析使用

---

## 📥 輸入格式

### 基本使用
```bash
# 預設模式：隨機 10 題
/practice-exam

# 指定題目數量
/practice-exam --count 5

# 按主題篩選
/practice-exam --topic Delta-Lake

# 按難度篩選
/practice-exam --level L2-Intermediate

# 組合篩選
/practice-exam --topic Streaming --level L2-Intermediate --count 8
```

### 參數說明

| 參數 | 說明 | 預設值 | 範例 |
|------|------|--------|------|
| `--count` | 題目數量 | 10 | `--count 5` |
| `--topic` | 主題篩選 | 全部 | `--topic Delta-Lake` |
| `--level` | 難度篩選 | 全部 | `--level L2-Intermediate` |
| `--source` | 題庫來源 | by-order_v1 | `--source by-topic` |
| `--seed` | 隨機種子 | None | `--seed 42` |
| `--review-mode` | 錯題複習模式 | false | `--review-mode` |

---

## 📤 輸出結構

### 答題流程

```markdown
# 📝 Databricks 練習考試

**模式:** 一般練習
**題目數量:** 5 題
**篩選條件:** Delta-Lake, L2-Intermediate

---

## 第 1/5 題

**題目 ID:** Q-01-023

在 Delta Lake 中，您需要永久刪除超過 30 天的舊版本資料以節省儲存空間。
以下哪個指令可以達成此目的？

**A.** VACUUM table_name RETAIN 30 HOURS
**B.** VACUUM table_name RETAIN 720 HOURS
**C.** DELETE FROM table_name WHERE _commit_timestamp < current_date() - 30
**D.** OPTIMIZE table_name ZORDER BY (date_column)

請輸入您的答案 (A/B/C/D):
```

### 即時反饋 - 答對時

```markdown
✅ **正確！**

**正解:** B - VACUUM table_name RETAIN 720 HOURS

**快速提示:**
30 天 = 30 × 24 = 720 小時，VACUUM RETAIN 只接受 HOURS 作為單位。

---

[按 Enter 繼續下一題...]
```

### 即時反饋 - 答錯時

```markdown
❌ **答錯了！**

**您的答案:** A
**正確答案:** B

---

## 🔍 為什麼選項 A 不對？

### 錯誤定性
**錯誤類型:** 參數錯誤 - 時間單位換算錯誤
**陷阱標籤:** `Unit-Confusion`, `Number-Trap`

### 深度拆解

#### 層次 1: 表面錯誤
此選項僅保留 **30 小時**（約 1.25 天）的資料，而題目要求是「刪除超過 **30 天** 的舊版本」。

時間差距：
- 選項 A: 30 小時 = 1.25 天
- 題目需求: 30 天 = 720 小時
- **差距: 24 倍！**

#### 層次 2: 概念對比
VACUUM 指令的 RETAIN 參數**只接受 HOURS 作為單位**，無法直接使用 DAYS。

**正確換算:**
```
30 天 × 24 小時/天 = 720 小時
```

#### 層次 3: 陷阱設計
**出題者意圖:**
測試考生是否會進行單位換算，而非直接套用題目中的數字。

**為什麼容易誤選:**
1. **數字陷阱** - 題目中的「30 天」與選項中的「30」數字相同
2. **視覺捷徑** - 大腦看到相同數字就直接聯想，忽略單位

### 記憶強化
**記憶口訣:** "VACUUM 吸塵器，時間論小時；要用天數算，記得乘廿四"

**快速判斷法:**
看到 VACUUM RETAIN 題目時：
1. 先確認題目的時間單位（天/小時）
2. 若為「天」，立即換算：天數 × 24 = 小時數
3. 選擇對應小時數的選項

---

💡 **已將此題加入錯題本，可使用 `/review-mistakes` 複習**

[按 Enter 繼續下一題...]
```

### 最終成績報告

```markdown
# 📊 練習成績報告

**完成時間:** 2026-01-09 14:30
**總題數:** 5 題
**答對:** 3 題
**答錯:** 2 題
**準確率:** 60%

---

## 詳細結果

| 題號 | 題目 ID | 您的答案 | 正確答案 | 結果 |
|------|---------|----------|----------|------|
| 1 | Q-01-023 | A | B | ❌ |
| 2 | Q-01-007 | A | A | ✅ |
| 3 | Q-01-015 | C | C | ✅ |
| 4 | Q-01-042 | B | D | ❌ |
| 5 | Q-01-031 | B | B | ✅ |

---

## 🎯 建議

### 需加強主題
- **Delta-Lake** (1/2 題正確，50%)
- **Streaming** (0/1 題正確，0%)

### 常踩陷阱
- `Unit-Confusion` - 出現 2 次
- `Batch-vs-Stream` - 出現 1 次

### 下一步行動
1. 使用 `/review-mistakes` 複習錯題
2. 使用 `/weak-topic-analysis` 分析弱點主題
3. 針對 Delta-Lake 主題進行專項訓練

---

**答題記錄已保存至:** `.claude-exam-helper/user_data/practice_history.json`
```

---

## 🔑 核心特色

### 1. 互動式體驗
- 一次顯示一題，減少干擾
- 即時收集答案
- 立即反饋對錯

### 2. 智能解析
- 答對時提供簡短提示
- 答錯時自動深度解析（調用 `explain-why-not` 邏輯）
- 包含記憶口訣與解題技巧

### 3. 進度追蹤
- 顯示當前進度（第 X/N 題）
- 最終生成成績報告
- 保存答題記錄供後續分析

### 4. 靈活篩選
- 支援按主題、難度、來源篩選
- 支援錯題複習模式（與 `review-mistakes` 整合）

---

## 📋 完整使用範例

### 範例 1: 基本練習

**用戶輸入:**
```
/practice-exam --count 3
```

**助手回應:**
```markdown
# 📝 Databricks 練習考試

開始練習，共 3 題

---

## 第 1/3 題

**題目 ID:** Q-01-023

[題目內容...]

請輸入您的答案 (A/B/C/D):
```

**用戶輸入答案:**
```
B
```

**助手回應:**
```markdown
✅ **正確！**

[簡短解析...]

[按 Enter 繼續...]
```

---

### 範例 2: 主題專項訓練

**用戶輸入:**
```
/practice-exam --topic Delta-Lake --count 5
```

**助手回應:**
```markdown
# 📝 Databricks 練習考試 - Delta Lake 專項

開始練習，從 Delta Lake 主題挑選 5 題

---

[開始答題流程...]
```

---

### 範例 3: 錯題複習模式

**用戶輸入:**
```
/practice-exam --review-mode
```

**助手回應:**
```markdown
# 📝 錯題複習模式

從您的錯題本載入題目...

**錯題數量:** 8 題
**篩選條件:** 未精通的題目

---

## 第 1/8 題

**題目 ID:** Q-01-023 ⚠️ [錯誤 2 次]

[題目內容...]
```

---

## 🐍 Python 腳本架構

### 主要函式

#### `start_practice_exam(args)`
啟動互動式練習考試

```python
def start_practice_exam(args):
    """
    啟動互動式練習考試

    Args:
        args: 命令列參數（count, topic, level 等）

    Returns:
        成績報告與答題記錄
    """
    # 1. 根據篩選條件載入題目
    questions = load_questions(args)

    # 2. 初始化答題記錄
    session = {
        'start_time': datetime.now(),
        'questions': [],
        'results': []
    }

    # 3. 逐題作答循環
    for i, question in enumerate(questions):
        display_question(i + 1, len(questions), question)
        user_answer = get_user_input()
        result = check_answer(question, user_answer)

        if result['correct']:
            show_correct_feedback(question)
        else:
            show_incorrect_feedback(question, user_answer)

        session['results'].append(result)

    # 4. 生成成績報告
    report = generate_report(session)

    # 5. 保存答題記錄
    save_practice_history(session)

    return report
```

#### `load_questions(args)`
根據篩選條件載入題目

```python
def load_questions(args):
    """
    根據篩選條件載入題目

    Args:
        args: 包含 count, topic, level, review_mode 等參數

    Returns:
        List[Question]: 符合條件的題目列表
    """
    if args.review_mode:
        # 從錯題本載入
        return load_mistake_questions()

    # 從題庫載入
    all_questions = scan_question_bank(args.source)

    # 應用篩選條件
    filtered = filter_questions(
        all_questions,
        topic=args.topic,
        level=args.level
    )

    # 隨機挑選
    selected = random.sample(filtered, min(args.count, len(filtered)))

    return selected
```

#### `check_answer(question, user_answer)`
檢查答案並生成反饋

```python
def check_answer(question, user_answer):
    """
    檢查答案正確性

    Returns:
        {
            'correct': bool,
            'user_answer': str,
            'correct_answer': str,
            'question_id': str
        }
    """
    correct = (user_answer.upper() == question['correct_answer'].upper())

    return {
        'correct': correct,
        'user_answer': user_answer,
        'correct_answer': question['correct_answer'],
        'question_id': question['id']
    }
```

#### `show_incorrect_feedback(question, user_answer)`
顯示錯誤反饋與深度解析

```python
def show_incorrect_feedback(question, user_answer):
    """
    答錯時顯示深度解析
    調用 explain-why-not 的邏輯
    """
    print(f"❌ **答錯了！**\n")
    print(f"**您的答案:** {user_answer}")
    print(f"**正確答案:** {question['correct_answer']}\n")

    # 調用深度解析邏輯
    analysis = generate_wrong_option_analysis(
        question,
        user_answer
    )

    print(analysis)

    # 提示加入錯題本
    print("\n💡 **已將此題加入錯題本**")

    # 記錄到錯題本
    add_to_mistake_log(question, user_answer)
```

#### `generate_report(session)`
生成成績報告

```python
def generate_report(session):
    """
    生成詳細的成績報告
    包含統計、建議、弱點分析
    """
    results = session['results']
    correct_count = sum(1 for r in results if r['correct'])
    total_count = len(results)
    accuracy = (correct_count / total_count) * 100

    # 分析答錯的主題
    wrong_topics = analyze_wrong_topics(session)

    # 分析常踩的陷阱
    common_traps = analyze_common_traps(session)

    report = {
        'total': total_count,
        'correct': correct_count,
        'accuracy': accuracy,
        'wrong_topics': wrong_topics,
        'common_traps': common_traps,
        'suggestions': generate_suggestions(wrong_topics, common_traps)
    }

    return report
```

#### `save_practice_history(session)`
保存答題記錄

```python
def save_practice_history(session):
    """
    保存答題記錄到本地 JSON 檔案
    供後續分析使用
    """
    history_file = '.claude-exam-helper/user_data/practice_history.json'

    # 讀取現有記錄
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)
    else:
        history = {'sessions': []}

    # 添加新記錄
    history['sessions'].append({
        'timestamp': session['start_time'].isoformat(),
        'results': session['results'],
        'accuracy': calculate_accuracy(session['results'])
    })

    # 寫回檔案
    os.makedirs(os.path.dirname(history_file), exist_ok=True)
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)
```

---

## 🔗 技能整合

### 與 explain-why-not 整合
答錯時自動調用深度解析邏輯，提供三層次拆解

### 與 review-mistakes 整合
- 答錯的題目自動加入錯題本
- 支援 `--review-mode` 從錯題本載入題目

### 與 solve-question 整合
顯示題目時可選擇性顯示完整解析連結

---

## 📊 資料結構

### 答題記錄格式

```json
{
  "sessions": [
    {
      "timestamp": "2026-01-09T14:30:00",
      "mode": "general",
      "filters": {
        "topic": "Delta-Lake",
        "level": "L2-Intermediate"
      },
      "results": [
        {
          "question_id": "Q-01-023",
          "user_answer": "A",
          "correct_answer": "B",
          "correct": false,
          "topics": ["Delta-Lake", "Data-Retention"],
          "traps": ["Unit-Confusion", "Number-Trap"]
        }
      ],
      "accuracy": 0.6,
      "duration_seconds": 600
    }
  ]
}
```

---

## ⚙️ 實作優先級

### Phase 1: 核心功能 ✅
- [x] 基本答題流程
- [x] 即時反饋
- [x] 答錯時深度解析
- [x] 保存答題記錄

### Phase 2: 進階功能
- [ ] 支援多選題
- [ ] 計時功能
- [ ] 答題統計圖表
- [ ] 與 review-mistakes 完整整合

### Phase 3: 優化
- [ ] 自適應難度調整
- [ ] 學習曲線追蹤
- [ ] 匯出 PDF 成績報告

---

## 🔍 品質檢查清單

使用此技能前，請確認：
- [ ] 題庫路徑正確（question-bank/by-order_v1/）
- [ ] Python 3.7+ 環境
- [ ] 使用者資料目錄已建立（.claude-exam-helper/user_data/）
- [ ] 題目檔案格式符合標準模板

---

## 🐛 疑難排解

### 問題 1: 找不到題庫
**解決方案:**
確認執行路徑在專案根目錄，或使用絕對路徑

### 問題 2: 無法保存答題記錄
**解決方案:**
檢查寫入權限，手動建立 `.claude-exam-helper/user_data/` 目錄

### 問題 3: 題目解析失敗
**解決方案:**
檢查題目檔案格式是否符合 question-template.md

---

## 📚 相關資源

- [solve-question](../solve-question/SKILL.md) - 題目解析技能
- [explain-why-not](../explain-why-not/SKILL.md) - 錯誤選項深度拆解
- [review-mistakes](../review-mistakes/SKILL.md) - 錯題本管理
- [question-template.md](../../question-bank/_template/question-template.md) - 題目標準格式

---

**透過互動式練習，將被動閱讀轉化為主動學習！📝**
