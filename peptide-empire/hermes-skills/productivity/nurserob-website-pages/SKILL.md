---
name: nurserob-website-pages
description: Build HTML pages for nurserobhealth.com — two-tier funnel system (visible product pages + hidden SEO guides), Nurse Rob branding, Formspree forms, and mobile-first navigation.
---

# Nurse Rob Website Page Builder

Build production HTML pages for the Nurse Rob Health peptide education website (nurserobhealth.com). Every page follows a strict two-tier funnel system and must include mobile navigation.

## Trigger conditions
- User asks to build/add a new peptide page, guide page, or comparison page for nurserobhealth.com
- User asks to expand the site with new content pages
- Any task involving writing new .html files in the website source directory

## Website source
`/mnt/c/Users/Robert/Desktop/nurserobhealth-website/` (git → Vercel auto-deploy)

## Two-Tier Funnel System

Every peptide gets TWO pages:

| Tier | URL Pattern | Nav Visible? | Length | Purpose |
|------|------------|--------------|--------|---------|
| Product Page | `/peptide-name` | ✅ Yes | ~300-700 lines | Conversion-focused landing page with dosing, benefits, CTAs |
| SEO Guide | `/peptide-name-guide` | ❌ No (hidden) | ~600+ lines | Long-form educational content for Google ranking. Funnels to email capture. |

Comparison pages (e.g., BPC-157 vs TB-500) are hybrids — visible, comprehensive, no separate hidden guide.

## Brand Requirements (NON-NEGOTIABLE)
- Colors: navy #0A1F3F bg, teal #00C4B4 accent, gold #C9A84C
- Fonts: Inter + JetBrains Mono via Google Fonts CDN
- Tailwind CSS via CDN (`<script src="https://cdn.tailwindcss.com"></script>`)
- Tailwind config must define: navy:{950:'#080E1A',900:'#0A1F3F',800:'#0D2B54'}, teal:{DEFAULT:'#00C4B4',dark:'#009E91'}, gold:'#C9A84C', cream:'#FFF8F0', muted:'#64748B', body:'#1E293B', offwhite:'#F7F9FB'
- All forms POST to: `https://formspree.io/f/xnjwaowp`
- Consult booking: `https://cal.com/nurserob/peptide-consult`

## Mobile Menu (CRITICAL — DO NOT SKIP)

**Every page MUST have a mobile hamburger menu.** The user tests on iPhone first. Missing mobile menus are the #1 bug.

**ALL 10 pages must use the identical standardized nav.** After any page change, run the audit script to verify consistency.

### Standardized Desktop Nav (10 items — use on EVERY page)

```html
<!-- NAV -->
<nav class="fixed top-0 left-0 right-0 z-50 bg-navy-900/95 backdrop-blur-xl border-b border-white/5">
  <div class="max-w-7xl mx-auto px-6 lg:px-12 flex items-center justify-between" style="height:72px">
    <a href="/" class="text-white font-bold text-lg flex items-center gap-1" aria-label="Nurse Rob, RN home">
      Nurse <span class="border-b-2 border-teal">Rob</span>, RN
    </a>
    <div class="hidden md:flex items-center gap-6">
      <a href="/#about" class="text-white/70 hover:text-white transition text-sm font-medium">About</a>
      <a href="/#faq" class="text-white/70 hover:text-white transition text-sm font-medium">FAQ</a>
      <a href="/bpc-157-guide" class="text-white/70 hover:text-white transition text-sm font-medium">BPC-157</a>
      <a href="/tb-500-guide" class="text-white/70 hover:text-white transition text-sm font-medium">TB-500</a>
      <a href="/semaglutide" class="text-white/70 hover:text-white transition text-sm font-medium">Semaglutide</a>
      <a href="/tirzepatide" class="text-white/70 hover:text-white transition text-sm font-medium">Tirzepatide</a>
      <a href="/bpc-157-vs-tb-500" class="text-white/70 hover:text-white transition text-sm font-medium">Comparison</a>
      <a href="/wolverine-stack" class="text-white/70 hover:text-white transition text-sm font-medium">Wolverine Stack</a>
      <a href="https://cal.com/nurserob/peptide-consult" target="_blank" rel="noopener" class="bg-teal hover:bg-teal-dark text-white font-semibold px-5 py-2.5 rounded-full text-sm hover:scale-105 transition-all duration-200">Book a Consult →</a>
    </div>
    <button id="menu-btn" class="md:hidden flex items-center justify-center w-11 h-11 text-white" aria-label="Open menu" aria-expanded="false">
      <span class="flex flex-col gap-1.5"><span class="block w-6 h-0.5 bg-white rounded-full"></span><span class="block w-6 h-0.5 bg-white rounded-full"></span><span class="block w-6 h-0.5 bg-white rounded-full"></span></span>
    </button>
  </div>
</nav>
```

**Active state:** On the current page's own nav link, replace `text-white/70 hover:text-white transition text-sm font-medium` with `text-teal font-semibold border-b border-teal`. Every other link stays inactive.

