---
name: ghost-api
description: Use when the user wants to read, create, or publish blog posts on Ghost CMS, manage tags, or interact with the Ghost blogging platform. Also use when the user mentions "Ghost", "publish", "deploy post", "blog API", or wants to push articles to their site.
---

# Ghost API

Interact with a Ghost blog via Admin API and Content API using bash/curl.

## Setup

Credentials live in `.env` at the project root:

```
GHOST_URL=https://your-site.ghost.io
GHOST_ADMIN_API_KEY=<id>:<secret>
GHOST_CONTENT_API_KEY=<content-api-key>
```

Get these from Ghost Admin > Settings > Integrations > Add custom integration.

Load them into shell variables with:
```bash
export $(grep -v '^#' .env | xargs)
```

**Note:** `source .env` does NOT work reliably in Claude Code's bash environment. Always use the `export ... xargs` pattern above, or inline the values directly with `export GHOST_URL="..."` etc.

## Authentication

### Content API (read-only, public data)

Just append the key as a query parameter:
```
${GHOST_URL}/ghost/api/content/posts/?key=${GHOST_CONTENT_API_KEY}
```

### Admin API (read/write, requires JWT)

Generate a short-lived JWT from the Admin API key:

```bash
generate_ghost_token() {
  local KEY="$GHOST_ADMIN_API_KEY"
  local ID="${KEY%%:*}"
  local SECRET="${KEY##*:}"
  local NOW=$(date +%s)
  local EXP=$(($NOW + 300))

  local HEADER=$(printf '{"alg":"HS256","typ":"JWT","kid":"%s"}' "$ID")
  local PAYLOAD=$(printf '{"iat":%d,"exp":%d,"aud":"/admin/"}' "$NOW" "$EXP")

  b64url() { base64 | tr -d '=' | tr '+' '-' | tr '/' '_'; }

  local H=$(printf '%s' "$HEADER" | b64url)
  local P=$(printf '%s' "$PAYLOAD" | b64url)
  local SIG=$(printf '%s' "${H}.${P}" | openssl dgst -binary -sha256 -mac HMAC -macopt hexkey:"$SECRET" | b64url)

  echo "${H}.${P}.${SIG}"
}

TOKEN=$(generate_ghost_token)
```

Use in requests:
```
Authorization: Ghost ${TOKEN}
```

## Quick Reference

| Operation | API | Method | Endpoint |
|-----------|-----|--------|----------|
| List posts | Content | GET | `/ghost/api/content/posts/` |
| Read post by slug | Content | GET | `/ghost/api/content/posts/slug/{slug}/` |
| List tags | Content | GET | `/ghost/api/content/tags/` |
| List all posts (incl. drafts) | Admin | GET | `/ghost/api/admin/posts/` |
| Create post | Admin | POST | `/ghost/api/admin/posts/` |
| Update post | Admin | PUT | `/ghost/api/admin/posts/{id}/` |
| Delete post | Admin | DELETE | `/ghost/api/admin/posts/{id}/` |
| Upload image | Admin | POST | `/ghost/api/admin/images/upload/` |
| List tags (admin) | Admin | GET | `/ghost/api/admin/tags/` |
| Create tag | Admin | POST | `/ghost/api/admin/tags/` |

## Reading Posts

```bash
# List published posts (Content API, simple)
curl -s "${GHOST_URL}/ghost/api/content/posts/?key=${GHOST_CONTENT_API_KEY}&limit=10&include=tags,authors" | jq .

# Read single post by slug
curl -s "${GHOST_URL}/ghost/api/content/posts/slug/my-post-slug/?key=${GHOST_CONTENT_API_KEY}&include=tags" | jq .

# List ALL posts including drafts (Admin API)
TOKEN=$(generate_ghost_token)
curl -s -H "Authorization: Ghost ${TOKEN}" \
  "${GHOST_URL}/ghost/api/admin/posts/?limit=all&include=tags" | jq .

# Filter posts by tag
curl -s "${GHOST_URL}/ghost/api/content/posts/?key=${GHOST_CONTENT_API_KEY}&filter=tag:my-tag&include=tags" | jq .

# Filter posts by status (Admin API only)
curl -s -H "Authorization: Ghost ${TOKEN}" \
  "${GHOST_URL}/ghost/api/admin/posts/?filter=status:draft&include=tags" | jq .
```

### Useful query parameters

- `limit` — number of results (default: 15, use `all` for everything)
- `page` — pagination page number
- `include` — comma-separated: `tags`, `authors`
- `fields` — comma-separated field names to return
- `filter` — NQL filter (e.g. `tag:javascript`, `status:published`, `author:homuchen`)
- `order` — e.g. `published_at desc`

## Reading Tags

```bash
# All tags (Content API)
curl -s "${GHOST_URL}/ghost/api/content/tags/?key=${GHOST_CONTENT_API_KEY}&limit=all" | jq .

# Tags with post count
curl -s "${GHOST_URL}/ghost/api/content/tags/?key=${GHOST_CONTENT_API_KEY}&limit=all&include=count.posts" | jq .
```

