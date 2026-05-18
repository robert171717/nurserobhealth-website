# HyperFrames Integration for Nurse Rob Peptide Empire

HyperFrames (by HeyGen, available as optional skill: `optional-skills/creative/hyperframes/`) is an HTML-native video composition engine — GSAP animations + CSS styling + TTS narration + captions, rendered deterministically to MP4/WebM via headless Chrome + FFmpeg.

## Why HyperFrames > Raw FFmpeg

The current `video-repurposer` pipeline uses raw FFmpeg for captions, overlays, and branding. HyperFrames replaces the fragile FFmpeg filter chains with HTML/CSS/GSAP compositions that are:
- **Deterministic** — same HTML always produces the same frames (no `Math.random()`, no async)
- **Agent-authorable** — the agent writes HTML/CSS/GSAP directly, no FFmpeg filter syntax memorization
- **Professional quality** — shader transitions, marker highlighting, audio-reactive visuals, proper typesetting

## 6 Empire Use Cases (Session 2026-05-14)

| # | Use Case | Empire Impact |
|---|----------|---------------|
| 1 | **Peptide Education Reels** | Animated BPC-157/TB-500 explainers with TTS narration + captions synced to waveform |
| 2 | **X Video Posts** | Social overlays for vertical video — replaces static thread graphics |
| 3 | **Website-to-Video Promo** | Capture nurserobhealth.com → animate with overlays → 90s promo for X + pharmacy outreach |
| 4 | **Video Repurposer Upgrade** | video-repurposer cuts 8-12 raw clips → HyperFrames adds captions, lower-thirds, transitions per clip |
| 5 | **Pharmacy Outreach Decks** | Animated pitch videos attached to pharmacy-outreach-automator emails |
| 6 | **Welcome Sequence Video** | nurserob-onboarding email #1 gets animated lead magnet instead of static PDF |

## Integration Point with video-repurposer

The most immediate win is **Use Case #4**: `video-repurposer` identifies clip moments and extracts raw MP4 segments. Instead of burning captions with FFmpeg `subtitles=` filter, the extracted clip becomes a `<video>` element in a HyperFrames composition that layers:
- Captions (word-level, synced to waveform via `npx hyperframes transcribe`)
- Lower-third name bar ("Nurse Rob, RN")
- Animated CTA overlay
- Disclaimer watermark
- Scene transitions (crossfade, push-slide, etc.)

## Setup

```bash
# One-time install
bash ~/.hermes/hermes-agent/optional-skills/creative/hyperframes/scripts/setup.sh

# Verify
npx hyperframes doctor
```

Requires: Node.js >= 22, FFmpeg (already installed on WSL2), chrome-headless-shell (setup script handles this).

## Workflow: Clip → HyperFrames Composition

```
video-repurposer Step 4 (clip specs)
         ↓
Shell script generates one HyperFrames composition per clip
  - <video> element: raw clip .mp4
  - <audio> element: extracted audio (muted video + separate audio)
  - GSAP timeline: captions fade in/out per word timing
  - Animated overlays: lower-third, CTA, disclaimer
         ↓
npx hyperframes render --quality high --output clip_01_final.mp4
         ↓
content_scheduler posts to X/Discord
```

## Key HyperFrames Commands

```bash
npx hyperframes init my-clip                    # scaffold
npx hyperframes lint                            # validate before render
npx hyperframes preview                          # live-reload browser preview (port 3002)
npx hyperframes render --output final.mp4        # MP4 output
npx hyperframes tts "Script" --voice af_nova     # TTS narration
npx hyperframes transcribe narration.wav         # word-level captions
npx hyperframes doctor                           # diagnose issues
```

## Pitfalls Specific to Empire Integration

- **`repeat: -1`** breaks the capture engine — always compute finite repeat counts
- **Captions must hard-kill after exit** — `tl.set(el, { opacity: 0, visibility: "hidden" }, group.end)` or groups leak visible into later caption segments
- **Timeline must be synchronous** — no `async`/`await`/`setTimeout` during `window.__timelines` registration
- **`chrome-headless-shell` required** — system Chrome hangs for 120s then times out. Setup script installs it.
- **`hyperframes@>=0.4.2` required** — Chromium 147+ removed `HeadlessExperimental.beginFrame`. v0.4.2+ auto-falls back to screenshot mode.
