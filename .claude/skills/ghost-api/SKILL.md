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

Load them with:
```bash
source .env
```

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

### Create a draft

```bash
TOKEN=$(generate_ghost_token)
curl -s -X POST \
  -H "Authorization: Ghost ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "posts": [{
      "title": "My Post Title",
      "html": "<p>Post content in HTML</p>",
      "tags": [
        {"name": "AI"},
        {"name": "productivity"}
      ]
    }]
  }' \
  "${GHOST_URL}/ghost/api/admin/posts/" | jq .
```

### Create and publish immediately

Add `"status": "published"`:

```bash
TOKEN=$(generate_ghost_token)
curl -s -X POST \
  -H "Authorization: Ghost ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "posts": [{
      "title": "My Post Title",
      "html": "<p>Post content in HTML</p>",
      "status": "published",
      "tags": [
        {"name": "AI"},
        {"name": "productivity"}
      ]
    }]
  }' \
  "${GHOST_URL}/ghost/api/admin/posts/" | jq .
```

### Post fields reference

| Field | Type | Notes |
|-------|------|-------|
| `title` | string | Required |
| `html` | string | Post body as HTML |
| `lexical` | string | Post body in Lexical format (alternative to html) |
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

1. **Read the post file** and parse frontmatter (title, tags, description, date)
2. **Convert markdown to HTML** — use `pandoc` or similar
3. **Generate JWT token** from `.env` credentials
4. **Create the post** with parsed metadata mapped to Ghost fields:
   - `title` ← frontmatter `title`
   - `html` ← converted markdown body
   - `tags` ← frontmatter `tags` array, mapped to `[{"name": "tag"}]`
   - `custom_excerpt` / `meta_description` ← frontmatter `description`
   - `status` ← `"published"` or `"draft"`
   - `published_at` ← frontmatter `date` in ISO 8601

## Common Mistakes

- **Post created as draft instead of published** — must explicitly set `"status": "published"`
- **JWT expired** — tokens are valid for 5 minutes only; regenerate before each request
- **Tags replaced on edit** — when updating, pass the FULL list of tags, not just new ones
- **Missing `updated_at` on edit** — causes 409 conflict; always fetch current version first
- **Wrong audience in JWT** — must be `"/admin/"`, not `"/v2/admin/"` or other paths
- **Content-Type missing** — POST/PUT requests need `Content-Type: application/json`