## Creating / Publishing Posts

### Ghost v6.0: Must use Lexical format

**`source: "html"` is BROKEN in Ghost v6.0** — it silently creates empty posts. You must convert HTML to Lexical JSON format and pass it via the `lexical` field.

### Create a draft (Lexical format)

```bash
TOKEN=$(generate_ghost_token)
curl -s -X POST \
  -H "Authorization: Ghost ${TOKEN}" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{
    "posts": [{
      "title": "My Post Title",
      "lexical": "{\"root\":{\"children\":[{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Post content here\",\"type\":\"extended-text\",\"version\":1}],\"direction\":null,\"format\":\"\",\"indent\":0,\"type\":\"paragraph\",\"version\":1}],\"direction\":null,\"format\":\"\",\"indent\":0,\"type\":\"root\",\"version\":1}}",
      "tags": [
        {"name": "AI"},
        {"name": "productivity"}
      ]
    }]
  }' \
  "${GHOST_URL}/ghost/api/admin/posts/" | jq .
```

### Create and publish immediately

Add `"status": "published"` to the post object.

### Post fields reference

| Field | Type | Notes |
|-------|------|-------|
| `title` | string | Required |
| `lexical` | string | **Required for v6.0.** Post body as Lexical JSON string |
| `html` | string | ~~`source: "html"` broken in v6.0~~ — do NOT use |
| `status` | string | `draft` (default), `published`, `scheduled` |
| `tags` | array | `[{"name": "tag"}]` or `[{"slug": "tag-slug"}]` — creates tag if not exists |
| `authors` | array | `[{"email": "..."}]` or `[{"slug": "..."}]` |
| `featured` | boolean | Feature the post |
| `published_at` | string | ISO 8601 datetime (required for `scheduled`) |
| `custom_excerpt` | string | Custom excerpt / description |
| `meta_title` | string | SEO title |
| `meta_description` | string | SEO description |
| `og_title` | string | Open Graph title |
| `og_description` | string | Open Graph description |
| `feature_image` | string | URL of feature image |
| `slug` | string | URL slug (auto-generated from title if omitted) |

### Tags behavior

- Pass `{"name": "New Tag"}` — Ghost creates the tag if it doesn't exist
- Pass `{"slug": "existing-tag"}` — references existing tag by slug
- When editing: you must pass ALL tags (replaces entire tag list)
- First tag in array becomes the "primary tag"

## Updating Posts

**Important:** You must include `updated_at` from the current version to avoid conflicts.

```bash
# First, get the current post to obtain updated_at
POST=$(curl -s -H "Authorization: Ghost ${TOKEN}" \
  "${GHOST_URL}/ghost/api/admin/posts/{id}/")
UPDATED_AT=$(echo "$POST" | jq -r '.posts[0].updated_at')

# Then update
curl -s -X PUT \
  -H "Authorization: Ghost ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"posts\": [{
      \"title\": \"Updated Title\",
      \"updated_at\": \"${UPDATED_AT}\"
    }]
  }" \
  "${GHOST_URL}/ghost/api/admin/posts/{id}/" | jq .
```

## Uploading Images

```bash
TOKEN=$(generate_ghost_token)
curl -s -X POST \
  -H "Authorization: Ghost ${TOKEN}" \
  -F "file=@/path/to/image.jpg" \
  -F "purpose=image" \
  "${GHOST_URL}/ghost/api/admin/images/upload/" | jq .
```

Response includes the hosted image URL to use in `feature_image` or post HTML.

## Creating Tags

```bash
TOKEN=$(generate_ghost_token)
curl -s -X POST \
  -H "Authorization: Ghost ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "tags": [{
      "name": "AI",
      "slug": "ai",
      "description": "Articles about artificial intelligence"
    }]
  }' \
  "${GHOST_URL}/ghost/api/admin/tags/" | jq .
```

## Workflow: Markdown Post to Ghost

When publishing a markdown blog post from this project to Ghost:

1. **Read the post file** and parse frontmatter (title, tags, description, date, image)
2. **Preprocess markdown** before conversion:
   - Add blank line before list items (`* `, `- `) that follow a non-list line (Python `markdown` module requires this, otherwise list merges into paragraph)
3. **Convert markdown to HTML** — use Python `markdown` module with `tables` and `fenced_code` extensions
4. **Convert HTML to Lexical JSON** — Ghost v6.0 requires Lexical format (see Lexical Format section below)
5. **Generate JWT token** from `.env` credentials
6. **Create the post** with parsed metadata mapped to Ghost fields:
   - `title` ← frontmatter `title`
   - `lexical` ← Lexical JSON string (converted from HTML)
   - `tags` ← frontmatter `tags` array + `category`, mapped to `[{"name": "tag"}]`
   - `custom_excerpt` / `meta_description` ← frontmatter `description`
   - `feature_image` ← frontmatter `image.path`
   - `slug` ← filename without date prefix (e.g. `2024-07-04-my-post.md` → `my-post`)
   - `status` ← `"published"` or `"draft"`
   - `published_at` ← frontmatter `date` in ISO 8601

