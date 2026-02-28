---
name: question-quality-lint
description: 題庫品質檢查技能，使用 lint_questions 檢查題目格式、正解一致性、標籤品質，適合 PR 前自檢與 CI 問題排查。
allowed-tools: Read, Write, Bash, Grep
---

# Question Quality Lint

> 在提交題目前，先用一致規則檢查內容品質。

## 何時使用

- 新增或修改 `question-bank/` 題目後
- PR 被 `Question Quality` workflow 擋下時
- 想確認 `by-order_v1` 舊題與 `b1-b4` 新題的結構差異

## 執行方式

```bash
# 基本檢查（與 CI 一致）
python .github/skills/question-quality-lint/scripts/lint_questions.py

# 嚴格模式：warning 也視為失敗
python .github/skills/question-quality-lint/scripts/lint_questions.py --strict

# 含 by-topic
python .github/skills/question-quality-lint/scripts/lint_questions.py --include-by-topic

# 加上標籤字典檢查
python .github/skills/question-quality-lint/scripts/lint_questions.py --check-tag-schema
```

## 規則來源

- 實作腳本：`.github/skills/question-quality-lint/scripts/lint_questions.py`
- 標籤字典：`.github/skills/tagging-schema/references/tagging-schema.md`

## 注意事項

- `by-order_v1` 視為 legacy 題池，部分結構問題降級為 warning。
- `by-order_b1 ~ by-order_b4` 屬新題池，結構問題預期直接報 error。
