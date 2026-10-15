#!/usr/bin/env python3
"""Post a single post or chained thread to Threads via Meta Graph API.

Usage:
    post_threads.py <posts.json> [--ids-out ids.json]
    post_threads.py --refresh-only

    posts.json is a JSON array of strings (or {"posts": [...], "topic_tag": "..."}).
    Each string is one post in the thread. topic_tag applies to the first post.
    A single-element array posts one standalone post. Multi-element arrays post
    a chained thread where post N+1 is a reply to post N.

Requires THREADS_ACCESS_TOKEN in the project root .env file.

Before posting, the long-lived token is refreshed (another 60 days) and the new
value is written back to .env. Refresh failures (e.g. token < 24h old) are
non-fatal: posting continues with the current token.
"""

import json
import os
import sys
import time
from pathlib import Path

import requests


def load_env(project_root: Path) -> None:
    env_path = project_root / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def find_project_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / ".env").exists() or (p / ".git").exists():
            return p
    return start


def refresh_token(project_root: Path, token: str) -> str:
    """Extend the long-lived token and save it to .env; return the token to use."""
    try:
        r = requests.get(
            "https://graph.threads.net/refresh_access_token",
            params={"grant_type": "th_refresh_token", "access_token": token},
            timeout=30,
        )
        r.raise_for_status()
        data = r.json()
        new_token = data["access_token"]
    except Exception as e:
        detail = getattr(getattr(e, "response", None), "text", "") or str(e)
        print(f"Token refresh skipped: {detail[:200]}", file=sys.stderr)
        return token

    env_path = project_root / ".env"
    lines = env_path.read_text().splitlines(keepends=True) if env_path.exists() else []
    for i, line in enumerate(lines):
        if line.split("=", 1)[0].strip() == "THREADS_ACCESS_TOKEN":
            lines[i] = f"THREADS_ACCESS_TOKEN={new_token}\n"
            break
    else:
        lines.append(f"THREADS_ACCESS_TOKEN={new_token}\n")
    tmp = env_path.with_suffix(".env.tmp")
    tmp.write_text("".join(lines))
    os.chmod(tmp, env_path.stat().st_mode if env_path.exists() else 0o600)
    tmp.replace(env_path)
    os.environ["THREADS_ACCESS_TOKEN"] = new_token
    days = int(data.get("expires_in", 0)) // 86400
    print(f"Token refreshed (valid ~{days} days), saved to .env")
    return new_token


def get_user_id(token: str) -> str:
    r = requests.get(
        "https://graph.threads.net/v1.0/me",
        params={"fields": "id,username", "access_token": token},
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    print(f"Account: @{data.get('username')} ({data['id']})")
    return data["id"]


def create_text_container(
    user_id: str, token: str, text: str, reply_to_id: str | None = None,
    topic_tag: str | None = None,
) -> str:
    params = {"media_type": "TEXT", "text": text, "access_token": token}
    if reply_to_id:
        params["reply_to_id"] = reply_to_id
    if topic_tag:
        params["topic_tag"] = topic_tag
    r = requests.post(
        f"https://graph.threads.net/v1.0/{user_id}/threads",
        params=params,
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["id"]


def publish_container(user_id: str, token: str, creation_id: str) -> str:
    r = requests.post(
        f"https://graph.threads.net/v1.0/{user_id}/threads_publish",
        params={"creation_id": creation_id, "access_token": token},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["id"]


def post_one(
    user_id: str, token: str, text: str, reply_to_id: str | None = None,
    topic_tag: str | None = None,
) -> str:
    container_id = create_text_container(user_id, token, text, reply_to_id, topic_tag)
    # Meta recommends waiting before publishing; 5s is enough for TEXT posts.
    time.sleep(5)
    return publish_container(user_id, token, container_id)


def get_permalink(token: str, thread_id: str) -> str | None:
    try:
        r = requests.get(
            f"https://graph.threads.net/v1.0/{thread_id}",
            params={"fields": "permalink", "access_token": token},
            timeout=30,
        )
        r.raise_for_status()
        return r.json().get("permalink")
    except Exception:
        return None


def main() -> int:
    args = sys.argv[1:]
    ids_out = None
    if "--ids-out" in args:
        i = args.index("--ids-out")
        ids_out = Path(args[i + 1])
        del args[i : i + 2]
    if len(args) != 1:
        print(__doc__, file=sys.stderr)
        return 2

    refresh_only = args[0] == "--refresh-only"
    posts: list[str] = []
    topic_tag: str | None = None
    if not refresh_only:
        posts_path = Path(args[0])
        posts = json.loads(posts_path.read_text())
        if isinstance(posts, dict):
            topic_tag = posts.get("topic_tag")
            posts = posts.get("posts")
        if not isinstance(posts, list) or not all(isinstance(p, str) for p in posts):
            print("posts.json must be a JSON array of strings.", file=sys.stderr)
            return 2
        if not posts:
            print("posts.json is empty.", file=sys.stderr)
            return 2

        over = [(i + 1, len(p)) for i, p in enumerate(posts) if len(p) > 500]
        if over:
            print(
                f"Posts exceed 500-char limit: {over}. Split further before posting.",
                file=sys.stderr,
            )
            return 2

    project_root = find_project_root(Path.cwd())
    load_env(project_root)
    token = os.environ.get("THREADS_ACCESS_TOKEN")
    if not token:
        print(
            "Missing THREADS_ACCESS_TOKEN (checked env and project .env).",
            file=sys.stderr,
        )
        return 1

    token = refresh_token(project_root, token)
    if refresh_only:
        return 0

    user_id = get_user_id(token)

    parent_id: str | None = None
    ids: list[str] = []
    for i, text in enumerate(posts, 1):
        print(f"Posting {i}/{len(posts)} ({len(text)} chars)...")
        thread_id = post_one(
            user_id, token, text, reply_to_id=parent_id,
            topic_tag=topic_tag if i == 1 else None,
        )
        print(f"  -> {thread_id}")
        ids.append(thread_id)
        parent_id = thread_id
        if i < len(posts):
            time.sleep(3)

    if ids_out:
        permalink = get_permalink(token, ids[0])
        ids_out.write_text(json.dumps({"ids": ids, "permalink": permalink}))
        print(f"Permalink: {permalink}")

    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
