---
name: social-media-link-preview
description: Fix social media link previews for static websites — Twitter/X Cards, Open Graph meta tags, OG image generation, and validator testing
version: 1.4
author: Nurse Rob
---

# Social Media Link Preview Setup v1.5

**When to use:** A website shows a blank/broken link preview when shared on X/Twitter, Facebook, LinkedIn, Discord, or iMessage. The card is missing, has no image, or shows generic text instead of a branded preview.

## Trigger Conditions
- Link preview on X shows blank box or no image
- "summary_large_image" card is set but no image appears
- OG image dimensions are wrong (Twitter requires 1200×630, Facebook 1200×630)
- Need to force a social platform to re-crawl the page

## Quick Reference

| Platform | Validator URL |
|----------|--------------|
| X/Twitter | https://cards-dev.twitter.com/validator |
| Facebook | https://developers.facebook.com/tools/debug/ |
| LinkedIn | https://www.linkedin.com/post-inspector/ |

## Workflow

### Step 1: Check Existing Meta Tags

```bash
curl -s https://[domain] | grep -E 'twitter:|og:'
```

Key tags to verify:
- `twitter:card` — must be `summary_large_image` for big preview card (NOT `summary`)
- `twitter:image` / `og:image` — must point to an absolute URL with a real image
- `og:image:width` / `og:image:height` — must be 1200 and 630

### Step 2: Add Missing Meta Tags

The minimum working set for Twitter/X large card:

```html
<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Site Title">
<meta name="twitter:description" content="Description (under 200 chars)">
<meta name="twitter:image" content="https://[domain]/og-image.png">

<!-- Open Graph (Facebook, LinkedIn, Discord, iMessage) -->
<!-- og:image MUST come before og:url/og:type — X crawler reads top-down and may miss image if buried -->
<meta property="og:title" content="Site Title">
<meta property="og:description" content="Description (under 200 chars — match twitter:description)">
<meta property="og:image" content="https://[domain]/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="https://[domain]">
<meta property="og:type" content="website">
```

### Step 3: Generate OG Image

**Requirements:**
- Dimensions: exactly 1200×630 pixels
- Format: PNG or JPG (Twitter does NOT support SVG)
- File size: under 5MB (under 1MB recommended)
- Must be accessible at the URL specified in meta tags
- **The image MUST contain visible text and design elements** — a solid-color rectangle with no content will cause X to show the fallback blue box

**⚠️ CRITICAL — DO NOT use pure Python struct/zlib to generate PNGs.** This approach consistently produces blank solid-color images with zero text. The PNG binary is valid, Pillow opens it, X serves it — but it's just one solid color. Always use Pillow with actual font rendering for text.

**Option A — Pillow with system fonts (recommended):**

A pre-built script is available: `scripts/generate_og_card.py` — generates a Nurse Rob branded 1200×630 OG card with brightness verification.

```python
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
img = Image.new('RGBA', (W, H), (8, 14, 26, 255))  # navy #080E1A
draw = ImageDraw.Draw(img)

# Find available bold font (Inter > Liberation Sans > DejaVu Sans)
font_paths = [
    '/usr/share/fonts/truetype/inter/Inter-Bold.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
]
title_font = None
for fp in font_paths:
    if os.path.exists(fp):
        title_font = ImageFont.truetype(fp, 52)
        break
if title_font is None:
    title_font = ImageFont.load_default()

# Design elements
draw.text((100, 190), "Site Name", fill=(201, 168, 76, 255), font=title_font)  # gold
draw.text((100, 270), "Tagline Here", fill=(0, 196, 180, 255), font=subtitle_font)  # teal
# ... add more text, icons, accents as needed

img.save('og-image.png', 'PNG', optimize=True)
```

**Option B — image_generate tool (if FAL_KEY is configured):**

Use `image_generate` with a detailed prompt. Fall back to Option A if FAL_KEY is not set.

**Option C — External tools (DALL-E / Midjourney):**

Generate externally, download, and add to repo. Prompt: "Professional OG image card, dark navy background, clean white typography centered, teal accent, 1200x630, no text smaller than 24pt, minimalist medical-tech aesthetic."

**Option D — User-provided image (resize required):**

When the user provides their own image (e.g., `o5DE5.jpg`), it must be resized to exactly 1200×630. User images rarely come in the correct 2:1 aspect ratio:

```python
from PIL import Image

img = Image.open('user-image.jpg')
w, h = img.size
target_ratio = 1200/630  # ~1.905

# Crop from center to 2:1 aspect ratio
if w/h > target_ratio:
    new_w = int(h * target_ratio)
    left = (w - new_w) // 2
    img = img.crop((left, 0, left + new_w, h))
else:
    new_h = int(w / target_ratio)
    top = (h - new_h) // 2
    img = img.crop((0, top, w, top + new_h))

# Resize to exactly 1200x630
img = img.resize((1200, 630), Image.LANCZOS)
img.save('og-image-{ts}.jpg', 'JPEG', quality=92, optimize=True)
```

