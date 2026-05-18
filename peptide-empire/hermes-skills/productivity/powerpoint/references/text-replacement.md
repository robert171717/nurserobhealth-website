# Lightweight Text Replacement in PptxGenJS-Generated Slides

## When to use

When you need to change only **text content** (not positions, sizes, or colors) in a PptxGenJS-generated .pptx, and regenerating from JavaScript would lose manual edits the user already made in PowerPoint.

This is faster and safer than the full `unpack → edit XML → clean → pack` workflow for text-only changes.

## How it works

PptxGenJS stores text inside `<a:t>` elements in the slide XML. You can open the .pptx as a zipfile, find and replace text strings inside those tags, and repack.

## Step-by-step

```python
import zipfile, re, os, shutil

def replace_text_in_slide(pptx_path, slide_num, replacements):
    """
    Replace text strings in a specific slide of a PptxGenJS-generated .pptx.
    
    replacements: dict of {old_text: new_text} — exact strings as they appear
                  inside <a:t> tags in the XML.
    """
    tmpdir = "/tmp/pptx_text_replace"
    shutil.rmtree(tmpdir, ignore_errors=True)
    os.makedirs(tmpdir, exist_ok=True)
    
    # Extract
    with zipfile.ZipFile(pptx_path, 'r') as z:
        z.extractall(tmpdir)
    
    # Modify slide XML
    slide_path = os.path.join(tmpdir, f'ppt/slides/slide{slide_num}.xml')
    with open(slide_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
        else:
            # Try with XML-escaped variants
            escaped = old.replace("'", "&apos;").replace('"', '&quot;').replace('&', '&amp;')
            if escaped in content:
                content = content.replace(escaped, new)
    
    with open(slide_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Repack
    with zipfile.ZipFile(pptx_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for root, dirs, files in os.walk(tmpdir):
            for file in files:
                fp = os.path.join(root, file)
                zout.write(fp, os.path.relpath(fp, tmpdir))
```

## Finding the exact text to replace

Use this to extract all text from a slide:

```python
with zipfile.ZipFile(pptx_path, 'r') as z:
    xml = z.read(f'ppt/slides/slide{slide_num}.xml').decode('utf-8')
texts = re.findall(r'<a:t[^>]*>(.*?)</a:t>', xml, re.DOTALL)
for t in texts:
    clean = re.sub(r'<[^>]+>', '', t).strip()
    if clean:
        print(clean)
```

## Common XML entities to handle

| Character | XML Entity |
|-----------|-----------|
| `'` (apostrophe) | `&apos;` |
| `"` (quote) | `&quot;` |
| `&` (ampersand) | `&amp;` |
| `–` (en dash) | `&#x2013;` |
| `—` (em dash) | `&#x2014;` |

## Pitfalls

- **Only works for text inside `<a:t>` tags.** Shapes, images, and positioning are untouched.
- **Exact match required.** "Covers ~1 vehicle's charging needs" won't match "Covers ~1 vehicle&apos;s charging needs" — try the XML-escaped variant.
- **String must be unique within the slide.** If "vehicle #5" appears in both a title and a body, both get replaced. Use more context in the search string if needed.
- **No Content_Types or relationship changes needed** — those are only required when adding/removing slides, not editing existing ones.

## When NOT to use

- When changing positions, sizes, or adding new elements (use slide-merging or full regeneration)
- When the change affects multiple slides that all need coordination (regenerate from JS)
- When the existing PPTX uses embedded media with complex relationships
