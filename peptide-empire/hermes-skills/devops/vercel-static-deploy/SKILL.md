---
name: vercel-static-deploy
description: Deploy a static HTML website to Vercel with custom domain, GitHub integration, and Formspree form handling — end-to-end pipeline from local files to live production
version: 1.1
author: Nurse Rob
---

# Vercel Static Deploy

**Purpose:** End-to-end deployment pipeline for static HTML websites — GitHub push → Vercel import → custom domain DNS → Formspree form integration. Covers the exact steps, gotchas, and DNS configuration needed.

## Trigger Conditions
- "deploy this website to Vercel"
- "host my HTML site"
- "put this site online with my domain"
- "connect my domain to Vercel"
- "set up GitHub pages or Vercel for my site"

## Project Structure
```
website-folder/
├── index.html    (your main site — must be named index.html)
└── guide.pdf     (optional static assets — PDFs, images, etc.)
```

## Pre-Flight Checklist
- [ ] Single HTML file or simple static folder (no React/Next.js build step needed)
- [ ] File named `index.html` (Vercel requirement for root page)
- [ ] GitHub account created
- [ ] Domain purchased (Porkbun, Namecheap, etc.)
- [ ] Formspree account (if site has forms)

## Workflow

### Step 1: GitHub Setup

```bash
# Initialize repo in your website folder
cd /path/to/website-folder
git init
git branch -m master main
git config user.email "you@yourdomain.com"
git config user.name "Your Name"
git add index.html guide.pdf  # add your files
git commit -m "Initial deploy"
```

Create repo on GitHub (github.com/new):
- Name: `yourproject-website`
- Public
- No README, no .gitignore (you already have files)

```bash
git remote add origin https://github.com/YOUR_USERNAME/yourproject-website.git
git push -u origin main  # will prompt for authentication
```

**Authentication gotcha:** GitHub requires a Personal Access Token for HTTPS push. Generate at github.com/settings/tokens → "Generate new token (classic)" → check "repo" scope. Use the token in the push URL directly:
```bash
git push https://TOKEN@github.com/USER/REPO.git main
```
This avoids interactive password prompts in non-interactive terminals. After push, set the remote back to the clean URL:
```bash
git remote set-url origin https://github.com/USER/REPO.git
```
Never commit the token URL — only use it inline for the push command.

### Mailto Links: Desktop vs Mobile Behavior

**The problem:** `mailto:` links behave differently across platforms:
- **Mobile with email app:** Works perfectly
- **Mobile without email app:** Silently fails (nothing happens)
- **Desktop with email client (Outlook/Mail):** Works perfectly
- **Desktop without email client (web Gmail only):** Silently fails

**The wrong fix (do NOT use):** Adding `target="_blank"` to mailto links. This causes `about:blank` blank tabs on desktop browsers. It does not solve the underlying issue.

**The correct fix:** A JavaScript clipboard fallback. When a `mailto:` link is clicked and no email client opens within 1.5 seconds, the email address is automatically copied to the clipboard and a toast notification appears. This works on all platforms.

```javascript
// Add this before </script> in your HTML
document.querySelectorAll('a[href^="mailto:"]').forEach(function(link) {
  link.addEventListener('click', function(e) {
    var email = link.getAttribute('href').replace('mailto:', '').split('?')[0];
    var fallbackTimer = setTimeout(function() {
      navigator.clipboard.writeText(email).then(function() {
        var toast = document.createElement('div');
        toast.textContent = 'Copied: ' + email;
        toast.style.cssText = 'position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#0A1F3F;color:#fff;padding:12px 24px;border-radius:999px;font-size:14px;z-index:9999;box-shadow:0 4px 20px rgba(0,0,0,0.3);';
        document.body.appendChild(toast);
        setTimeout(function() { toast.remove(); }, 2000);
      }).catch(function() {});
    }, 1500);
    window.addEventListener('focus', function() { clearTimeout(fallbackTimer); }, {once: true});
  });
});
```

**When to use this fix:** Any static site with `mailto:` links, especially when the audience includes desktop users who may use web-based email (Gmail in Chrome) rather than a native email client.

### git working tree clean after syncing
If you `cp` a file into the repo folder and `git status` shows "nothing to commit, working tree clean", the file was already identical. The deployed version is current. Vercel auto-deploys from GitHub within 30-60 seconds of a push.

### Step 2: Vercel Deploy

