---
name: form-debugging-static-site
description: Debug form submission failures on deployed static sites — Formspree, Netlify Forms, mobile Safari fetch failures, mailto link bugs, Vercel deploy verification, and inbox delivery testing with curl + himalaya
version: 1.3
author: Nurse Rob
---

# Form Debugging — Static Sites

**When to use:** A deployed static site form (Formspree, Netlify Forms, etc.) works on desktop but fails silently on mobile, or submissions aren't arriving in the inbox. User reports "I submitted but nothing happened."

## Trigger Conditions
- Form submission works via direct curl/API test but not from the live site
- Mobile users report form doesn't submit
- No new submissions appearing in the target inbox
- Form uses JavaScript fetch/async and `preventDefault()`
- **Funnel leak**: SEO-optimized content pages (guide articles, blog posts) are indexed by Google and get traffic, but have ZERO email capture forms — visitors read everything and leave without giving an email
- Need to deploy the same email capture form across multiple pages consistently

## Workflow

### Step 1: Isolate — Server or Client?

Test the form endpoint directly with curl:
```bash
curl -s -X POST https://formspree.io/f/[FORM_ID] \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","message":"Debug test"}'
```
- If `{"ok":true}` → server is fine, issue is client-side
- If fails → check Formspree dashboard, endpoint URL, rate limits

### Step 2: Check Inbox Delivery

After a successful curl test, verify the email arrived:
```bash
himalaya envelope list --page-size 5 2>&1 | grep -i "formspree"
```
- If arrived → pipeline works end-to-end, issue is 100% frontend
- If not arrived → wait 30-60s (Formspree delivery delay), check again

### Step 3: Check Live Site Code

Verify the deployed code has the correct form configuration:
```bash
curl -s https://[domain] | grep -o 'formspree.io[^"'\'']*'
curl -s https://[domain] | grep 'email-capture-form'
```
- Compare deployed code vs local code
- Check that `action="https://formspree.io/f/[ID]"` is present on the `<form>` tag

### Step 4: Fix — Replace fetch with Native POST (Most Common Fix)

**Root cause on mobile:** The JavaScript `fetch()` API silently fails on mobile Safari when the page is in certain states (background tab, low power mode, ad blockers, etc.). The form uses `e.preventDefault()` + `fetch()`, so when fetch fails, nothing happens.

**The fix:** Remove the async fetch handler entirely. Add `action="[ENDPOINT]" method="POST"` to the `<form>` tag and let the browser submit natively. No JavaScript required.

```html
<!-- BEFORE (fragile) -->
<form id="email-form">
  <input type="email" name="email">
  <button type="submit">Send</button>
</form>
<script>
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    await fetch('https://formspree.io/f/xxx', { ... }); // Fails silently on mobile
  });
</script>

<!-- AFTER (reliable) -->
<form id="email-form" action="https://formspree.io/f/xxx" method="POST">
  <input type="email" name="email">
  <button type="submit">Send</button>
</form>
```

### Step 5: Configure Formspree Return Detection (Critical for Free Tier)

Formspree's "Redirect URL" setting is a paid feature. Use a hidden field instead — no upgrade needed:
```html
<input type="hidden" name="_next" value="https://[domain]/?thanks=true">
```
Add this inside the `<form>` tag. Formspree honors `_next` as a redirect target on all plans.

**⚠️ CRITICAL: Formspree Free Tier "Go Back" ≠ Redirect.** On the free tier, after submission Formspree shows its own branded "Thank you" page with a "Go Back" button. That button uses **browser history** (`history.back()`), NOT the `_next` redirect URL. So `?thanks=true` will NEVER appear in the URL on free tier. URL parameter detection alone will silently fail.

**The fix: `sessionStorage` + `pageshow` event.** sessionStorage survives the round-trip to Formspree and back within the same tab. Set a flag before form submission, detect it on return:

**Before form submits** (in the submit event handler, before the POST leaves):
```javascript
emailForm.addEventListener('submit', function() {
  sessionStorage.setItem('mysite_thanks', 'true');
  // ... form proceeds to Formspree natively
});
```

