# Converting MP4 to Animated GIF for PowerPoint

PptxGenJS supports animated GIFs (not MP4 video). Convert MP4 to GIF with ffmpeg before embedding.

## Quick conversion

```bash
ffmpeg -i input.mp4 -vf "fps=10,scale=800:435:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=96[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5" -loop 0 output.gif -y
```

## Parameters explained

| Flag | Effect | Tuning |
|------|--------|--------|
| `fps=10` | 10 frames/sec | 10 is smooth enough for PowerPoint; 15 doubles file size |
| `scale=800:435` | Output resolution | Match to slide display area (~8" wide at 100dpi) |
| `max_colors=96` | Color palette size | 96 is good for photos; 64 is smaller but posterized |
| `dither=bayer:bayer_scale=5` | Dithering method | Bayer dithering is fast and produces small files |
| `-loop 0` | Infinite loop | Required for PowerPoint auto-play |

## Size targets

| Resolution | FPS | Colors | Typical Size (10 sec video) |
|-----------|-----|--------|----------------------------|
| 960×522 | 15 | 128 | ~24 MB |
| 800×435 | 10 | 96 | ~11 MB |
| 600×326 | 8 | 64 | ~5 MB |

## Pitfalls

- Animated GIFs over ~20 MB can cause PowerPoint to stutter or crash on lower-end machines
- Target ~10-15 MB for a hero slide GIF
- The GIF plays automatically in PowerPoint slideshow mode when you advance to the slide
- Some older PowerPoint versions require the GIF to be on the slide (not in a shape) for auto-play

## Embedding in PptxGenJS

```javascript
s.addImage({ path: "/tmp/hero.gif", x: 0.8, y: 0.2, w: 8.4, h: 3.8, sizing: { type: "contain", w: 8.4, h: 3.8 } });
```

Use `sizing: { type: "contain" }` to preserve aspect ratio within the bounding box.
