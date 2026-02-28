---
name: review-mistakes
description: 錯題本管理系統，追蹤答錯的題目、分析錯題模式、生成專屬錯題測驗、標記已精通題目。支援統計分析與弱點識別，幫助系統化複習錯題。
allowed-tools: Read, Write, Bash
---

# Review Mistakes - 錯題本管理技能

> 系統化管理錯題，將弱點轉化為優勢

---

## 🎯 技能目的

此技能用於**管理和複習答錯的題目**，確保：
1. **自動追蹤** - 答錯的題目自動記錄到錯題本
2. **分類整理** - 按主題、陷阱類型、難度分組
3. **智能複習** - 生成專屬錯題測驗
4. **進度追蹤** - 標記已精通的題目，追蹤複習進度

---

## 📥 使用方式

### 基本命令

```bash
# 查看錯題統計
/review-mistakes --show-stats

# 列出所有錯題
/review-mistakes --list

# 按主題查看錯題
/review-mistakes --list --topic Delta-Lake

# 開始錯題複習（所有未精通的題目）
python .github/skills/practice-exam/scripts/interactive_exam.py --review-mode

# 複習特定主題的錯題
python .github/skills/practice-exam/scripts/interactive_exam.py --review-mode --topic Streaming

# 標記題目為已精通
/review-mistakes --mark-mastered Q-023

# 清除已精通的題目
/review-mistakes --clear-mastered

# 匯出錯題本（JSON 格式）
/review-mistakes --export mistakes_backup.json

# 匯入錯題本
/review-mistakes --import mistakes_backup.json
```

### 參數說明

| 參數 | 說明 | 範例 |
|------|------|------|
| `--show-stats` | 顯示錯題統計 | `--show-stats` |
| `--list` | 列出錯題清單 | `--list` |
| `--topic` | 主題篩選 | `--topic Delta-Lake` |
| `--review-mode` | 在 practice-exam 啟用錯題複習 | `interactive_exam.py --review-mode` |
| `--mark-mastered` | 標記為已精通 | `--mark-mastered Q-001` |
| `--clear-mastered` | 清除已精通題目 | `--clear-mastered` |
| `--export` | 匯出錯題本 | `--export file.json` |
| `--import` | 匯入錯題本 | `--import file.json` |

---

## 📤 輸出範例

### 1. 錯題統計 (`--show-stats`)

```markdown
# 📊 您的錯題統計報告

**統計時間:** 2026-01-09 15:30
**總錯題數:** 15 題
**未精通:** 12 題
**已精通:** 3 題

---

## 🔴 最常錯的主題

| 主題 | 錯題數 | 準確率 |
|------|--------|--------|
| Delta-Lake | 6 題 | 40% |
| Streaming | 4 題 | 50% |
| Cluster-Management | 3 題 | 60% |
| MLflow | 2 題 | 75% |

---

## ⚠️ 最常踩的陷阱

| 陷阱類型 | 出現次數 | 說明 |
|---------|---------|------|
| `Unit-Confusion` | 5 次 | 時間單位混淆 |
| `Command-Purpose` | 3 次 | 指令用途錯誤 |
| `Batch-vs-Stream` | 2 次 | 批次與串流混淆 |

---

## 📈 複習進度

**最近一次複習:** 2026-01-08
**複習次數最多的題目:** Q-023 (4 次)
**進步最明顯的主題:** Cluster-Management (60% → 80%)

---

## 💡 建議

1. **優先複習:** Delta-Lake 主題（錯題最多）
2. **注意陷阱:** 特別留意 Unit-Confusion 類型的題目
3. **複習頻率:** 依到期題每日複習（1/3/7/14 天間隔）

使用 `python .github/skills/practice-exam/scripts/interactive_exam.py --review-mode --topic Delta-Lake` 開始專項訓練
```

---

### 2. 錯題清單 (`--list`)

