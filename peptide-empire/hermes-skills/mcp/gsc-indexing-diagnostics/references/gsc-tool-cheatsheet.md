# GSC MCP Tool Reference

Quick parameter reference for the Google Search Console MCP tools. All return live GSC API data.

## Diagnostic Tools

### site_snapshot
Quick overview of site performance with period comparison.
```
mcp_gsc_site_snapshot(days=28)
```
Returns: clicks, impressions, CTR, position — current period vs. prior, plus % changes.

### list_sitemaps
All submitted sitemaps with status.
```
mcp_gsc_list_sitemaps()
```
Returns: sitemap URLs, lastSubmitted, errors, warnings, submitted/indexed counts per type.
**WARNING**: "indexed" count has reporting lag — trust individual inspect_url calls instead.

### inspect_url
Check if a specific URL is indexed and why/why not.
```
mcp_gsc_inspect_url(url="https://example.com/page")
```
Returns: indexed (bool), indexingState, lastCrawlTime, crawlAllowed, indexingAllowed, googleCanonical, userCanonical, issues[], mobileUsability.
This is the **source of truth** for indexing status.

### check_alerts
Position drops, CTR collapses, click losses, disappeared pages.
```
mcp_gsc_check_alerts(days=7, position_drop_threshold=20, ctr_drop_threshold=50, click_drop_threshold=30)
```
Returns: severity-rated alerts (critical/warning/info), matched against configurable thresholds.

## Opportunity Tools

### quick_wins
Keywords at positions 4-15 with high impressions — near page-one candidates.
```
mcp_gsc_quick_wins(days=28, min_impressions=100, max_position=15)
```

### ctr_opportunities
Pages with high impressions but CTR below expected for their position.
```
mcp_gsc_ctr_opportunities(days=28, min_impressions=500)
```

### ctr_vs_benchmark
CTR comparison against industry benchmarks by position.
```
mcp_gsc_ctr_vs_benchmark(days=28, min_impressions=200)
```

### content_gaps
Queries with impressions but ranking beyond a position threshold (unmet demand).
```
mcp_gsc_content_gaps(days=90, min_impressions=50, min_position=20)
```

## Problem Detection Tools

### traffic_drops
Pages losing the most traffic, with root cause diagnosis (ranking loss/CTR collapse/demand decline).
```
mcp_gsc_traffic_drops(days=28)
```

### content_decay
Pages with consistent traffic decline over 3 consecutive 30-day periods.
```
mcp_gsc_content_decay()
```

### cannibalization_check
Keywords where multiple pages compete against each other.
```
mcp_gsc_cannibalization_check(days=28, min_impressions=50)
```

## Indexing Actions

### submit_url / submit_batch
Request crawling via Indexing API. 200 URL daily quota.
```
mcp_gsc_submit_url(url="https://example.com/page", action="URL_UPDATED")
mcp_gsc_submit_batch(urls=["..."], action="URL_UPDATED")
```

### submit_sitemap
Notify Google of a new/updated sitemap.
```
mcp_gsc_submit_sitemap(sitemap_url="https://example.com/sitemap.xml")
```

## Advanced Analysis

### advanced_search_analytics
Custom query with flexible dimensions and filters.
```
mcp_gsc_advanced_search_analytics(days=28, dimensions=["query","page"], filters=[...], row_limit=100)
```

### topic_cluster_performance
Aggregate performance for a group of pages matching a URL path.
```
mcp_gsc_topic_cluster_performance(path_pattern="/blog/seo", days=28)
```

### content_recommendations
Cross-references quick wins, content gaps, and cannibalization for prioritized actions.
```
mcp_gsc_content_recommendations(days=28, max_recommendations=10)
```

### generate_report
Comprehensive markdown report saved to disk.
```
mcp_gsc_generate_report(days=28, output_path="./gsc-report.md")
```

### multi_site_dashboard
Health check across multiple GSC properties.
```
mcp_gsc_multi_site_dashboard(site_urls=["https://site1.com/","https://site2.com/"], days=28)
```
