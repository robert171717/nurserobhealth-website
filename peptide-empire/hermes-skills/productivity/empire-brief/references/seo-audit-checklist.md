# SEO Audit Checklist for nurserobhealth.com

Run this when auditing the Nurse Rob website for search engine optimization.

## Quick Audit (curl + grep)

```bash
# 1. Title tag
curl -sL https://nurserobhealth.com | grep -oP '<title>\K[^<]+'

# 2. Meta description
curl -sL https://nurserobhealth.com | grep -oP '<meta name="description" content="\K[^"]+'

# 3. H1
curl -sL https://nurserobhealth.com | grep -oP '<h1[^>]*>\K[^<]+'

# 4. All headings (structure check)
curl -sL https://nurserobhealth.com | grep -oP '<h[1-6][^>]*>[^<]+' | sort

# 5. Structured data presence
curl -sL https://nurserobhealth.com | grep -c 'application/ld+json'

# 6. Robots.txt
curl -sI https://nurserobhealth.com/robots.txt | head -1

# 7. Sitemap
curl -sI https://nurserobhealth.com/sitemap.xml | head -1

# 8. Canonical
curl -sL https://nurserobhealth.com | grep -oP '<link rel="canonical" href="\K[^"]+'
```

## Full Audit (Python — write to /tmp first, python3 -c is blocked)

See `scripts/seo-audit.py` for the comprehensive audit script.

## Checklist

| Element | Target | Our Status (May 14, 2026) |
|---------|--------|---------------------------|
| Title tag | 50-60 chars, keyword-rich | ✅ 54 chars, "Nurse Rob, RN — Licensed Peptide Educator & Consultant" |
| Meta description | 150-160 chars | ✅ 155 chars, mentions RN + peptide + consultation |
| H1 | One per page, primary keyword | ⚠️ Just "Nurse Rob, RN" — too sparse |
| H2-H6 hierarchy | Logical nesting | ⚠️ H4 used for footer links (semantically wrong) |
| Structured data | JSON-LD Organization + Person | ❌ None — template at `templates/json-ld-structured-data.html` |
| OpenGraph | og:title, og:description, og:image, og:url | ✅ Complete |
| Twitter Card | summary_large_image + @handle | ✅ Complete |
| Canonical URL | Set correctly | ✅ `https://nurserobhealth.com` |
| Robots.txt | Present, allows crawling | ✅ 200 OK |
| Sitemap.xml | Present, submitted to GSC | ❌ 404 |
| Mobile viewport | Responsive meta tag | ✅ Set |
| Image alt text | Descriptive on all `<img>` | ⚠️ No `<img>` tags (canvas/SVG site) |
| Page size | <100KB | ✅ 38KB |
| HTTPS | Forced | ✅ (Vercel handles) |

## Missing High-Value Keywords

These get search volume but aren't on the homepage:
- "peptide therapy", "peptide stack for healing", "semaglutide consulting"
- "tirzepatide", "ghk-cu", "ipamorelin", "cjc-1295", "bodybuilding peptides"
- "anti-aging peptides", "peptide injection guide", "peptide mixing calculator"

## Site Architecture Notes

- **Single-page app**: All content on one page with anchor sections (#about, #services, #resources)
- **Lead form**: Formspree `xnjwaowp` embedded in #resources section — working
- **No subpages**: `/wolverine-stack-calculator` returns 404 (correct — it's a section, not a page)
- **Implication**: Only 1 page can rank. AI search engines (Perplexity, ChatGPT, Claude) have very little content to crawl and cite. A separate `/wolverine-stack` content page would dramatically improve AI visibility.

## AI Search Engine Optimization

AI crawlers (Perplexity, ChatGPT, Claude, Grok) prioritize:
1. **Structured data** (JSON-LD) — tells them who you are
2. **Content depth** — separate pages with 300+ words per topic
3. **Fresh content** — blog, guides, FAQ pages on your domain (not just X posts)
