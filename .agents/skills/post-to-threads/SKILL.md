---
name: post-to-threads
description: Publish a single post or chained thread to the user's Threads account via the Meta Graph API. Use when the user says "發到 Threads", "發串文", "post to Threads", "publish this to my Threads", "幫我發佈到 Threads", or otherwise asks to publish prepared content to the Threads social platform (distinct from Meta Threads messaging app, and unrelated to Twitter threads).
---

# Post to Threads

Publishes one or more posts to the user's Threads account (@homuchen.build.ai). Multi-post
inputs are chained as a thread — post N+1 is published as a reply to post N.

## When to use

Invoke when the user asks to publish prepared content to Threads (the Meta social platform).
Do NOT invoke for drafting, editing, or strategizing content — that's upstream work. This
skill handles only the publish step.

Typical triggers:
- 發到 threads / 發佈到 threads / 發串文
- "post this to Threads" / "publish to Threads"

## Prerequisites

- `THREADS_ACCESS_TOKEN` must be present in the project root `.env`. The script auto-loads it.
- Each post must be ≤ 500 characters (Threads platform limit). The script rejects the job if
  any post exceeds this. If the user's draft exceeds 500 chars, split it into a chained
  thread at natural boundaries (section dividers, topic shifts) BEFORE calling the script.

## How to use

1. **Confirm the final content with the user.** Never publish without explicit go-ahead. If
   the content is still being edited, stop and confirm.

2. **Character-check every post.** If any post exceeds 500 chars, propose a split and get
   approval before proceeding. Count including spaces, punctuation, English, numbers,
   dividers — everything.

3. **Write the posts to a temporary JSON file** as a JSON array of strings. One string per
   post. Order matters — index 0 is the root post, the rest become chained replies in order.

   ```json
   ["first post text", "reply 1 text", "reply 2 text"]
   ```

   Write to a temp path like `/tmp/threads_posts_<timestamp>.json`. Do NOT commit this file.

4. **Run the script:**

   ```bash
   python3 .agents/skills/post-to-threads/scripts/post_threads.py /tmp/threads_posts_<timestamp>.json
   ```

   The script prints the account, then a line per post with the returned Thread ID.

5. **Report the result** to the user with the returned post IDs so they can verify on
   threads.net. Mention the account (@homuchen.build.ai) that the content was posted to.

## Content guidelines

Respect existing style conventions from `homuchen-writing-style` and `social-content` skills
when drafting — this skill does not redraft. If content was produced without those skills
and feels off-voice, flag it to the user rather than silently publishing.

## Troubleshooting

- **401/OAuth error**: The access token expired or is invalid. Ask the user to refresh it
  from Meta Developer Portal and update `.env`.
- **"Posts exceed 500-char limit"**: Split the offending post(s) further.
- **Publish fails after container creation**: The Meta API occasionally returns a container
  ID but then 500s on publish. Re-running with the same JSON re-creates fresh containers and
  usually succeeds.
