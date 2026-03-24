#!/usr/bin/env python3
"""Batch upload markdown posts to Ghost as drafts."""

import os
import re
import json
import time
import base64
import hashlib
import hmac
import struct
import sys
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.error import HTTPError

import markdown
import yaml

# ── Config ──────────────────────────────────────────────────────────────────

GHOST_URL = os.environ.get("GHOST_URL", "").rstrip("/")
GHOST_ADMIN_API_KEY = os.environ.get("GHOST_ADMIN_API_KEY", "")

import glob as globmod

def get_post_files():
    """Get post files from command line args (glob patterns) or default list."""
    if len(sys.argv) > 1:
        files = []
        for pattern in sys.argv[1:]:
            files.extend(sorted(globmod.glob(pattern)))
        return files
    return sorted(globmod.glob("posts/*.md"))

# ── JWT Generation ──────────────────────────────────────────────────────────

def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

def generate_ghost_token() -> str:
    key_id, secret = GHOST_ADMIN_API_KEY.split(":")
    now = int(time.time())
    header = json.dumps({"alg": "HS256", "typ": "JWT", "kid": key_id})
    payload = json.dumps({"iat": now, "exp": now + 300, "aud": "/admin/"})
    h = b64url(header.encode())
    p = b64url(payload.encode())
    sig = hmac.new(bytes.fromhex(secret), f"{h}.{p}".encode(), hashlib.sha256).digest()
    return f"{h}.{p}.{b64url(sig)}"

# ── Frontmatter Parsing ────────────────────────────────────────────────────

