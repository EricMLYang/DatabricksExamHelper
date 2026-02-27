# Contributing Guide

感謝你願意一起完善 DatabricksExamHelper。

## 提交前原則

- 保持內容可讀、可驗證、可追溯。
- 優先小步提交，避免一次大型混合變更。
- 不提交任何密鑰、token、個資或內部連結。

## 內容與命名規範

- 題目檔名請使用半形格式：`Q-001.md`。
- 新增題目時請同步補上「答案說明」與「關鍵概念」。
- 範例帳號、email、主機資訊請使用匿名資料（如 `user@example.com`）。
- 新增模板或流程文件時，優先放在 `tooling/` 或 `question-bank/_template/`。

## Pull Request 建議流程

1. 建立分支並完成單一主題變更。
2. 確認沒有敏感資訊。
3. 更新必要文件（README、相關 docs）。
4. 送出 PR，描述變更範圍與影響路徑。

## 基本檢查清單

- `git status` 僅包含預期變更
- `rg -n 'pk_[A-Za-z0-9_]+|AKIA|BEGIN PRIVATE KEY|token|secret' .` 無敏感資訊
- 檔名與目錄結構符合既有規範

## 題庫維護建議

- 優先維護單一來源版本，避免多份內容手動同步造成漂移。
- 如需批次重整，請先在 PR 說明生成規則與比對方式。
