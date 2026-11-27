---
date: 2026-11-27
type: single
source: repurposed
source_post: /posts/agent-instruction-claude-md/
idea: CLAUDE.md vs AGENTS.md 怎麼選，加上全域與專案兩層指令怎麼分
topic: claude code
tags: [Claude Code, CLAUDE.md, AGENTS.md]
status: draft
threads_url:
---

CLAUDE.md 跟 AGENTS.md，到底要寫哪個？

簡單記：
・CLAUDE.md：Claude Code 的約定，每次啟動自動讀進去
・AGENTS.md：跨工具的開放標準，Codex、Cursor、Copilot 都能讀，官方說明已有六萬多個專案採用

只用 Claude Code → 寫 CLAUDE.md 就好
會在多個工具間切換 → 主力寫 AGENTS.md，再讓 CLAUDE.md 一行 import 過去，一份指令兩邊共用

另外還有兩層要分清楚：
・全域（~/.claude/CLAUDE.md）：「回我中文」這種到哪都適用的偏好
・專案：股票 agent 的盯盤規則，就放它自己的資料夾

通用的習慣放全域，專屬的守則放專案。
全部塞同一個檔，股票 agent 就會被你寫給電商 agent 的規則干擾😂

---

兩者都是純 Markdown，沒有魔法，重點永遠是裡面寫得夠不夠具體～
👉 完整做法：https://homuchen.com/posts/agent-instruction-claude-md/
