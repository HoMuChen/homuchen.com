---
date: 2026-11-27
type: single
source: repurposed
source_post: /posts/agent-instruction-claude-md/
idea: instruction 不用一次寫完美：先陽春版開跑、看它出包、每次出包補一條規則；草稿也可以叫 AI 幫你擬
topic: AI Agent
tags: [AI Agent, CLAUDE.md, Agent Instruction]
status: draft
threads_url:
---

別想在腦中把 agent 的規則一次想齊。

我的做法是讓它先跑、讓它出包，再用出包反推漏寫的規則：

它洗版？加一條「漲跌幅 5% 內不通知」。
格式亂？補一個範例。

每條規則背後，都是一次真實的踩坑。這比閉門空想快太多了。

連第一版草稿都不用自己硬擠：直接跟 Claude 說「幫我擬一份盯台股 agent 的 instruction，要有角色、能力、邊界、輸出格式、範例」，再用人話來回微調幾輪就好～

我負責出判斷（要什麼、紅線在哪），AI 負責出草稿和結構😎

你們的 CLAUDE.md 裡，哪一條規則是被 agent 氣到才加的？
