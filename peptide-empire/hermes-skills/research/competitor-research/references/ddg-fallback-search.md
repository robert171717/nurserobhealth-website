# DuckDuckGo HTML Search Fallback

When `web_search` and `web_extract` fail (Firecrawl credit exhaustion), use terminal curl against DuckDuckGo's HTML endpoint.

## Search command

```bash
curl -s --max-time 12 -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64)" \
  "https://html.duckduckgo.com/html/?q=<URL_ENCODED_QUERY>" \
  | grep -oP "result__snippet[^>]*>\K[^<]+" | head -15
```

## How the grep pattern works

- `result__snippet` — matches the CSS class on DDG's HTML result divs
- `[^>]*>` — skips remaining attributes and the closing `>`
- `\K` — resets the match start (so only text AFTER the tag is captured)
- `[^<]+` — captures everything up to the next `<` (the snippet text)

This avoids needing lookbehind assertions (which `grep -P` handles but plain grep doesn't).

## URL encoding

Spaces → `+`, special characters → `%XX`. In practice, for simple queries, just replace spaces with `+`.

## Limitations

- Snippets are truncated (~150 chars)
- No URL extraction with this simple pattern (need separate grep for `result__url`)
- Rate limited if called too frequently (add `sleep 2` between calls if needed)
- DDG may serve different HTML structure over time — if results are empty, inspect raw HTML with `| head -100` to find the current structure
