# OG Card Brightness — Battle-Tested Parameters

Lessons from multiple OG card generations for nurserobhealth.com:

## Background Colors That FAIL (>80% dark pixels, even with enhancers)
| Color | RGB | Avg Brightness | Dark Pixel % |
|-------|-----|---------------|--------------|
| Navy #080E1A | (8, 14, 26) | 16/255 | 99.4% |
| Deep navy #141E32 | (20, 30, 50) | 33/255 | 97.2% |
| Slate navy #19283C | (25, 40, 60) | 42/255 | 96.3% |

Even with ImageEnhance 1.4x, these stay above 94% dark pixels.

## Background Colors That PASS
| Color | RGB | Dark Pixel % |
|-------|-----|-------------|
| Medium blue-gray #2A3F5F | (42, 63, 95) | ~65-70% |
| Steel blue #3A5070 | (58, 80, 112) | ~45-55% |
| Light slate #4A6080 | (74, 96, 128) | ~25-35% |

## Enhancement Stack That Works
For backgrounds in the #2A3F5F range, this enhancement chain brings dark pixels below 80%:
```python
from PIL import ImageEnhance
enhancer = ImageEnhance.Brightness(img)
img = enhancer.enhance(1.4)      # +40% brightness
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(1.1)      # +10% contrast
```

## Design Elements That Add Brightness
- Gold accent lines (RGB 230,190,90) — bright, professional
- Teal pill-shaped feature badges with white text
- White title text (centered, large font 64pt)
- Teal subtitle text against the dark background
- Keep text areas covering at least 15-20% of the image area

## Quick Validation Script
```python
from PIL import Image
img = Image.open('og-image.jpg')
pixels = list(img.getdata())
brightness = [(r+g+b)//3 for (r,g,b) in pixels]
dark_pct = 100 * sum(1 for b in brightness if b < 50) / len(brightness)
avg = sum(brightness) / len(brightness)
print(f"Dark: {dark_pct:.1f}% | Avg brightness: {avg:.0f}/255")
print("PASS" if dark_pct < 80 else "FAIL - too dark for X")
```