## Lexical Format Reference (Ghost v6.0)

Ghost v6.0 uses the Lexical editor internally. Content must be sent as a JSON string in the `lexical` field.

### Top-level structure

```json
{
  "root": {
    "children": [ /* block nodes */ ],
    "direction": null,
    "format": "",
    "indent": 0,
    "type": "root",
    "version": 1
  }
}
```

### Block node types

**Paragraph** (`<p>`):
```json
{"children": [/* inline nodes */], "direction": null, "format": "", "indent": 0, "type": "paragraph", "version": 1}
```

**Heading** (`<h1>`–`<h6>`):
```json
{"children": [/* inline nodes */], "direction": null, "format": "", "indent": 0, "type": "extended-heading", "version": 1, "tag": "h2"}
```

**Blockquote** (`<blockquote>`):
```json
{"children": [/* inline nodes */], "direction": null, "format": "", "indent": 0, "type": "extended-quote", "version": 1}
```

**List** (`<ul>`, `<ol>`):
```json
{"children": [/* listitem nodes */], "direction": null, "format": "", "indent": 0, "type": "list", "version": 1, "listType": "bullet", "start": 1, "tag": "ul"}
```
- `listType`: `"bullet"` or `"number"`
- `tag`: `"ul"` or `"ol"`

**List item** (`<li>`):
```json
{"children": [/* inline nodes */], "direction": null, "format": "", "indent": 0, "type": "listitem", "version": 1, "value": 1}
```

**Image** (`<img>`):
```json
{"type": "image", "version": 1, "src": "https://...", "alt": "desc", "title": "", "width": null, "height": null, "caption": "", "cardWidth": "wide"}
```

**HTML card** (for tables and other complex HTML):
```json
{"type": "html", "version": 1, "html": "<table>...</table>"}
```

**Code block** (`<pre><code>`):
```json
{"type": "codeblock", "version": 1, "code": "...", "language": ""}
```

**Horizontal rule** (`<hr>`):
```json
{"type": "horizontalrule", "version": 1}
```

### Inline node types

**Text** (with formatting):
```json
{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "hello", "type": "extended-text", "version": 1}
```
- `format` flags (bitmask): `0` = normal, `1` = bold, `2` = italic, `4` = strikethrough, `8` = underline, `16` = code

**Link** (`<a>`):
```json
{"children": [/* text nodes */], "direction": null, "format": "", "indent": 0, "type": "link", "version": 1, "url": "https://...", "target": "_blank", "rel": "noopener noreferrer"}
```
- External links (`http://`, `https://`): add `target` and `rel`
- Internal links (`/posts/...`): omit `target` and `rel`

**Line break** (`<br>`):
```json
{"type": "linebreak", "version": 1}
```

### HTML-to-Lexical conversion rules

1. Parse HTML into DOM elements
2. Map each top-level element to the corresponding Lexical block node
3. Handle inline formatting (`<strong>` → format `1`, `<em>` → format `2`, `<code>` → format `16`)
4. Handle links (`<a>`) as `link` nodes wrapping `extended-text` children
5. Promote images: if a `<p>` only contains `<img>`, promote the image to top-level instead of wrapping in paragraph
6. Tables (`<table>`) → use `html` card node (raw HTML passthrough)
7. Filter out whitespace-only text nodes inside `<ul>`/`<ol>` containers (HTML whitespace between `<li>` tags creates phantom empty list items)

### Markdown preprocessing

Python's `markdown` module requires a blank line before list items. Without it, `* item` after a paragraph line gets merged into the paragraph as literal text.

```python
def preprocess_markdown(md):
    """Add blank line before list items that follow a non-list, non-blank line."""
    lines = md.split('\n')
    result = []
    for i, line in enumerate(lines):
        if i > 0 and re.match(r'^[\*\-\+] ', line):
            prev = lines[i-1].strip()
            if prev and not re.match(r'^[\*\-\+] ', lines[i-1]) and not re.match(r'^\d+\. ', lines[i-1]):
                result.append('')
        result.append(line)
    return '\n'.join(result)
```

## Common Mistakes

- **`source: "html"` broken in Ghost v6.0** — creates empty posts. Must use `lexical` field with Lexical JSON
- **Empty list items** — whitespace between `</li>` and `<li>` in HTML becomes phantom text nodes; filter non-listitem children when building list nodes
- **List merged into paragraph** — markdown needs blank line before `* ` items; preprocess markdown before conversion
- **Post created as draft instead of published** — must explicitly set `"status": "published"`
- **JWT expired** — tokens are valid for 5 minutes only; regenerate before each request
- **Tags replaced on edit** — when updating, pass the FULL list of tags, not just new ones
- **Missing `updated_at` on edit** — causes 409 conflict; always fetch current version first
- **Wrong audience in JWT** — must be `"/admin/"`, not `"/v2/admin/"` or other paths
- **Content-Type missing** — POST/PUT requests need `Content-Type: application/json; charset=utf-8`
- **`source .env` fails silently** — in Claude Code's bash, `source .env` doesn't persist variables; use `export $(grep -v '^#' .env | xargs)` instead
