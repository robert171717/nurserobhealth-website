---
name: nurse-rob-video-production
description: Produce branded medical education videos for Nurse Rob Peptide Empire using HyperFrames — kinetic typography explainers with TTS narration, brand colors, and social-media-ready output. Load when asked to create a peptide explainer video, animate the Wolverine Stack guide, or produce social video content for @NurseRobHealth.
version: 1.0.0
metadata:
  hermes:
    tags: [video, hyperframes, nurse-rob, peptide, branding]
    category: productivity
    requires_toolsets: [terminal]
---

# Nurse Rob Video Production

Produce branded medical education videos using HyperFrames. This skill encodes the Nurse Rob brand identity, composition patterns, and production workflow for peptide explainers.

**Depends on:** HyperFrames skill (`hyperframes`) for CLI commands, GSAP patterns, and composition rules. Load both.

## Brand Identity

See `references/nurse-rob-brand.md` for the full brand spec. Quick reference:

| Element | Value |
|---------|-------|
| Primary | `#1B2A4A` (navy) |
| Accent | `#C0392B` (medical red) |
| Background | `#F7F9FC` (light gray) |
| Display font | Playfair Display 700-900 |
| Body font | Inter 400-600 |
| Canvas | Light mode only |

## Video Types

### 1. Medical Explainer (60-90s)
Purpose: Educate on a single peptide. Structure:
```
0-12s  → Hook: peptide name + one-line value prop
12-24s → What: amino acids, origin, class
24-36s → How: mechanism of action (angiogenesis, receptors)
36-50s → Protocol: dosing, frequency, cycle length
50-60s → CTA: "DM [keyword]" + "Nurse Rob, RN" + consult link
```

### 2. Protocol Walkthrough (45-60s)
Purpose: Step-by-step injection/dosing guide.

### 3. Social Short (15-30s)
Purpose: Vertical (1080×1920) for TikTok/Reels/Shorts.

## Production Workflow

### Step 1: Generate TTS Narration
```bash
npx hyperframes tts "Script text here..." --voice af_nova --output assets/narration.wav
```
**Pitfall:** TTS needs `pip install kokoro-onnx soundfile` first. If "kokoro-onnx package is not installed", install it and retry.

### Step 2: Scaffold Project
```bash
npx hyperframes init video-name --example kinetic-type --non-interactive
cd video-name
```

### Step 3: Build Composition
Use `templates/medical-explainer.html` as starter. Replace content while keeping:
- Nurse Rob brand colors and fonts
- Medical badge at top
- Branding bar at bottom
- Fade transitions between scenes
- GSAP timeline registered on `window.__timelines`

### Step 4: Lint + Render
```bash
npx hyperframes lint
npx hyperframes render --quality high --fps 30 --output final.mp4
```

### Step 5: Deliver
Copy to `"/mnt/c/Users/Robert/Desktop/Daily Brief/NurseRob_PeptideEmpire/[video-name].mp4"`

## Scene Animation Pattern

Every scene follows this pattern:
1. `tl.set("#scene-N", { opacity: 1 }, startTime)` — make visible
2. Stagger entrances: title → cards/items (0.5s stagger) → subtitle
3. Hold for reading time (2-3× the narration passage length)
4. Fade out: `tl.to("#scene-N", { opacity: 0 }, endTime)`
5. Fade overlay flash: `tl.to(".fade-overlay", { opacity: 0.3, duration: 0.15 })` → `tl.to(".fade-overlay", { opacity: 0, duration: 0.15 })`

## Pitfalls

- **TTS kokoro-onnx missing:** `pip install kokoro-onnx soundfile` in Hermes venv
- **npm install -g permission denied (WSL2):** `npm config set prefix ~/.npm-global && export PATH="$HOME/.npm-global/bin:$PATH"`
- **Chrome not found:** `npx hyperframes browser ensure`
- **Mismatched data-duration:** index.html and sub-composition durations must agree. If narration is only 36s but video is 60s, index.html duration=60, audio data-duration=36.2, graphics data-duration=60
- **`gsap.timeline` not on `window.__timelines`:** HyperFrames engine reads `window.__timelines` to control playback. Every composition MUST register its timeline there.

## References

- [nurse-rob-brand.md](references/nurse-rob-brand.md) — Full brand identity (colors, fonts, design rules, anti-patterns)
- [medical-explainer.html](templates/medical-explainer.html) — 60s 5-scene composition template with `{{PLACEHOLDERS}}` — copy and replace content
