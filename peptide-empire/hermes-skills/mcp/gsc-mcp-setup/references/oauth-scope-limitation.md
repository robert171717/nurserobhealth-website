# OAuth Scope Limitation: View vs Manage

## The Problem

During the May 13, 2026 GSC OAuth setup, only the "View" scope was granted:

- ✅ `View Search Console data for your verified sites` — CHECKED
- ❌ `View and manage Search Console data for your verified sites` — NOT CHECKED

## What Works (View scope)
- All 15 analysis tools: site_snapshot, quick_wins, traffic_drops, content_gaps, check_alerts, etc.
- inspect_url
- advanced_search_analytics
- generate_report
- multi_site_dashboard

## What Doesn't Work (Manage scope required)
- submit_url
- submit_batch
- submit_sitemap
- list_sitemaps

## Error Signature
```
"Insufficient Permission" (generic 403)
```
No clear indication that the issue is OAuth scope, not property access.

## Manual Workaround (Used on May 13)
For sitemap submission specifically:
1. Go to GSC web UI → URL-prefix property
2. Sitemaps → paste sitemap URL → Submit
3. Takes 10 seconds, no re-auth needed

## Re-Auth Fix (If Manage Access Required Later)
1. Find and clear the cached OAuth token for the GSC MCP server:
   ```bash
   rm -f ~/.hermes/.gsc-oauth-token.json  # or wherever it caches
   ```
2. Restart gateway
3. Call any GSC tool → OAuth popup appears
4. This time, check BOTH boxes:
   - ✅ View Search Console data
   - ✅ View and manage Search Console data
5. Complete consent

## Why We Kept View-Only
- Analysis is the primary use case (daily briefs, SEO monitoring)
- Indexing tools can be used manually via web UI
- Broader scopes = broader risk if token is compromised
- Can always re-auth later if programmatic indexing becomes necessary
