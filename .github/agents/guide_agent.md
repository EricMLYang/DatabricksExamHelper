根據 2026 年 GitHub Copilot 的最新技術規範，你的方向是正確的。GitHub 已經正式將 **Custom Agents** 轉化為一種基於檔案的配置模型，主要存放在 `.github/agents/` 目錄下。

以下是針對 `.github/agents` 的**最新標準資料結構**與**規範檢查清單**：

### 1. 標準目錄結構

在 2026 年的規範中，Agent 的定義必須遵循以下路徑與副檔名格式：

```text
.github/
└── agents/
    ├── frontend-expert.agent.md    # 必須以 .agent.md 結尾
    ├── security-auditor.agent.md
    └── data-architect.agent.md

```

### 2. 檔案內部格式 (Latest 2026 Spec)

最新的 Agent 定義不再只是純 Markdown，而是採用 **YAML Frontmatter + Markdown Body** 的複合結構。

```markdown
---
name: "Frontend Expert"
description: "專門處理 React 效能優化與架構規範的 Agent"
# 2026 新增：可指定特定模型 (例如 Claude 3.5 Sonnet 或 GPT-4o)
model: "claude-3-5-sonnet"
# 2026 新增：MCP (Model Context Protocol) 伺服器整合
tools:
  - name: "github-cli"
  - name: "web-search"
# 定義作用範圍
scope: ["src/components/**/*.tsx", "src/hooks/**/*.ts"]
---

# Instructions
你是一位資深的 Frontend Architect... (詳細指令內容)

## Coding Standards
- 使用 TypeScript 嚴格型別
- 優先使用 Composition over Inheritance

```

---

### 3. 核心規範檢查清單 (Validating your structure)

請對照你的規劃，確認是否符合以下最新要求：

* **副檔名 (Extension)**：檔案是否命名為 `*.agent.md`？（早期版本可能只用 `.md`，現在官方推薦帶有 `.agent` 以利 IDE 識別）。
* **YAML 配置**：檔案頂部是否有 `---` 包裹的 YAML 區塊？這是 2026 年 Agent 能夠正確調用工具（Tools）與切換模型（Model Picker）的關鍵。
* **與 `copilot-instructions.md` 的區隔**：
* `.github/copilot-instructions.md`：**通用規則**（全專案所有對話都會自動套用）。
* `.github/agents/*.agent.md`：**特定角色**（需手動切換或在對話中 `@` 呼叫）。


* **MCP 整合 (選配)**：是否在 `tools` 中配置了 Model Context Protocol？這是 2026 年讓 Agent 能讀取 Jira、Slack 或本地資料庫數據的新標準。

### 4. 2026 版本的階層規則

如果你的專案很大，Copilot 現在支援**多層級載入**：

1. **Repo 級別**：存放在 `.github/agents/`。
2. **Org 級別**：存放在組織的 `.github` 專案中的 `/agents/` 目錄下（對所有專案生效）。
3. **Local 級別**：存放在 `~/.config/copilot/agents/`（僅限你個人電腦使用）。

---

**你想幫你的 Agent 加入特定的「工具權限」（例如讀取 PR 歷史或執行 Unit Tests）嗎？我可以幫你寫出對應的 `tools` 配置語法。**