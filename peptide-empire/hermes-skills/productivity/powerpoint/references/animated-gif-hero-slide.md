# Animated GIF Hero Slides in PowerPoint (PptxGenJS)

## Overview

PptxGenJS supports animated GIFs natively via `slide.addImage()`. This enables impressive hero/reveal slides with looping animations. The workflow: obtain a video (MP4) → convert to optimized GIF with ffmpeg → embed in PptxGenJS → PowerPoint plays it automatically.

## ffmpeg Conversion Recipe

### Raw conversion (high quality, large file)

```bash
ffmpeg -i input.mp4 -vf "fps=15,scale=960:522:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5" -loop 0 output.gif -y
```

Typical result: ~24MB for 10 seconds @ 15fps, 960px wide.

### Optimized conversion (presentation-ready)

```bash
ffmpeg -i input.mp4 -vf "fps=10,scale=800:435:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=96[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5" -loop 0 output.gif -y
```

Typical result: ~11MB for 10 seconds @ 10fps, 800px wide. Good balance of quality and file size.

### Parameters explained

| Flag | Purpose |
|------|---------|
| `fps=10` | Frames per second — 10fps is smooth enough for most animations |
| `scale=800:435` | Output dimensions — calculate height from 16:9 ratio (800 × 9/16 ≈ 435) |
| `flags=lanczos` | High-quality scaling algorithm |
| `palettegen=max_colors=96` | Color palette size — 96 colors is a good balance |
| `paletteuse=dither=bayer:bayer_scale=5` | Dithering for smooth gradients |
| `-loop 0` | Infinite loop (required for PowerPoint) |
| `-y` | Overwrite output without prompt |

## Embedding in PptxGenJS

```javascript
s.addImage({ 
    path: "/tmp/cybercab_hero.gif",
    x: 0.8, y: 0.2, 
    w: 8.4, h: 3.8, 
    sizing: { type: "contain", w: 8.4, h: 3.8 }
});
```

The GIF will animate automatically when the slide is displayed in PowerPoint. No special settings needed.

## Hero Slide Design Pattern

A hero slide with an animated GIF typically uses:

```javascript
const s = pres.addSlide();
s.background = { color: DARK };  // Dark background for contrast
sectionBar(s, 0, 0, 10, 0.04, GOLD);  // Thin accent line at top

// Large centered animated GIF (fills ~70% of slide)
s.addImage({ path: "/tmp/hero.gif", x: 0.8, y: 0.2, w: 8.4, h: 3.8, 
             sizing: { type: "contain", w: 8.4, h: 3.8 } });

// Dramatic tagline below the GIF — bold, centered, gold accent
s.addText("MEET THE FUTURE. NOW.", {
    x: 0.5, y: 4.2, w: 9, h: 0.55, fontSize: 20, color: GOLD,
    fontFace: "Arial Black", align: "center", charSpacing: 4, margin: 0
});

// Subtitle — lighter, italic
s.addText("Supporting tagline text here", {
    x: 0.5, y: 4.75, w: 9, h: 0.4, fontSize: 14, color: LIGHT,
    fontFace: "Calibri", align: "center", italic: true, margin: 0
});

sectionBar(s, 0, 5.585, 10, 0.04, GOLD);  // Bottom accent line
```

## File Size Considerations

- Total PPTX should stay under 20MB for easy sharing
- GIF should be ≤15MB (the rest of a 16-slide icon-heavy deck is ~4MB)
- If total exceeds 25MB, reduce frame rate or scale further
- PowerPoint handles large GIFs fine — the limit is email/file-sharing constraints

## Alternatives When ffmpeg is Unavailable

- **Static image hero**: Use `image_generate` tool for a dramatic AI-generated image
- **GIF from web**: Use the `gif-search` skill to find relevant GIFs via Tenor API
- **User-supplied media**: Ask the user to provide an image/GIF/video and convert/embed
