# Nurse Rob Website Content Page Template

Pattern for building SEO-optimized content pages on `nurserobhealth.com`. The site is a static HTML site deployed via Vercel + GitHub (repo: `robert171717/nurserobhealth-website`). Local source lives at `/mnt/c/Users/Robert/Desktop/nurserobhealth-website/`.

## Site Architecture

| File | Route | Purpose |
|------|-------|---------|
| `index.html` | `/` | Homepage (about, FAQ, services, resources) |
| `wolverine-stack.html` | `/wolverine-stack` | Wolverine Stack guide + calculator |
| `bpc-157-guide.html` | `/bpc-157-guide` | BPC-157 deep dive |
| `tb-500-guide.html` | `/tb-500-guide` | TB-500 deep dive + BPC-157 comparison |
| `vercel.json` | — | Rewrite rules (clean URLs → `.html` files) |
| `sitemap.xml` | `/sitemap.xml` | All page URLs + priorities |
| `robots.txt` | `/robots.txt` | Allows all crawlers |
| `guide.pdf` | `/guide.pdf` | Downloadable PDF guide |
| `og-card.jpg` | `/og-card.jpg` | Open Graph share image |

## Adding a New Content Page

### 1. Create the HTML file

Copy structure from `bpc-157-guide.html` or `tb-500-guide.html`. Required sections:

```html
<!-- HEAD: SEO metadata -->
<title>PAGE TITLE with Keywords | Nurse Rob, RN</title>
<meta name="description" content="DESCRIPTION with target keywords">
<!-- Open Graph tags -->
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:url" content="https://nurserobhealth.com/PAGE-SLUG">
<meta property="og:image" content="https://nurserobhealth.com/og-card.jpg">
<!-- Twitter tags -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="...">
<meta name="twitter:image" content="https://nurserobhealth.com/og-card.jpg">
<link rel="canonical" href="https://nurserobhealth.com/PAGE-SLUG">

<!-- JSON-LD: Article + FAQPage schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Article",
      "headline": "...",
      "author": { "@type": "Person", "name": "Nurse Rob", "honorificSuffix": "RN" },
      "publisher": { "@type": "Organization", "name": "Nurse Rob Health" },
      "datePublished": "YYYY-MM-DD",
      "dateModified": "YYYY-MM-DD"
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        { "@type": "Question", "name": "...", "acceptedAnswer": { "@type": "Answer", "text": "..." } }
      ]
    }
  ]
}
</script>

<!-- Tailwind config: navy/teal/gold colors -->
<!-- NAV: consistent across all pages, highlight current page -->
<!-- HERO: gradient bg, H1 with teal underline, CTA buttons -->
<!-- MAIN CONTENT: sections with H2 headers -->
<!-- CTA section: dark card with calculator + consult buttons -->
<!-- FOOTER: minimal, disclaimer -->
```

### 2. Add Vercel rewrite rule

In `vercel.json`, add:
```json
{ "source": "/PAGE-SLUG", "destination": "/PAGE-SLUG.html" }
```

### 3. Add to sitemap.xml

```xml
<url>
  <loc>https://nurserobhealth.com/PAGE-SLUG</loc>
  <lastmod>YYYY-MM-DD</lastmod>
  <changefreq>weekly</changefreq>
  <priority>0.9</priority>
</url>
```

### 4. Update nav on ALL existing pages

Every page's `<nav>` needs the new link. The current page gets `class="text-teal font-semibold text-sm border-b border-teal"`, others get `class="text-white/70 hover:text-white transition text-sm font-medium"`.

### 5. Deploy

```bash
cd /mnt/c/Users/Robert/Desktop/nurserobhealth-website
git add -A
git commit -m "Add PAGE-SLUG content page"
git push origin main
# Vercel auto-deploys on push to main
```

## SEO Checklist Per Page

- [ ] Title tag: 50-60 chars, primary keyword first
- [ ] Meta description: 120-160 chars, includes CTA
- [ ] H1: matches title, includes keyword
- [ ] H2s: outline structure, keyword variants
- [ ] Open Graph tags: title, description, image, URL
- [ ] Twitter card: summary_large_image
- [ ] Canonical URL: absolute, no trailing slash inconsistency
- [ ] JSON-LD: Article + FAQPage (for rich snippets)
- [ ] Internal links: 2-3 links to other site pages
- [ ] External links: X profile, cal.com booking
- [ ] CTA: clear next action (calculator, consult, PDF)
- [ ] Mobile: Tailwind responsive classes, no fixed widths

## Content Structure Template

```
1. WHAT IT IS — Definition, origin, key facts
2. HOW IT WORKS — Mechanism, 2x2 grid of key actions
3. BENEFITS — 4 research-backed benefits with citations
4. [Optional: COMPARISON TABLE if comparing to another peptide]
5. DOSING — Standard + Recovery protocols, 2-column grid
6. SAFETY — RN safety flags, contraindicated groups, side effects
7. INJECTION GUIDE — 3-step visual, checklist
8. CTA — Dark card: "Get Your Personalized Protocol"
```

## Gotchas

- **Trailing slash canonical:** Google treats `https://site.com` and `https://site.com/` as different. Match the canonical to what GSC shows as the indexed version.
- **Empty H1s:** Check after generating — `<h1>  </h1>` with only whitespace/children is a real SEO issue.
- **Sitemap timing:** New sitemap submissions take days to weeks to process. Don't expect instant indexing.
- **GSC Indexing API:** Requires service account with **Owner** permission (not Full). Submit individual URLs via `submit_batch` for faster indexing than waiting for sitemap crawl.
- **Mobile usability:** No GSC mobile verdict by default on new pages — Google needs to crawl first.
