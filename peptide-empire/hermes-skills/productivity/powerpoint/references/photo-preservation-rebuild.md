# Photo Preservation During PptxGenJS Rebuild

## Problem

User edits a PptxGenJS-generated PPTX in PowerPoint (e.g., adds a family photo to slide 1, tweaks text positioning). You need to rebuild the deck from JavaScript (to fix overlapping elements or add slides), but must preserve the user's photo.

## Solution: Extract → Rebuild → Embed

### Step 1: Extract the photo from the existing PPTX

```python
import zipfile

with zipfile.ZipFile("existing.pptx", 'r') as z:
    # Check slide 1 relationships to find the image
    rels = z.read('ppt/slides/_rels/slide1.xml.rels').decode('utf-8')
    # Find rId for the user-added image (usually the largest JPEG)
    
    # List media files by size
    media = [(n, z.getinfo(n).file_size) for n in z.namelist() if 'media' in n]
    media.sort(key=lambda x: -x[1])
    
    # The largest file is likely the user's photo
    largest = media[0][0]
    data = z.read(largest)
    
with open('/tmp/family_photo.jpg', 'wb') as f:
    f.write(data)
```

### Step 2: Embed in the PptxGenJS rebuild

Use the `path` option (not base64 — too large for JS source):

```javascript
// Slide 1 - title with family photo
s.addImage({ 
    path: "/tmp/family_photo.jpg",
    x: 2.5, y: 0.5, 
    w: 5.0, h: 1.3, 
    sizing: { type: "contain", w: 5.0, h: 1.3 }
});
```

### Step 3: Regenerate

```bash
cd /tmp && NODE_PATH=/tmp/node_modules node deck.js
```

## Notes

- **Don't use base64** for photos > 100KB — the JS file becomes unmanageable
- **Use `sizing: { type: "contain" }`** to preserve aspect ratio while fitting the allocated space
- The user may need to adjust photo position in PowerPoint after rebuild — tell them
- If the photo was placed in a complex layout, use the XML position extraction approach from overlap-fix-pptxgenjs.md to find the exact x/y/w/h
- Supporting file formats: JPEG, PNG, GIF (including animated)
