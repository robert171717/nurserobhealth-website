# PptxGenJS Patterns Learned

## Financial Presentation Deck with Dark Theme

When building decks for financial/investment presentations:

### Color Palette
- Dark background: `111111` (near-black) or `1A1A1A`
- Gold accent: `F4C542` (works well for highlights, section bars)
- Teal data: `0A9396` (for financial callouts, metrics)
- Red danger: `E63946` (for warnings, stop rules)
- Gray cards: `2A2A2A` or `3A3A3A` (for content cards on dark bg)
- Light text: `CCCCCC` on dark backgrounds
- Muted text: `888888` for secondary info

### Typography
- Headers: `Arial Black` (bold, modern)
- Body: `Calibri` (clean, readable)
- Section bars: thin (0.04" height) gold accent line at top of each slide

### Shadow Helper
Always use a factory function for shadows to avoid object mutation bugs:
```javascript
const shadow = () => ({ type: "outer", blur: 4, offset: 1, angle: 135, color: "000000", opacity: 0.3 });
```

### Slide Numbering
Use a helper function:
```javascript
function addSlideNum(slide, num) {
  slide.addText(`${num} / ${totalSlides}`, {
    x: 8.8, y: 5.2, w: 1, h: 0.3, fontSize: 9, color: "888888",
    fontFace: "Calibri", align: "right"
  });
}
```

## Animated GIF from MP4

Convert MP4 video to animated GIF for PowerPoint embedding:
```bash
ffmpeg -i input.mp4 \
  -vf "fps=10,scale=800:435:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=96[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5" \
  -loop 0 output.gif
```

Key params:
- `fps=10`: Good balance of smoothness and file size for presentations
- `scale=800:WIDTH`: Scale to presentation-appropriate size
- `max_colors=96`: Reduces file size (~60% smaller than 256 colors)
- `-loop 0`: Infinite loop for PowerPoint auto-play

PptxGenJS embeds animated GIFs natively via `addImage({ path: "file.gif", ... })`. PowerPoint plays them automatically.

## Image Sizing
Use `sizing: { type: "contain" }` to fit images within bounds while preserving aspect ratio:
```javascript
slide.addImage({ 
  path: "image.jpg", 
  x: 1, y: 1, w: 8, h: 4,
  sizing: { type: "contain", w: 8, h: 4 }
});
```

## Slide Insertion & Renumbering

When inserting a new slide in a PptxGenJS script:
1. Add the slide code block at the insertion point
2. Shift all `addSlideNum(s, N)` calls from the insertion point forward by +1
3. Update `totalSlides` in the `addSlideNum` helper
4. Work backwards (highest number to lowest) when applying shifts to avoid conflicts
5. The title slide typically has no `addSlideNum` call

## Modifying Existing PptxGenJS PPTX

When a PptxGenJS-generated PPTX needs edits:
- **Avoid XML surgery** for coordinate changes — too many interdependent elements
- **Rebuild from the JS** with corrected coordinates instead
- For simple text-only changes, ZipFile-level XML edits can work (find/replace within `<a:t>` tags)
- For image/photo additions by the user: extract the photo from the existing PPTX, include it in the rebuild

## LINE Shapes
Horizontal separator lines work with `h: 0`:
```javascript
slide.addShape(pres.shapes.LINE, { 
  x: 3.5, y: 2.65, w: 0.4, h: 0, 
  line: { color: "F4C542", width: 2 } 
});
```

## Icon Generation
Icons via react-icons + sharp produce clean PNGs at any size:
```javascript
const { FaCar, FaCheckCircle } = require("react-icons/fa");
const iconData = await iconToBase64(FaCheckCircle, "#0A9396", 256);
slide.addImage({ data: iconData, x: 1, y: 1, w: 0.5, h: 0.5 });
```
Use size 256 for crisp rendering. The display size is controlled by `w` and `h` in inches.