### Standardized Mobile Menu (use identical on EVERY page)

```html
<!-- MOBILE MENU -->
<div id="mobile-menu" class="mobile-menu-panel fixed inset-0 bg-navy-900 backdrop-blur-xl z-[60] flex flex-col items-center justify-center gap-8 md:hidden" role="dialog" aria-hidden="true">
  <button id="menu-close" class="absolute top-6 right-6 w-11 h-11 flex items-center justify-center text-white text-3xl leading-none" aria-label="Close menu">×</button>
  <a href="/" class="text-white text-xl font-medium menu-link">Home</a>
  <a href="/#about" class="text-white text-xl font-medium menu-link">About</a>
  <a href="/bpc-157-guide" class="text-white text-xl font-medium menu-link">BPC-157</a>
  <a href="/tb-500-guide" class="text-white text-xl font-medium menu-link">TB-500</a>
  <a href="/semaglutide" class="text-white text-xl font-medium menu-link">Semaglutide</a>
  <a href="/tirzepatide" class="text-white text-xl font-medium menu-link">Tirzepatide</a>
  <a href="/bpc-157-vs-tb-500" class="text-white text-xl font-medium menu-link">BPC vs TB-500</a>
  <a href="/wolverine-stack" class="text-white text-xl font-medium menu-link">Wolverine Stack</a>
  <a href="https://cal.com/nurserob/peptide-consult" target="_blank" rel="noopener" class="bg-teal hover:bg-teal-dark text-white font-semibold px-8 py-3 rounded-full text-lg menu-link">Book a Consult →</a>
</div>
```

**Mobile active state:** On the current page's link, replace `text-white font-medium` with `text-teal font-semibold`.

### Step 3: Add CSS
In the `<style>` block, AFTER the body rule:
```css
body.menu-open { overflow: hidden; }
.mobile-menu-panel { display: none !important; }
.mobile-menu-panel.open { display: flex !important; }
```

### Step 4: Add JavaScript
At the bottom of the page, BEFORE `</body>`:
```js
// Mobile menu toggle
(function() {
  var menuBtn = document.getElementById('menu-btn');
  var menuClose = document.getElementById('menu-close');
  var mobileMenu = document.getElementById('mobile-menu');
  if (!menuBtn || !menuClose || !mobileMenu) return;
  function closeMenu() {
    mobileMenu.classList.remove('open');
    document.body.classList.remove('menu-open');
    menuBtn.setAttribute('aria-expanded', 'false');
    mobileMenu.setAttribute('aria-hidden', 'true');
  }
  menuBtn.addEventListener('click', function() {
    mobileMenu.classList.add('open');
    document.body.classList.add('menu-open');
    menuBtn.setAttribute('aria-expanded', 'true');
    mobileMenu.setAttribute('aria-hidden', 'false');
  });
  menuClose.addEventListener('click', closeMenu);
  var links = mobileMenu.querySelectorAll('.menu-link');
  for (var i = 0; i < links.length; i++) {
    links[i].addEventListener('click', closeMenu);
  }
})();
```

## Page Structure Template

### Visible Product Page (e.g., `/semaglutide`)
1. `<head>` — SEO meta, OG tags, JSON-LD (Article + FAQPage with 5 Q&As)
2. Tailwind config + brand colors
3. Fixed nav (72px) with desktop links to all pages
4. Hero — navy bg with gradient, badge, H1 with `<span class="border-b-2 border-teal">` highlight
5. Content sections (6-8): What Is X, How It Works, Benefits, Dosing, Risks/RN Safety Flags, Is It Right For You, Sourcing
6. Mid-page content upgrade form (Formspree, unique source tag)
7. Email capture section (Formspree, unique source tag)
8. CTA section — navy bg card with Book Consult + Calculator buttons
9. Footer with newsletter form + all page links
10. Exit-intent popup
11. sessionStorage scripts for thank-you return detection (use unique prefix per page)

