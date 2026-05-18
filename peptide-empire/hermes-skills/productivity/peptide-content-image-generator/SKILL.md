---
name: peptide-content-image-generator
description: Generate branded images for Nurse Rob peptide content — X posts, educational graphics, protocol cards. Uses navy/teal/gold branding with consistent RN-educator style.
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [nurse-rob, peptide, content, image-generation, branding]
---

# Peptide Content Image Generator

Generates branded images for Nurse Rob's peptide education content using the `image_generate` tool.

## Brand Specs

- **Primary BG:** Navy #0A1F3F
- **Accent:** Teal #00C4B4
- **Highlight:** Gold #C9A84C
- **Fonts:** Cormorant Garamond (headlines), Inter (body)
- **Style:** Clean, clinical, educational — warm nurse vibe, not pharma-cold

## When to Use

- Generating images for X posts (landscape 16:9)
- Creating educational peptide graphics
- Protocol/dosing reference cards
- Quote cards from research

## Image Types

### 1. Educational Post Image
For peptide education tweets. Landscape. Clean infographic style.
```
image_generate(
  prompt="Educational peptide infographic. Navy (#0A1F3F) background with teal (#00C4B4) accents and gold (#C9A84C) highlights. [TOPIC TITLE] in large white Cormorant Garamond text at top. 3-4 key bullet points in Inter font below. Clean medical-educational style. Professional nurse educator brand. No bro-science aesthetic. Research-backed, clinical feel. Subtle molecular or DNA motif in background.",
  aspect_ratio="landscape"
)
```

### 2. Protocol Card
For dosing/protocol reference images. Square for mobile readability.
```
image_generate(
  prompt="Clean protocol reference card. Navy (#0A1F3F) background. '[PEPTIDE NAME] Protocol' in teal (#00C4B4) at top. Dosing information in white text below: dosing schedule, injection method, cycle length. Gold (#C9A84C) caution line at bottom: 'RN Education — Not Medical Advice.' Professional clinical design. Pharmacist-grade layout. White text on navy, high contrast for mobile screens.",
  aspect_ratio="square"
)
```

### 3. Quote/Stat Card
For research citation or key fact posts.
```
image_generate(
  prompt="Research citation card. Navy (#0A1F3F) gradient background with subtle DNA helix pattern. Large quote or statistic in white Cormorant Garamond centered. Source citation in small teal (#00C4B4) Inter at bottom. Gold (#C9A84C) accent line. Scientific journal aesthetic. Clean, authoritative, trustworthy nurse educator brand.",
  aspect_ratio="landscape"
)
```

### 4. Comparison Graphic
For comparing peptides, protocols, or approaches.
```
image_generate(
  prompt="Side-by-side comparison infographic. Split navy (#0A1F3F) background. Left side and right side each with a header in teal (#00C4B4). Comparison points in white text with gold (#C9A84C) bullets. Clean medical-educational design. Mobile-readable. Professional RN educator brand.",
  aspect_ratio="landscape"
)
```

## Quick Reference

| Content Type | Ratio | Style |
|---|---|---|
| Educational post | landscape | Infographic, 3-4 bullets |
| Protocol card | square | Dense info, clinical |
| Quote/stat | landscape | Large text, cited |
| Comparison | landscape | Two-column, clean |
| Safety/risk flag | square | Bold, caution-oriented |

## Usage Pattern

When generating content for Nurse Rob posts:
1. Generate the post text
2. Pick the appropriate image type
3. Generate the image using the template above
4. Deliver both together

## Pitfalls

- Don't use AI-looking or "bro-science" aesthetics — keep it clinical and educational
- Text in images must be large enough for mobile (5" screens minimum)
- Always include "RN Education — Not Medical Advice" on protocol/reference images
- Avoid stock-photo medical imagery — stick to clean typographic and molecular motifs
- Colors must be exactly navy #0A1F3F, teal #00C4B4, gold #C9A84C for brand consistency
