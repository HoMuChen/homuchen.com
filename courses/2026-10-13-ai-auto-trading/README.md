---
title: "用 AI 打造自動化交易系統"
date: 2026-10-13
duration: "6-8 小時"
chapters: "7 章 + Bonus"
status: planning
course_url:
tags: [課程, AI, Claude Code, 自動交易, Shioaji]
---

《用 AI 打造自動化交易系統》線上課程規劃文件。用 Claude Code 從資料、策略研究、回測，一路做到會自己下單、而且出錯會自己停下來的交易系統。

## 檔案說明

- `outline.md` — 課程大綱（7 章 + Bonus，每章實作 demo）
- `plan.md` — 定位、受眾、驗證計畫（waitlist）、定價與拆篇方案、銷售頁文案、法規邊界、**waitlist 回饋 / 訪談紀錄（第八節）**

## 核心理念

不是教一個會賺錢的策略，而是教你**讓 AI 幫你做研究、回測、寫下單程式，並且用安全機制把它關在籠子裡**。

## 相關企劃與文章

- 「即將推出」頁：https://homuchen.com/ai-auto-trading-course/ （出現在 `/courses/` 卡片；預設 page 模板、無價格；腳本 `scripts/create_trading_course_waitlist_page.py`）。正式開賣時改套 `custom-course` 模板並換成銷售頁內容。

- 跨平台企劃：`docs/plans/2026-10-06-ai-auto-trading-course-design.md`
- 導流文章（已放 waitlist CTA：LINE 輸入「交易課」）：
  - [/posts/claude-code-finmind-stock-tracking/](https://homuchen.com/posts/claude-code-finmind-stock-tracking/)
  - [/posts/claude-code-stock-agent-monitor-alert/](https://homuchen.com/posts/claude-code-stock-agent-monitor-alert/)
  - AI 自動交易系列 #1–#4、#6（#5 待寫）
- 素材 repo：`fire-auto`（`futures_live.py`、`futures_grid_monitor.py`、`strategies/tsmc_grid_income.md`、`research/`）

## 公開邊界（錄課也適用）

- 不講本金、不講實盤報酬率、不說明實盤參數設定；數字一律用回測研究。
- Shioaji 模擬測試由 agent 自己跑；API 同意書簽署只用文字說明。
- 不推薦個股、不承諾報酬，定位為「工具打造」。
