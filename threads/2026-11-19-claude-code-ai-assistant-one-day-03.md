---
date: 2026-11-19
type: single
source: repurposed
source_post: /posts/claude-code-ai-assistant-one-day/
idea: LINE Messaging API 沒有讀取歷史訊息的功能，webhook 收到要先存下來，AI 處理之後再做
topic: AI Agent
tags: [AI Agent, LINE, LINE Bot]
status: published
threads_url: https://www.threads.com/@homuchen.build.ai/post/DgHmRixmUFF
published_at: 2026-11-24T17:08:34+08:00
---

用 LINE 官方帳號做 bot 的人，要知道一件事：

LINE 的 Messaging API 沒有「讀取歷史訊息」的功能。
訊息只會用 webhook 推給你一次，服務掛掉的那段時間，訊息就永遠拿不回來了😱

所以我的 AI 助理收到 LINE 通知時，只做三件事：
1. 驗證
2. 存進資料庫
3. 排進工作佇列

然後馬上回應。叫 AI 摘要、抽待辦，都是之後背景慢慢做。

先存下來，再想要怎麼處理。
