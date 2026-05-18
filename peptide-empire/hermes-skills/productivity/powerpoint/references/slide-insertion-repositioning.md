# Insert Slides at Specific Positions (Not Just Append)

**When to use:** You need to add new slides at specific positions within an existing PPTX, not just at the end. The standard merge technique (`merge-slide-into-existing.md`) only supports appending as the last slide.

**Technique: Park-and-Shift**

Insertion requires shifting existing slides to make room, working from high-to-low to avoid overwrites, and updating three XML files: `presentation.xml`, `presentation.xml.rels`, and `[Content_Types].xml`.

## Step 1: Build and Park

1. Generate new slides as a standalone PPTX (python-pptx or PptxGenJS)
2. Extract the target deck and the new-slides deck into separate directories

## Step 2: Park-and-Shift (Python zipfile approach)

For each insertion position (process highest first to avoid collisions):

```python
import zipfile, os, shutil, re

# Example: insert at positions 8 and 11 in a 21-slide deck
# New slide 1 (from standalone) → position 8
# New slide 2 (from standalone) → position 11

INSERTIONS = [(8, 'slide1.xml'), (11, 'slide2.xml')]  # sorted by position

for pos, src_name in sorted(INSERTIONS, reverse=True):
    # Park: move the new slide to a temp name so shifts don't touch it
    temp = os.path.join(slides_dir, f'slide_TEMP_{pos}.xml')
    shutil.copy2(os.path.join(new_dir, 'ppt', 'slides', src_name), temp)
    
    # Shift: move existing slides from LAST down to pos, by +1
    last = get_current_last_slide()
    for n in range(last, pos - 1, -1):
        shutil.move(f'slide{n}.xml', f'slide{n+1}.xml')
        # Also shift .xml.rels
    
    # Place: move temp to the now-empty position
    shutil.move(temp, f'slide{pos}.xml')
```

## Step 3: Fix Referential Integrity

Three XML files must be updated after any insertion:

### presentation.xml.rels
```python
# Fix shifted slide targets
rels_content = rels_content.replace(
    'Target="slides/slide8.xml"', 'Target="slides/slide9.xml"'
)
# ...for all shifted slides...

# Add new rIds for inserted slides
new_rid = max(existing_rids) + 1
new_rel = f'<Relationship Id="rId{new_rid}" Type="...relationships/slide" Target="slides/slide{pos}.xml"/>'
rels_content = rels_content.replace('</Relationships>', f'  {new_rel}\n</Relationships>')
```

### presentation.xml (sldIdLst)
Rebuild the `<p:sldIdLst>` block with the correct rId order:
```python
ordered_rids = ['rId101', 'rId102', 'rId103',  # slides 1-3
                f'rId{new_rid1}',               # inserted slide
                'rId104', 'rId105', ...]        # shifted slides

new_entries = [f'<p:sldId id="{256+i}" r:id="{rid}"/>' for i, rid in enumerate(ordered_rids)]
```

### [Content_Types].xml
Add entries for inserted slides if not already present:
```python
ct_entry = f'<Override PartName="/ppt/slides/slide{pos}.xml" ContentType="...slide+xml"/>'
```

## Step 4: Repack and Verify

```python
with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
    for root, dirs, files in os.walk(workdir):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, workdir)
            if 'slide_TEMP' not in arcname:  # clean up temp files
                zout.write(full_path, arcname)
```

Always verify by reading all slide titles in order after repacking.

## Pitfalls

- **rId collision**: The `rId{N}` pattern in `presentation.xml.rels` maps to slide filenames. After shifting, rId108 which pointed to `slide8.xml` now points to `slide9.xml` because the file was renamed. You must update the Target attributes, not just the sldIdLst order.
- **Temp file cleanup**: Always park new slides under a name like `slide_TEMP.xml` before shifting. If you shift first and the new slide's target position gets overwritten, you lose the content.
- **Two inserts in one operation**: When inserting multiple slides, process from HIGHEST position to LOWEST. Inserting at position 4 first would shift position 8 to 9, invalidating your second target.
- **Slide number mismatch**: The slide page numbers embedded in the old slides (e.g., "7 / 20") will be wrong after insertion. This is cosmetic — the user fixes it in PowerPoint with Insert → Slide Number → Update.
- **Media references**: The inserted slide's relationship file (`slideN.xml.rels`) references media by relative path (`../media/image-1.png`). These paths work unchanged as long as you also copy the media files from the standalone PPTX to the target deck's media folder.
- **Discord file size limit**: PPTX files over ~8 MB will fail to upload to Discord (HTTP 413). If the deck has large GIFs, compress them before sending — reduce frame count with `gif.seek(0..n_frames:step)` and resize with `frame.resize()`. See the GIF compression pattern below.

## GIF Compression Pattern (for Discord delivery)

```python
from PIL import Image
gif = Image.open('large.gif')
frames = []
for i in range(0, gif.n_frames, 4):  # every 4th frame
    gif.seek(i)
    frame = gif.copy().convert('RGB')
    frame = frame.resize((600, 327), Image.LANCZOS)
    frames.append(frame)
frames[0].save('compressed.gif', save_all=True, append_images=frames[1:],
               optimize=True, duration=80, loop=0)
```

This typically reduces a 10.8 MB 100-frame 800×435 GIF to ~2.6 MB 25-frame 600×327.
