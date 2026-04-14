#!/usr/bin/env python3
"""Post a single post or chained thread to Threads via Meta Graph API.

Usage:
    post_threads.py <posts.json>

    posts.json is a JSON array of strings. Each string is one post in the thread.
    A single-element array posts one standalone post. Multi-element arrays post
    a chained thread where post N+1 is a reply to post N.

Requires THREADS_ACCESS_TOKEN in the project root .env file.
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
    user_id: str, token: str, text: str, reply_to_id: str | None = None
) -> str:
    params = {"media_type": "TEXT", "text": text, "access_token": token}
    if reply_to_id:
        params["reply_to_id"] = reply_to_id
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
    user_id: str, token: str, text: str, reply_to_id: str | None = None
) -> str:
    container_id = create_text_container(user_id, token, text, reply_to_id)
    # Meta recommends waiting before publishing; 5s is enough for TEXT posts.
    time.sleep(5)
    return publish_container(user_id, token, container_id)


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2

    posts_path = Path(sys.argv[1])
    posts = json.loads(posts_path.read_text())
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

    user_id = get_user_id(token)

    parent_id: str | None = None
    for i, text in enumerate(posts, 1):
        print(f"Posting {i}/{len(posts)} ({len(text)} chars)...")
        thread_id = post_one(user_id, token, text, reply_to_id=parent_id)
        print(f"  -> {thread_id}")
        parent_id = thread_id
        if i < len(posts):
            time.sleep(3)

    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
