#!/usr/bin/env python3
"""Threads 留言回覆：抓新留言 → Claude 分類擬稿 → 簡單的自動回、問題送 outbox 核准（Telegram）。

  replies.py poll [--dry-run] [--days N]   處理最近 N 天（預設 7）自己貼文底下的新留言
  replies.py status [--limit N]            列出最近處理過的留言

讀留言、發回覆、Telegram 通知與核准都透過 outbox（https://outbox.homuchen.com），這裡不放 Threads token：
  - 自動回的直接 threads_publish（reply_to_id = 留言 id）
  - 要確認的帶 require_approval，outbox 把擬稿推到 Telegram：✅ 送出、🙈 略過、回覆那則通知 = 用你的版本
  - 下一輪 poll 用 GET /sends/:id 把結果記回 SQLite；還在等核准時你已經在 app 回過了，就取消那筆

環境變數（systemd 從 ~/.config/threads-replies.env 讀）：
  OUTBOX_API_KEY                         outbox 金鑰 threads-replies（threads:homuchen.build.ai、telegram:me 都是 auto）
  OUTBOX_URL                             預設 https://outbox.homuchen.com
  THREADS_REPLIES_MODE=auto（預設）       thanks/share 且通過護欄就自動回；review = 全部送去核准
  THREADS_REPLIES_AUTO_CAP=10            一天最多自動回幾則

在 hq VM 以 threads 帳號由 systemd 執行（見同資料夾 systemd/、README.md）。
"""

import argparse
import json
import os
import re
import sqlite3
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUTBOX = os.environ.get("OUTBOX_URL", "https://outbox.homuchen.com").rstrip("/")
TPE = timezone(timedelta(hours=8))
STATE = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local/state")) / "threads-replies"
MODE = os.environ.get("THREADS_REPLIES_MODE", "auto")
AUTO_CAP = int(os.environ.get("THREADS_REPLIES_AUTO_CAP", "10"))
NOTIFY_TO = "telegram:me"

SKIP = {"promo", "bot", "spam", "emoji", "media"}  # 不回、不通知，只記錄
AUTO = {"thanks", "share"}                          # 可以自動回的類型（還要過護欄）
MAX_REPLY = 150
MAX_ATTEMPTS = 3


def log(msg: str) -> None:
    print(f"[{datetime.now(TPE):%F %T}] {msg}", flush=True)


