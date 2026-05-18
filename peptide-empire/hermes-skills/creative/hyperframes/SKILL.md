---
name: hyperframes
description: Create HTML-based video compositions, animated title cards, social overlays, captioned talking-head videos, audio-reactive visuals, and shader transitions using HyperFrames. HTML is the source of truth for video. Use when the user wants a rendered MP4/WebM from an HTML composition, wants to animate text/logos/charts over media, needs captions synced to audio, wants TTS narration, or wants to convert a website into a video.
version: 1.0.0
author: heygen-com
license: Apache-2.0
platforms: [linux, macos, windows]
prerequisites:
  commands: [node, ffmpeg, npx]
metadata:
  hermes:
    tags: [creative, video, animation, html, gsap, motion-graphics]
    related_skills: [manim-video]
    category: creative
    requires_toolsets: [terminal]
---

# HyperFrames

HTML is the source of truth for video. A composition is an HTML file with `data-*` attributes for timing, a GSAP timeline for animation, and CSS for appearance. The HyperFrames engine captures the page frame-by-frame and encodes to MP4/WebM with FFmpeg.

Full skill reference: `~/.hermes/hermes-agent/optional-skills/creative/hyperframes/SKILL.md`

## Quick Reference

```bash
npx hyperframes init my-video --example kinetic-type --non-interactive
npx hyperframes tts "Script text..." --voice am_adam --output narration.wav  # male, warm
npx hyperframes lint && npx hyperframes render --quality high --fps 30 --output final.mp4
```

## Setup

```bash
# Fix npm global install on Linux/WSL
npm config set prefix ~/.npm-global
export PATH="$HOME/.npm-global/bin:$PATH"
npm install -g hyperframes@latest

# Install Chrome headless shell for rendering
npx hyperframes browser ensure

# Install TTS engine
pip install kokoro-onnx soundfile
```

## Branded Video Workflow

See [references/branded-video-workflow.md](references/branded-video-workflow.md) for the end-to-end pattern: extract brand identity from project files → DESIGN.md → scaffold → TTS → render.

## References

- [branded-video-workflow.md](references/branded-video-workflow.md) — End-to-end branded video production pattern (brand extraction, DESIGN.md, TTS narration, composition structure, rendering)
- [mobile-sizing.md](references/mobile-sizing.md) — **MOBILE-FIRST sizing.** 1920×1080 → 5" phone = 1/8 scale. All elements 50-75% larger than desktop-default. Sizing table for titles, body, cards, icons.

## Pitfalls

- **npm global install fails on Linux/WSL**: Set npm prefix before install (see Setup above).
- **TTS fails with "kokoro-onnx not installed"**: `pip install kokoro-onnx soundfile`
- **Chrome headless shell missing**: `npx hyperframes browser ensure`
- **`repeat: -1` anywhere**: Breaks capture engine. Always compute finite repeat count.
- **Audio shorter than composition**: HyperFrames does NOT truncate to audio length. Composition runs full `data-duration`.
