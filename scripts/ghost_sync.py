"""把 repo 兩個 commit 之間「已發布文章」的 description / 內文變更，一篇一篇安全地同步到 Ghost。

適用：改舊文（補 description、加內部連結、修錯字）。新文章請用 upload_to_ghost.py。

每篇：
  1. 讀 Ghost 現況並備份
  2. 內文有變更時，用 ghost_patch.py 在 Ghost 現有的 Lexical 上只插入／接上新內容，
     不重送整篇（Ghost 上常有 repo 沒有的內容：圖片說明、刪除線、後台改過的字）。
     找不到唯一對應位置的就跳過不動。
  3. PUT（只送 meta_description 和/或 lexical；title、excerpt、tags 都不送）
  4. 驗證：後台欄位沒被改到、新增的文字緊接在預期位置、圖片與原有連結都在、
     線上頁面 200、meta description 正確、新連結都在
  驗證失敗就停下來，不繼續下一篇。

用法（任何目錄都可以）：
  python3 scripts/ghost_sync.py <base> <head> --dry-run      # 先看會做什麼
  python3 scripts/ghost_sync.py <base> <head> --limit 1      # 先跑一篇，自己看線上結果
  python3 scripts/ghost_sync.py <base> <head>                # 跑剩下的（已成功的會略過）
  python3 scripts/ghost_sync.py <base> <head> --rollback <slug>

備份與紀錄放在 repo 外：~/.cache/homuchen-ghost-sync/<base>..<head>/（可用 GHOST_SYNC_STATE 指定）。
"""
import argparse
import difflib
import html as htmlmod
import json
import os
import re
import subprocess
import sys
import time

import requests
import yaml

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(SCRIPTS)
sys.path.insert(0, SCRIPTS)
STATE = os.path.expanduser(os.environ.get("GHOST_SYNC_STATE", "~/.cache/homuchen-ghost-sync"))
BACKUP_DIR = LOG = None  # 依 <base>..<head> 決定，見 set_run_dir()
KEEP_FIELDS = ["title", "slug", "status", "published_at", "feature_image", "custom_excerpt",
               "visibility", "featured", "canonical_url", "og_title", "og_description",
               "twitter_title", "twitter_description", "meta_title"]


def load_env():
    env = {}
    for line in open(os.path.join(REPO, ".env"), encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip("'\"")
    for k in ("GHOST_URL", "GHOST_ADMIN_API_KEY"):
        os.environ.setdefault(k, env.get(k, ""))
    return env["GHOST_URL"].rstrip("/")


GHOST = load_env()
import upload_to_ghost as U  # noqa: E402  （讀 env 後再 import，沿用發布腳本的轉換）
import ghost_patch as P  # noqa: E402


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True, check=True).stdout


