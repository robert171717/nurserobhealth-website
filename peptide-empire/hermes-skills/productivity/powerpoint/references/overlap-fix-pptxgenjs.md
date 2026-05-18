# Overlap Fix Pattern for PptxGenJS-Generated Slides

## Problem

Slides with two or more content-dense sections (especially with rows/items using fixed spacing) frequently overlap when there isn't enough vertical room. The 16:9 slide is only 5.625" tall. Title + subtitle consume ~1.2". That leaves ~4.4" for content. Two sections with headers + rows easily exceed this.

## Detection

Extract element positions from the XML using the regex pattern:

```python
xfrms = list(re.finditer(
    r'<a:xfrm[^>]*>\s*<a:off x="(\d+)" y="(\d+)"/>\s*<a:ext cx="(\d+)" cy="(\d+)"/>',
    content
))
```

Convert EMU to inches (÷ 914400). Compare `y + h` (bottom) of one section's last row against the `y` of the next section's header. If `bottom > next_y`, you have overlap.

## Fix (PptxGenJS Source Edit)

Do NOT attempt XML surgery for coordinate changes — the number of interdependent xfrm elements is too high. Instead:

1. Reduce row heights (`h`) by 0.06–0.10"
2. Reduce row spacing (the increment value) by 0.06–0.09"
3. Shift the second section's start `y` down to create a gap
4. Regenerate the entire deck from the modified JS

### Example: Two-section slide with 5 + 4 rows (this session)

**Before (overlapping):**
```javascript
// Red triggers: h=0.38, spacing=0.44 → last bottom = 1.75 + 4×0.44 + 0.38 = 3.89
let ry2 = 1.75;
for (const r of reds) {
  s.addShape(pres.shapes.RECTANGLE, { x: 0.7, y: ry2, w: 5.0, h: 0.38, ... });
  ry2 += 0.44;
}
// "NEW ADDITIONS" header at y=3.65 ← OVERLAPS (3.89 > 3.65)
s.addText("🟡 NEW ADDITIONS", { ... y: 3.65 ... });
// New rows: h=0.32, spacing=0.36, start=4.05 → last bottom = 5.45 (only 0.175" margin!)
```

**After (fixed):**
```javascript
// Red triggers: h=0.32, spacing=0.35 → last bottom = 1.75 + 4×0.35 + 0.32 = 3.47
let ry2 = 1.75;
for (const r of reds) {
  s.addShape(pres.shapes.RECTANGLE, { x: 0.7, y: ry2, w: 5.0, h: 0.32, ... });
  ry2 += 0.35;
}
// Header at y=3.60 ← gap of 0.13" ✓
s.addText("🟡 NEW ADDITIONS", { ... y: 3.60 ... });
// New rows: h=0.30, spacing=0.33, start=3.95 → last bottom = 5.24 (0.385" margin) ✓
```

## Verification

After fixing, verify the gap with:
```python
import re
# Extract bottom of last row in section A
# Extract top of first element in section B
# Assert: section_b_top - section_a_bottom > 0
```