### Step 3.5: VERIFY IMAGE HAS CONTENT (MANDATORY)

**This step would have prevented the most common silent failure.** A PNG file can be valid (correct dimensions, proper encoding, 200 OK from server) but still be a blank solid-colored rectangle with no text. X correctly shows the fallback card because there's nothing to display.

```python
from PIL import Image
import requests, io

# Get the deployed image
r = requests.get('https://domain/og-image.png')
img = Image.open(io.BytesIO(r.content))

# Count unique colors — a design with text has 100+; a blank has 1-5
pixels = list(img.getdata())
unique = len(set(pixels))
print(f"Unique colors: {unique}")

if unique < 50:
    print("FAIL: Image is blank/solid color — X will show fallback card")
else:
    print(f"PASS: {unique} unique colors — image has actual content")

# ALSO CHECK BRIGHTNESS — an image with 29K colors can still be 90% dark pixels
# Grok-generated moody images often have great color variety but are near-black
brightness = [(r+g+b)//3 for (r,g,b) in pixels]
dark_pct = 100 * sum(1 for b in brightness if b < 50) / len(brightness)
avg_brightness = sum(brightness) / len(brightness)
print(f"Dark pixels (<50): {dark_pct:.1f}% | Avg brightness: {avg_brightness:.1f}/255")
if dark_pct > 80:
    print(f"WARN: Image is very dark ({dark_pct:.1f}% dark pixels) — may look like a void on X")
    print("ACTION: Brighten with ImageEnhance before deploying (see Level 5)")
```

**Do this BEFORE deploying, or immediately after. Re-deploy if the image fails either check.**

**Image Caching by X:** X caches the OG image URL aggressively. Even after fixing a broken image, X may serve the old cached version for hours. To break the image cache, you must change the filename (Level 2) AND bump `og:url` (Level 3) simultaneously — changing just one isn't enough. X's image cache is keyed by the image URL, and the page cache is keyed by `og:url`. Both must change for a guaranteed fresh crawl.

### Step 4: Deploy and Validate

```bash
git add og-image.png index.html
git commit -m "Add OG image + social card meta tags"
git push
```

After deploy (~30s for Vercel):

1. Verify tags are live: `curl -s https://domain | grep -E 'og:|twitter:'`
2. Verify image is accessible: `curl -I https://domain/og-image.png` returns 200
3. **Test in X tweet composer** — paste the URL into a new post and check the preview box. This is the ONLY accurate test as of 2026. The Card Validator at cards-dev.twitter.com no longer shows visual previews.
4. If image doesn't appear in composer → escalate through the Cache-Busting Escalation Path above.
5. After pushing each cache-busting fix, re-test in composer (not the validator).

### Step 5: Common Card Types

| Card Type | `twitter:card` value | Image size | Use case |
|-----------|---------------------|------------|----------|
| Large Image | `summary_large_image` | 1200×630 | Standard — used 90% of the time |
| Small Summary | `summary` | 120×120 (square) | Minimal — rarely preferred |
| Player | `player` | Video embed | For video content |
| App | `app` | App store link | Mobile app installs |

