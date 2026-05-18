# MCP Server Setup Recipes

Specific setup workflows for commonly-used MCP servers. These expand on the `native-mcp` skill's config reference with step-by-step OAuth, permission minimization, and known pitfalls.

## Zapier MCP

**Type:** HTTP  
**Package:** n/a (SaaS, no local install)  
**Auth model:** Token embedded in URL query parameter

### Setup (User Side)
1. Go to **https://mcp.zapier.com** on desktop Chrome/Firefox (NOT mobile Safari — JS modal is blocked)
2. Sign in with Google
3. Click **"+ New MCP Server"** → select **"Other"** as client type
4. Copy the MCP Server URL (it has `?token=...` embedded)

### Permission Minimization (per app)
When authorizing Zapier to access services, **only check the minimum required scopes**:

| Service | Required Tools | Skip |
|---------|---------------|------|
| Discord | Send Channel Message, Send Direct Message, Find Channel, Find User | Administrator, Manage Server, Kick/Ban, Manage Roles/Channels |
| Discord scopes | View Channels, Send Messages, Embed Links, Read Message History | Everything else |
| Google Sheets | Create Spreadsheet Row, Find Worksheet | All other sheet/Drive scopes |
| Gmail | Send Email | Read inbox, delete contacts |
| Cal.com | Skip entirely — just embed the static booking link in text | n/a |

### Config (Hermes)
```yaml
  zapier:
    url: "https://mcp.zapier.com/api/v1/connect?token=YOUR_TOKEN"
    timeout: 180
    connect_timeout: 60
```

### Tools Registered
14 tools: `mcp_zapier_discover_zapier_actions`, `mcp_zapier_enable_zapier_action`, `mcp_zapier_disable_zapier_action`, `mcp_zapier_list_enabled_zapier_actions`, `mcp_zapier_execute_zapier_read_action`, `mcp_zapier_execute_zapier_write_action`, `mcp_zapier_send_feedback`, `mcp_zapier_auto_provision_mcp`, `mcp_zapier_list_zapier_skills`, `mcp_zapier_get_zapier_skill`, `mcp_zapier_create_zapier_skill`, `mcp_zapier_update_zapier_skill`, `mcp_zapier_delete_zapier_skill`, `mcp_zapier_get_configuration_url`

### Pitfalls
- **Mobile Safari**: Zapier's MCP dashboard uses a JavaScript modal that mobile Safari blocks. Must use desktop browser.
- **"Find Worksheet" IS "Find Spreadsheet"**: Zapier names it differently than Google does.
- **Google extra scopes**: After initial auth, Google shows optional extra scopes (all Drive files, all spreadsheets, delete contacts). Hit "Continue" without selecting any — the base permissions are already granted.
- **Token in URL**: The Zapier token is embedded as a query parameter in the URL itself. No separate Authorization header needed.

---

## Google Search Console MCP (suganthan-gsc-mcp)

**Type:** stdio (npx)  
**Package:** `suganthan-gsc-mcp` (npm)  
**Auth model:** OAuth 2.0 (Desktop app type)

### Setup (OAuth — Desktop App, may hit unverified-app block)
1. **console.cloud.google.com** → Create Project → name `GSC MCP` → No Organization (fine for personal)
2. Search for "Search Console API" → **ENABLE**
3. ☰ → APIs & Services → Credentials → **+ CREATE CREDENTIALS** → OAuth client ID
4. If prompted for consent screen: External → App name `Hermes GSC` → email → Save and Continue (skip scopes, skip test users)
5. Application type: **Desktop app** → name `Hermes Desktop` → Create → **DOWNLOAD JSON**
6. Save downloaded JSON as `~/.hermes/gsc-oauth-secrets.json`

### Config (Hermes)
```yaml
  gsc:
    command: "npx"
    args: ["-y", "suganthan-gsc-mcp"]
    env:
      GSC_AUTH_MODE: "oauth"
      GSC_OAUTH_SECRETS_FILE: "/home/robert/.hermes/gsc-oauth-secrets.json"
      GSC_SITE_URL: "sc-domain:example.com"
    timeout: 180
    connect_timeout: 60
```

### Setup (Service Account — production path, no OAuth popups)

Service account is the **recommended production path**. No browser popups, no consent screens, no unverified-app blocks. Use this if OAuth fails with "Access blocked" or you want a stable headless setup.

1. **Google Cloud Console** → Create Project (or reuse existing) → name it anything (e.g. `nurserob-gsc`)
2. **APIs & Services → Library** → search `Search Console API` → **Enable**
3. (Optional for indexing tools) Also enable **Web Search Indexing API**
4. **IAM & Admin → Service Accounts → Create Service Account**
   - Name: `hermes-gsc`
   - Role: **Owner** (needed for Indexing API; can use `Viewer` if only reading data)
   - Click `Done`
