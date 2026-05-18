# GSC MCP Server — Service Account Setup

For `suganthan-gsc-mcp` (v2.2.2+). Covers the service account path — the reliable alternative when OAuth hits Google's "unverified app" block.

## Why service account over OAuth

- **OAuth**: First tool call opens browser for Google consent. Can fail with "Access blocked: Hermes GSC has not completed Google verification" if the app isn't verified. The "Advanced → proceed anyway" link may be missing in stricter Google regions.
- **Service account**: JSON key auth, no popups, no consent screens. The service account is added as a user in GSC with Full permission. Works immediately.

## Setup (5 steps)

### 1. Google Cloud Project + API

1. [console.cloud.google.com](https://console.cloud.google.com) → New Project (e.g. `nurserob-gsc`)
2. APIs & Services → Library → search "Search Console API" → Enable
3. (Optional) Also enable "Web Search Indexing API" for `submit_url`/`submit_batch`

### 2. Service Account + JSON Key

1. ☰ → IAM & Admin → Service Accounts → + CREATE SERVICE ACCOUNT
2. Name: `hermes-gsc`, Role: Owner (needed for Indexing API)
3. Click the new account → Keys → Add Key → Create New Key → JSON
4. Save to `~/.hermes/gsc-service-account.json`, `chmod 600`

### 3. Verify Domain in GSC

1. [search.google.com/search-console](https://search.google.com/search-console) → Add Property → Domain → `yoursite.com`
2. Google gives a TXT verification string like `google-site-verification=XXXX`
3. Add TXT record at DNS provider — **check where DNS is actually managed** (may not be the hosting platform):
   ```bash
   curl -s "https://dns.google/resolve?name=yoursite.com&type=NS" | python3 -c "import sys,json; d=json.load(sys.stdin); [print(a['data']) for a in d.get('Answer',[])]"
   ```
4. Host: `@`, Type: TXT, Value: the full verification string
5. Click Verify — usually instant with most registrars

### 4. Grant Service Account Access

1. GSC → Settings → Users and permissions → ADD USER
2. Paste service account email (from JSON key's `client_email` field)
3. Permission: **Owner** (needed for Indexing API; Full suffices for read-only)
4. **If you get \"email address not found\":** This is a propagation delay — new service accounts can take 5-60 minutes before GSC recognizes them. Wait, then retry. If it persists past 1 hour, verify the email is copied exactly (no trailing spaces, correct project suffix). This was observed May 13, 2026 with `hermes-gsc@nurserob-gsc.iam.gserviceaccount.com` — the account worked for Sheets API immediately but GSC rejected it for ~30 minutes.
5. Add

### 5. Update Hermes Config

```yaml
# In ~/.hermes/config.yaml, under mcp_servers:
gsc:
  command: "npx"
  args: ["-y", "suganthan-gsc-mcp"]
  env:
    GSC_KEY_FILE: "/home/robert/.hermes/gsc-service-account.json"
    GSC_SITE_URL: "sc-domain:yoursite.com"   # domain property
    # or "https://yoursite.com/"             # URL prefix property
  timeout: 180
  connect_timeout: 60
```

Key changes from OAuth config:
- Remove `GSC_AUTH_MODE` and `GSC_OAUTH_SECRETS_FILE`
- Add `GSC_KEY_FILE` pointing to service account JSON
- Default auth mode is `service_account` — no `GSC_AUTH_MODE` needed

Then: `systemctl --user restart hermes-gateway`

## Troubleshooting

### "Insufficient Permission" on submit_url / submit_batch / submit_sitemap

This has two distinct causes:

**A) OAuth scope is "view" only.** If GSC was set up via OAuth (`GSC_AUTH_MODE: oauth`), the granted scope is `.../searchconsole.readonly`. Sitemap submission and Indexing API calls require `.../webmasters` (manage) scope. Re-authenticate with the broader scope, or switch to service account with Owner access.

**B) Service account doesn't have Owner in GSC.** The Indexing API specifically requires Owner-level permission (Full is insufficient for URL submission). Verify: GSC → Settings → Users and permissions → the service account email → Permission: **Owner**.

### "email address not found" when adding service account to GSC

Propagation delay. New service accounts can take 5-60 minutes before GSC's user directory recognizes them. Wait and retry. Verified: `hermes-gsc@nurserob-gsc.iam.gserviceaccount.com` (created May 13, 2026) was rejected for ~30 minutes, then worked for Sheets API immediately, and worked for GSC after the delay. If it persists past 1 hour, double-check the email is copied exactly from the JSON key's `client_email` field.

### "User does not have sufficient permission for site"

1. Verify the service account email appears in GSC → Settings → Users with "Full" (not "Restricted")
2. Check property type matches: `sc-domain:` for domain properties, `https://...` for URL prefix
3. Permission propagation can take 1-5 minutes
4. Try listing sites directly from the API to confirm what the service account can see

### "MCP server 'gsc' is unreachable"

Wait 10-15s after gateway restart for MCP server initialization. Check `~/.hermes/logs/mcp-stderr.log`.

### Indexing API tools (submit_url, etc.)

Requires "Web Search Indexing API" enabled AND service account must have Owner-level (not just Full) in GSC.

### Sitemap stuck on "couldn't fetch" (grayed-out dots menu)

If GSC shows a submitted sitemap with status "couldn't fetch" / "General HTTP error" and the three-dots menu is grayed out:

1. **Do NOT try to delete it** — the menu is disabled when stuck
2. Go to Sitemaps page → "Add a new sitemap" field at the top
3. Paste the **full URL** (e.g. `https://yoursite.com/sitemap.xml` — NOT just `sitemap.xml`)
4. Click Submit → creates a fresh submission, triggers immediate fetch
5. The old broken entry can stay — it won't interfere

Google caches the first failed fetch and won't retry a stuck entry. Adding it again as a "new" sitemap bypasses the cache.
