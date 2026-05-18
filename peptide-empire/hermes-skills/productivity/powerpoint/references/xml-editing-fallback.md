# Text-Only XML Editing Fallback for PptxGenJS PPTX Files

## When to use

When you need to change only TEXT content in an existing PptxGenJS-generated PPTX, and the user has already edited the file in PowerPoint (added photos, tweaked positions). XML surgery for coordinates is fragile, but text-only replacements inside `<a:t>` tags are safe.

## Preconditions

- You only need to change text strings, NOT positions/sizes/coordinates
- The text to replace exists as exact strings inside `<a:t>...</a:t>` tags
- You have Python's `zipfile` and `re` available (no pip needed)

## Procedure

### 1. Extract the slide XML

```python
import zipfile, re, os, shutil

src = "presentation.pptx"
dst = "/tmp/edited.pptx"
shutil.copy2(src, dst)
tmpdir = "/tmp/pptx_edit"

with zipfile.ZipFile(dst, 'r') as z:
    z.extractall(tmpdir)

slide_path = os.path.join(tmpdir, 'ppt', 'slides', 'slide5.xml')
with open(slide_path, 'r', encoding='utf-8') as f:
    content = f.read()
```

### 2. Define exact text replacements

Use the EXACT text as it appears in the `<a:t>` tags. Watch for XML entities:
- `&amp;` = `&`
- `&apos;` = `'`
- `&#x201C;` / `&#x201D;` = smart quotes

```python
replacements = [
    ('old text exactly as found', 'new replacement text'),
    ("Covers ~1 vehicle&apos;s charging needs", "Powers 100% of our house load"),
]
```

### 3. Apply and repack

```python
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"  ✓ Replaced: '{old[:40]}...'")
    else:
        print(f"  ✗ NOT FOUND: '{old[:40]}...'")

with open(slide_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Repack
with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zout:
    for root, dirs, files in os.walk(tmpdir):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, tmpdir)
            zout.write(full_path, arcname)
```

### 4. Verify

```python
with zipfile.ZipFile(dst, 'r') as z:
    content = z.read('ppt/slides/slide5.xml').decode('utf-8')
    texts = re.findall(r'<a:t[^>]*>(.*?)</a:t>', content, re.DOTALL)
    for t in texts:
        clean = re.sub(r'<[^>]+>', '', t).strip()
        if clean:
            print(f"  {clean}")
```

## Limitations

- **Cannot fix overlapping elements** — coordinates need JS rebuild (see overlap-fix-pptxgenjs.md)
- **Cannot add/remove slides** — use JS rebuild
- **Can only change existing text** — not add new text boxes
- XML entities like `&apos;` must be preserved in the search string

## When NOT to use

- If changes involve positions, sizes, or adding/removing elements → rebuild from PptxGenJS
- If the user hasn't edited the file → rebuild from JS (cleaner)
- If unpack.py is available → use the proper editing workflow with `python scripts/office/unpack.py`, edit, `python scripts/clean.py`, `python scripts/office/pack.py`