def parse_post(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Split frontmatter and body
    m = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if not m:
        raise ValueError(f"No frontmatter in {filepath}")
    fm = yaml.safe_load(m.group(1))
    body = m.group(2).strip()

    # Derive slug from filename
    basename = os.path.basename(filepath)
    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", basename).replace(".md", "")

    # Parse date (fallback to filename date if frontmatter date is missing)
    date_val = fm.get("date", "")
    if hasattr(date_val, "isoformat"):
        date_str = date_val.isoformat() + "T00:00:00.000Z" if len(date_val.isoformat()) == 10 else date_val.isoformat()
    else:
        date_str = str(date_val).strip()
        date_match = re.match(r"(\d{4}-\d{2}-\d{2})", date_str)
        if date_match:
            date_str = date_match.group(1) + "T00:00:00.000Z"
        else:
            # Fallback: extract date from filename
            fname_match = re.match(r"(\d{4}-\d{2}-\d{2})", basename)
            if fname_match:
                date_str = fname_match.group(1) + "T00:00:00.000Z"
            else:
                date_str = None

    # Tags: combine category + tags
    tags = []
    cat = fm.get("category")
    if cat:
        tags.append({"name": cat})
    for t in fm.get("tags", []):
        tags.append({"name": t})

    # Feature image
    image = fm.get("image")
    feature_image = None
    if isinstance(image, dict):
        feature_image = image.get("path")
    elif isinstance(image, str):
        feature_image = image

    description = fm.get("description", "")

    return {
        "title": fm.get("title", ""),
        "slug": slug,
        "date": date_str,
        "tags": tags,
        "feature_image": feature_image,
        "description": description,
        "body": body,
    }

# ── Markdown to HTML ────────────────────────────────────────────────────────

def preprocess_markdown(md: str) -> str:
    """Add blank line before list items that follow a non-list, non-blank line."""
    lines = md.split("\n")
    result = []
    for i, line in enumerate(lines):
        if i > 0 and re.match(r"^[\*\-\+] ", line):
            prev = lines[i - 1].strip()
            if prev and not re.match(r"^[\*\-\+] ", lines[i - 1]) and not re.match(r"^\d+\. ", lines[i - 1]):
                result.append("")
        # Also handle ordered list items
        if i > 0 and re.match(r"^\d+\.", line):
            prev = lines[i - 1].strip()
            if prev and not re.match(r"^[\*\-\+] ", lines[i - 1]) and not re.match(r"^\d+\.", lines[i - 1]):
                result.append("")
        result.append(line)
    return "\n".join(result)

def md_to_html(md_text: str) -> str:
    md_text = preprocess_markdown(md_text)
    return markdown.markdown(md_text, extensions=["tables", "fenced_code"])

# ── HTML to Lexical JSON ───────────────────────────────────────────────────

class LexicalConverter(HTMLParser):
    """Convert HTML to Ghost Lexical JSON nodes."""

    def __init__(self):
        super().__init__()
        self.nodes = []        # top-level block nodes
        self.stack = []        # stack of (tag, attrs, children)
        self.current_text = "" # text buffer

    def _flush_text(self):
        if self.current_text:
            self.stack[-1][2].append(("text", self.current_text, {}))
            self.current_text = ""

    def handle_starttag(self, tag, attrs):
        if self.stack:
            self._flush_text()
        self.stack.append((tag, dict(attrs), []))

    def handle_endtag(self, tag):
        if not self.stack:
            return
        if self.stack:
            self._flush_text()

        t, attrs, children = self.stack.pop()

        if self.stack:
            # Nested element, push as child
            self.stack[-1][2].append((t, children, attrs))
        else:
            # Top-level element, convert to lexical node
            node = self._to_lexical_block(t, attrs, children)
            if node:
                if isinstance(node, list):
                    self.nodes.extend(node)
                else:
                    self.nodes.append(node)

    def handle_data(self, data):
        if self.stack:
            self.current_text += data

    def _to_lexical_block(self, tag, attrs, children):
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            return {
                "children": self._inline_nodes(children),
                "direction": None,
                "format": "",
                "indent": 0,
                "type": "extended-heading",
                "version": 1,
                "tag": tag,
            }
        elif tag == "p":
            # Check if paragraph only contains an image
            imgs = [c for c in children if isinstance(c, tuple) and c[0] == "img"]
            if len(imgs) == 1 and len(children) == 1:
                img_attrs = imgs[0][2] if len(imgs[0]) > 2 else {}
                return {
                    "type": "image",
                    "version": 1,
                    "src": img_attrs.get("src", ""),
                    "alt": img_attrs.get("alt", ""),
                    "title": "",
                    "width": None,
                    "height": None,
                    "caption": "",
                    "cardWidth": "wide",
                }
            return {
                "children": self._inline_nodes(children),
                "direction": None,
                "format": "",
                "indent": 0,
                "type": "paragraph",
                "version": 1,
            }
        elif tag == "blockquote":
            # Flatten inner paragraphs
            inline = []
            for c in children:
                if isinstance(c, tuple) and c[0] == "p":
                    inline.extend(self._inline_nodes(c[1]))
                else:
                    inline.extend(self._inline_nodes([c]))
            return {
                "children": inline,
                "direction": None,
                "format": "",
                "indent": 0,
                "type": "extended-quote",
                "version": 1,
            }
        elif tag in ("ul", "ol"):
            list_type = "bullet" if tag == "ul" else "number"
            items = []
            val = 1
            for c in children:
                if isinstance(c, tuple) and c[0] == "li":
                    # Check for nested lists inside li
                    li_children = c[1] if len(c) > 1 else []
                    inline_children = []
                    nested_list = None
                    for lc in li_children:
                        if isinstance(lc, tuple) and lc[0] in ("ul", "ol"):
                            nested_list = lc
                        else:
                            inline_children.append(lc)

                    item = {
                        "children": self._inline_nodes(inline_children),
                        "direction": None,
                        "format": "",
                        "indent": 0,
                        "type": "listitem",
                        "version": 1,
                        "value": val,
                    }
                    items.append(item)

                    # If there's a nested list, add it as separate list items with indent
                    if nested_list:
                        nested_tag = nested_list[0]
                        nested_children = nested_list[1] if len(nested_list) > 1 else []
                        nested_type = "bullet" if nested_tag == "ul" else "number"
                        nval = 1
                        for nc in nested_children:
                            if isinstance(nc, tuple) and nc[0] == "li":
                                nli_children = nc[1] if len(nc) > 1 else []
                                nitem = {
                                    "children": self._inline_nodes(nli_children),
                                    "direction": None,
                                    "format": "",
                                    "indent": 1,
                                    "type": "listitem",
                                    "version": 1,
                                    "value": nval,
                                }
                                items.append(nitem)
                                nval += 1
                    val += 1
            return {
                "children": items,
                "direction": None,
                "format": "",
                "indent": 0,
                "type": "list",
                "version": 1,
                "listType": list_type,
                "start": 1,
                "tag": tag,
            }
        elif tag == "pre":
            # Extract code from <pre><code>
            code_text = ""
            lang = ""
            for c in children:
                if isinstance(c, tuple) and c[0] == "code":
                    code_attrs = c[2] if len(c) > 2 else {}
                    cls = code_attrs.get("class", "")
                    if cls.startswith("language-"):
                        lang = cls.replace("language-", "")
                    code_children = c[1] if len(c) > 1 else []
                    code_text = self._extract_text(code_children)
                elif isinstance(c, tuple) and c[0] == "text":
                    code_text += c[1]
            return {
                "type": "codeblock",
                "version": 1,
                "code": code_text,
                "language": lang,
            }
        elif tag == "hr":
            return {"type": "horizontalrule", "version": 1}
        elif tag == "table":
            # Use HTML card for tables
            html_str = self._reconstruct_html(tag, attrs, children)
            return {"type": "html", "version": 1, "html": html_str}
        elif tag == "img":
            return {
                "type": "image",
                "version": 1,
                "src": attrs.get("src", ""),
                "alt": attrs.get("alt", ""),
                "title": "",
                "width": None,
                "height": None,
                "caption": "",
                "cardWidth": "wide",
            }
        else:
            # Fallback: treat as paragraph
            return {
                "children": self._inline_nodes(children),
                "direction": None,
                "format": "",
                "indent": 0,
                "type": "paragraph",
                "version": 1,
            }

    def _inline_nodes(self, children):
        """Convert children list to inline Lexical nodes."""
        nodes = []
        for c in children:
            if isinstance(c, tuple):
                if c[0] == "text":
                    text = c[1]
                    if text.strip() or text:
                        nodes.append(self._text_node(text, 0))
                elif c[0] == "strong" or c[0] == "b":
                    inner = c[1] if len(c) > 1 else []
                    for n in self._inline_nodes(inner):
                        n["format"] = n.get("format", 0) | 1
                        nodes.append(n)
                elif c[0] == "em" or c[0] == "i":
                    inner = c[1] if len(c) > 1 else []
                    for n in self._inline_nodes(inner):
                        n["format"] = n.get("format", 0) | 2
                        nodes.append(n)
                elif c[0] == "code":
                    inner = c[1] if len(c) > 1 else []
                    text = self._extract_text(inner)
                    nodes.append(self._text_node(text, 16))
                elif c[0] == "a":
                    attrs = c[2] if len(c) > 2 else {}
                    inner = c[1] if len(c) > 1 else []
                    url = attrs.get("href", "")
                    link_node = {
                        "children": self._inline_nodes(inner),
                        "direction": None,
                        "format": "",
                        "indent": 0,
                        "type": "link",
                        "version": 1,
                        "url": url,
                    }
                    if url.startswith("http"):
                        link_node["target"] = "_blank"
                        link_node["rel"] = "noopener noreferrer"
                    nodes.append(link_node)
                elif c[0] == "img":
                    # Inline image - shouldn't happen often but handle it
                    img_attrs = c[2] if len(c) > 2 else {}
                    nodes.append(self._text_node(img_attrs.get("alt", "[image]"), 0))
                elif c[0] == "br":
                    nodes.append({"type": "linebreak", "version": 1})
                elif c[0] == "del" or c[0] == "s":
                    inner = c[1] if len(c) > 1 else []
                    for n in self._inline_nodes(inner):
                        n["format"] = n.get("format", 0) | 4
                        nodes.append(n)
                else:
                    # Unknown inline tag, extract text
                    inner = c[1] if len(c) > 1 else []
                    nodes.extend(self._inline_nodes(inner))
            elif isinstance(c, str):
                if c.strip() or c:
                    nodes.append(self._text_node(c, 0))
        return nodes if nodes else [self._text_node("", 0)]

    def _text_node(self, text, fmt):
        return {
            "detail": 0,
            "format": fmt,
            "mode": "normal",
            "style": "",
            "text": text,
            "type": "extended-text",
            "version": 1,
        }

    def _extract_text(self, children):
        """Recursively extract plain text from children."""
        parts = []
        for c in children:
            if isinstance(c, tuple):
                if c[0] == "text":
                    parts.append(c[1])
                else:
                    inner = c[1] if len(c) > 1 else []
                    parts.append(self._extract_text(inner))
            elif isinstance(c, str):
                parts.append(c)
        return "".join(parts)

    def _reconstruct_html(self, tag, attrs, children):
        """Reconstruct HTML from parsed elements (for table passthrough)."""
        attr_str = ""
        for k, v in attrs.items():
            attr_str += f' {k}="{v}"'
        inner = self._children_to_html(children)
        return f"<{tag}{attr_str}>{inner}</{tag}>"

    def _children_to_html(self, children):
        parts = []
        for c in children:
            if isinstance(c, tuple):
                if c[0] == "text":
                    parts.append(c[1])
                else:
                    tag = c[0]
                    inner = c[1] if len(c) > 1 else []
                    attrs = c[2] if len(c) > 2 else {}
                    attr_str = ""
                    for k, v in attrs.items():
                        attr_str += f' {k}="{v}"'
                    parts.append(f"<{tag}{attr_str}>{self._children_to_html(inner)}</{tag}>")
        return "".join(parts)


def html_to_lexical(html: str) -> str:
    converter = LexicalConverter()
    converter.feed(html)

    # Filter out empty paragraph nodes
    nodes = []
    for n in converter.nodes:
        if n.get("type") == "paragraph":
            children = n.get("children", [])
            if len(children) == 1 and children[0].get("text", "").strip() == "":
                continue
        nodes.append(n)

    lexical = {
        "root": {
            "children": nodes,
            "direction": None,
            "format": "",
            "indent": 0,
            "type": "root",
            "version": 1,
        }
    }
    return json.dumps(lexical, ensure_ascii=False)

# ── Ghost API ───────────────────────────────────────────────────────────────

def create_draft(post_data: dict) -> dict:
    token = generate_ghost_token()
    url = f"{GHOST_URL}/ghost/api/admin/posts/"

    body = {
        "posts": [{
            "title": post_data["title"],
            "slug": post_data["slug"],
            "lexical": post_data["lexical"],
            "status": "draft",
            "tags": post_data["tags"],
            "published_at": post_data["date"],
        }]
    }

    if post_data.get("feature_image"):
        body["posts"][0]["feature_image"] = post_data["feature_image"]
    if post_data.get("description"):
        body["posts"][0]["custom_excerpt"] = post_data["description"]
        body["posts"][0]["meta_description"] = post_data["description"]

    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Ghost {token}")
    req.add_header("Content-Type", "application/json; charset=utf-8")

    try:
        resp = urlopen(req)
        result = json.loads(resp.read())
        return result
    except HTTPError as e:
        error_body = e.read().decode()
        return {"error": error_body, "status": e.code}

# ── Main ────────────────────────────────────────────────────────────────────

def main():
    if not GHOST_URL or not GHOST_ADMIN_API_KEY:
        print("ERROR: Set GHOST_URL and GHOST_ADMIN_API_KEY environment variables")
        sys.exit(1)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    post_files = get_post_files()
    success = 0
    failed = 0

    print(f"Found {len(post_files)} files to upload")

    for filepath in post_files:
        full_path = os.path.join(base_dir, filepath)
        print(f"\n{'='*60}")
        print(f"Processing: {filepath}")

        try:
            post = parse_post(full_path)
            html = md_to_html(post["body"])
            lexical = html_to_lexical(html)

            post_data = {
                "title": post["title"],
                "slug": post["slug"],
                "date": post["date"],
                "tags": post["tags"],
                "feature_image": post["feature_image"],
                "description": post["description"],
                "lexical": lexical,
            }

            result = create_draft(post_data)

            if "error" in result:
                print(f"  FAILED: {result['error'][:200]}")
                failed += 1
            else:
                ghost_post = result.get("posts", [{}])[0]
                print(f"  OK: {ghost_post.get('title', '?')}")
                print(f"  ID: {ghost_post.get('id', '?')}")
                print(f"  Slug: {ghost_post.get('slug', '?')}")
                success += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            failed += 1

        # Small delay between requests
        time.sleep(0.5)

    print(f"\n{'='*60}")
    print(f"Done! Success: {success}, Failed: {failed}")

if __name__ == "__main__":
    main()
