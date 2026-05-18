---
name: nurse-rob-image-gen
description: "Generate consistently branded Nurse Rob Peptide Empire images — navy/teal/gold medical education visuals for X posts, guides, and product pages."
version: 1.0.0
author: Hermes Agent
tags: [nurse-rob, image-gen, branding, peptides, xai]
---

# Nurse Rob Branded Image Generation

Generate on-brand images for Nurse Rob Peptide Empire using xAI Imagine API. Every image follows the Nurse Rob visual identity system.

## Setup (One-Time)

Two-step activation — both required:

```bash
# Step 1: Enable the image_gen toolset
hermes tools enable image_gen

# Step 2: Switch backend from FAL (default) to xAI
hermes plugins enable image_gen/xai

# Step 3: Restart for plugin to take effect
systemctl --user restart hermes-gateway
```

Verify: `XAI_API_KEY` must be set in `~/.hermes/.env`. The key from [console.x.ai](https://console.x.ai) works for chat, image gen, and video gen — one key covers all endpoints.

**⚠️ Gotcha:** After enabling `image_gen/xai` plugin, the `image_generate` tool won't route to xAI until the gateway restarts AND a new session starts. Until then, it falls back to FAL and fails with `FAL_KEY environment variable is not set`. Use `scripts/generate_image.py` (direct API) as immediate workaround.

## Brand Constants

Always embed these in every prompt:

```
COLORS:
- Background: deep navy #0A1F3F
- Primary accent: teal #00C4B4
- Secondary accent: gold #C9A84C
- Text: clean white on navy backgrounds

TYPOGRAPHY VIBE:
- Headlines: elegant serif (Cormorant Garamond style)
- Body: clean modern sans-serif (Inter style)
- Medical/professional feel, not clinical

STYLE:
- Glass-morphism cards with subtle borders
- Medical education aesthetic — clean, trustworthy, modern
- Subtle gradients, soft glows on accent elements
- Molecular/peptide-chain decorative elements when relevant
- NO: cartoon style, clip art, overly corporate stock photo look
```

## Content-Type Templates

### 1. X Post Image (Landscape 16:9)

Best for the 2x/day X posts. Bold, scannable, designed for mobile feed.

```
PROMPT: Medical education social media graphic, 16:9 landscape.
Background: deep navy #0A1F3F with subtle molecular pattern overlay.
A glass-morphism card in the center with teal #00C4B4 border glow.
[HOOK TEXT] in elegant serif white font at top.
[SUBHEADING] in smaller gold #C9A84C Inter-style font below.
Subtle peptide chain icon or DNA helix element in teal, small, bottom corner.
Professional medical education aesthetic — clean, modern, trustworthy.
NO text rendering errors, NO garbled letters.
```

### 2. Product/Protocol Card (Square 1:1)

For product spotlights, protocol guides, comparison posts.

```
PROMPT: Medical product card, square 1:1.
Background: deep navy #0A1F3F.
Central glass card with rounded corners, teal #00C4B4 thin border, subtle inner glow.
Top: peptide name in gold #C9A84C elegant serif.
Middle: 2-3 bullet points in white Inter-style text (dosage, frequency, benefits).
Bottom: small teal molecular structure icon.
Clean medical education design — no clutter, no cartoon elements.
```

### 3. Guide/Educational Header (Landscape 16:9)

For blog headers, guide covers, long-form content.

```
PROMPT: Educational medical guide header, 16:9 landscape.
Background: deep navy #0A1F3F with gradient fade to darker bottom.
Top third: [GUIDE TITLE] in elegant white serif, large.
Middle: subtle teal #00C4B4 decorative line separator.
Bottom third: "Nurse Rob, RN" in gold #C9A84C, "Evidence-Based Peptide Education" in small white below.
Professional, academic-medical feel — like a journal cover but modern.
```

### 4. Comparison Graphic (Landscape 16:9)

For BPC-157 vs TB-500, Semaglutide vs Tirzepatide, etc.

```
PROMPT: Medical comparison graphic, 16:9 landscape.
Background: deep navy #0A1F3F.
Two glass cards side by side with subtle teal #00C4B4 borders.
Left card: [PEPTIDE A NAME] in gold #C9A84C, with 3 key features in white below.
Right card: [PEPTIDE B NAME] in gold #C9A84C, with 3 key features in white below.
"VS" in teal glow between the cards.
Professional medical education layout — balanced, clean, trustworthy.
```

### 5. Video Thumbnail (Landscape 16:9)

For short-form video covers.

```
PROMPT: Video thumbnail, 16:9 landscape, bold and eye-catching.
Background: deep navy #0A1F3F with dramatic teal #00C4B4 light rays from center.
Center: [TOPIC] in large white elegant serif, with gold #C9A84C underline accent.
Bottom-left: "Nurse Rob, RN" in small white.
Bottom-right: play button icon in teal.
High contrast, designed to stop the scroll — YouTube thumbnail energy but medical-professional.
```

## Usage

### Method A: Direct xAI API (Works Immediately)

The `image_generate` Hermes tool may default to FAL even when the `image_gen/xai` plugin is enabled — the plugin takes effect on next session restart. Use the bundled Python script for immediate image generation:

```bash
python3 ~/.hermes/skills/productivity/nurse-rob-image-gen/scripts/generate_image.py \
  --prompt "[FILLED TEMPLATE]" \
  --aspect landscape \
  --output "/mnt/c/Users/Robert/Desktop/Daily Brief/NurseRob_PeptideEmpire/images/YYYY-MM-DD_post1.jpg"
```

The script reads `XAI_API_KEY` from `~/.hermes/.env`, calls `POST https://api.x.ai/v1/images/generations` with model `grok-imagine-image`, downloads the result, and prints the output path + cost. Supported `--aspect` values: `landscape`, `square`, `portrait`.

**Cost:** $0.02/image (grok-imagine-image). $0.05-0.07/image (grok-imagine-image-quality — use `--quality hq`).

### Method B: Hermes image_generate Tool (After Session Restart)

Once the gateway has been restarted after enabling the `image_gen/xai` plugin, the `image_generate` tool routes through xAI automatically:

```python
image_generate(
    prompt="[use one of the templates above, filled in with actual content]",
    aspect_ratio="landscape"  # or "square" or "portrait"
)
```

If `image_generate` returns a `FAL_KEY` error, the plugin hasn't activated yet — use Method A.

## Integration with peptide_content_operator

When generating content via `peptide_content_operator`:
1. Generate the post text first
2. Extract the hook/title from the post
3. Pick the appropriate template based on content type
4. Call `image_generate` with the filled template
5. Deliver both text + MEDIA path together

## Quality Checklist

Before using an image:
- [ ] Navy background present?
- [ ] Teal accent visible?
- [ ] Gold used for emphasis?
- [ ] Text looks clean (no garbled letters)?
- [ ] Medical-professional, not cartoon?
- [ ] Right aspect ratio for platform?

## Pitfalls
## Pitfalls

- **AI text rendering**: Image gen models sometimes garble text. If text in the image looks wrong, simplify the text in the prompt or use fewer words.
- **Color drift**: If colors drift from brand, reinforce "deep navy #0A1F3F, teal #00C4B4 accent only" in the prompt.
- **Cartoon creep**: Some models default to illustration style. Add "photorealistic medical education graphic, not cartoon, not illustration" if needed.
- **Cost awareness**: grok-imagine-image = ~$0.02/image. grok-imagine-image-quality = ~$0.05-0.07/image. Use standard for posts, quality for hero/guide images. Full pricing in `references/xai-api-pricing.md`.
- **Temp URLs expire**: xAI image URLs are temporary (~24hrs). For permanent use, download and save to the website assets folder.
- **X API free tier limitation (May 17, 2026)**: Images auto-generate to Desktop but CANNOT be attached to tweets via API. Media upload works but tweet creation rejects media_ids on free tier. Content scheduler posts text-only; images wait on Desktop for manual attach in X app. Upgrade to X API Basic ($100/mo) enables `--media-id` flag for automated image posting.
- **xAI API vs X Premium**: These are completely separate. X Premium ($8/mo blue check) does NOT include xAI API access. xAI API key comes from console.x.ai — one key covers chat, image gen, video gen, and voice.
- **X API free tier**: Cannot attach images to tweets via API. Images save to Desktop for manual attach in X app. See `content_scheduler` skill for details.
