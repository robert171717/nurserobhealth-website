# Programmatic Slide Merging (PptxGenJS + Zipfile)

## When to use

When you need to update slides in an existing .pptx but the user has made manual edits (photo placement, spacing tweaks) that would be lost by regenerating the entire deck from JavaScript. Or when you need to add a brand-new slide to an existing deck without touching the other slides.

## The Core Technique

Generate the new/updated slide as a **standalone single-slide PPTX** using PptxGenJS, then merge it into the existing deck using Python's `zipfile`.

## Step-by-Step

### 1. Build the new slide standalone

Write a minimal JS file that generates a single slide:

```javascript
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
const s = pres.addSlide();
// ... build your slide ...
await pres.writeFile({ fileName: "/tmp/new_slide.pptx" });
```

### 2. Merge into existing PPTX

```python
import zipfile, os, shutil, re

def merge_slide(src_pptx, new_slide_pptx, output_path, slide_num=None):
    """Merge a standalone single-slide PPTX into an existing PPTX."""
    workdir = "/tmp/pptx_merge"
    shutil.rmtree(workdir, ignore_errors=True)
    os.makedirs(workdir, exist_ok=True)
    
    with zipfile.ZipFile(src_pptx, 'r') as z:
        z.extractall(os.path.join(workdir, 'main'))
    with zipfile.ZipFile(new_slide_pptx, 'r') as z:
        z.extractall(os.path.join(workdir, 'new'))
    
    main_dir = os.path.join(workdir, 'main')
    new_dir = os.path.join(workdir, 'new')
    slides_dir = os.path.join(main_dir, 'ppt', 'slides')
    
    # Auto-detect next slide number if not specified
    if slide_num is None:
        existing = sorted([f for f in os.listdir(slides_dir) 
                          if f.startswith('slide') and f.endswith('.xml')])
        slide_num = max([int(re.search(r'slide(\d+)', f).group(1)) 
                         for f in existing]) + 1
    
    # Copy slide XML and relationships
    shutil.copy2(os.path.join(new_dir, 'ppt/slides/slide1.xml'),
                 os.path.join(slides_dir, f'slide{slide_num}.xml'))
    
    rels_src = os.path.join(new_dir, 'ppt/slides/_rels/slide1.xml.rels')
    rels_dst = os.path.join(slides_dir, '_rels', f'slide{slide_num}.xml.rels')
    os.makedirs(os.path.join(slides_dir, '_rels'), exist_ok=True)
    if os.path.exists(rels_src):
        shutil.copy2(rels_src, rels_dst)
    
    # Update presentation.xml to include new slide
    pres_xml_path = os.path.join(main_dir, 'ppt/presentation.xml')
    with open(pres_xml_path, 'r') as f:
        pres_xml = f.read()
    new_slide_entry = f'<p:sldId id="{250+slide_num}" r:id="rId{100+slide_num}"/>'
    pres_xml = re.sub(rf'<p:sldId id="\d+" r:id="rId{100+slide_num}"/>', '', pres_xml)
    pres_xml = pres_xml.replace('</p:sldIdLst>', f'  {new_slide_entry}\n  </p:sldIdLst>')
    with open(pres_xml_path, 'w') as f:
        f.write(pres_xml)
    
    # Update presentation relationships
    pres_rels_path = os.path.join(main_dir, 'ppt/_rels/presentation.xml.rels')
    with open(pres_rels_path, 'r') as f:
        pres_rels = f.read()
    new_rel = f'<Relationship Id="rId{100+slide_num}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{slide_num}.xml"/>'
    if f'rId{100+slide_num}' not in pres_rels:
        pres_rels = pres_rels.replace('</Relationships>', f'  {new_rel}\n</Relationships>')
        with open(pres_rels_path, 'w') as f:
            f.write(pres_rels)
    
    # Update Content_Types.xml
    ct_path = os.path.join(main_dir, '[Content_Types].xml')
    with open(ct_path, 'r') as f:
        ct_xml = f.read()
    new_ct = f'<Override PartName="/ppt/slides/slide{slide_num}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
    if f'slide{slide_num}.xml' not in ct_xml:
        ct_xml = ct_xml.replace('</Types>', f'  {new_ct}\n</Types>')
        with open(ct_path, 'w') as f:
            f.write(ct_xml)
    
    # Repack
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for root, dirs, files in os.walk(main_dir):
            for file in files:
                fp = os.path.join(root, file)
                zout.write(fp, os.path.relpath(fp, main_dir))
```

## Pitfalls

- **Slide relationships and Content_Types MUST be updated.** Missing either causes PowerPoint to reject the file as corrupt.
- **Existing slide numbers are preserved.** The standalone slide is always `slide1.xml` in its source PPTX — rename to the target number.
- **Rerunning the merge is idempotent** if you clean up the old entry first (the regex removal of old `rId` handles this).
- **This only works for PptxGenJS-generated slides** — the new slide uses the same slide layout/master as the existing deck. Mixing generator sources (python-pptx + PptxGenJS) can cause layout conflicts.
- **Fonts not embedded.** PowerPoint falls back to system fonts if the viewer doesn't have them.

## When NOT to use

- When all slides need changes (regenerate full deck from JS instead)
- When the existing deck has complex slide transitions or animations (merge may break them)
- When the new slide needs video embedding (PptxGenJS doesn't support MP4 — use GIF conversion via ffmpeg first)