**On return** (check on both initial load AND back-navigation):
```javascript
function showPostSubmitSuccess() {
  if (sessionStorage.getItem('mysite_thanks') === 'true') {
    sessionStorage.removeItem('mysite_thanks'); // one-shot — clear immediately
    var successDiv = document.getElementById('post-submit-success');
    if (successDiv) {
      successDiv.classList.remove('hidden');
      setTimeout(function() {
        document.getElementById('resources').scrollIntoView({ behavior: 'smooth', block: 'start' });
        setTimeout(function() {
          successDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 400);
      }, 300);
    }
  }
}

// Check on initial page load
showPostSubmitSuccess();

// Check on back-navigation (pageshow fires when returning via browser history)
window.addEventListener('pageshow', function(e) {
  if (e.persisted) showPostSubmitSuccess(); // e.persisted = true when restored from bfcache
});
```

**Why both checks matter:** The initial-load check catches the Formspree `_next` redirect (paid tier or if it works). The `pageshow` listener catches the browser-history "Go Back" (free tier). `e.persisted` is `true` when the page is restored from the back-forward cache — exactly what happens after Formspree's "Go Back" button.

**URL param method (keep as fallback for paid tier):**
```javascript
// Only works on paid tier or if _next redirect fires
if (window.location.search.includes('thanks=true')) {
  document.getElementById('post-submit-success').classList.remove('hidden');
  window.history.replaceState({}, '', window.location.pathname);
}
```

### Step 6B: Success Div Placement (Critical for Mobile)

The success div shown after Formspree redirect **must not be nested inside CSS-animated containers**. On redirect, the page loads fresh at the top — `section-reveal`, `IntersectionObserver`, and fade-in classes haven't fired yet.

**WRONG** (success div inside animated parent — invisible on redirect):
```html
<section id="resources">
  <div class="section-reveal">  <!-- opacity: 0 on page load -->
    <div class="calculator-card">
      <div id="post-submit-success" class="hidden">...</div>  <!-- NEVER visible -->
    </div>
  </div>
</section>
```

**RIGHT** (success div as direct child of section, BEFORE any animated wrappers):
```html
<section id="resources">
  <!-- Always visible — no parent animations -->
  <div id="post-submit-success" class="hidden mb-12 p-8 bg-white border-2 border-teal rounded-2xl text-center max-w-lg mx-auto">
    <div class="text-green-600 text-xl font-bold mb-3">✅ Your stack is ready!</div>
    <a href="/guide.pdf" class="...">Download Guide →</a>
    <a href="https://cal.com/your-consult" class="...">Book a Consult →</a>
  </div>

  <!-- These can be animated — they don't contain the success state -->
  <div class="section-reveal">
    <div class="calculator-card">...</div>
  </div>
</section>
```

**Scroll timing fix for mobile** (Formspree redirect loads at top):
```javascript
if (window.location.search.includes('thanks=true')) {
  var successDiv = document.getElementById('post-submit-success');
  if (successDiv) {
    successDiv.classList.remove('hidden');
    // Delay scroll — mobile Safari throttles immediate scrollIntoView on page load
    setTimeout(function() {
      var resourcesEl = document.getElementById('resources');
      if (resourcesEl) resourcesEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
      setTimeout(function() {
        successDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }, 400);
    }, 200);
    var cleanUrl = window.location.pathname;
    window.history.replaceState({}, '', cleanUrl);
  }
}
```

### Step 7: Verify Fix

```bash
# Commit and push
cd [project-dir]
git add index.html
git commit -m "Fix: replace JS fetch with native form POST for mobile reliability"
git push

# Wait for Vercel deploy (30-60s), then test via curl
curl -s https://[domain] | grep 'action="https://formspree'
```

## Multi-Page Email Capture Deployment (SEO Guide Pages)

When you have multiple SEO-optimized content pages (e.g., `/bpc-157-guide`, `/tb-500-guide`, `/wolverine-stack`) that all need the same email capture form, use a consistent template across all pages. This ensures:

1. All Google traffic gets funneled through the email gate
2. The same Formspree endpoint collects all leads with a `source` hidden field for attribution
3. Return detection works identically on every page

**Template:** See `references/guide-page-email-capture.html` — drop-in HTML + JS for any content page.

**Before deploying to multiple pages, check for and remove direct download links:**
```bash
cd [project-dir]
grep -rn 'href="[^"]*guide\.pdf"' *.html
```
Replace any direct PDF links with links to the gated entry point (e.g., `/#resources` on the homepage where the calculator form lives). A direct PDF link on an SEO page completely bypasses the email gate.

**Hidden source field for attribution:**
```html
<input type="hidden" name="source" value="bpc-157-guide">
```
This tags Formspree submissions with which page the lead came from — essential for measuring which SEO pages convert best.

