---
name: gsc-indexing-diagnostics
description: Diagnose why pages aren't indexed in Google Search Console — sitemap analysis, URL inspection, redirect detection, and false-alarm identification.
category: mcp
tags: [seo, gsc, mcp, indexing, sitemap]
---

# GSC Indexing Diagnostics

Systematic diagnosis of Google Search Console indexing issues. Use when the user gets a GSC email about indexing problems, sees pages not appearing in search results, or discovers sitemap discrepancies.

## Triggers

- User forwards a GSC email (e.g., "Page with redirect," "Crawled - currently not indexed," "Discovered - currently not indexed")
- User asks "why aren't my pages indexed?"
- Sitemap shows submitted count > indexed count
- Post-launch indexing verification

## Diagnostic Workflow (in order)

### 1. Big-picture scan

Start with three parallel calls:
```
mcp_gsc_site_snapshot(days=7)
mcp_gsc_list_sitemaps()
mcp_gsc_check_alerts(days=7)
```

The site snapshot shows if there's any traffic at all. The sitemap shows submitted vs. indexed counts. Alerts surface ranking/CTR drops — but for new sites they'll usually be empty.

### 2. Get the sitemap contents

```bash
curl -s https://<domain>/sitemap.xml
```

This gives you the exact list of URLs Google knows about, so you can inspect each one.

### 3. Inspect every sitemap URL individually

Use `mcp_gsc_inspect_url(url=...)` on each URL from the sitemap. Do NOT trust the sitemap's aggregate "indexed" count — it has reporting lag (can show 0 indexed when pages are actually indexed). Individual URL inspection returns live data.

For each URL, record:
- `indexingState`: "Submitted and indexed" = good
- `lastCrawlTime`: when Google last visited
- `issues[]`: any fetch/indexing problems

### 4. HTTP status verification

For URLs showing issues, verify they're actually reachable:

```bash
curl -s -o /dev/null -w "HTTP %{http_code} | redirect: %{redirect_url} | type: %{content_type}" "$URL"
```

Check for:
- 200 vs. 301/302/308 redirects
- Correct content-type (text/html, application/pdf, etc.)
- Redirect chains (unexpected intermediate hops)

### 5. Check for redirect variants

The most common "page with redirect" false alarm is HTTP→HTTPS redirects (Vercel does 308 by default). Check:

```bash
for url in \
  "http://<domain>/" \
  "http://www.<domain>/" \
  "https://www.<domain>/"; do
  curl -s -o /dev/null -w "HTTP %{http_code} → %{redirect_url}" --max-redirs 0 "$url"
done
```

HTTP→HTTPS redirects are **expected and correct**. Google will index the HTTPS destination instead. This is not a real problem.

### 6. Check page HTML for issues

```bash
curl -s "$URL" | grep -iE '(http://|canonical|href=|src=)'
```

Verify:
- All internal links use relative paths or HTTPS (no `http://`)
- Canonical tag points to the correct HTTPS URL
- No mixed content (HTTP resources on HTTPS pages)

### 7. Check deployment config

For Vercel sites, check `vercel.json`:
```
read_file(path="<project>/vercel.json")
```

Look for:
- **rewrites** (server-side, URL doesn't change — good)
- **redirects** (client-side, URL changes — these generate the "page with redirect" notice)

Rewrites are preferred for clean URLs. Redirects are fine for HTTP→HTTPS but will trigger GSC notices.

## Common GSC Email Patterns

| Email Subject | Real Issue? | Action |
|---|---|---|
| "Page with redirect" | Usually false alarm (HTTP→HTTPS) | Verify redirects are intentional, ignore if so |
| "Crawled - currently not indexed" | Maybe — quality/content issue | Check page content, wait and re-submit |
| "Discovered - currently not indexed" | Usually timing for new sites | Wait, re-submit sitemap after 1 week |
| "Server error (5xx)" | Real problem | Check deployment logs immediately |
| "Not found (404)" | Real problem | Fix broken links or add redirects |

## Critical Pitfalls

### DO NOT trust sitemap aggregate counts
The "submitted/indexed" numbers in `mcp_gsc_list_sitemaps()` have significant reporting lag (can be 24-48 hours behind). Always verify with individual `mcp_gsc_inspect_url()` calls. A sitemap showing "0 indexed" when pages were just crawled is normal.

### DO NOT act on "page with redirect" emails without checking
HTTP→HTTPS redirects (Vercel's 308 default) trigger this email. It's informational — Google indexes the HTTPS destination. Only act if pages are redirecting to unexpected destinations or there's a redirect chain.

### DO NOT panic about 0 traffic on new sites
4 impressions in 7 days for a site launched within the last month is normal. SEO takes time (months, not days).

## References

- `references/gsc-tool-cheatsheet.md` — Quick reference for MCP GSC tools and their parameters