```markdown
# 📝 錯題清單

**未精通題目:** 12 題
**已精通題目:** 3 題

---

## 🔴 未精通 (12 題)

### Delta-Lake (6 題)

| 題目 ID | 錯誤次數 | 下次複習 | 狀態 |
|---------|---------|----------|------|
| Q-023 | 4 次 | Due | 🔴 需加強 |
| Q-031 | 3 次 | 01-09 | 🔴 需加強 |
| Q-042 | 2 次 | 01-10 | 🟡 練習中 |
| Q-015 | 1 次 | 01-12 | 🟢 接近精通 |

[點擊題目 ID 查看詳細解析]

### Streaming (4 題)

...

---

## 🟢 已精通 (3 題)

| 題目 ID | 主題 | 精通日期 |
|---------|------|----------|
| Q-007 | MLflow | 2026-01-05 |
| Q-018 | Delta-Lake | 2026-01-04 |
| Q-025 | Cluster | 2026-01-03 |
```

---

### 3. 錯題複習模式（practice-exam `--review-mode`）

```markdown
# 📝 錯題複習模式

從錯題本載入題目...

**未精通題目:** 12 題
**複習策略:** 優先複習已到期題目，無到期題時回退未精通題

---

## 第 1/12 題  ⚠️ [錯誤 4 次]

**題目 ID:** Q-023
**主題:** Delta-Lake, Data-Retention
**上次答錯:** 2026-01-08

[題目內容...]

請輸入您的答案 (A/B/C/D):
```

答對後提示：
```markdown
✅ **太棒了！連續答對 2 次**

如果再答對 1 次，此題將標記為「已精通」

[按 Enter 繼續...]
```

答錯後提示：
```markdown
❌ **又答錯了！這已經是第 5 次答錯此題**

**建議:**
1. 仔細閱讀完整解析
2. 記住陷阱類型: Unit-Confusion, Number-Trap
3. 使用記憶口訣: "VACUUM 吸塵器，時間論小時；要用天數算，記得乘廿四"

[按 Enter 繼續...]
```

---

## 🔑 核心特色

### 1. 自動記錄
- 在 `practice-exam` 中答錯的題目自動加入錯題本
- 記錄錯誤次數、答題時間、錯誤原因

### 2. 智能分類
- 按主題分組（Delta-Lake, Streaming 等）
- 按陷阱類型分組（Unit-Confusion, Command-Purpose 等）
- 按難度等級分組（L1-Basic, L2-Intermediate, L3-Advanced）

### 3. 進度追蹤
- 追蹤每題的複習次數
- 間隔複習排程（1/3/7/14 天）
- 自動判斷掌握程度（需加強/練習中/接近精通）
- 連續答對 3 次自動標記為「已精通」

### 4. 統計分析
- 最常錯的主題排行
- 最常踩的陷阱類型
- 複習進度趨勢

---

## 📋 資料結構

### 錯題本格式 (`mistakes.json`)

```json
{
  "version": "1.0",
  "last_updated": "2026-01-09T15:30:00",
  "mistakes": [
    {
      "question_id": "Q-023",
      "first_wrong_date": "2026-01-05T10:30:00",
      "attempts": [
        {
          "date": "2026-01-05T10:30:00",
          "user_answer": "A",
          "correct_answer": "B",
          "correct": false
        },
        {
          "date": "2026-01-06T14:20:00",
          "user_answer": "A",
          "correct_answer": "B",
          "correct": false
        },
        {
          "date": "2026-01-08T16:45:00",
          "user_answer": "B",
          "correct_answer": "B",
          "correct": true
        }
      ],
      "wrong_count": 4,
      "correct_count": 1,
      "consecutive_correct": 1,
      "mastered": false,
      "mastered_date": null,
      "review_stage": 1,
      "last_review_date": "2026-01-08T16:45:00",
      "next_review_date": "2026-01-11T16:45:00",
      "topics": ["Delta-Lake", "Data-Retention"],
      "traps": ["Unit-Confusion", "Number-Trap"],
      "level": "L2-Intermediate",
      "notes": ""
    }
  ],
  "statistics": {
    "total_mistakes": 15,
    "mastered": 3,
    "not_mastered": 12,
    "topics": {
      "Delta-Lake": 6,
      "Streaming": 4,
      "Cluster-Management": 3
    },
    "traps": {
      "Unit-Confusion": 5,
      "Command-Purpose": 3
    }
  }
}
```

