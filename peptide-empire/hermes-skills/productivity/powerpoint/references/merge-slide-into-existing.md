# Merge a New Slide Into an Existing PPTX (Preserving Manual Edits)

**When to use:** The user has manually edited slides in PowerPoint (repositioned photos, tweaked spacing, adjusted layouts). You need to add a new slide WITHOUT losing those edits. A full JS rebuild will revert manual changes. The unpack/edit/pack workflow is fragile for PptxGenJS-generated XML.

**Technique:** Generate ONLY the new slide(s) as a standalone PptxGenJS PPTX, then use Python zipfile operations to splice them into the existing file.

## Step 1: Generate standalone slide(s)

**Preferred: PptxGenJS** (matches deck aesthetic, supports same color/theme system)

```javascript
const pptxgen = require("pptxgenjs");
// ... define colors, helpers ...
// Build new slide(s) only
await pres.writeFile({ fileName: "/tmp/new_slide_only.pptx" });
```

Run: `cd /tmp && NODE_PATH=/tmp/node_modules node new_slide.js`

**Fallback: python-pptx** (when node/PptxGenJS unavailable)

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor

prs = Presentation()
prs.slide_width = Emu(12192000)
prs.slide_height = Emu(6858000)
# Build slide(s) manually
prs.save("/tmp/new_slide_only.pptx")
```

Install if needed: `python3 -m pip install python-pptx`

## Step 2: Merge into existing PPTX

```python
import zipfile, os, shutil, re

existing_path = "user_edited.pptx"
new_slide_path = "/tmp/new_slide_only.pptx"
output_path = "output_with_new_slide.pptx"

workdir = "/tmp/pptx_merge"
shutil.rmtree(workdir, ignore_errors=True)
os.makedirs(workdir, exist_ok=True)

with zipfile.ZipFile(existing_path, 'r') as z:
    z.extractall(os.path.join(workdir, 'existing'))
with zipfile.ZipFile(new_slide_path, 'r') as z:
    z.extractall(os.path.join(workdir, 'new'))

existing_dir = os.path.join(workdir, 'existing')
new_dir = os.path.join(workdir, 'new')
slides_dir = os.path.join(existing_dir, 'ppt', 'slides')

# Find next slide number
import re
existing = sorted([f for f in os.listdir(slides_dir) if f.startswith('slide') and f.endswith('.xml')])
last_num = max([int(re.search(r'slide(\d+)', f).group(1)) for f in existing])
new_num = last_num + 1

# Copy slide XML
shutil.copy2(
    os.path.join(new_dir, 'ppt', 'slides', 'slide1.xml'),
    os.path.join(slides_dir, f'slide{new_num}.xml')
)

# Copy slide relationships
dst_rels = os.path.join(existing_dir, 'ppt', 'slides', '_rels')
os.makedirs(dst_rels, exist_ok=True)
src_rels = os.path.join(new_dir, 'ppt', 'slides', '_rels', 'slide1.xml.rels')
shutil.copy2(src_rels, os.path.join(dst_rels, f'slide{new_num}.xml.rels'))

# Copy any new layouts/masters (only if not already present)
for folder in ['slideLayouts', 'slideMasters']:
    src = os.path.join(new_dir, 'ppt', folder)
    dst = os.path.join(existing_dir, 'ppt', folder)
    if os.path.exists(src):
        for f in os.listdir(src):
            sf = os.path.join(src, f)
            df = os.path.join(dst, f)
            if not os.path.exists(df) and os.path.isfile(sf):
                shutil.copy2(sf, df)
    # Copy _rels for this folder
    src_r = os.path.join(src, '_rels')
    dst_r = os.path.join(dst, '_rels')
    if os.path.exists(src_r):
        os.makedirs(dst_r, exist_ok=True)
        for f in os.listdir(src_r):
            sf = os.path.join(src_r, f)
            df = os.path.join(dst_r, f)
            if not os.path.exists(df):
                shutil.copy2(sf, df)

# Update presentation.xml — add new slide to <p:sldIdLst>
pres_xml = os.path.join(existing_dir, 'ppt', 'presentation.xml')
with open(pres_xml, 'r') as f:
    content = f.read()
slide_id = f'<p:sldId id="{250 + new_num}" r:id="rId{100 + new_num}"/>'
content = content.replace('</p:sldIdLst>', f'  {slide_id}\n  </p:sldIdLst>')
with open(pres_xml, 'w') as f:
    f.write(content)

# Update presentation.xml.rels
pres_rels = os.path.join(existing_dir, 'ppt', '_rels', 'presentation.xml.rels')
with open(pres_rels, 'r') as f:
    content = f.read()
rel = f'<Relationship Id="rId{100 + new_num}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{new_num}.xml"/>'
content = content.replace('</Relationships>', f'  {rel}\n</Relationships>')
with open(pres_rels, 'w') as f:
    f.write(content)

# Update [Content_Types].xml
ct_path = os.path.join(existing_dir, '[Content_Types].xml')
with open(ct_path, 'r') as f:
    content = f.read()
ct_entry = f'<Override PartName="/ppt/slides/slide{new_num}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
if ct_entry not in content:
    content = content.replace('</Types>', f'  {ct_entry}\n</Types>')
    with open(ct_path, 'w') as f:
        f.write(content)

# Repack
with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
    for root, dirs, files in os.walk(existing_dir):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, existing_dir)
            zout.write(full_path, arcname)
```

## Pitfalls

- **ID collisions:** Python's `zipfile` doesn't verify rId uniqueness. If you merge multiple slides in separate runs, the `rId{100 + new_num}` pattern may collide. Always use `os.path.exists()` checks or remove old slide entries before adding new ones.
- **Layout/masters mismatch:** If the new slide uses a different master or layout than any existing slide, you MUST copy those from the standalone PPTX. The script above handles this, but verify.
- **Slide numbering:** The new slide will inherit its own `addSlideNum()` value from the standalone generation. Make sure it's correct for its position in the deck — update the standalone JS before generating the slide.
- **File size:** Each merge may leave orphaned references or slightly bloat the file. For production delivery, do a Save As in PowerPoint to compact.

## Repositioning After Merge

This technique appends to the end. If the slide needs to go at a specific position (e.g., insert at slide 4 instead of slide 21), use **[slide-repositioning.md](slide-repositioning.md)** after merging.