## Pitfalls
- **Blank/solid-color OG image** — a valid PNG that is just one solid color (e.g., navy rectangle, no text) will cause X to show the fallback card. The file is technically correct: right dimensions, valid encoding, 200 OK. But X correctly treats it as having no image content. Always verify unique pixel colors before deploying: a real design has 100+ unique colors; a blank has 1-5. Pure Python PNG generation (struct/zlib without Pillow font rendering) is especially prone to this.
- **Tag ORDER matters for X/Twitter** — the crawler reads meta tags top-down. `og:image` and its dimensions MUST appear before `og:url` and `og:type` in the `<head>`. If `og:image` is buried after `og:url`/`og:type`, X may silently ignore it and show the fallback preview even when all tags are correct and the image is accessible. Symptom: correct tags, valid image, but X compositor shows no image.
- **Mismatched og:description and twitter:description** — if these differ, the crawler may pick the wrong one or show inconsistency. Keep them identical or make twitter:description shorter/punchier and og:description longer — never the reverse.
- **SVG images don't work on Twitter** — X/Twitter does not render SVG for card images. Must use PNG, JPG, WEBP, or GIF.
- **X caches at the PAGE level, not the image level** — X's crawler caches the entire page's OG data keyed by `og:url`. Changing the image filename (e.g., `og-image.png` → `og-image-v2.png`) will NOT force a re-crawl unless the page URL also changes. The crawler has no reason to revisit the page, so it never discovers the new image reference. To force a re-crawl, you must bump the `og:url` itself.
- **X Card Validator no longer shows visual previews** — as of 2026, the validator at `cards-dev.twitter.com/validator` only confirms meta tag count and card type. It does NOT show what the card looks like. The only way to see the actual preview is to paste the URL into the X/Twitter tweet composer.
- **Image URL must be absolute** — `og:image` and `twitter:image` must be full `https://` URLs, not relative paths. `/og-image.png` will NOT work.
- **Dark images look broken on X** — an image with 29K unique colors can still be 90% dark pixels (brightness <50). Grok and other AI image generators often produce moody, near-black images that technically have content but appear as a dark void in X's card preview. **Do NOT rely on ImageEnhance alone to fix very dark backgrounds.** Navy (#080E1A) and near-black backgrounds (RGB channels all < 30) will STILL fail brightness checks even after aggressive enhancement (1.4x). Start with a brighter base background (RGB channels 25-65+) and add light-colored design elements (white text, teal pills, gold accents) to bring dark pixel percentage below 80%. Always check the dark pixel percentage during verification. If >80% of pixels are below brightness 50, regenerate with a lighter background.
- **Vercel static sites don't strip .html extensions for clean URLs** — adding a redirect page like `/wolverine.html` won't be accessible at `/wolverine` without a `vercel.json` rewrite rule: `{"rewrites": [{"source": "/wolverine", "destination": "/wolverine.html"}]}`. Remember this when creating redirect pages or landing pages on Vercel static deploys.
- **Image too small** — Twitter requires at least 300×157 for `summary_large_image`. Under that, it silently falls back to `summary` card. 1200×630 is the safe, recommended size.
- **Crawler can't access the image** — if the site is behind auth, on localhost, or the image URL 404s, Twitter silently falls back to no image. Verify with `curl -I https://[domain]/og-image.png` returns 200.

## Discord & Other Platforms

Discord and most non-X platforms use `og:` tags exclusively (Open Graph protocol). If the card shows correctly on Discord but not on X, the `og:` tags are correct — the problem is X-specific (`twitter:site`, `twitter:creator`, `robots.txt`, or tag ordering). Discord also renders differently: large image cards display at full width in chat with bold title and description, making it a good quick-test platform before debugging X-specific issues.

## X Card Validator Output Interpretation

When using `cards-dev.twitter.com/validator`, the diagnostic output tells you exactly where the problem is:

```
INFO:  Page fetched successfully      → Crawler reached your site (if missing: DNS or server issue)
INFO:  24 metatags were found          → All tags parsed (expect 15-30 for a well-configured page)
INFO:  twitter:card = summary_large_image tag found  → Card type recognized correctly
INFO:  Card loaded successfully        → THE GREEN LIGHT: X can render the card with the image
```

If you see all four INFO lines, the card WILL work — even if the composer preview shows old cached version. Actually posting the tweet pulls fresh data. If any line is missing or shows WARN/ERROR, that's your target.

## Cache-Busting Escalation Path

When X/Twitter won't show the card despite correct tags, escalate through these levels. Each level applies more force to break X's page-level cache.

### Level 0: Verify Image Content FIRST (before anything else)
- **The most common silent failure:** OG image exists, is valid PNG, returns 200, has correct dimensions — but is a solid-color rectangle with no text. X shows the fallback card because there's nothing to display.
- Check unique pixel colors: `python3 -c "from PIL import Image; import requests, io; img=Image.open(io.BytesIO(requests.get('https://domain/og-image.png').content)); print(len(set(img.getdata())))"` — must be >50. 1-5 = blank image, redeploy.
- This single check prevents hours of debugging tag order and cache busting when the image was never the problem.

### Level 1: Verify and Wait
- Confirm tags are live: `curl -s https://domain | grep -E 'og:|twitter:'`
- Confirm image accessible: `curl -I https://domain/og-image.png` returns 200
- Confirm image has content (Level 0 check above)
- Paste URL into X tweet composer (NOT the Card Validator — it no longer shows previews)
- Wait 30-60 minutes. X can take up to 48 hours on newer domains.

**When to escalate:** Tags correct, image 200, but composer still shows no image after 60+ min.

### Level 2: Rename the Image File
- Use a **timestamped filename** for guaranteed uniqueness: `og-image-{unix_ts}.jpg` (not sequential `-v2`, `-v3`, `-final` which risk collision)
- Update `og:image` and `twitter:image` meta tags to new filename
- Push and wait. X may discover the new image reference during a routine re-crawl.
- **Limitation:** This often fails because X caches at the page level — it may never re-crawl the page to discover the new image filename.

**When to escalate:** 30-60 min after Level 2, image still doesn't appear.

