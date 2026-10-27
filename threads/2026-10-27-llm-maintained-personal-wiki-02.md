---
date: 2026-10-27
type: single
source: repurposed
source_post: /posts/llm-maintained-personal-wiki/
idea: LLM 維護知識庫的三層架構 raw/ + wiki/ + CLAUDE.md，關鍵是 CLAUDE.md 的規則
topic: claude code
tags: [Claude Code, 知識管理, CLAUDE.md]
status: draft
threads_url:
---

讓 LLM 幫我維護個人知識庫，整個架構只有三層：

📥 raw/：我只管丟素材，不改、不刪、不整理
📚 wiki/：LLM 整理出來的知識庫，一個概念一頁，有 TL;DR 和交叉連結
📏 CLAUDE.md：規範 LLM 怎麼整理

最關鍵的是第三個。光說「去整理」不夠，要給它規則，例如：
・同一個概念在三個以上地方出現，才獨立成一頁
・兩個來源有矛盾，都保留，標 [CONFLICT]

這次知識庫第一次活過了三個月，wiki 快 60 個概念頁。

---

CLAUDE.md 的規範範例和整套做法：
👉 https://homuchen.com/posts/llm-maintained-personal-wiki/
