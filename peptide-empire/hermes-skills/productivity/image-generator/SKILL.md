---
name: image-generator
description: Generates all graphics for Nurse Rob Peptide Empire via Hermes image_gen — thread headers, carousels, stat cards, Reels thumbnails, logos
version: 1.0
author: Nurse Rob
---

# Image Generator 🎨

**Purpose:** Centralized image generation for all Nurse Rob Peptide Empire content. Uses Hermes `image_generate` tool for thread headers, carousel slides, stat cards, Reels thumbnails, and branding assets.

## TRIGGER
- Called by: peptide_content_operator, content-batch-generator, video-repurposer
- Manual: "generate image for [content]" / "create graphic for [topic]"

## SETUP — xAI Image Generation (Zero Cost Path)

Hermes `image_generate` tool requires an xAI API key. This is SEPARATE from X Premium — no upgrade needed.

### One-Time Setup
1. Go to [console.x.ai](https://console.x.ai) → sign up (free account)
2. Create API key → copy it
3. Add to Hermes: `hermes config set providers.xai.api_key ${XAI_API_KEY}` + add `XAI_API_KEY=xai-...` to `~/.hermes/.env`
4. Enable tool: `hermes tools enable image_gen`
5. Restart: `systemctl --user restart hermes-gateway`

### Cost: $0/month for Nurse Rob's volume
xAI gives **$25/month free API credits**. Nurse Rob's usage at 60 images/month (2/day):
- Standard quality (`grok-imagine-image`): $0.02/image → **$1.20/month**
- HQ quality (`grok-imagine-image-quality`): $0.05-0.07/image → **$3.00-4.20/month**
- Well within free credits. Pure pay-as-you-go beyond $25 — no subscription.

Full pricing breakdown: `references/xai-api-pricing.md`

### Pitfall — X Premium ≠ xAI API
- X Premium (blue check, $8/mo) does NOT include API access
- X Premium+ ($16/mo) is NOT required for image gen
- Supergrok is NOT required for image gen
- The xAI API is a separate free account at console.x.ai

## PROFILE ROUTING
Use `creative-mode` (gpt-5.5-codex) for prompt engineering.

## NURSE ROB BRANDING SPECS
- **Subject:** Professional male nurse, 30s, approachable but authoritative
- **Colors:** Navy blue (#0A1F3F) + Teal (#00C4B4) + Gold (#C9A84C) — no red
- **Style:** Clean, clinical, modern — think "premium medical education" not "influencer"
- **Lighting:** Bright, natural, warm — like a modern clinic
- **Typography feel:** Cormorant Garamond for headlines, Inter for body text

## IMAGE TYPES & PROMPTS

### 1. Thread Headers (16:9 Landscape)
```
Professional male nurse (30s),
wearing modern navy scrubs with subtle RN patch, standing in bright modern clinic,
clean white background with subtle medical cross pattern,
warm professional lighting, confident but approachable expression,
looking directly at camera, slight knowing smile,
text overlay space on right side (30% of image),
"Nurse Rob, RN" subtle branding in corner,
4K photorealistic, editorial style
```

### 2. Carousel Slides (1:1 Square)
```
Clean medical education slide, navy (#0A1F3F) and white color scheme,
modern minimalist design, bold [KEY STAT NUMBER] in large white font,
subtle medical iconography (molecule, DNA helix, cross),
3 data points arranged cleanly, teal (#00C4B4) accent lines,
gold (#C9A84C) highlights on key numbers,
"Nurse Rob, RN" small branding bottom-right,
clean infographic style, high contrast, readable
```

### 3. Stat Cards (1:1 Square)
```
Bold stat card design — navy background (#0A1F3F),
large white number "[STAT]" centered prominently,
small subtitle text "[LABEL]" below in teal (#00C4B4),
thin gold accent line (#C9A84C) separating number from label,
"Nurse Rob, RN" small watermarked bottom-right,
clean, clinical, premium feel
```

### 4. Reels/Shorts Thumbnails (9:16 Portrait)
```
Professional male nurse (30s), expressive face showing [EMOTION: surprise/concern/confident],
wearing navy scrub top, clean modern background,
bold text overlay: "[HOOK TEXT]" in large white font with dark shadow,
teal accent underline (#00C4B4) beneath key word,
"Nurse Rob, RN" small branding,
high contrast, eye-catching, YouTube thumbnail style
```

### 5. Quote Cards (1:1 Square)
```
Clean white background with subtle texture,
large navy (#0A1F3F) quote text: "[QUOTE]" in elegant serif,
"Nurse Rob, RN" attribution below in teal (#00C4B4),
thin gold line (#C9A84C) separating quote from attribution,
minimalist, premium, shareable
```

### 6. Lead Magnet Cover (3:4 Portrait)
```
Professional e-book cover design,
title: "WOLVERINE STACK CALCULATOR & GUIDE" in bold white,
subtitle: "by Nurse Rob, RN" in teal (#00C4B4),
deep navy background with subtle molecular structure patterns,
gold (#C9A84C) accent borders,
modern clean layout, premium feel,
photorealistic medical textbook quality
```

### 7. Consult Promo (16:9 Landscape)
```
Split design — left 60%: professional male nurse in navy scrubs,
right 40%: navy (#0A1F3F) background with white text:
"PEPTIDE CONSULTATION"
"1-on-1 Clinical Review"
"$197 — 30 Minutes"
Teal (#00C4B4) CTA button: "BOOK NOW"
Clean, premium, trustworthy
```

## WORKFLOW

### Step 1: Receive Request
Other skills call with: "Generate [image_type] for [topic/content]"
Include: image type, text to overlay, emotion/tone, specific data points.

### Step 2: Select Prompt Template
Choose from templates above based on image_type.

### Step 3: Customize Prompt
- Insert specific text, data, hook into template
- Adjust emotion/tone based on content (serious for safety, confident for authority)
- Ensure Nurse Rob branding elements included

### Step 4: Generate Image
```python
image_generate(
    prompt="[customized prompt]",
    aspect_ratio="[landscape|square|portrait]"
)
```

### Step 5: Save & Return
Save to: `~/NurseRob_PeptideEmpire/images/[type]/[date]_[slug].png`
Return path to requesting skill.

## BATCH GENERATION (For content-batch-generator)
When generating 30 days of content:
1. Generate 10 thread header images (16:9)
2. Generate 10 carousel slide sets (1:1, 5-7 slides each)
3. Generate 5 stat cards (1:1)
4. Generate 5 engagement post images (1:1)
5. Save all to date-organized folders

## PITFALLS
- Nurse Rob visual must remain consistent across generations
- Don't use medical symbols that imply "doctor" — use RN badge, not stethoscope
- Keep text simple — no long paragraphs on images
- Always include "Nurse Rob, RN" branding
- Teal accent should be #00C4B4 and gold #C9A84C specifically — consistent brand colors (NOT red)

## QUALITY CHECKLIST
- [ ] Correct aspect ratio for platform
- [ ] Nurse Rob branding visible
- [ ] Text readable at small sizes
- [ ] Color scheme consistent (navy #0A1F3F + teal #00C4B4 + gold #C9A84C)
- [ ] Image saved to correct folder
- [ ] No misleading medical imagery
- [ ] Disclaimer space available if needed
