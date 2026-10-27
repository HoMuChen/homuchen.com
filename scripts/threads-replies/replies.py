#!/usr/bin/env python3
"""Threads 留言回覆：抓新留言 → Claude 分類擬稿 → 簡單的自動回、問題推 Telegram 等你確認。

  replies.py poll [--dry-run] [--days N]   處理最近 N 天（預設 7）自己貼文底下的新留言
  replies.py bot                           Telegram long polling：處理「送出／略過」按鈕與修改後的回覆
  replies.py status [--limit N]            列出最近處理過的留言

環境變數（systemd 從 ~/.config/threads-replies.env 讀）：
  TELEGRAM_BOT_TOKEN、TELEGRAM_CHAT_ID   專用 bot，只接受這個 chat 的操作
  THREADS_REPLIES_MODE=auto（預設）       thanks/share 且通過護欄就自動回；review = 全部推 Telegram
  THREADS_REPLIES_AUTO_CAP=10            一天最多自動回幾則
THREADS_ACCESS_TOKEN 每次從 repo .env 讀（post_threads.py 發文時會更新它）。

在 hq VM 以 threads 帳號由 systemd 執行（見同資料夾 systemd/、README.md）。
"""

import argparse
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO / ".agents/skills/post-to-threads/scripts"))
from post_threads import post_one  # noqa: E402

API = "https://graph.threads.net/v1.0"
TPE = timezone(timedelta(hours=8))
STATE = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local/state")) / "threads-replies"
MODE = os.environ.get("THREADS_REPLIES_MODE", "auto")
AUTO_CAP = int(os.environ.get("THREADS_REPLIES_AUTO_CAP", "10"))
TG_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TG_CHAT = os.environ.get("TELEGRAM_CHAT_ID", "")

SKIP = {"promo", "bot", "spam", "emoji", "media"}  # 不回、不通知，只記錄
AUTO = {"thanks", "share"}                          # 可以自動回的類型（還要過護欄）
MAX_REPLY = 150
MAX_ATTEMPTS = 3


def log(msg: str) -> None:
    print(f"[{datetime.now(TPE):%F %T}] {msg}", flush=True)