1. Go to [vercel.com](https://vercel.com) → **Sign Up with GitHub**
2. Authorize Vercel → **New Project** → find your repo → **Import**
3. For static HTML sites: leave ALL settings at default (preset: Other, root: ./, no build command, no environment variables)
4. Click **Deploy**

Your site is live at: `project-name.vercel.app`

### Step 3: Custom Domain

1. In Vercel dashboard → your project → **Settings → Domains**
2. Add: `yourdomain.com`
3. Vercel shows required DNS record (typically a CNAME pointing to `cname.vercel-dns.com`)
4. Go to your domain registrar (Porkbun, etc.) → DNS settings
5. Add the CNAME record exactly as Vercel shows
6. Wait 2-5 minutes for DNS propagation
7. Also add any redirect domains (e.g., `yourdomain.health` → `yourdomain.com`)

**Porkbun DNS tip:** Delete any existing A or CNAME records that point elsewhere before adding Vercel's record. The "Host" field may be labeled "Name" in Porkbun.

### Step 4: Formspree Integration

For vanilla JS sites (no React), use AJAX:

```javascript
// In your form submit handler
const res = await fetch('https://formspree.io/f/YOUR_FORM_ID', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: userEmail, message: formData })
});
if (res.ok) { /* show success */ }
```

**Formspree auto-reply:** In dashboard → form settings → enable Auto-Reply. Use `{{message}}` to include form data in the reply email.

### Step 5: Host Static Assets

Any file in your repo is accessible at the same path on your domain:
- `index.html` → `yourdomain.com`
- `guide.pdf` → `yourdomain.com/guide.pdf`

No special configuration needed. Vercel serves all static files automatically.

## Plan Selection
Always choose **Hobby** (free) for static sites. 100 GB bandwidth/month is more than enough for HTML + PDF files. Pro ($20/mo) is only needed for serverless functions or high-traffic commercial apps.

## SEO Improvements (Implement, Don't Recommend)

**CRITICAL ANTI-PATTERN:** When the user asks for SEO improvements, an audit, or website changes — do NOT list recommendations for the user to implement themselves. The agent has file access and git push access. IMPLEMENT the changes directly:

1. Read the current HTML source (from the repo or Desktop source copy)
2. Edit the file with `patch` to add JSON-LD, improve headings, add keywords, add FAQ sections, etc.
3. Copy updated files to the git repo
4. Commit and push — Vercel auto-deploys

**Recommended edits to apply proactively during any SEO pass:**
- JSON-LD structured data: Organization + Person + WebSite schema (see `references/json-ld-schema-pattern.md`)
- H1 improvement: include target keywords beyond just the brand name
- FAQ section with FAQPage JSON-LD schema (4+ questions targeting high-volume searches)
- Keyword expansion: add missing high-value terms naturally into existing content
- Sitemap.xml: generate and deploy (see below)
- og:image + twitter:image meta tags if missing
- Canonical URL if missing
- Content page for AI search engines (Perplexity, ChatGPT, Grok) — a standalone article page with JSON-LD Article schema

**After editing, always deploy.** Don't ask the user to paste code or redeploy — the agent does the full loop.

### Sitemap Generation

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://yourdomain.com</loc>
    <lastmod>YYYY-MM-DD</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <!-- one <url> block per page -->
</urlset>
```

Include every page in the repo. Commit to root. Vercel serves it at `/sitemap.xml`.

### Vercel Rewrites for Clean URLs

If you create a standalone page like `wolverine-stack.html`, add a rewrite in `vercel.json` so it's accessible at `/wolverine-stack` (no `.html`):

```json
{
  "rewrites": [
    { "source": "/wolverine-stack", "destination": "/wolverine-stack.html" }
  ]
}
```

## Common Gotchas

### GitHub Push Fails with "Repository not found"
The repo doesn't exist on GitHub yet. Create it at github.com/new first, THEN push.

### Git Author Identity Unknown
```bash
git config user.email "you@yourdomain.com"
git config user.name "Your Name"
```

### Vercel Shows Build Error for Static Site
You may have accidentally selected a framework preset (Next.js, React). For pure HTML sites, select preset "Other" and leave build/output settings empty.

### Domain Shows "Invalid Configuration" in Vercel
DNS hasn't propagated yet. Wait 5 minutes and refresh. If still failing, double-check the CNAME record in your registrar — it must match exactly what Vercel shows.

### Formspree Not Delivering Emails
- Verify the form ID in your fetch URL is correct
- Check that the email field is named `email` (Formspree uses this for the reply-to address)
- Test with a curl command: `curl -X POST https://formspree.io/f/YOUR_ID -H "Content-Type: application/json" -d '{"email":"test@test.com","message":"test"}'`
- Check Formspree dashboard for submission logs

### Formspree Auto-Reply Limitation (Free Tier)
Formspree's free plan does NOT include auto-reply emails to submitters. The free tier only delivers submissions to the form owner. For auto-reply on the free tier, use the **on-screen download** approach instead — instant gratification, no email needed.

**The fix:** After the user submits the form, show the download link and CTAs directly in the success message:

```javascript
if (res.ok) {
  resultDiv.innerHTML = `
    <div>✅ Your results are ready!</div>
    <a href="/guide.pdf">Download Guide →</a>
    <a href="https://cal.com/you/booking">Book a Consult →</a>
  `;
}
```

### Auto-Reply Template (Paid Tier Only)
If you upgrade to Formspree paid ($20/mo), use this template in Settings → Auto-Reply:

**Subject:** `🧬 Your Results + Complete Guide`

**Body:**
```
Hi there,

Thanks for using the [tool name]!

Here's a recap of your results:
{{message}}

I've prepared my full guide for you — download it here:
https://yourdomain.com/guide.pdf

[Optional CTA — consult booking, follow-up, etc.]

—
Your Name
your@email.com
yourdomain.com
```

The `{{message}}` variable includes whatever you sent in the `message` field of your Formspree POST. The download link points to a static file hosted on Vercel (same domain, same repo).

## Quality Checklist
- [ ] `index.html` present and named correctly (not `index-final.html`)
- [ ] GitHub repo created and files pushed
- [ ] Vercel deployed and site loads at `.vercel.app` URL
- [ ] Custom domain connected and resolving
- [ ] SSL certificate active (Vercel auto-provisions — look for the lock icon)
- [ ] Form submissions working end-to-end
- [ ] Static assets (PDFs, images) accessible at their URLs
- [ ] OG tags and meta description show correctly when sharing on social media
- [ ] `sitemap.xml` present in repo and returns 200 at `/sitemap.xml`
- [ ] JSON-LD structured data present (see `references/json-ld-schema-pattern.md`)
- [ ] `vercel.json` rewrites configured for any clean-URL pages