## Dynamically-Injected Forms (Calculator Results, etc.)

When a form is created by JavaScript and injected into the DOM (e.g., after a calculator generates results), build the form with `action` and `method` in the HTML string itself:

```javascript
// RIGHT: action + method + hidden fields in the HTML string
resultDiv.innerHTML = `
  <form id="email-capture-form" action="https://formspree.io/f/xxx" method="POST">
    <input type="hidden" name="_next" value="https://domain/?thanks=true">
    <input type="hidden" name="bpc_dose" value="${bpc}">
    <input type="hidden" name="tb_dose" value="${tb}">
    <input type="email" name="email" placeholder="your@email.com" required>
    <button type="submit">Send →</button>
  </form>
`;
// Only add the sessionStorage setter — no fetch, no preventDefault
document.getElementById('email-capture-form').addEventListener('submit', function() {
  sessionStorage.setItem('mysite_thanks', 'true');
});
```

## Multiple Forms on One Page — Separate sessionStorage Keys

When a page has more than one email capture form (e.g., homepage calculator + footer newsletter, or guide-page email gate + content upgrade + footer newsletter), each form needs its OWN sessionStorage key to avoid collision. If two forms share `mysite_thanks`, the first form's return will trigger the wrong success div.

**Pattern — unique key per form purpose:**

| Form | sessionStorage Key |
|------|-------------------|
| Calculator email capture | `mysite_thanks` |
| Guide page email gate | `mysite_guide_thanks` |
| Content upgrade (mid-page) | `mysite_cu_thanks` |
| Footer newsletter | `mysite_nl_thanks` |

Each form gets its own isolated handler block — copy the same pattern with different IDs and keys.

## Email Capture Strategy Patterns

### Content Upgrade — Mid-Page CTA

Insert between content sections (after "How It Works", before "Benefits/Dosing") on long-form SEO guide pages. The pitch: "📄 Want this guide as a printable PDF?" — reader gets the PDF version in exchange for email. Contextually relevant, not interruptive.

Placement rule: after the reader has consumed enough content to know it's valuable (~40-60% scroll depth), but before the next major section heading. Use the same Formspree endpoint with a `source` hidden field (`content-upgrade-[page]`).

### Footer Newsletter — Bottom-of-Page Capture

Non-intrusive signup in the site footer. Catches readers who scrolled past all CTAs. Pattern: "🧬 Stay Updated on Peptide Research — No spam. Just clinical insights from a licensed RN." Single email field, same Formspree endpoint, source tagged (`newsletter-footer`, `newsletter-[page]`).

Place on every page — homepage + all guide pages. Footer is the one place users expect a newsletter signup; it won't annoy anyone.

## Formspree Tier Comparison — "Go Back" Abandonment

| | Free Tier | Gold ($20/mo) |
|---|---|---|
| After submit | Branded "Thanks!" page | Auto-redirect via `_next` |
| User action required | Must click "Go Back" | None — instant return |
| Abandonment rate | ~5-15% | ~0% |
| `_next` hidden field | Dormant (ignored) | Active (honored) |
| sessionStorage detection | Required | Works as fallback |

**The `_next` field is already in every form — it activates automatically when upgraded to Gold.** No code changes needed. At $20/mo, if it saves one extra $197 consult per month from someone who would've bounced, it's 10x ROI.

## Funnel Audit Checklist

When auditing a site's email capture funnel, check every page systematically:

```bash
# 1. Find all HTML pages
ls *.html

# 2. Check each page for email capture presence
for f in *.html; do
  count=$(grep -c 'formspree.io' "$f" 2>/dev/null || echo 0)
  echo "$f: $count email forms"
done

# 3. Find direct download links bypassing the gate
grep -rn 'href="[^"]*\.pdf"' *.html
grep -rn 'href="[^"]*guide\.pdf"' *.html

# 4. Verify deployed pages match
for page in index.html bpc-157-guide.html tb-500-guide.html wolverine-stack.html; do
  echo "=== $page ==="
  curl -s https://[domain]/${page%.html} | grep -c 'formspree.io'
done
```

**Red flags:**
- SEO-indexed content page with zero email forms → leak
- Direct `/guide.pdf` link → bypasses gate, replace with `/#resources`
- Page with valuable content below the fold but email form only at the top → add mid-page CTA

