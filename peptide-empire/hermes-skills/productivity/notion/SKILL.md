---
name: notion
description: "Notion API: ntn CLI (preferred) or curl. Pages, databases, markdown, Workers."
version: 2.0.0
author: community
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Notion, Productivity, Notes, Database, API, CLI]
    homepage: https://developers.notion.com
prerequisites:
  env_vars: [NOTION_API_TOKEN]
---

# Notion API

Two ways to talk to Notion. Same integration token works for both — pick by what's available.

◆ **`ntn` CLI** — Notion's official CLI. Shorter syntax, one-line file uploads, required for Workers. macOS + Linux (WSL2 counts as Linux). **Default when installed.**
◆ **HTTP + curl** — works everywhere. **Default fallback** when `ntn` isn't installed.

## Setup

### 1. Get an integration token

1. Create an integration at https://notion.so/my-integrations
2. Copy the API key (starts with `ntn_` or `secret_`)
3. Store in `~/.hermes/.env`:
   ```
   NOTION_API_TOKEN=ntn_your_key_here
   ```
   (The old `NOTION_API_KEY` name also works — `ntn` reads `NOTION_API_TOKEN` first, then falls back to `NOTION_API_KEY`.)
4. **Share target pages/databases with the integration** in Notion: page menu `...` → `Connect to` → your integration name. Without this, the API returns 404.

### 2. Install `ntn` (Linux/macOS)

```bash
# Standard install
curl -fsSL https://ntn.dev | bash

# WSL2 / non-root: use NTN_INSTALL_DIR if /usr/local/bin isn't writable
NTN_INSTALL_DIR="$HOME/.local/bin" curl -fsSL https://ntn.dev | bash

ntn --version    # verify
```

**Skip `ntn login`** — use the integration token instead. This works headlessly:
```bash
export NOTION_API_TOKEN=ntn_...
export NOTION_KEYRING=0          # don't try to use OS keychain
```

Add those to `~/.hermes/.env` so every session inherits them.

### 3. Choose path at runtime

```bash
if command -v ntn >/dev/null 2>&1; then
  # use ntn
else
  # fall back to curl
fi
```

## Path A — `ntn` CLI (preferred when installed)

### Raw API calls (shorthand for curl)
```bash
ntn api v1/pages/{page_id}                    # GET
ntn api v1/pages/{page_id}/markdown           # GET markdown
ntn api v1/search query="page title"          # POST search
ntn api v1/pages -X POST parent[page_id]=xxx \  # POST with inline body
  properties[title][0][text][content]="Title"
ntn api v1/pages/{page_id} -X PATCH archived:=true  # := is non-string (bool/num/null)
```

Syntax notes:
- `key=value` — string fields
- `key[nested]=value` — nested object fields  
- `key:=value` — typed assignment (booleans, numbers, null, arrays)

### Query a database
```bash
ntn api v1/data_sources/{data_source_id}/query -X POST \
  filter[property]=Status filter[select][equals]=Active
```

### File uploads (one-liner — biggest CLI win)
```bash
ntn files create < photo.png
ntn files create --external-url https://example.com/photo.png
ntn files list
```

### Create page from Markdown
```bash
ntn api v1/pages -X POST \
  parent[page_id]=xxx \
  properties[title][0][text][content]="Notes" \
  markdown="# Heading\n\nContent here"
```

### Patch a page with Markdown
```bash
ntn api v1/pages/{page_id}/markdown -X PATCH \
  markdown="## Update\n\nShipped the prototype."
```

### Read page as Markdown (agent-friendly)
```bash
ntn api v1/pages/{page_id}/markdown
```

### Useful env vars
| Var | Effect |
|---|---|
| `NOTION_API_TOKEN` | Auth token (overrides keychain) |
| `NOTION_KEYRING=0` | File-based creds instead of OS keychain |
| `NOTION_WORKSPACE_ID` | Skip workspace picker prompt |

## Path B — HTTP + curl (fallback, always available)

All requests:
```bash
curl -s -X GET "https://api.notion.com/v1/..." \
  -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json"
```

### Common operations (quick reference)

**Search:**
```bash
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query": "page title"}'
```

**Get page as Markdown (agent-friendly):**
```bash
curl -s "https://api.notion.com/v1/pages/{page_id}/markdown" \
  -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H "Notion-Version: 2025-09-03"
```

**Query database:**
```bash
curl -s -X POST "https://api.notion.com/v1/data_sources/{data_source_id}/query" \
  -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"filter": {"property": "Status", "select": {"equals": "Active"}}}'
```

**Create page in database:**
```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "xxx"},
    "properties": {"Name": {"title": [{"text": {"content": "New Item"}}]}}
  }'
```

## Property Types

- **Title:** `{"title": [{"text": {"content": "..."}}]}`
- **Rich text:** `{"rich_text": [{"text": {"content": "..."}}]}`
- **Select:** `{"select": {"name": "Option"}}`
- **Multi-select:** `{"multi_select": [{"name": "A"}, {"name": "B"}]}`
- **Date:** `{"date": {"start": "2026-01-15", "end": "2026-01-16"}}`
- **Checkbox:** `{"checkbox": true}`
- **Number:** `{"number": 42}`
- **URL:** `{"url": "https://..."}`
- **Email:** `{"email": "user@example.com"}`

## API Version 2025-09-03 Notes

- **Databases → Data Sources:** Use `/data_sources/` for queries. Use `database_id` for parenting pages.
- Each database has both IDs — `database_id` for create-page parent, `data_source_id` for queries.
- Search results return `"object": "data_source"` with their `data_source_id`.

## Notes

- Page/database IDs are UUIDs (dashes optional)
- Rate limit: ~3 requests/second average
- Cannot set database view filters via API (UI-only)
- Always pass `-s` to curl (suppress progress bars)
- Pipe through `jq` for readability: `... | jq '.results[0].properties'`
- In WSL2, `ntn` works natively — it's a Linux binary, no special handling needed beyond the install-dir fix for non-root users