### Hidden SEO Guide (e.g., `/semaglutide-guide`)
Same as visible page but:
- Desktop nav does NOT link to this page (it's hidden)
- Longer content (8+ sections, 600+ lines)
- More detailed: trial data, comparison tables, sourcing safety
- Footer links to visible product page

## Funnel System (Per Page)
Each page needs 3 Formspree forms with unique source tracking:
1. **Content upgrade** (mid-page): `source=content-upgrade-{peptide}` → offer PDF
2. **Email capture** (bottom): `source={peptide}-guide` → offer protocol guide
3. **Newsletter** (footer): `source=newsletter-{peptide}` → ongoing updates
4. **Exit popup**: `source=exit-intent-{peptide}` — triggers at 50% scroll + mouseleave

sessionStorage keys must use unique prefixes per page to avoid collisions:
- `nurserob_{peptide}_guide_thanks`
- `nurserob_{peptide}_cu_thanks`
- `nurserob_{peptide}_nl_thanks`
- `nurserob_{peptide}_exit_shown`
- `nurserob_{peptide}_exit_submitted`

## Favicon

The site currently uses an inline SVG emoji favicon. Google and browsers need a proper square icon for search results. When generating:

1. **Expect 4-6 rounds of iteration.** The user provides detailed visual feedback. Budget for it upfront. Round structure: show 5 candidates → get feedback → refine 5 → get feedback → show 10 variations of the narrowed concept → user picks winner.
2. **Create SVG candidates** — build an HTML preview page with options at realistic sizes (16px, 24px, 32px) plus a Google search result mockup. Use inline SVGs — no external tools needed. Let the user pick. Save preview files to `Desktop/Daily Brief/NurseRob_PeptideEmpire/favicon-*.html`.
3. **Brand constraints**: navy #0A1F3F background, gold #C9A84C and/or teal #00C4B4 mark. Must read at 16×16.
4. **DNA helix designs**: the user wants premium twisted helices, not flat ladder rungs. Use overlapping sine-wave curves (`Q`/`C` SVG paths) with varying opacity to create depth illusion. Include visible white rung lines or dots between strands. Diagonal flow (bottom-left to top-right) is preferred.
5. **CRITICAL: when rotating an approved design, use SVG `transform="rotate(45 50 50)"` — do NOT recompute the bezier paths.** Recomputing curves changes the visual character and the user will reject it. Wrap the exact approved paths in a `<g transform="...">` group.
6. Once the user picks, generate the final `favicon.svg` in the website root.
7. **Bulk deploy**: `sed`-replace the favicon `<link>` tag across all `.html` files, `git add . && git commit && git push`. Vercel auto-deploys. Google takes days to weeks to update the favicon in search results.
8. **Favicon HTML link**: `<link rel="icon" type="image/svg+xml" href="/favicon.svg">`
9. See `references/favicon-helix-candidates.md` for tested designs including the deployed E8 winner.

## Deployment Checklist
After building new pages:
1. Add clean URL rewrites to `vercel.json`
2. Add URLs to `sitemap.xml`
3. Update desktop nav on ALL existing pages to include new page links
4. Update mobile menu on ALL existing pages to include new page links
5. `git add . && git commit -m "..." && git push origin main`
6. Vercel auto-deploys from main branch

## Pitfalls
- **DO NOT use delegate_task/subagents** for building HTML pages. They timeout on large file writes (~600s). Build directly with `write_file`.
- **CRITICAL: DO NOT use execute_code with read_file() + write_file() together.** `read_file()` defaults to 500 lines. If the file is larger, it silently truncates. Combining truncated content with `write_file()` permanently destroys the bottom of the file. This truncated 8 production HTML files (100-400 lines each) on May 16, 2026 — requiring full git restore. **Use `patch` tool for all modifications to existing files.** If you must read+write, pass explicit `limit=2000` to `read_file` and verify `tail -3` shows closing html tag before writing.
- **Always verify mobile menu exists** before deploying. Search for `menu-btn` in the file.
- **The tirzepatide.html subagent** produced a non-standard mobile menu with inline style=display:none — never use inline display:none on the mobile menu div. Always use the .mobile-menu-panel CSS class pattern.
- **Footer links must also be updated** on existing pages when new pages are added.
- **sessionStorage key collisions**: if two pages share the same key prefix, returning from Formspree on one page will trigger the success state on the wrong page. Use unique prefixes per page.
- **Mobile menu JS must be wrapped in script tags.** Do not inject raw JS before closing body — it will not execute. Always use proper script tag wrapper.
- **Standardize mobile menu implementation:** Every page must use the same .mobile-menu-panel class + .open toggle + important CSS pattern. Non-standard implementations (inline style.display, hidden md:hidden, missing CSS) will break on Safari iPhone.
- **Nav drift over time:** Pages accumulate different nav links after multiple build sessions. Run this audit after any page addition: `grep -oP 'href="/[^"]*"[^>]*>[^<]+</a>' *.html | sort | uniq -c`. All 10 pages must show identical nav item counts. May 17, 2026: found pages with 0, 5, 6, 8, 9, and 10 nav items — fixed by standardizing all to the 10-item template above.
- **Book a Consult button:** Must always link to `https://cal.com/nurserob/peptide-consult` (NOT mailto:). Check all pages with `grep -c 'cal.com/nurserob/peptide-consult' *.html` — every page must return at least 1.
- **GSC "Page with redirect" email is a FALSE ALARM.** Vercel redirects `http://` → `https://` via 308. Google discovers the HTTP versions and flags them. Do NOT click "Validate Fix" in GSC — the redirect is intentional and correct. Google indexes the HTTPS versions instead. The sitemap "0 indexed" count is reporting lag (often 24-48h behind the actual crawl status). Verify real indexing with URL Inspection tool (`mcp_gsc_inspect_url`), not the sitemap summary.
- **GSC submission order:** submit sitemap first, then use per-URL "Request Indexing" in GSC URL Inspection for stubborn pages. The Indexing API (`mcp_gsc_submit_url`) requires service account owner access which may not be configured.
