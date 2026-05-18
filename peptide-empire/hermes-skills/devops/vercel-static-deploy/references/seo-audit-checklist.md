# SEO Audit Checklist for Static Websites

Run this when the user asks about search engine optimization, keyword analysis, or "is my site optimized for Google/AI search."

## Quick Audit (curl-based)

```bash
# 1. Page size
curl -sL https://DOMAIN | wc -c

# 2. Structured data present?
curl -sL https://DOMAIN | grep -c 'application/ld+json'

# 3. Title tag
curl -sL https://DOMAIN | grep -oP '<title>\K[^<]+'

# 4. Meta description
curl -sL https://DOMAIN | grep -oP '<meta name="description" content="\K[^"]+'

# 5. H1 heading
curl -sL https://DOMAIN | grep -oP '<h1[^>]*>\K[^<]+'

# 6. Canonical
curl -sL https://DOMAIN | grep -oP '<link rel="canonical" href="\K[^"]+'

# 7. Robots.txt
curl -sI https://DOMAIN/robots.txt | head -1

# 8. Sitemap
curl -sI https://DOMAIN/sitemap.xml | head -1

# 9. OpenGraph image
curl -sL https://DOMAIN | grep -oP '<meta property="og:image" content="\K[^"]+'
```

## Deep Audit (Python script)

Save to /tmp and run. Parses full HTML and reports:
- Title tag length (ideal: 50-60 chars)
- Meta description length (ideal: 150-160 chars)
- Heading hierarchy (H1-H6) — flag H1 weaker than H2, missing H1, H4 misuse
- All meta tags inventory
- Canonical URL
- Structured data presence (JSON-LD, Microdata)
- Image alt text coverage
- Internal vs external link ratio
- Keyword density against target list
- Social card completeness
- Page size and script/stylesheet count

## What to Check

| Element | Ideal | Flag If |
|---------|-------|---------|
| Title tag | 50-60 chars, includes primary keyword | <40 or >70 chars, generic |
| Meta description | 150-160 chars, includes CTA | Missing or <100 chars |
| H1 | One H1, includes keywords | "just brand name", missing |
| H2-H3 | True subsections (not footer links) | H4 used for nav/footer |
| Structured data | JSON-LD present | Missing entirely |
| Canonical | Set to page URL | Missing |
| og:image | 1200x630, absolute URL | Missing |
| Sitemap | 200 OK | 404 |
| Keywords | Target terms appear naturally in body text | Missing high-value terms |

## Common Gaps Found
- No JSON-LD at all (biggest and most common gap)
- H1 is just a brand name with no descriptive keywords
- Missing og:image/twitter:image despite having social cards otherwise
- Sitemap returns 404 even if submitted to GSC
- No FAQ or Article schema on content pages
- `knowsAbout` array missing high-value search terms
