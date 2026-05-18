# Merging Slides into Existing PPTX Without Losing Manual Edits

## When to use

When a user has manually tweaked slides in PowerPoint (photo sizing, spacing adjustments) and you need to add/update slides without blowing away their edits.

## The Problem

Regenerating from PptxGenJS JavaScript always produces a fresh PPTX. Any manual edits the user made in PowerPoint are lost. The unpack/edit/pack XML surgery approach is fragile with PptxGenJS output (deeply nested absolute-positioned elements).

## Solution: Generate standalone slide + zipfile merge

### Step 1: Generate a single-slide PPTX with PptxGenJS

Write a minimal JS that produces exactly one slide. Use the same color palette, fonts, and shadow helper as the main deck so the new slide matches.

```javascript
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";

const s = pres.addSlide();
// ... design the single slide ...

await pres.writeFile({ fileName: "/tmp/new_slide.pptx" });
```

### Step 2: Merge into the existing PPTX using Python zipfile

```python
import zipfile, os, shutil, re

# Extract both PPTXs
with zipfile.ZipFile(existing_pptx, 'r') as z:
    z.extractall(workdir + '/main')
with zipfile.ZipFile(new_slide_pptx, 'r') as z:
    z.extractall(workdir + '/new')

# Find highest existing slide number
slides_dir = workdir + '/main/ppt/slides'
existing_slides = [f for f in os.listdir(slides_dir) if f.startswith('slide') and f.endswith('.xml')]
last_num = max([int(re.search(r'slide(\d+)', f).group(1)) for f in existing_slides])
new_num = last_num + 1

# Copy the new slide XML and its relationships
shutil.copy2(
    workdir + '/new/ppt/slides/slide1.xml',
    slides_dir + f'/slide{new_num}.xml'
)
shutil.copy2(
    workdir + '/new/ppt/slides/_rels/slide1.xml.rels',
    slides_dir + f'/_rels/slide{new_num}.xml.rels'
)

# Update presentation.xml (slide list)
pres_xml = pres_xml.replace('</p:sldIdLst>',
    f'  <p:sldId id="{250+new_num}" r:id="rId{100+new_num}"/>\n  </p:sldIdLst>')

# Update presentation.xml.rels
pres_rels = pres_rels.replace('</Relationships>',
    f'  <Relationship Id="rId{100+new_num}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{new_num}.xml"/>\n</Relationships>')

# Update [Content_Types].xml
ct_xml = ct_xml.replace('</Types>',
    f'  <Override PartName="/ppt/slides/slide{new_num}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>\n</Types>')

# Repack
with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
    for root, dirs, files in os.walk(workdir + '/main'):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, workdir + '/main')
            zout.write(full_path, arcname)
```

## Pitfalls

- The slide's page number inside the new slide (e.g., "19 / 19") must be set correctly in the JS — it will read whatever number you hardcoded
- If the standalone slide references any media (images, GIFs), those files must already exist in the main PPTX. Better to use only text/shapes/colors in standalone slides
- The `r:id` in presentation.xml.rels must be unique. Use `100 + new_num` to avoid collisions
- `[Content_Types].xml` needs an Override entry for the new slide
- After merging, open the file in PowerPoint to verify — zipfile repacking can occasionally produce files that need a "Repair" on open

## Alternative: Rebuild with embedded photo

If the user added a photo to slide 1, you CAN rebuild the whole deck if:
1. You extract the photo from the existing PPTX (find in `ppt/media/`)
2. Reference it by file path in the JS: `s.addImage({ path: "/tmp/extracted_photo.jpg", ... })`
3. You know the exact position/size they used

The merge approach is safer when you don't know photo positions.
