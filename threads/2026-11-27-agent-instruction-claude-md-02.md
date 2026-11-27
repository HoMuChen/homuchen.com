---
date: 2026-11-27
type: thread
source: repurposed
source_post: /posts/agent-instruction-claude-md/
idea: 一份好 agent instruction 的五塊骨架：角色、能力、邊界、輸出格式、範例；最常漏的是邊界和範例
topic: claude code
tags: [Claude Code, CLAUDE.md, AI Agent]
status: draft
threads_url:
---

寫 CLAUDE.md（或任何 agent 的指令檔），我每次都繞著這 5 塊寫：

1. 角色
2. 能力
3. 邊界
4. 輸出格式
5. 範例

不一定每塊都寫滿，但寫之前在心裡過一遍，你會發現自己漏掉的，通常就是「邊界」跟「範例」👇

---

1️⃣ 角色：你是誰、做事的調性
謹慎還是大膽？寧可漏報還是寧可多報？這會影響它所有的判斷傾向。

2️⃣ 能力：你負責做什麼
講清楚範圍，它才不會東摸西摸，做一堆你沒要的事。

---

3️⃣ 邊界：你絕對不要做什麼
這塊最常被漏掉。「不要做什麼」往往比「要做什麼」更能定義一隻 agent 靠不靠譜。
不要給投資建議、不要洗版、不要刪檔案、不確定就說不確定。

4️⃣ 輸出格式：做完要長什麼樣
條列、表格還是一段話？固定欄位有哪些？決定你每次收到要不要再重讀整理。

---

5️⃣ 範例：給它一個照抄的樣本
這塊 CP 值最高。講十句「要簡潔」，不如直接給它一個你心目中完美的輸出。模型超會模仿範例✅

沒範例，格式天天在飄；沒邊界，它遲早做出你嚇一跳的事。

我那隻台股 agent 的 CLAUDE.md 骨架也貼在文章裡～
👉 完整做法：https://homuchen.com/posts/agent-instruction-claude-md/
