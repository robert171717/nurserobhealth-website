# Web Search Fallback — DuckDuckGo HTML via Terminal Curl

When `web_search` returns "Payment Required" (Firecrawl credits exhausted) or `web_extract` fails, fall back to scraping DuckDuckGo HTML directly via terminal `curl`.

## Trigger
- `web_search` returns `"Payment Required: Failed to search. Insufficient credits..."`
- `web_extract` returns the same error
- Browser tool (Camofox) is unavailable

## Fallback Command

```bash
curl -s --max-time 12 \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64)' \
  'https://html.duckduckgo.com/html/?q=URL_ENCODED_QUERY' \
  | grep -oP 'result__snippet[^>]*>\K[^<]+' \
  | head -15
```

For URLs alongside snippets:
```bash
curl -s --max-time 12 \
  -H 'User-Agent: Mozilla/5.0' \
  'https://html.duckduckgo.com/html/?q=URL_ENCODED_QUERY' \
  | grep -oP '(?<=class="result__url"[^>]*>)[^<]+' \
  | head -10
```

## URL Encoding

Replace spaces with `+` in queries. No special encoding needed for most alphanumeric queries.

## Pitfalls

- **Truncated snippets**: DDG HTML returns truncated snippet text (~50-80 chars). Use multiple targeted queries rather than one broad query.
- **Regex fragility**: The HTML class structure (`result__snippet`, `result__url`) is DDG-specific and may change. If grep returns nothing, inspect raw HTML with `curl ... | head -200`.
- **Rate limiting**: DDG HTML endpoint is low-volume. Don't fan out >5 parallel curls at once. Space calls by 1-2 seconds.
- **No date filtering**: Unlike web_search, you can't filter by date. Add `2025` or `2026` to the query string if recency matters.
- **Incomplete results**: DDG HTML returns fewer results than the API. Supplement with X API searches (`xurl search`) when topic-relevant.

## When This Fallback Won't Help

- The topic requires browsing full page content (DDG only returns snippets)
- You need structured data (pricing, tables, stats) — DDG HTML is text-only
- The query requires specific date ranges or advanced operators

## Alternative: X API via xurl

For topics with Twitter presence:
```bash
xurl search "query terms" -n 20
```

This returns full tweet text with metrics — often better than DDG snippets for real-time discussion topics.