# ── 狀態（SQLite，poll 與 bot 兩個程式共用）────────────────────
def db() -> sqlite3.Connection:
    STATE.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(STATE / "replies.db", timeout=30, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS comments (
      id TEXT PRIMARY KEY, root_id TEXT, root_text TEXT, root_permalink TEXT, source_post TEXT,
      parent_text TEXT, username TEXT, text TEXT, permalink TEXT, ts TEXT,
      -- new → skipped / pending / auto_sent / answered_elsewhere；pending → sending → sent / dismissed / error
      status TEXT, category TEXT, draft TEXT, note TEXT, attempts INTEGER DEFAULT 0,
      reply_text TEXT, reply_id TEXT, tg_message_id INTEGER, error TEXT,
      created_at TEXT DEFAULT (datetime('now')), updated_at TEXT DEFAULT (datetime('now')));
    CREATE INDEX IF NOT EXISTS comments_tg ON comments (tg_message_id);
    CREATE TABLE IF NOT EXISTS kv (k TEXT PRIMARY KEY, v TEXT);
    """)
    return conn


def update(conn, cid: str, **fields) -> None:
    sets = ", ".join(f"{k} = ?" for k in fields)
    conn.execute(f"UPDATE comments SET {sets}, updated_at = datetime('now') WHERE id = ?",
                 (*fields.values(), cid))


def claim(conn, cid: str, frm: tuple[str, ...]) -> bool:
    """把留言從 frm 狀態改成 sending；只有一個程式搶得到，避免重複回覆。"""
    q = ",".join("?" * len(frm))
    cur = conn.execute(f"UPDATE comments SET status = 'sending', updated_at = datetime('now') "
                       f"WHERE id = ? AND status IN ({q})", (cid, *frm))
    return cur.rowcount == 1


# ── Threads API ──────────────────────────────────────────────
def threads_token() -> str:
    for line in (REPO / ".env").read_text().splitlines():
        if line.startswith("THREADS_ACCESS_TOKEN="):
            return line.split("=", 1)[1].strip()
    sys.exit("THREADS_ACCESS_TOKEN not found in .env")


def api_get(path: str, **params) -> dict:
    r = requests.get(f"{API}/{path}", params={**params, "access_token": threads_token()}, timeout=30)
    r.raise_for_status()
    return r.json()


def api_list(path: str, limit_pages: int = 5, **params) -> list[dict]:
    out, data = [], api_get(path, **params)
    for _ in range(limit_pages):
        out += data.get("data", [])
        nxt = data.get("paging", {}).get("next")
        if not nxt:
            break
        r = requests.get(nxt, timeout=30)
        r.raise_for_status()
        data = r.json()
    return out


def me() -> dict:
    return api_get("me", fields="id,username")


def conversation(root_id: str) -> list[dict]:
    return api_list(f"{root_id}/conversation",
                    fields="id,text,username,timestamp,permalink,replied_to,hide_status")


def my_replies_to(conv: list[dict], username: str) -> set[str]:
    return {c["replied_to"]["id"] for c in conv
            if c.get("username") == username and c.get("replied_to")}


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


def send_threads_reply(conn, c: sqlite3.Row, text: str, done_status: str) -> bool:
    """呼叫前要先 claim()。回覆前再確認一次穆穆沒有自己在 app 裡回過。"""
    try:
        if c["id"] in my_replies_to(conversation(c["root_id"]), me()["username"]):
            update(conn, c["id"], status="answered_elsewhere")
            return False
        user = me()
        reply_id = post_one(user["id"], threads_token(), text, reply_to_id=c["id"])
        update(conn, c["id"], status=done_status, reply_text=text, reply_id=reply_id, error=None)
        log(f"{done_status} {c['id']} @{c['username']}: {text[:60]}")
        return True
    except Exception as e:
        detail = getattr(getattr(e, "response", None), "text", "") or str(e)
        update(conn, c["id"], status="error", error=detail[:500])
        log(f"reply FAILED {c['id']}: {detail[:200]}")
        tg_send(f"⚠️ 回覆 @{c['username']} 失敗：{detail[:200]}")
        return False


# ── Telegram ─────────────────────────────────────────────────
def tg(method: str, **payload) -> dict:
    if not (TG_TOKEN and TG_CHAT):
        return {}
    try:
        r = requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/{method}", json=payload, timeout=70)
        data = r.json()
        if not data.get("ok"):
            # URL 帶 bot token，只記 Telegram 的回應
            log(f"telegram {method}: {str(data)[:200]}")
        return data
    except Exception as e:
        log(f"telegram {method} failed: {e}")
        return {}


def quiet_hours() -> bool:
    return not 8 <= datetime.now(TPE).hour < 23


def tg_send(text: str, silent: bool = False, buttons: list | None = None) -> int | None:
    payload = {"chat_id": TG_CHAT, "text": text[:4000], "disable_notification": silent or quiet_hours(),
               "link_preview_options": {"is_disabled": True}}
    if buttons:
        payload["reply_markup"] = {"inline_keyboard": [buttons]}
    return (tg("sendMessage", **payload).get("result") or {}).get("message_id")


def short(s: str | None, n: int) -> str:
    s = (s or "").replace("\n", " ").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def review_message(c: sqlite3.Row) -> str:
    lines = [f"💬 @{c['username']} 在「{short(c['root_text'], 30)}」留言：", c["text"] or "", ""]
    if c["parent_text"]:
        lines[1:1] = [f"（回覆你的：{short(c['parent_text'], 40)}）"]
    lines += ["✍️ 擬好的回覆：", c["draft"] or "（需要你本人回答）"]
    if c["note"]:
        lines += ["", f"📝 {c['note']}"]
    lines += ["", f"🔗 {c['permalink'] or c['root_permalink'] or ''}", "要改內容：直接回覆這則訊息，打你要送出的版本"]
    return "\n".join(lines)


# ── poll ─────────────────────────────────────────────────────
def collect(conn, days: int) -> list[dict]:
    """找出還沒處理過、直接回覆穆穆（主貼文或他的回覆）的留言。"""
    user = me()
    since = int(time.time()) - days * 86400
    roots = [p for p in api_list("me/threads", fields="id,text,timestamp,permalink,is_reply", since=since)
             if not p.get("is_reply")]
    sources = source_posts()
    seen = {r[0] for r in conn.execute("SELECT id FROM comments")}
    found = []
    for p in roots:
        conv = conversation(p["id"])
        mine = {p["id"]} | {c["id"] for c in conv if c.get("username") == user["username"]}
        texts = {p["id"]: p.get("text") or ""} | {c["id"]: c.get("text") or "" for c in conv}
        answered = my_replies_to(conv, user["username"])
        code = (p.get("permalink") or "").rstrip("/").rsplit("/", 1)[-1]
        for c in conv:
            parent = (c.get("replied_to") or {}).get("id")
            if c.get("username") == user["username"] or parent not in mine or c["id"] in seen:
                continue
            if c.get("hide_status") not in (None, "NOT_HUSHED", "UNHUSHED"):
                continue
            found.append({
                "id": c["id"], "root_id": p["id"], "root_text": p.get("text") or "",
                "root_permalink": p.get("permalink"), "source_post": sources.get(code),
                "parent_text": texts.get(parent) if parent != p["id"] else None,
                "username": c.get("username"), "text": c.get("text") or "",
                "permalink": c.get("permalink"), "ts": c.get("timestamp"),
                "status": "answered_elsewhere" if c["id"] in answered else "new",
            })
    return found


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
    items = collect(conn, days)
    if not dry_run:
        for i in items:
            cols = list(i)
            conn.execute(f"INSERT OR IGNORE INTO comments ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
                         [i[k] for k in cols])
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
        if action == "skip":
            update(conn, i["id"], status="skipped")
            log(f"skipped {cat} @{i['username']}: {short(i['text'], 40)}")
        elif action == "auto":
            update(conn, i["id"], status="pending")
            if claim(conn, i["id"], ("pending",)):
                row = conn.execute("SELECT * FROM comments WHERE id = ?", (i["id"],)).fetchone()
                if send_threads_reply(conn, row, reply, "auto_sent"):
                    tg_send(f"🤖 已自動回覆 @{i['username']}\n留言：{short(i['text'], 120)}\n回覆：{reply}\n🔗 {i['permalink'] or ''}",
                            silent=True)
        else:
            update(conn, i["id"], status="pending")
            row = conn.execute("SELECT * FROM comments WHERE id = ?", (i["id"],)).fetchone()
            buttons = [{"text": "🙈 略過", "callback_data": f"skip:{i['id']}"}]
            if reply:
                buttons.insert(0, {"text": "✅ 送出", "callback_data": f"send:{i['id']}"})
            mid = tg_send(review_message(row), buttons=buttons)
            update(conn, i["id"], tg_message_id=mid)
            log(f"review {cat} @{i['username']} → telegram {mid}")


# ── bot ──────────────────────────────────────────────────────
def finish_message(c: sqlite3.Row, mark: str) -> None:
    if c["tg_message_id"]:
        tg("editMessageReplyMarkup", chat_id=TG_CHAT, message_id=c["tg_message_id"],
           reply_markup={"inline_keyboard": []})
        tg("sendMessage", chat_id=TG_CHAT, text=mark, reply_parameters={"message_id": c["tg_message_id"]},
           disable_notification=True)


def handle_callback(conn, cq: dict) -> None:
    chat = str(((cq.get("message") or {}).get("chat") or {}).get("id"))
    action, _, cid = (cq.get("data") or "").partition(":")
    # Telegram 只給幾秒回應按鈕，發 Threads 要十幾秒，所以先回應，結果另外發訊息
    tg("answerCallbackQuery", callback_query_id=cq["id"], text="送出中…" if action == "send" else "")
    if chat != TG_CHAT:
        return
    c = conn.execute("SELECT * FROM comments WHERE id = ?", (cid,)).fetchone()
    if c and action == "skip" and conn.execute(
            "UPDATE comments SET status = 'dismissed', updated_at = datetime('now') "
            "WHERE id = ? AND status = 'pending'", (cid,)).rowcount:
        finish_message(c, "🙈 略過")
    elif c and action == "send" and c["draft"] and claim(conn, cid, ("pending",)):
        ok = send_threads_reply(conn, c, c["draft"], "sent")
        finish_message(c, "✅ 已送出" if ok else "⚠️ 沒有送出（可能你已經在 app 回過，或發送失敗）")
    elif c:
        tg("sendMessage", chat_id=TG_CHAT, text=f"這則留言已經處理過了（{c['status']}）",
           reply_parameters={"message_id": cq["message"]["message_id"]})


def handle_message(conn, msg: dict) -> None:
    if str(msg.get("chat", {}).get("id")) != TG_CHAT:
        return
    parent = (msg.get("reply_to_message") or {}).get("message_id")
    text = (msg.get("text") or "").strip()
    c = conn.execute("SELECT * FROM comments WHERE tg_message_id = ?", (parent,)).fetchone() if parent else None
    if not (c and text):
        tg("sendMessage", chat_id=TG_CHAT, text="要改回覆內容：在留言通知那則訊息上按「回覆」，打你要送出的版本。")
        return
    if claim(conn, c["id"], ("pending",)):
        ok = send_threads_reply(conn, c, text, "sent")
        finish_message(c, "✅ 已用你的版本送出" if ok else "⚠️ 沒有送出（可能你已經在 app 回過，或發送失敗）")
    else:
        tg("sendMessage", chat_id=TG_CHAT, text=f"這則留言已經處理過了（{c['status']}）",
           reply_parameters={"message_id": msg["message_id"]})


def bot() -> None:
    if not (TG_TOKEN and TG_CHAT):
        sys.exit("TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID not set")
    conn = db()
    row = conn.execute("SELECT v FROM kv WHERE k = 'tg_offset'").fetchone()
    offset = int(row[0]) if row else 0
    log("telegram bot started")
    while True:
        data = tg("getUpdates", offset=offset, timeout=50, allowed_updates=["callback_query", "message"])
        if not data.get("ok"):
            time.sleep(10)
            continue
        for u in data["result"]:
            offset = u["update_id"] + 1
            conn.execute("INSERT OR REPLACE INTO kv (k, v) VALUES ('tg_offset', ?)", (str(offset),))
            try:
                if "callback_query" in u:
                    handle_callback(conn, u["callback_query"])
                elif "message" in u:
                    handle_message(conn, u["message"])
            except Exception as e:
                log(f"update {u['update_id']} failed: {e}")


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
    sub.add_parser("bot")
    s = sub.add_parser("status")
    s.add_argument("--limit", type=int, default=30)
    args = ap.parse_args()
    if args.cmd == "poll":
        poll(args.days, args.dry_run)
    elif args.cmd == "bot":
        bot()
    else:
        status(args.limit)


if __name__ == "__main__":
    main()