def git_show(rev, path):
    r = subprocess.run(["git", "show", f"{rev}:{path}"], cwd=REPO, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def set_run_dir(base, head):
    global BACKUP_DIR, LOG
    run = os.path.join(STATE, f"{git('rev-parse', '--short', base).strip()}..{git('rev-parse', '--short', head).strip()}")
    BACKUP_DIR = os.path.join(run, "backups")
    LOG = os.path.join(run, "sync-log.jsonl")
    os.makedirs(BACKUP_DIR, exist_ok=True)


def split(md):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", md, re.S)
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def text_of(h):
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", h or "", flags=re.S)
    return P.norm(re.sub(r"<[^>]+>", "", h))


def imgs(h):
    return sorted(re.findall(r'<img[^>]+src="([^"]+)"', h))


def hrefs(h):
    out = []
    for x in re.findall(r'<a[^>]+href="([^"]+)"', h or ""):
        x = htmlmod.unescape(x).replace("https://homuchen.com/", "/")
        out.append(re.sub(r"[?&]ref=homuchen\.com$", "", x))
    return sorted(out)


def headers():
    return {"Authorization": f"Ghost {U.generate_ghost_token()}", "Accept-Version": "v6.0"}


def get_post(slug):
    r = requests.get(f"{GHOST}/ghost/api/admin/posts/slug/{slug}/",
                     params={"formats": "html,lexical", "include": "tags"}, headers=headers(), timeout=30)
    r.raise_for_status()
    return r.json()["posts"][0]


def put_post(post_id, fields):
    r = requests.put(f"{GHOST}/ghost/api/admin/posts/{post_id}/", json={"posts": [fields]},
                     headers={**headers(), "Content-Type": "application/json"}, timeout=60)
    if r.status_code != 200:
        raise RuntimeError(f"PUT {r.status_code}: {r.text[:300]}")
    return r.json()["posts"][0]


def public_page(slug):
    r = requests.get(f"https://homuchen.com/posts/{slug}/", headers={"User-Agent": "Mozilla/5.0"},
                     params={"nocache": str(time.time())}, timeout=30)
    return r.status_code, r.text


def short_diff(a, b, n=3):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    out = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != "equal":
            out.append(f"{op}: ghost「{a[max(0,i1-15):i2+15][:120]}」 vs repo「{b[max(0,j1-15):j2+15][:120]}」")
        if len(out) >= n:
            break
    return out


def changed_files(base, head):
    # 只處理「修改」的檔案：新文章走 upload_to_ghost.py，改名／刪除要人工處理
    out = git("diff", "--name-only", "--diff-filter=M", base, head, "--", "posts/")
    return [p for p in out.split() if p.endswith(".md")]


def plan(base, head, path):
    old_fm, old_body = split(git_show(base, path))
    new_fm, new_body = split(git_show(head, path))
    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", os.path.basename(path)[:-3]).lower()
    return dict(path=path, slug=slug, old_body=old_body, new_body=new_body,
                desc=new_fm.get("description") if new_fm.get("description") != old_fm.get("description") else None,
                body_changed=old_body != new_body)


def verify(p, before, after, new_links):
    errs = []
    for k in KEEP_FIELDS:
        if before.get(k) != after.get(k):
            errs.append(f"{k} 被改了：{before.get(k)!r} → {after.get(k)!r}")
    if [t["name"] for t in before.get("tags", [])] != [t["name"] for t in after.get("tags", [])]:
        errs.append("tags 被改了")
    if p["desc"] and after.get("meta_description") != p["desc"]:
        errs.append(f"meta_description 不是新版：{after.get('meta_description')!r}")
    if not p["desc"] and after.get("meta_description") != before.get("meta_description"):
        errs.append("meta_description 被改了")
    if p["body_changed"]:
        bt, at = text_of(before.get("html")), text_of(after.get("html"))
        exp = bt
        for o, n in p.get("replaced", []):
            if exp.count(o) != 1:
                errs.append(f"預期替換的文字在原文出現 {exp.count(o)} 次")
            exp = exp.replace(o, n, 1)
        rest = at
        for t in p.get("added", []):
            if rest.count(t) < 1:
                errs.append(f"後台內文找不到新增的文字：{t[:40]}")
            rest = rest.replace(t, "", 1)
        if not errs and rest != exp:
            errs.append("內文除了預期的新增/替換之外還有其他變動：" + " | ".join(short_diff(rest, exp)))
        for c in p.get("ctx", []):
            if c not in at:
                errs.append(f"新內容的位置不對（沒有緊接在錨點旁）：{c[:50]}")
        if imgs(after.get("html")) != imgs(before.get("html")):
            errs.append("圖片變了")
        missing = [h for h in set(hrefs(before.get("html"))) if h not in hrefs(after.get("html"))]
        if missing:
            errs.append(f"原有連結不見了：{missing[:3]}")
        for link in new_links:
            if link not in hrefs(after.get("html")):
                errs.append(f"後台內文找不到新連結 {link}")
    elif (after.get("html") or "") != (before.get("html") or ""):
        errs.append("內文被改了（這篇只該改 description）")
    # 線上頁面（Ghost 前台可能有快取，重試幾次）
    for attempt in range(4):
        code, page = public_page(p["slug"])
        m = re.search(r'<meta name="description" content="([^"]*)"', page)
        live_desc = htmlmod.unescape(m.group(1)) if m else None
        live_errs = []
        if code != 200:
            live_errs.append(f"線上 HTTP {code}")
        if p["desc"] and live_desc != p["desc"]:
            live_errs.append(f"線上 meta description 不是新版：{live_desc!r}")
        for link in new_links:
            if link not in hrefs(page):
                live_errs.append(f"線上頁面找不到新連結 {link}")
        if not live_errs:
            break
        time.sleep(5)
    return errs + live_errs


def new_links_of(p):
    if not p["body_changed"]:
        return []
    old = set(re.findall(r"\]\((/posts/[^)\s]+)\)", p["old_body"]))
    return sorted(set(re.findall(r"\]\((/posts/[^)\s]+)\)", p["new_body"])) - old)


def log(rec):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def rollback(slug):
    b = json.load(open(os.path.join(BACKUP_DIR, f"{slug}.json"), encoding="utf-8"))
    cur = get_post(slug)
    fields = {"updated_at": cur["updated_at"], "lexical": b["lexical"], "meta_description": b.get("meta_description")}
    put_post(cur["id"], fields)
    print(f"已還原 {slug}（內文 + meta_description 回到備份）")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base", nargs="?")
    ap.add_argument("head", nargs="?")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--skip", default="")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--rollback")
    a = ap.parse_args()
    if not (a.base and a.head):
        ap.error("需要 <base> <head> 兩個 commit")
    set_run_dir(a.base, a.head)
    print(f"備份與紀錄：{os.path.dirname(LOG)}")
    if a.rollback:
        return rollback(a.rollback)
    plans = [plan(a.base, a.head, f) for f in changed_files(a.base, a.head)]
    other = [p["slug"] for p in plans if not (p["desc"] or p["body_changed"])]
    if other:
        print(f"只改了 description／內文以外的欄位（title、image、tags…不在同步範圍，需要的話到後台改）：{', '.join(other)}")
    plans = [p for p in plans if p["desc"] or p["body_changed"]]
    if a.only:
        plans = [p for p in plans if p["slug"] in a.only.split(",")]
    skip = set(filter(None, a.skip.split(",")))
    done_slugs = set()
    if os.path.exists(LOG):
        done_slugs = {json.loads(l)["slug"] for l in open(LOG, encoding="utf-8") if json.loads(l).get("ok")}
    plans = [p for p in plans if p["slug"] not in skip and p["slug"] not in done_slugs]
    # 只改 description 的先跑（風險低），再跑有改內文的
    plans.sort(key=lambda p: (p["body_changed"], p["slug"]))
    if a.limit:
        plans = plans[:a.limit]
    print(f"待處理 {len(plans)} 篇（已完成 {len(done_slugs)} 篇略過）")

    drifted = []
    for i, p in enumerate(plans, 1):
        kind = ("內文+desc" if p["desc"] else "內文") if p["body_changed"] else "desc"
        ghost = get_post(p["slug"])
        if p["body_changed"]:
            try:
                new_lex, ops, added, replaced, ctx = P.patch(ghost["lexical"], p["old_body"], p["new_body"])
                p.update(lexical=new_lex, ops=ops, added=added, replaced=replaced, ctx=ctx)
            except P.PatchError as e:
                drifted.append((p["slug"], [str(e)]))
                print(f"[{i}/{len(plans)}] ⏭  {p['slug']}（{kind}）無法安全 patch，跳過：{e}")
                continue
        if a.dry_run:
            print(f"[{i}/{len(plans)}] ✔ 可以更新 {p['slug']}（{kind}）")
            for op in p.get("ops", []):
                print("      ·", op)
            continue
        json.dump(ghost, open(os.path.join(BACKUP_DIR, f"{p['slug']}.json"), "w", encoding="utf-8"),
                  ensure_ascii=False)
        fields = {"updated_at": ghost["updated_at"]}
        if p["desc"]:
            fields["meta_description"] = p["desc"]
        if p["body_changed"]:
            fields["lexical"] = p["lexical"]
        put_post(ghost["id"], fields)
        after = get_post(p["slug"])
        errs = verify(p, ghost, after, new_links_of(p))
        log({"slug": p["slug"], "kind": kind, "ok": not errs, "errors": errs, "at": time.strftime("%F %T")})
        if errs:
            print(f"[{i}/{len(plans)}] ✖ {p['slug']}（{kind}）驗證失敗，停止：")
            for e in errs:
                print("      -", e)
            print(f"   還原：python3 {os.path.abspath(__file__)} {a.base} {a.head} --rollback {p['slug']}")
            sys.exit(1)
        print(f"[{i}/{len(plans)}] ✅ {p['slug']}（{kind}）已更新並驗證"
              + (f"，新連結 {len(new_links_of(p))} 個" if p["body_changed"] else ""))
    if drifted:
        print(f"\n跳過 {len(drifted)} 篇（無法安全 patch）：{', '.join(s for s, _ in drifted)}")


if __name__ == "__main__":
    main()
