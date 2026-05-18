# Third-Party MCP Server Setups

Worked examples for non-standard or high-value MCP server integrations.

---

## Zapier MCP (HTTP, token-in-URL)

**What it gives you:** Access to 8,000+ apps (Discord, Gmail, Google Sheets, etc.) via 14 meta-tools. Build automation pipelines from conversation.

**Setup at [mcp.zapier.com](https://mcp.zapier.com):**
1. Sign in with Google
2. Click "+ New MCP Server" → select client type: **"Other"** (Hermes speaks standard MCP)
3. Go to **Connect** tab → click **Generate Token**
4. Copy the full Server URL (it includes `?token=...` — leave it intact)
5. Go to **Apps** tab → **Add Tools** → pick only what you need

**Minimal tool selection (principle: least privilege):**
| App | Tools Needed | Skip |
|-----|-------------|------|
| Discord | Send Channel Message, Send Direct Message, Find Channel, Find User | Role mgmt, kick/ban, channel create/rename, webhooks, nicknames |
| Google Sheets | Create Spreadsheet Row, Find Worksheet | Everything else |
| Gmail | Send Email | Read inbox, delete contacts |
| Cal.com | **Skip entirely** — static booking link in email body is sufficient | All |

**Discord OAuth scopes (uncheck everything except):**
- View Channels
- Send Messages
- Embed Links
- Read Message History

→ **Never grant:** Administrator, Manage Server, Manage Roles, Manage Channels, Kick/Ban Members

**Google OAuth: hit Continue without selecting additional scopes.** Zapier already has what it needs from login.

**Hermes config:**
```yaml
mcp_servers:
  zapier:
    url: "https://mcp.zapier.com/api/v1/connect?token=<full-token-here>"
    timeout: 180
    connect_timeout: 60
```

---

## Google Search Console MCP (stdio, OAuth)

**Package:** `suganthan-gsc-mcp` (npm) — 20 SEO tools. OAuth or service account. v2.2.1+.

**Tools provided:** Site snapshot, quick wins, content gaps, traffic drops, CTR opportunities, cannibalisation check, content decay, URL inspection, topic clusters, CTR vs benchmarks, advanced search analytics, check alerts, verify claim, content recommendations, generate report, multi-site dashboard, submit URL, batch submit, submit sitemap, list sitemaps.

**Setup at [console.cloud.google.com](https://console.cloud.google.com/):**
1. Create project (e.g., `GSC MCP`) — leave org as "No organization" for personal accounts
2. Search for "Search Console API" → **Enable**
3. ☰ → APIs & Services → Credentials → + CREATE CREDENTIALS → OAuth client ID
4. If prompted for consent screen: External, name "Hermes GSC", save, skip scopes, skip test users
5. Application type: **Desktop app**, name "Hermes Desktop"
6. Download JSON → save as `~/.hermes/gsc-oauth-secrets.json`

**Site URL format:** Use `sc-domain:yoursite.com` (domain property — covers all protocols and subdomains).

**Hermes config:**
```yaml
mcp_servers:
  gsc:
    command: "npx"
    args: ["-y", "suganthan-gsc-mcp"]
    env:
      GSC_AUTH_MODE: "oauth"
      GSC_OAUTH_SECRETS_FILE: "/home/robert/.hermes/gsc-oauth-secrets.json"
      GSC_SITE_URL: "sc-domain:yoursite.com"
    timeout: 180
    connect_timeout: 60
```

**First-run OAuth flow:** On gateway restart, the MCP server will open a browser tab for Google authorization. Click Allow — it's one-time. The server handles the redirect to localhost and stores the refresh token automatically.

**Pitfalls:**
- If the consent screen wasn't configured first, the OAuth client creation will redirect to it — configure it with External type and bare minimum fields, then retry
- Safari mobile blocks Zapier's MCP dashboard modal — use Chrome/Firefox on desktop
- The `sc-domain:` prefix is required for domain properties; omit for URL-prefix properties (`https://example.com/`)