# ── 狀態（SQLite）────────────────────────────────────────────
def db() -> sqlite3.Connection:
    STATE.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(STATE / "replies.db", timeout=30, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS comments (
      id TEXT PRIMARY KEY, root_id TEXT, root_text TEXT, root_permalink TEXT, source_post TEXT,
      parent_text TEXT, username TEXT, text TEXT, permalink TEXT, ts TEXT,
      -- new → skipped / pending / sending / notified / answered_elsewhere
      -- pending（outbox 等核准）、sending（outbox 重試中）→ sent / auto_sent / dismissed / expired / error
      status TEXT, category TEXT, draft TEXT, note TEXT, attempts INTEGER DEFAULT 0,
      reply_text TEXT, reply_id TEXT, tg_message_id INTEGER, error TEXT,
      created_at TEXT DEFAULT (datetime('now')), updated_at TEXT DEFAULT (datetime('now')));
    CREATE INDEX IF NOT EXISTS comments_tg ON comments (tg_message_id);
    CREATE TABLE IF NOT EXISTS kv (k TEXT PRIMARY KEY, v TEXT);
    """)
    # 改用 outbox 之後加的欄位：send_id = outbox 那筆發送；auto = 自動回的
    cols = {r["name"] for r in conn.execute("PRAGMA table_info(comments)")}
    if "send_id" not in cols:
        conn.execute("ALTER TABLE comments ADD COLUMN send_id TEXT")
    if "auto" not in cols:
        conn.execute("ALTER TABLE comments ADD COLUMN auto INTEGER DEFAULT 0")
    return conn


def update(conn, cid: str, **fields) -> None:
    sets = ", ".join(f"{k} = ?" for k in fields)
    conn.execute(f"UPDATE comments SET {sets}, updated_at = datetime('now') WHERE id = ?",
                 (*fields.values(), cid))


# ── outbox ───────────────────────────────────────────────────
def outbox(method: str, path: str, body: dict | None = None, **params) -> dict:
    r = requests.request(method, f"{OUTBOX}/api/v1{path}", json=body, params=params or None,
                         headers={"Authorization": f"Bearer {os.environ['OUTBOX_API_KEY']}"},
                         timeout=120)
    if not r.ok:
        raise RuntimeError(f"outbox {r.status_code}: {r.text[:300]}")
    return r.json()


def my_replies_to(conv: list[dict]) -> set[str]:
    return {c["replied_to_id"] for c in conv if c["is_mine"] and c["replied_to_id"]}


def notify(text: str, key: str | None = None) -> None:
    """推 Telegram（靜音）。通知失敗不影響回覆本身。"""
    body = {"to": NOTIFY_TO, "text": text[:4000], "silent": True}
    if key:
        body["idempotency_key"] = key
    try:
        outbox("POST", "/telegram/send", body)
    except Exception as e:
        log(f"telegram notify failed: {e}")


def source_posts() -> dict[str, str]:
    """Threads 貼文代碼（permalink 最後一段）→ 部落格原文路徑（posts/*.md）。"""
    out = {}
    for f in (REPO / "threads").glob("*.md"):
        head = f.read_text(encoding="utf-8").split("\n---\n", 1)[0]
        url = re.search(r"^threads_url:\s*(\S+)", head, re.M)
        sp = re.search(r"^source_post:\s*/posts/([a-z0-9-]+)/", head, re.M)
        if url and sp:
            hits = list((REPO / "posts").glob(f"*-{sp.group(1)}.md"))
            if hits:
                out[url.group(1).rstrip("/").rsplit("/", 1)[-1]] = str(hits[0].relative_to(REPO))
    return out


def short(s: str | None, n: int) -> str:
    s = (s or "").replace("\n", " ").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def context_lines(c) -> list[str]:
    lines = [f"💬 @{c['username']} 在「{short(c['root_text'], 30)}」留言：", short(c["text"], 400)]
    if c["parent_text"]:
        lines.insert(1, f"（回覆你的：{short(c['parent_text'], 40)}）")
    return lines


def approval_note(c) -> str:
    """給核准人看的說明（outbox 通知裡的 note）；要發的內容就是擬稿本身。"""
    lines = context_lines(c)
    if c["note"]:
        lines += [f"📝 {c['note']}"]
    lines += [f"🔗 {c['permalink'] or c['root_permalink'] or ''}"]
    return "\n".join(lines)[:1000]


# ── 送出 ─────────────────────────────────────────────────────
def publish_reply(conn, c, text: str, review: bool) -> None:
    """回覆留言（outbox threads_publish，reply_to_id = 留言 id）。review = 先送去核准。"""
    body = {"posts": [text], "reply_to_id": c["id"], "idempotency_key": f"threads-replies:{c['id']}"}
    if review:
        body |= {"require_approval": True, "note": approval_note(c)}
    try:
        send = outbox("POST", "/threads/publish", body)
    except Exception as e:
        update(conn, c["id"], status="error", error=str(e)[:500])
        log(f"reply FAILED {c['id']}: {e}")
        notify(f"⚠️ 回覆 @{c['username']} 失敗：{str(e)[:200]}")
        return
    update(conn, c["id"], send_id=send["send_id"], auto=0 if review else 1)
    apply_result(conn, c, send, auto=not review)


def apply_result(conn, c, send: dict, auto: bool) -> None:
    """把 outbox 那筆發送的狀態記回來。"""
    status, part = send["status"], send["parts"][0]
    if status == "sent":
        done = "auto_sent" if auto else "sent"
        update(conn, c["id"], status=done, reply_text=part["text"], reply_id=part.get("id"), error=None)
        log(f"{done} {c['id']} @{c['username']}: {short(part['text'], 60)}")
        if auto:
            notify(f"🤖 已自動回覆 @{c['username']}\n留言：{short(c['text'], 120)}\n回覆：{part['text']}\n"
                   f"🔗 {c['permalink'] or ''}", key=f"threads-replies:auto:{c['id']}")
    elif status == "pending_approval":
        update(conn, c["id"], status="pending")
        log(f"review {c['category']} @{c['username']} → outbox {send['send_id']}")
    elif status in ("queued", "sending", "scheduled"):
        update(conn, c["id"], status="sending")
    elif status in ("rejected", "canceled"):
        update(conn, c["id"], status="dismissed")
        log(f"dismissed {c['id']} @{c['username']}")
    elif status == "expired":
        update(conn, c["id"], status="expired")
        log(f"approval expired {c['id']} @{c['username']}")
    else:  # failed / partial
        err = send.get("error") or part.get("error") or status
        update(conn, c["id"], status="error", error=err[:500])
        log(f"reply FAILED {c['id']}: {err[:200]}")
        if auto:  # 核准過的失敗 outbox 會通知核准人；自動回的要自己說
            notify(f"⚠️ 自動回覆 @{c['username']} 失敗：{err[:200]}")


def request_review(conn, c) -> None:
    """要穆穆確認：有擬稿就送 outbox 核准；沒有擬稿（要本人回答）就只通知。"""
    if c["draft"]:
        publish_reply(conn, c, c["draft"], review=True)
        return
    notify("\n".join([*context_lines(c), "", "✍️ 需要你本人回答，請直接在 Threads 回覆",
                      *([f"📝 {c['note']}"] if c["note"] else []),
                      f"🔗 {c['permalink'] or c['root_permalink'] or ''}"]),
           key=f"threads-replies:ask:{c['id']}")
    update(conn, c["id"], status="notified")
    log(f"notified {c['category']} @{c['username']} (no draft)")


def sync(conn, answered: set[str]) -> None:
    """上一輪送出去還沒有結果的（等核准、重試中）：問 outbox 現在怎樣了。"""
    for c in conn.execute("SELECT * FROM comments WHERE status IN ('pending', 'sending')").fetchall():
        if not c["send_id"]:
            # 改用 outbox 之前、還在等舊 bot 按鈕的：改送 outbox 核准
            if c["status"] == "pending" and c["id"] not in answered:
                request_review(conn, c)
            elif c["id"] in answered:
                update(conn, c["id"], status="answered_elsewhere")
            continue
        try:
            send = outbox("GET", f"/sends/{c['send_id']}")
            if send["status"] == "pending_approval" and c["id"] in answered:
                outbox("POST", f"/sends/{c['send_id']}/cancel")
                update(conn, c["id"], status="answered_elsewhere")
                log(f"answered in the app, canceled {c['send_id']}")
                continue
            if send["status"] != "pending_approval":
                apply_result(conn, c, send, auto=bool(c["auto"]))
        except Exception as e:
            log(f"sync {c['id']} failed: {e}")


# ── poll ─────────────────────────────────────────────────────
def collect(conn, days: int) -> tuple[list[dict], set[str]]:
    """找出還沒處理過、直接回覆穆穆（主貼文或他的回覆）的留言；另外回傳穆穆已經回過的留言 id。"""
    roots = outbox("GET", "/threads/posts", days=days)["posts"]
    sources = source_posts()
    seen = {r[0] for r in conn.execute("SELECT id FROM comments")}
    found, answered = [], set()
    for p in roots:
        conv = outbox("GET", f"/threads/posts/{p['id']}/replies")["replies"]
        mine = {p["id"]} | {c["id"] for c in conv if c["is_mine"]}
        texts = {p["id"]: p["text"]} | {c["id"]: c["text"] for c in conv}
        answered |= my_replies_to(conv)
        code = (p.get("permalink") or "").rstrip("/").rsplit("/", 1)[-1]
        for c in conv:
            parent = c["replied_to_id"]
            if c["is_mine"] or parent not in mine or c["id"] in seen or c["hidden"]:
                continue
            found.append({
                "id": c["id"], "root_id": p["id"], "root_text": p["text"],
                "root_permalink": p.get("permalink"), "source_post": sources.get(code),
                "parent_text": texts.get(parent) if parent != p["id"] else None,
                "username": c["username"], "text": c["text"],
                "permalink": c.get("permalink"), "ts": c["created_at"],
                "status": "answered_elsewhere" if c["id"] in answered else "new",
            })
    return found, answered


def classify(items: list[dict]) -> dict[str, dict]:
    """一次把所有新留言丟給 Claude，回傳 id → {category, reply, auto_ok, note}。"""
    payload = [{
        "id": i["id"], "post_text": i["root_text"], "source_post_file": i["source_post"],
        "replying_to_your_reply": i["parent_text"], "comment_author": i["username"],
        "comment_text": i["text"],
    } for i in items]
    prompt = (HERE / "prompt.md").read_text(encoding="utf-8") + "\n" + json.dumps(payload, ensure_ascii=False, indent=1)
    out = STATE / f"claude-{datetime.now(TPE):%Y%m%dT%H%M%S}.json"
    with open(out, "w") as f:
        subprocess.run(["claude", "-p", prompt, "--allowedTools", "Read", "Glob", "Grep",
                        "--max-turns", "30", "--output-format", "json"],
                       cwd=REPO, stdout=f, stderr=subprocess.STDOUT, timeout=15 * 60)
    d = json.loads(out.read_text())
    log(f"claude: {d.get('subtype')} turns {d.get('num_turns')} est. ${d.get('total_cost_usd') or 0:.2f}")
    text = (d.get("result") or "").strip()
    m = re.search(r"\[.*\]", text, re.S)
    if not m:
        raise ValueError(f"no JSON array in Claude result: {text[:200]}")
    return {r["id"]: r for r in json.loads(m.group(0)) if isinstance(r, dict) and "id" in r}


def auto_block(conn, item: dict, reply: str) -> str | None:
    """自動送出的護欄；回傳擋下的原因，None 表示可以送。"""
    if MODE != "auto":
        return "review 模式"
    if not reply or len(reply) > MAX_REPLY:
        return f"回覆空白或超過 {MAX_REPLY} 字"
    if re.search(r"https?://|www\.|\.com\b", reply, re.I):
        return "回覆有連結"
    if "掰掰" in reply:
        return "回覆有「掰掰」"
    if conn.execute("SELECT 1 FROM comments WHERE root_id = ? AND username = ? AND status = 'auto_sent'",
                    (item["root_id"], item["username"])).fetchone():
        return "這則貼文已經自動回過這個人"
    today = conn.execute("SELECT count(*) FROM comments WHERE status = 'auto_sent' "
                         "AND date(updated_at, '+8 hours') = date('now', '+8 hours')").fetchone()[0]
    if today >= AUTO_CAP:
        return f"今天已自動回 {today} 則（上限 {AUTO_CAP}）"
    return None


def poll(days: int, dry_run: bool) -> None:
    conn = db()
    items, answered = collect(conn, days)
    if not dry_run:
        for i in items:
            cols = list(i)
            conn.execute(f"INSERT OR IGNORE INTO comments ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
                         [i[k] for k in cols])
        sync(conn, answered)
        # 上次沒處理完的（Claude 失敗）一起重試
        items = [dict(r) for r in conn.execute("SELECT * FROM comments WHERE status = 'new'")]
    else:
        items = [i for i in items if i["status"] == "new"]
    log(f"{len(items)} new comment(s)")
    if not items:
        return

    if not dry_run:
        conn.execute(f"UPDATE comments SET attempts = attempts + 1 WHERE id IN ({','.join('?' * len(items))})",
                     [i["id"] for i in items])
    try:
        decisions = classify(items)
    except Exception as e:
        log(f"classify failed: {e}")
        decisions = {}

    for i in items:
        d = decisions.get(i["id"])
        if not d:
            attempts = (i.get("attempts") or 0) + 1
            if dry_run or attempts < MAX_ATTEMPTS:
                log(f"no decision for {i['id']} (attempt {attempts}), retry next run")
                continue
            d = {"category": "other", "reply": "", "auto_ok": False, "note": "Claude 連續處理失敗，請直接看留言"}
        cat = d.get("category") or "other"
        reply = (d.get("reply") or "").strip()
        note = d.get("note") or ""
        if cat in SKIP or (not i["text"].strip() and cat != "question"):
            action = "skip"
        else:
            block = None if (cat in AUTO and d.get("auto_ok")) else "需要確認"
            block = block or auto_block(conn, i, reply)
            action = "auto" if block is None else "review"
            if block and block != "需要確認":
                note = f"{note}（沒有自動送出：{block}）".strip()

        if dry_run:
            print(f"\n[{action}] {cat} @{i['username']}: {short(i['text'], 80)}\n  → {reply}\n  📝 {note}")
            continue
        update(conn, i["id"], category=cat, draft=reply, note=note)
        row = conn.execute("SELECT * FROM comments WHERE id = ?", (i["id"],)).fetchone()
        if action == "skip":
            update(conn, i["id"], status="skipped")
            log(f"skipped {cat} @{i['username']}: {short(i['text'], 40)}")
        elif action == "auto":
            publish_reply(conn, row, reply, review=False)
        else:
            request_review(conn, row)


def status(limit: int) -> None:
    for r in db().execute("SELECT * FROM comments ORDER BY ts DESC LIMIT ?", (limit,)):
        print(f"{(r['ts'] or '')[:16]}  {r['status']:<18} {r['category'] or '-':<9} @{r['username']}: "
              f"{short(r['text'], 50)}" + (f"\n{'':>18}↳ {short(r['reply_text'], 70)}" if r["reply_text"] else ""))


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("poll")
    p.add_argument("--days", type=int, default=7)
    p.add_argument("--dry-run", action="store_true", help="只印出分類與擬稿，不寫狀態、不回覆、不發 Telegram")
    s = sub.add_parser("status")
    s.add_argument("--limit", type=int, default=30)
    args = ap.parse_args()
    if args.cmd == "poll":
        poll(args.days, args.dry_run)
    else:
        status(args.limit)


if __name__ == "__main__":
    main()
