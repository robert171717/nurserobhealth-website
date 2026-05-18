# Branded Video Workflow (HyperFrames)

End-to-end pattern for producing a branded animated explainer with TTS narration when no formal DESIGN.md exists in the project.

## Step 1: Extract Brand Identity from Project Files

When Firecrawl/website scraping is unavailable, mine the project's own files:

```bash
grep -rni '#[0-9a-fA-F]\{6\}' ~/ProjectName/
grep -rni 'color\|brand\|hex' ~/ProjectName/
```

Key sources: content calendars (image prompts often have color specs), project blueprints, existing posts.

## Step 2: Build Minimal DESIGN.md

```markdown
## Colors
- Primary: #XXXXXX (role)
- Background: #XXXXXX (role)
- Accent: #XXXXXX (role)
- Text secondary: #XXXXXX (role)

## Typography
- Headlines: [serif font] (authority)
- Body: [sans-serif font] (clean)

## What NOT to Do
- 3-5 anti-patterns
```

## Step 3: Scaffold + Customize

```bash
npx hyperframes init my-video --example kinetic-type --non-interactive
```

Replace index.html + compositions/main-graphics.html with custom branded composition.
- 1920×1080 for horizontal (X, YouTube) or 1080×1920 for vertical (TikTok, Reels)
- 5 scenes sweet spot for 60s explainers: Hook(0-12s) → What(12-24s) → How(24-36s) → Protocol(36-50s) → CTA(50-60s)
- Use GSAP `gsap.timeline({ paused: true })` registered on `window.__timelines["composition-id"]`

## Step 4: TTS Narration

```bash
npx hyperframes tts "Script text..." --voice af_nova --output assets/narration.wav
```

Voice reference (English, all Kokoro-82M):
- `am_adam` — warm, natural male voice (preferred for authoritative-medical when the persona is male)
- `af_nova` — clear, direct female voice
- `af_heart` — softer, warmer female voice
- `af_sky` — bright female voice
- `am_michael` — deeper male voice

List all voices with `--list`. Match narration pacing to scene timing — write the script with natural pauses (period breaks, not comma-spliced). Audio `data-duration` = actual spoken length. Visuals can extend past audio for breathing room and CTA hold.

## Step 5: Render + Verify

```bash
npx hyperframes lint --strict
npx hyperframes render --quality high --fps 30 --output final.mp4

# Verify
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 final.mp4
ls -lh final.mp4
```

## Example: Nurse Rob Peptide Empire Brand\n\nBrand extracted from project Content_Calendar files (`navy scrubs (#1B2A4A)`, `navy+white+red scheme`, `clean medical education aesthetic`). User later evolved palette for video:\n\n| Role | Color | Hex |\n|------|-------|-----|\n| Background | Deep navy | `#0A1F3F` |\n| Primary accent | Teal | `#00C4B4` |\n| Prestige highlight | Gold | `#C9A84C` |\n| Text primary | White | `#FFFFFF` |\n| Text secondary | White 50% | `rgba(255,255,255,0.5)` |\n\n| Element | Font | Role |\n|---------|------|------|\n| Headlines / titles | Cormorant Garamond (serif) | Authority, editorial prestige |\n| Body / labels / UI | Inter (sans-serif) | Clean, modern, readable |\n\n**What NOT to Do:** No red accents (replaced by teal). No white backgrounds (use dark navy). No rushed TTS pacing. No default system fonts (Roboto, Arial). No flat design without depth (use grid overlays, radial glows, translucent card borders).\n\nBrand files live at `~/NurseRob_PeptideEmpire/`. Extract updated brand from `Content_Calendar/30_Day_Calendar_*.md` image prompts and `NurseRob_Empire_Blueprint.md`.\n\n## Setup Pitfalls

- **npm global install fails on Linux/WSL**: `npm config set prefix ~/.npm-global && export PATH="$HOME/.npm-global/bin:$PATH"` before `npm install -g hyperframes`
- **TTS fails with "kokoro-onnx not installed"**: `pip install kokoro-onnx soundfile` in active Python environment
- **Chrome headless shell missing**: `npx hyperframes browser ensure`
- **Audio shorter than composition**: HyperFrames does NOT truncate to audio length — composition runs its full `data-duration`. Audio just stops playing when it ends.