---

## 🐍 Python 腳本架構

### 主要函式

#### `add_mistake(question_id, user_answer, correct_answer, result_data)`
添加錯題記錄

```python
def add_mistake(question_id, user_answer, correct_answer, result_data):
    """
    添加或更新錯題記錄

    Args:
        question_id: 題目 ID
        user_answer: 使用者答案
        correct_answer: 正確答案
        result_data: 包含 topics, traps, level 等資訊
    """
    mistakes_db = load_mistakes_db()

    # 查找是否已存在
    mistake = find_mistake(mistakes_db, question_id)

    if mistake:
        # 更新現有記錄
        mistake['attempts'].append({
            'date': datetime.now().isoformat(),
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'correct': (user_answer == correct_answer)
        })

        if user_answer == correct_answer:
            mistake['correct_count'] += 1
            mistake['consecutive_correct'] += 1

            # 連續答對 3 次標記為已精通
            if mistake['consecutive_correct'] >= 3:
                mistake['mastered'] = True
                mistake['mastered_date'] = datetime.now().isoformat()
        else:
            mistake['wrong_count'] += 1
            mistake['consecutive_correct'] = 0
    else:
        # 新增記錄
        mistakes_db['mistakes'].append({
            'question_id': question_id,
            'first_wrong_date': datetime.now().isoformat(),
            'attempts': [{
                'date': datetime.now().isoformat(),
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'correct': False
            }],
            'wrong_count': 1,
            'correct_count': 0,
            'consecutive_correct': 0,
            'mastered': False,
            'mastered_date': None,
            'topics': result_data.get('topics', []),
            'traps': result_data.get('traps', []),
            'level': result_data.get('level', ''),
            'notes': ''
        })

    save_mistakes_db(mistakes_db)
```

#### `show_statistics()`
顯示錯題統計

```python
def show_statistics():
    """顯示詳細的錯題統計報告"""
    mistakes_db = load_mistakes_db()

    # 基本統計
    total = len(mistakes_db['mistakes'])
    mastered = sum(1 for m in mistakes_db['mistakes'] if m['mastered'])
    not_mastered = total - mastered

    # 主題統計
    topic_stats = analyze_by_topic(mistakes_db)

    # 陷阱統計
    trap_stats = analyze_by_trap(mistakes_db)

    # 生成報告
    report = generate_statistics_report(
        total, mastered, not_mastered,
        topic_stats, trap_stats
    )

    print(report)
```

#### `list_mistakes(topic=None, include_mastered=False)`
列出錯題清單

```python
def list_mistakes(topic=None, include_mastered=False):
    """
    列出錯題清單

    Args:
        topic: 主題篩選
        include_mastered: 是否包含已精通的題目
    """
    mistakes_db = load_mistakes_db()

    # 篩選
    filtered = mistakes_db['mistakes']

    if not include_mastered:
        filtered = [m for m in filtered if not m['mastered']]

    if topic:
        filtered = [
            m for m in filtered
            if any(topic.lower() in t.lower() for t in m['topics'])
        ]

    # 分組顯示
    grouped = group_by_topic(filtered)

    for topic_name, mistakes in grouped.items():
        print(f"\n### {topic_name} ({len(mistakes)} 題)\n")
        print_mistake_table(mistakes)
```

#### `get_not_mastered_items(topic=None, due_only=False)`
取得未精通題目清單（可只取到期題）

