# Repositioning Slides After Merge (Non-Append Insertion)

**When to use:** You've appended slides to the end of the deck but need them at a specific position (e.g., slide 4 instead of slide 21). This technique renames and shifts slide XML files to achieve insertion at any position.

## Technique: Park → Shift → Place

1. **Park** the slide-to-be-moved at a temp filename (`slide_TEMP.xml`)
2. **Shift** existing slides upward to make room (work backwards to avoid collisions)
3. **Place** the parked slide at the target position
4. **Fix** `presentation.xml`, `presentation.xml.rels`, and `[Content_Types].xml`

### ⚠️ CRITICAL PITFALL: Always Park First

If you shift slides BEFORE parking the target slide, the shift will OVERWRITE it. Example of what goes wrong:

```
Starting: slide4=WhyThisMakesSense, slide5=SlowerSaferPlan, ..., slide21=Timeline
Goal: Timeline at position 4

WRONG (overwrite):
  Move slide4→5, slide5→6, ...
  Now slide21 got shifted to slide22, and slide20→21 overwrites the Timeline! ❌

RIGHT (park first):
  Rename slide21.xml → slide_TEMP.xml (park it safely)
  Shift slide4→5, slide5→6, ..., slide20→21 (now position 4 is empty)
  Rename slide_TEMP.xml → slide4.xml (place it) ✅
```

## Full Script: Insert One Slide at Position N

```python
import zipfile, os, shutil, re

existing_path = "deck.pptx"
output_path = "deck_repositioned.pptx"

workdir = "/tmp/pptx_reorder"
shutil.rmtree(workdir, ignore_errors=True)
os.makedirs(workdir, exist_ok=True)

with zipfile.ZipFile(existing_path, 'r') as z:
    z.extractall(workdir)

slides_dir = os.path.join(workdir, 'ppt', 'slides')
rels_dir = os.path.join(slides_dir, '_rels')

INSERT_POS = 4       # where the slide should go
SOURCE_SLIDE = 21     # where it currently is (appended at end)
LAST_ORIGINAL = 20    # highest original slide number (before the appended one)

# Step 1: PARK — move the source slide to a temp name
shutil.move(
    os.path.join(slides_dir, f'slide{SOURCE_SLIDE}.xml'),
    os.path.join(slides_dir, 'slide_TEMP.xml')
)
src_rel = os.path.join(rels_dir, f'slide{SOURCE_SLIDE}.xml.rels')
if os.path.exists(src_rel):
    shutil.move(src_rel, os.path.join(rels_dir, 'slide_TEMP.xml.rels'))

# Step 2: SHIFT — move existing slides up (backwards to avoid overwrites)
for n in range(LAST_ORIGINAL, INSERT_POS - 1, -1):
    src = os.path.join(slides_dir, f'slide{n}.xml')
    dst = os.path.join(slides_dir, f'slide{n+1}.xml')
    if os.path.exists(src):
        shutil.move(src, dst)
    src_rel = os.path.join(rels_dir, f'slide{n}.xml.rels')
    dst_rel = os.path.join(rels_dir, f'slide{n+1}.xml.rels')
    if os.path.exists(src_rel):
        shutil.move(src_rel, dst_rel)

# Step 3: PLACE — move temp to target position
shutil.move(
    os.path.join(slides_dir, 'slide_TEMP.xml'),
    os.path.join(slides_dir, f'slide{INSERT_POS}.xml')
)
temp_rel = os.path.join(rels_dir, 'slide_TEMP.xml.rels')
if os.path.exists(temp_rel):
    shutil.move(temp_rel, os.path.join(rels_dir, f'slide{INSERT_POS}.xml.rels'))

# Step 4: FIX — update presentation.xml.rels (rId → Target mappings)
pres_rels = os.path.join(workdir, 'ppt', '_rels', 'presentation.xml.rels')
with open(pres_rels, 'r') as f:
    rels = f.read()

# The source slide's rId pointed to slide{SOURCE_SLIDE}.xml — update to slide{INSERT_POS}.xml
rels = rels.replace(
    f'Target="slides/slide{SOURCE_SLIDE}.xml"',
    f'Target="slides/slide{INSERT_POS}.xml"'
)
# Shifted slides: rId for old slide N now points to slide N+1
for n in range(LAST_ORIGINAL, INSERT_POS - 1, -1):
    rels = rels.replace(
        f'Target="slides/slide{n}.xml"',
        f'Target="slides/slide{n+1}.xml"'
    )

with open(pres_rels, 'w') as f:
    f.write(rels)

# Step 5: FIX — rebuild presentation.xml sldIdLst in correct order
pres_xml = os.path.join(workdir, 'ppt', 'presentation.xml')
with open(pres_xml, 'r') as f:
    pres = f.read()

# Build ordered rId list:
# rId for slides 1 through INSERT_POS-1 stay same
# rId for source slide goes at INSERT_POS
# rId for INSERT_POS through LAST_ORIGINAL follow

# Determine rId from target names in presentation.xml.rels
rId_by_pos = {}
for m in re.finditer(r'Id="(rId\d+)".*?Target="slides/slide(\d+)\.xml"', rels):
    pos = int(m.group(2))
    rId_by_pos[pos] = m.group(1)

ordered = []
for p in range(1, LAST_ORIGINAL + 2):  # +2 because we added one slide
    if p in rId_by_pos:
        ordered.append(rId_by_pos[p])

new_entries = '\n  '.join(
    f'<p:sldId id="{256+i}" r:id="{rid}"/>' for i, rid in enumerate(ordered)
)

old = re.search(r'<p:sldIdLst>(.*?)</p:sldIdLst>', pres, re.DOTALL)
if old:
    pres = pres[:old.start()] + f'<p:sldIdLst>\n  {new_entries}\n</p:sldIdLst>' + pres[old.end():]

with open(pres_xml, 'w') as f:
    f.write(pres)

# Step 6: REPACK
with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
    for root, dirs, files in os.walk(workdir):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, workdir)
            if 'slide_TEMP' in arcname:
                continue  # skip temp files
            zout.write(full_path, arcname)
```

## Multi-Slide Insertion

When inserting multiple new slides at different positions, work from HIGHEST position to LOWEST to avoid cascading shifts:

```
Goal: Insert slides at positions 8 and 11
1. Shift existing slides 11+ up by 1 (now positions 12+)
2. Place slide at position 11
3. Shift existing slides 8+ up by 1 (now positions 9+)
4. Place slide at position 8
```

## Verification

After repositioning, verify ALL slides are in order with correct content:

```python
with zipfile.ZipFile(output_path, 'r') as z:
    for n in range(1, 999):
        fname = f'ppt/slides/slide{n}.xml'
        if fname not in z.namelist():
            break
        content = z.read(fname).decode('utf-8', errors='ignore')
        titles = re.findall(r'<a:t[^>]*>([^<]{15,80})</a:t>', content)
        title = titles[0][:55] if titles else "(no title)"
        print(f"  {n:2d}. {title}")
```

## Post-Repositioning Cleanup

- Slide page numbers embedded in the slides still show the old count (e.g., "7 / 20"). The user must update in PowerPoint: Insert → Slide Number → Update.
- rId assignment uses the existing rId from the source slide — no new rIds are created for repositioning alone.
