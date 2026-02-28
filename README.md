# Databricks Exam Helper

Databricks Data Engineer Associate 準備用的題庫與筆記整理專案。

## 專案內容

- 題目解析與練習題庫（依版本、依主題）
- 核心觀念速記與考點地圖
- 互動式練習、錯題追蹤、弱點報告工具

## 目錄說明

- `question-bank/`：題目與解析
- `docs/`：考點地圖、核心知識、經驗整理
- `.github/skills/`：Copilot/CLI 技能與互動腳本
- `tests/`：內容處理工具的測試

## 題庫分層策略

- `question-bank/by-order_b1 ~ by-order_b4`：**2025-2026 新題型**（建議主練）
- `question-bank/by-order_v1`：**2024-2025 舊題型**（補觀念與陷阱）
- `question-bank/by-topic`：主題補強與定向複習

## 建議練習流程

1. 先看考點總覽：[docs/exam-map/exam-plan.md](docs/exam-map/exam-plan.md)
2. 每日主練新題池（預設 `by-order_b4`）：
   - `python .github/skills/practice-exam/scripts/interactive_exam.py --count 15 --era new`
3. 用錯題模式清到期題：
   - `python .github/skills/practice-exam/scripts/interactive_exam.py --review-mode`
4. 每週跑一次弱點報告：
   - `python .github/skills/weak-topic-radar/scripts/weak_topic_radar.py --output docs/reports/weak-topic-radar.md`

## 品質檢查

- 題庫結構檢查：`python .github/skills/question-quality-lint/scripts/lint_questions.py`
- 嚴格模式（PR 建議）：`python .github/skills/question-quality-lint/scripts/lint_questions.py --strict`
- CI Workflow：`.github/workflows/question-quality.yml`

## 協作與貢獻

請先閱讀 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 安全與隱私

- 不要提交任何 token、密碼、個人憑證
- 範例帳號請使用 `user@example.com`

## 免責聲明

本專案為個人學習整理，非 Databricks 官方教材或題庫。

## License

本專案採用 [MIT License](LICENSE)。
