---
name: gsc-mcp-setup
description: Set up Google Search Console MCP integration (suganthan-gsc-mcp) — Google Cloud project, service account, DNS verification, Hermes config, and common pitfalls.
---

# GSC MCP Setup — Google Search Console MCP Integration

20 SEO analysis tools via `suganthan-gsc-mcp` (v2.2.2+). Three auth modes — use own-project OAuth (Path C) for fastest setup, service account (Path A) for headless/cron.

## Auth Mode Comparison

| Mode | Speed | Reliability | Best For |
|------|-------|-------------|----------|
| **Own-Project OAuth (Path C)** | ⚡ ~4 min | ✅ Most reliable | New setups, personal projects |
| **Service Account (Path A)** | 🐢 ~30-60 min | ⚠️ Propagation delay | Production, headless environments |
| **Public OAuth (Path B)** | 🚫 Often blocked | ❌ Don't use | Only if Advanced link appears |

**Recommendation:** Start with Path C (own-project OAuth). It's fast, reliable, and uses credentials YOU control. Only switch to Path A (service account) if you need headless operation (e.g., cron jobs that can't open a browser). Never use Path B — Google blocks it most of the time.

## Service Account Setup (Path A — Headless/Cron)

### 1. Google Cloud Project
- Go to [console.cloud.google.com](https://console.cloud.google.com)
- Create a project (e.g., `nurserob-gsc`)

### 2. Enable Search Console API
- **APIs & Services → Library** → search "Search Console API" → **Enable**

### 3. Create Service Account
- **IAM & Admin → Service Accounts → + CREATE SERVICE ACCOUNT**
- Name: `hermes-gsc`, role: **Owner** (needed for Indexing API)
- After creation: click account → **Keys → Add Key → Create New Key → JSON** → downloads key file

### 4. Copy Key to Hermes
```bash
cp ~/Downloads/your-key.json ~/.hermes/gsc-service-account.json
chmod 600 ~/.hermes/gsc-service-account.json
```

### 5. Add Service Account to GSC Property
- The JSON contains `client_email` (e.g., `hermes-gsc@project-id.iam.gserviceaccount.com`)
- **[Google Search Console](https://search.google.com/search-console)** → select property → **Settings → Users and permissions → ADD USER**
- Paste the email → **Owner** permission (not Full — Indexing API write operations like `submit_url`, `submit_batch`, `submit_sitemap` require Owner; Full is read-only for those endpoints)
- If the URL-prefix property and domain property both exist, add the service account to BOTH

**⚠️ PITFALL — "email address not found" when adding service account to GSC:** GSC's web UI maintains its own user directory that lags behind Google Cloud IAM by 30-60 minutes for new service accounts. The service account IS valid (tested: it gets OAuth API tokens immediately), but GSC's user-add dialog can't find it yet. **Don't wait — switch to Path C (own-project OAuth) instead.** You'll be back in ~4 minutes. If you must use service account, retry the ADD USER step every 15 minutes until it appears.

### 6. Hermes Config
```yaml
gsc:
    command: "npx"
    args: ["-y", "suganthan-gsc-mcp"]
    env:
      GSC_KEY_FILE: "/home/robert/.hermes/gsc-service-account.json"
      GSC_SITE_URL: "sc-domain:yoursite.com"   # Domain property
    timeout: 180
    connect_timeout: 60
```

**Site URL formats:**
- Domain property (recommended): `sc-domain:nurserobhealth.com`
- URL prefix property: `https://nurserobhealth.com/`

Check which type your GSC property is at the top of the dashboard ("Domain property" vs "URL prefix").

**Default auth mode is `service_account`** — do NOT set `GSC_AUTH_MODE` when using a key file. Only set it to `oauth` when using OAuth mode.

**⚠️ PITFALL — switching between service account and OAuth:** When flipping config from service account back to OAuth, you MUST explicitly set `GSC_AUTH_MODE: "oauth"` AND provide `GSC_OAUTH_SECRETS_FILE`. Simply removing `GSC_KEY_FILE` is not enough — the default auth mode is `service_account` and the server will fail silently. Also remove `GSC_KEY_FILE` to avoid confusion.

## OAuth Setup (Path B — Public OAuth, fragile)

```yaml
    env:
      GSC_AUTH_MODE: "oauth"
      GSC_OAUTH_SECRETS_FILE: "/home/robert/.hermes/gsc-oauth-secrets.json"
      GSC_SITE_URL: "sc-domain:yoursite.com"
```

**⚠️ PITFALL — "Access blocked: has not completed Google verification":** The public `suganthan-gsc-mcp` OAuth app is unverified. Google shows a warning — look for tiny "Advanced" link at bottom → "Go to Hermes GSC (unsafe)". If "Advanced" is missing, Google fully blocks it. In that case, skip to Path C (own-project OAuth) — it's the fast path that actually works.

## Own-Project OAuth (Path C — Fastest, Most Reliable)

**TL;DR:** Create your OWN OAuth credentials inside the same Google Cloud project you used for the service account. Since you own the app, Google won't show the unverified-app block. Takes ~4 minutes.

### C1. Configure OAuth Consent Screen
1. **APIs & Services → OAuth consent screen**
2. Click **Get Started** (if first time)
3. **App name:** `Hermes GSC`
4. **User support email:** your email
5. **Developer contact:** your email
6. Click **SAVE AND CONTINUE**
7. **Scopes page:** click **SAVE AND CONTINUE** (skip — not publishing)
8. **Test users page:** click **SAVE AND CONTINUE** for now (we'll come back)

### C2. Create OAuth Client ID
1. **Credentials → + CREATE CREDENTIALS → OAuth client ID**
2. Application type: **Desktop app**
3. Name: `hermes-gsc-oauth`
4. Click **CREATE** → download JSON

### C3. Copy Key to Hermes
```bash
cp ~/Downloads/client_secret_*.json ~/.hermes/gsc-oauth-secrets.json
chmod 600 ~/.hermes/gsc-oauth-secrets.json
```

### C4. Add Yourself as Test User
**⚠️ REQUIRED** — even though you own the app, it stays in "Testing" mode. You MUST add your own email:
1. **APIs & Services → OAuth consent screen → Audience tab**
2. Scroll to **Test users** section (below "Publishing status" and "User type")
3. **+ ADD USERS** → type your Gmail → **SAVE**
4. **⚠️ PITFALL — Google UI quirk:** Type the email, hit SAVE, then wait. If nothing appears, hit SAVE a second time. Google's OAuth console sometimes ignores the first click on the save button for test users. You know it worked when the email appears in the test users list immediately (not after refresh).

### C5. Hermes Config
```yaml
    env:
      GSC_AUTH_MODE: "oauth"
      GSC_OAUTH_SECRETS_FILE: "/home/robert/.hermes/gsc-oauth-secrets.json"
      GSC_SITE_URL: "sc-domain:yoursite.com"
```

### C6. Authenticate
Gateway restart → call any GSC tool → browser popup → sign in with your Google account → approve. Token caches automatically after first consent.

**⚠️ PITFALL — IAM notification is a red herring:** During OAuth setup, Google Cloud may show a notification: "Grant principals access to this resource — Nurse Rob GSC." This is an unrelated IAM prompt for the Cloud project itself. Ignore it. You don't need to add IAM roles to anyone. The only place you need to add users is the OAuth consent screen → Audience → Test users.

**⚠️ PITFALL — New sites show zero data:** If the site was just verified in GSC, `site_snapshot` and all analysis tools will return zeros (0 clicks, 0 impressions). This is EXPECTED — Google hasn't accumulated search data yet. Verify the integration works with `inspect_url` for the homepage instead, which returns indexing status regardless of traffic. Search data starts populating within days to weeks as Google crawls and ranks pages.

**Why Path C beats Path A (service account):** Service accounts sometimes take up to an hour to appear in Google's user directory, blocking the GSC "ADD USER" step. Path C bypasses this entirely — the OAuth popup authenticates YOU, who already owns the GSC property. No service-account propagation delay.

**Why Path C beats Path B (public OAuth):** Path B uses the npm package author's OAuth app, which Google flags as unverified and often fully blocks. Path C uses YOUR app — you're the developer and test user, so Google allows it.

## DNS Verification (Domain Property)

If you're adding a new domain property to GSC:

1. Choose **Domain** (not URL prefix) → enter `domain.com`
2. GSC provides a TXT record: `google-site-verification=<string>`
3. Add it at your DNS provider:
   - **Type:** TXT
   - **Host:** `@` (or blank for root)
   - **Value:** `google-site-verification=<string>`
4. Click **Verify** in GSC

Hosting-specific DNS paths:
- **Porkbun:** Domain Management → select domain → DNS → + ADD RECORD → TXT
- **Vercel:** Settings → Domains → DNS → Add Record → TXT

## Multi-Site

For multiple GSC properties:
```yaml
      GSC_SITE_URL: "sc-domain:primary.com"
      GSC_SITE_URLS: "sc-domain:primary.com,sc-domain:secondary.com"
```

## Testing

After gateway restart, verify with:
```
mcp_gsc_site_snapshot(days=7)
```

**⚠️ PITFALL — "User does not have sufficient permission":**
1. Check the service account appears in GSC → Settings → Users and permissions
2. Verify permission is "Full" not "Restricted"
3. Wait for propagation (new service accounts: up to 1 hour)
4. Check the site URL format matches the property type (sc-domain vs https://)

## Available Tools (20)

| Category | Tools |
|----------|-------|
| **Analysis** | `site_snapshot`, `quick_wins`, `ctr_opportunities`, `traffic_drops`, `content_gaps`, `cannibalization_check`, `content_decay`, `topic_cluster_performance`, `ctr_vs_benchmark`, `inspect_url`, `check_alerts`, `content_recommendations`, `advanced_search_analytics`, `generate_report`, `multi_site_dashboard` |
| **Indexing** | `submit_url`, `submit_batch`, `submit_sitemap`, `list_sitemaps` |
| **Safety** | `verify_claim` |

## Sitemap / Indexing API Limitations

**Domain properties (sc-domain:*) do NOT support the Sitemaps API** — you'll get "Insufficient Permission" even with correct auth. Workarounds:

1. **Manual submission (fastest):** In GSC web UI, go to the URL-prefix property → Sitemaps → paste sitemap URL → Submit. Takes 10 seconds.
2. **API submission:** Temporarily switch `GSC_SITE_URL` to `https://yoursite.com/` (URL-prefix format), restart gateway, submit sitemap, switch back. Requires URL-prefix property to be added and verified in GSC first.
3. **URL-prefix auto-verification:** If the domain property is already verified, adding `https://yoursite.com/` as a URL-prefix property auto-verifies instantly — no extra DNS step needed.

**OAuth scope warning:** Sitemap/indexing tools require "Manage" scope. If you only granted "View" during OAuth consent, indexing calls will fail with "Insufficient Permission." To fix: clear OAuth cache and re-authenticate with both checkboxes checked.

**Consent screen audience type:** Choose **External** (not Internal) during OAuth consent screen setup. Internal requires Google Workspace org — personal Gmail accounts won't work. The app stays in "Testing" mode regardless (no verification needed).

## References
- Package: `suganthan-gsc-mcp` (npm) — `npx -y suganthan-gsc-mcp`
- Homepage: https://suganthan.com/blog/google-search-console-mcp-server/
- GitHub: https://github.com/suganthanmn/Suganthans-GSC-MCP
- `references/debugging-flow.md` — Full error chain from 2026-05-13 auth debugging session
- `references/navigation-dead-ends.md` — Console navigation pitfalls (OAuth consent screen redirects to metrics, Audience tab location, "Save twice" test-user quirk)
- `references/oauth-scope-limitation.md` — View vs Manage scope: which tools require which, and the manual sitemap workaround
- `references/nurserob-site-content-pattern.md` — Nurse Rob website content page template: HTML structure, JSON-LD, Vercel rewrites, sitemap integration, deploy flow