### Level 2.5: Switch to JPEG + Add twitter Image Dimensions
- Convert image to **JPEG format** (RGB, not RGBA) — X may handle different MIME types differently for caching
- Add `og:image:type` meta tag: `<meta property="og:image:type" content="image/jpeg">`
- Add explicit `twitter:image:width` and `twitter:image:height` meta tags — X's newer parser sometimes requires these in addition to the `og:` versions for `summary_large_image` cards
- Use a fresh timestamped filename to combine with the format change
- Combined tag block example:
```html
<meta property="og:image" content="https://domain/og-image-{ts}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:type" content="image/jpeg">
<!-- ... --->
<meta name="twitter:image" content="https://domain/og-image-{ts}.jpg">
<meta name="twitter:image:width" content="1200">
<meta name="twitter:image:height" content="630">
```

**When to escalate:** 30-60 min after Level 2.5, image still doesn't appear.

### Level 3: Bump the Page URL (Nuclear Option)
- Change `og:url` from `https://domain` to `https://domain?v=2`
- This is invisible to users but forces X to treat it as a brand new page
- X MUST perform a full re-crawl, discovering all current meta tags and image references
- Increment the version number each time you need another re-crawl (`?v=3`, `?v=4`, etc.)
- **Do NOT add** `?v=N` to the actual page — only to the `<meta property="og:url">` tag

```html
<!-- Before -->
<meta property="og:url" content="https://yoursite.com">
<!-- After (forces re-crawl) -->
<meta property="og:url" content="https://yoursite.com?v=2">
```

**This is the definitive fix.** If Level 3 doesn't work within 30 minutes, something is wrong with the image itself (wrong dimensions, SVG format, CORS blocking, 404).

### Level 4: Add robots.txt + Twitter Identity Tags + Canonical

**⚠️ If you've been debugging for 30+ minutes with correct tags and a verified image, skip directly here.** Level 4 is frequently THE fix when everything looks right but the card won't render — not a last resort. X's 2026 crawler requires explicit permission and identity signals that many sites are missing.

If Levels 1-3 all fail, X may be refusing to crawl due to missing infrastructure or identity signals:

1. **Add `robots.txt`** — a missing robots.txt (404) can cause conservative crawlers to skip the site:
```
User-agent: Twitterbot
Allow: /

User-agent: *
Allow: /
```

2. **Add `twitter:site` and `twitter:creator`** — X's card renderer often requires these for `summary_large_image`:
```html
<meta name="twitter:site" content="@YourHandle">
<meta name="twitter:creator" content="@YourHandle">
```

3. **Add `og:site_name` and `og:locale`** — additional OG metadata that helps crawlers trust the page:
```html
<meta property="og:site_name" content="Site Name">
<meta property="og:locale" content="en_US">
```

4. **Add `<link rel="canonical">`** — X may use this instead of `og:url` to resolve the canonical page:
```html
<link rel="canonical" href="https://yoursite.com">
```

5. **Clean `og:url`** — remove any `?v=N` cache-busting params from previous escalation levels. Once robots.txt and identity tags are in place, return to a clean URL:
```html
<meta property="og:url" content="https://yoursite.com">
```

### Level 5: Image Brightness Enhancement

An image can have thousands of unique colors but STILL look like a dark void. AI-generated images (DALL-E, Grok, Midjourney) often produce moody designs where 90%+ of pixels are below brightness 50. Always verify AND enhance.

**See `references/og-card-brightness-guide.md` for battle-tested background color parameters and enhancement stacks.**

```python
from PIL import Image, ImageEnhance

img = Image.open('og-image.jpg')
pixels = list(img.getdata())
brightness = [(r+g+b)//3 for (r,g,b) in pixels]
dark_pct = 100 * sum(1 for b in brightness if b < 50) / len(brightness)

if dark_pct > 80:
    # Brighten without destroying the design
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.3)      # +30% brightness
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.15)     # +15% contrast
    img.save('og-image-bright.jpg', 'JPEG', quality=93)
```

**Important:** If the source background uses navy/black tones (RGB channels all < 30), enhancers alone won't fix it — even at 1.4x brightness the image stays >94% dark. Regenerate with a lighter background (see reference guide).

**When to escalate past Level 3:** Tags correct, image 200, image has content (Level 0), page URL bumped (Level 3), composer still shows no image after 60+ min across multiple attempts.

## Quality Checklist
- [ ] `twitter:image` + `og:image` are absolute HTTPS URLs
- [ ] Image is 1200×630 PNG or JPG (not SVG)
- [ ] `og:image:width` = 1200, `og:image:height` = 630
- [ ] Deployed and accessible (curl returns 200 for image URL)
- [ ] Validated at cards-dev.twitter.com/validator
- [ ] Card preview shows image, title, and description correctly
