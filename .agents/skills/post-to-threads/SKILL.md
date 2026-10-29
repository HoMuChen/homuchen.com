---
name: post-to-threads
description: Publish a single post or chained thread to the user's Threads account through the outbox MCP server. Use when the user says "發到 Threads", "發串文", "post to Threads", "publish this to my Threads", "幫我發佈到 Threads", or otherwise asks to publish prepared content to the Threads social platform (distinct from Meta Threads messaging app, and unrelated to Twitter threads).
---

# Post to Threads

Publishes one or more posts to the user's Threads account (@homuchen.build.ai) through
**outbox** (https://outbox.homuchen.com), the user's own publishing gateway. Multi-post inputs
are chained as a thread — post N+1 is published as a reply to post N. The Threads token lives
only in outbox (which also refreshes it); this repo no longer needs it to publish.

## When to use

Invoke when the user asks to publish prepared content to Threads (the Meta social platform).
Do NOT invoke for drafting, editing, or strategizing content — that's upstream work. This
skill handles only the publish step.

Typical triggers:
- 發到 threads / 發佈到 threads / 發串文
- "post this to Threads" / "publish to Threads"

## Prerequisites

- The `outbox` MCP server must be connected (tools `threads_check`, `threads_publish`,
  `get_send`, …). It is registered in Claude Code user scope. If the tools are missing, tell
  the user and stop — do not fall back to calling the Threads API directly.
- Destination: `threads:homuchen.build.ai` (the org's only Threads account, so `to` can be
  omitted).

## How to use

1. **Confirm the final content with the user.** Never publish without explicit go-ahead. If
   the content is still being edited, stop and confirm. Publishing is public and can't be
   taken back.

2. **Check first with `threads_check`** (same arguments you will publish with: `posts`, and
   `topic_tag` if the file has a `topic`). It reports per-post character counts (500 max),
   links in the main post, duplicates of recent posts and quota. If a post is too long,
   propose a split at natural boundaries and get approval before proceeding.

3. **Publish with `threads_publish`**:
   - `posts`: one string per post, index 0 is the main post.
   - `topic_tag`: from the file's `topic` frontmatter, if any.
   - `idempotency_key`: `homuchen-threads:{file name without .md}` when publishing a file
     from `threads/`, so a retry never posts twice.
   - `note` is optional (shown to the approver if approval is required).

4. **Read the result.** `status: sent` comes back with each part's `id` and `permalink`.
   - `pending_approval`: it was sent to Telegram for approval; tell the user, don't poll.
   - `queued`: a temporary error, outbox retries by itself; check later with `get_send`.
   - `partial` / `failed`: some or none of the posts went out. Report which parts were
     sent; do NOT republish the whole thing. Resuming from the failed part is done on the
     outbox side (`ops send:resume <send_id>`).

5. **Record and report.** For a file in `threads/`, set `status: published` and fill
   `threads_url` with the main post's permalink (see CLAUDE.md). Tell the user the account
   (@homuchen.build.ai) and the permalink.

## Content guidelines

Respect existing style conventions from `homuchen-writing-style` and `threads-writing` skills
when drafting — this skill does not redraft. If content was produced without those skills
and feels off-voice, flag it to the user rather than silently publishing.

## Legacy script

`scripts/post_threads.py` (direct Graph API with the token in `.env`) is only still used by
`scripts/threads-replies/replies.py`, until replies move to outbox too. Don't use it for
publishing.