## Pitfalls
- Don't keep both JS fetch AND native action — pick one. Native is more reliable.
- **Multiple forms on same page MUST use unique sessionStorage keys** — if the calculator form and footer newsletter both set `mysite_thanks`, returning from one will show the wrong success message (or no message at all). Use `mysite_thanks`, `mysite_guide_thanks`, `mysite_nl_thanks`, `mysite_cu_thanks` — one per form.
- Formspree free tier doesn't include auto-reply — handle welcome emails separately (e.g., via himalaya cron)
- On Vercel, allow 30-60s for deploy propagation after git push
- The `fetch` API is NOT reliable on mobile Safari — always prefer native form POST for production forms
- **Never add `target="_blank"` to `mailto:` links** — it opens `about:blank` on desktop Windows. `mailto:` should be bare.
- **Dynamically-created forms need native attributes** — don't rely on JS event listeners for forms created at runtime (e.g., after a calculator result). Use `action` and `method` attributes directly on the HTML, not `addEventListener('submit', ...)`.
- **Dynamically-injected forms should carry calculator data as hidden fields** — when a form is shown after computation (e.g., calculator results → email capture), include the computed values as `<input type="hidden">` fields so Formspree receives them. Use template literals: `value="${bpc}"`.
- Formspree submissions can take 30-60s to arrive in the inbox — wait before retesting
- **Success div MUST be outside CSS-animated containers** — if the success div is nested inside a parent with `opacity: 0` (e.g., `.section-reveal`, IntersectionObserver animations, fade-in classes), removing `hidden` won't make it visible. The Formspree return does a full page load from the top — those animation classes haven't triggered yet. Place the success div as a direct child of the section, BEFORE any animated wrappers.
- **Mobile Formspree return scrolls to top** — after returning from Formspree, the page loads fresh at the top. The `scrollIntoView` call needs a `setTimeout` delay (300ms+) before scrolling, and should scroll to the section anchor first, then fine-tune to the success div. Mobile Safari throttles `scrollIntoView` on page load otherwise.
- **⚠️ Formspree free tier "Go Back" uses browser history, NOT `_next` redirect** — the `?thanks=true` URL parameter will NEVER appear on free tier. Formspree shows its own thank-you page; the "Go Back" button is `history.back()`. Must use `sessionStorage` flag (set before submission leaves) + `pageshow` event listener (catches bfcache restore on back-navigation) instead of URL detection. See Step 5 for full implementation.
- **SEO guide pages without email capture are funnel leaks** — if a page is indexed by Google, gets organic traffic, and has valuable content but no email form, every visitor is a lost lead. Audit all indexed pages: `curl -s https://domain/sitemap.xml | grep '<loc>'`. Every HTML page with substantial content should have an email capture form.
- **Direct PDF/file download links on SEO pages bypass the email gate** — search for `href="[^"]*\.(pdf|zip)"` across all HTML files and replace with links to the gated entry point. A visitor who downloads the resource directly never enters the funnel.
- **Mobile hamburger menus with hash links don't auto-close** — when a mobile menu uses `href="#section"` links, tapping them scrolls to the section but the menu overlay stays open. Must add a click handler on all `.menu-link` elements that removes the `.open` class and `body.menu-open`: `document.querySelectorAll('.menu-link').forEach(l => l.addEventListener('click', () => { menu.classList.remove('open'); body.classList.remove('menu-open'); }))`.

## Quality Checklist
- [ ] curl test returns `{"ok":true}` from the endpoint
- [ ] Submission arrives in target inbox
- [ ] Deployed HTML has `action="[endpoint]" method="POST"` on EVERY form
- [ ] No `e.preventDefault()` blocking native submission on any form
- [ ] Formspree redirect URL configured via hidden `_next` field on every form
- [ ] Success div is OUTSIDE any CSS-animated parent (section-reveal, fade-in, IntersectionObserver)
- [ ] Every form uses a unique sessionStorage key (no collisions between calculator/guide/newsletter/upgrade forms)
- [ ] `?thanks=true` JS uses `setTimeout` before `scrollIntoView` (200ms+ delay for mobile)
- [ ] All 4 pages (homepage + 3 guide pages) have at least one email capture form
- [ ] All direct `/guide.pdf` links replaced with gated entry points (`/#resources`)
- [ ] Footer newsletter present on all pages
- [ ] Content upgrade CTA present mid-page on all guide pages (~40-60% scroll depth)
- [ ] Each form has a unique `source` hidden field for Formspree attribution
- [ ] Mobile hamburger menu closes on link tap (`.menu-link` click handler removes `.open`)
- [ ] Tested on both desktop and mobile