5. Click the new account → **Keys → Add Key → Create New Key → JSON** → downloads a `.json` file
6. Copy it: `cp ~/Downloads/<project>-*.json ~/.hermes/gsc-service-account.json`
7. Open the JSON, find `client_email` (e.g. `hermes-gsc@nurserob-gsc.iam.gserviceaccount.com`)
8. **Google Search Console** → select your property → **Settings → Users and permissions → Add User** → paste `client_email` → **Full** permission
9. Flip your Hermes config:

```yaml
  gsc:
    command: "npx"
    args: ["-y", "suganthan-gsc-mcp"]
    env:
      GSC_KEY_FILE: "/home/robert/.hermes/gsc-service-account.json"
      GSC_SITE_URL: "sc-domain:example.com"
    timeout: 180
    connect_timeout: 60
```

**Key difference from OAuth config:** Remove `GSC_AUTH_MODE` and `GSC_OAUTH_SECRETS_FILE`. The default auth mode is `service_account` — `GSC_KEY_FILE` is all it needs.

### Site URL Format
- `sc-domain:example.com` — domain property (recommended, covers all subdomains + both http/https)
- `https://example.com/` — URL prefix property (narrower)

### DNS Verification for Domain Properties

When adding a domain property (`sc-domain:...`) in Google Search Console, Google requires DNS TXT record verification. The record looks like:

```
google-site-verification=<random-string>
```

**Step 1: Find your DNS provider**

```bash
curl -s "https://dns.google/resolve?name=example.com&type=NS" | python3 -c "
import sys, json
d = json.load(sys.stdin)
for a in d.get('Answer', []):
    print(a['data'])
"
```

Example output: `salvador.ns.porkbun.com.` → DNS is managed at **Porkbun**.

**Step 2: Add the TXT record** (varies by provider)

*Porkbun:* Account → Domain Management → click domain → DNS tab → + ADD RECORD → Type: TXT, Host: `@` (or blank), Answer: the full `google-site-verification=...` string, TTL: default → Save.

*Cloudflare:* DNS → Records → Add Record → Type: TXT, Name: `@`, Content: the full verification string.

*Vercel:* Settings → Domains → click domain → DNS → Add TXT Record.

**Step 3:** Back in Google Search Console, click **Verify**. DNS propagation is usually under 60 seconds.

If DNS is managed by Vercel but you don't have Vercel CLI/API access, use the Vercel dashboard. Note: Zapier's Vercel integration (find_project, create_deployment, create_project) does NOT include DNS record management.

### Tools Registered
20 tools: `mcp_gsc_quick_wins`, `mcp_gsc_ctr_opportunities`, `mcp_gsc_traffic_drops`, `mcp_gsc_content_gaps`, `mcp_gsc_site_snapshot`, `mcp_gsc_inspect_url`, `mcp_gsc_cannibalization_check`, `mcp_gsc_content_decay`, `mcp_gsc_topic_cluster_performance`, `mcp_gsc_ctr_vs_benchmark`, `mcp_gsc_verify_claim`, `mcp_gsc_advanced_search_analytics`, `mcp_gsc_check_alerts`, `mcp_gsc_content_recommendations`, `mcp_gsc_generate_report`, `mcp_gsc_multi_site_dashboard`, `mcp_gsc_submit_url`, `mcp_gsc_submit_batch`, `mcp_gsc_submit_sitemap`, `mcp_gsc_list_sitemaps`

### Pitfalls
- **Domain property requires DNS TXT verification**: When adding `sc-domain:...` as a new property in GSC, Google requires you to prove ownership by adding a DNS TXT record. Use `curl -s "https://dns.google/resolve?name=DOMAIN&type=NS"` to find where DNS is managed. The TXT record host should be `@` (root), value is the full `google-site-verification=...` string from Google.
- **Vercel via Zapier has no DNS management**: The Zapier Vercel integration provides `find_project`, `create_deployment`, and `create_project` — no DNS record actions. Use the Vercel dashboard directly, or Vercel CLI (`vercel dns add`).
- **Lazy OAuth**: The OAuth consent popup fires on the *first tool call*, not at startup. If no browser popup appears after restart, it's working — the auth will happen when you first ask for GSC data.
- **"Access blocked: has not completed the Google verification process"**: Google's unverified-app warning. Look for tiny `Advanced` link at bottom-left → `Go to Hermes GSC (unsafe)`. If no Advanced link appears, switch to service account (above) — it bypasses OAuth entirely.
- **"Select a project" → NEW PROJECT**: The button is in the top-right corner of the project selector popup, not visible on the Cloud Console homepage.
- **No Organization**: For personal Google accounts, leave parent resource as "No organization". Don't create a folder.
- **Desktop app type** is correct for CLI/agent use. NOT "Web application".