```python
def get_not_mastered_items(topic=None, due_only=False):
    """
    取得未精通題目（可選僅到期）
    """
    db = load_mistakes_db()
    items = []
    for m in db['mistakes']:
        if m.get('mastered', False):
            continue
        if topic and not any(topic.lower() in t.lower() for t in m.get('topics', [])):
            continue
        due = is_due_for_review(m)
        if due_only and not due:
            continue
        items.append({
            'question_id': m['question_id'],
            'question_batch': m.get('question_batch'),
            'due': due,
            'next_review_date': m.get('next_review_date'),
            'wrong_count': m.get('wrong_count', 0),
        })

    # 排序策略：到期優先，其次下次複習時間，最後看錯誤次數
    items.sort(key=lambda x: (0 if x['due'] else 1, x.get('next_review_date') or "", -x['wrong_count']))
    return items
```

#### `mark_as_mastered(question_id)`
標記題目為已精通

```python
def mark_as_mastered(question_id):
    """手動標記題目為已精通"""
    mistakes_db = load_mistakes_db()

    mistake = find_mistake(mistakes_db, question_id)

    if mistake:
        mistake['mastered'] = True
        mistake['mastered_date'] = datetime.now().isoformat()
        save_mistakes_db(mistakes_db)
        print(f"✅ {question_id} 已標記為「已精通」")
    else:
        print(f"⚠️ 找不到題目: {question_id}")
```

---

## 🔗 技能整合

### 與 practice-exam 整合
- `practice-exam` 答錯時自動調用 `add_mistake()`
- 由 `practice-exam --review-mode` 載入錯題（先到期題，再未精通題）

### 與外部分析技能整合
- 目前僅提供錯題資料輸出與統計
- 若未來新增弱點分析技能，可直接復用 `mistakes.json`

---

## 📊 精通判定邏輯

### 自動精通條件
連續答對 **3 次** 即自動標記為已精通

### 狀態等級

| 狀態 | 條件 | 說明 |
|------|------|------|
| 🔴 需加強 | 錯誤次數 ≥ 3 且連續答對 < 2 | 需重點複習 |
| 🟡 練習中 | 錯誤次數 < 3 或連續答對 = 1 | 正在進步中 |
| 🟢 接近精通 | 連續答對 = 2 | 再答對 1 次即精通 |
| ✅ 已精通 | 連續答對 ≥ 3 | 可從複習清單移除 |

---

## ⚙️ 實作優先級

### Phase 1: 核心功能 ✅
- [x] 基本錯題記錄
- [x] 查看錯題統計
- [x] 列出錯題清單
- [x] 錯題複習模式

### Phase 2: 進階功能
- [x] 自動精通判定
- [x] 匯入/匯出功能
- [ ] 複習提醒
- [ ] 進度趨勢圖表

### Phase 3: 優化
- [ ] 智能排序（根據遺忘曲線）
- [ ] 筆記功能
- [ ] 標籤管理
- [ ] 團隊共享

---

## 🔍 品質檢查清單

使用此技能前，請確認：
- [ ] 使用者資料目錄已建立 (`.claude-exam-helper/user_data/`)
- [ ] 錯題本檔案格式正確 (`mistakes.json`)
- [ ] 與 `practice-exam` 正確整合
- [ ] 備份機制完善（建議定期匯出）

---

## 🐛 疑難排解

### 問題 1: 錯題本檔案損壞
**解決方案:**
使用 `--import` 匯入之前的備份檔案

### 問題 2: 統計數據不正確
**解決方案:**
檢查 `mistakes.json` 格式，必要時重建統計資料

### 問題 3: 無法載入錯題
**解決方案:**
確認題目 ID 正確，且題目檔案仍存在於題庫中

---

## 📚 相關資源

- [practice-exam](../practice-exam/SKILL.md) - 互動式練習考試

---

**透過系統化管理錯題，將每個錯誤轉化為進步的階梯！📚**
