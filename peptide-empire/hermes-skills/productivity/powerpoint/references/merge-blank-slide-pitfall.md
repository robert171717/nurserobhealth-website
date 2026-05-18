# Why Merged PptxGenJS Slides Appear Blank

## The Problem

When you generate a standalone slide with PptxGenJS (e.g., a summary slide in its own PPTX) and then zip-merge it into an existing deck, the merged slide appears **completely blank** in PowerPoint. All text and shapes are invisible — even though the XML looks structurally correct.

## Root Cause

Each PptxGenJS generation creates its own set of **slide layouts** (`slideLayout1.xml`, `slideLayout2.xml`, etc.) and **slide masters** (`slideMaster1.xml`) with unique relationship IDs. These IDs are embedded in every slide's XML via `<p:sldLayout>` and inherited through the slide's `_rels/slideN.xml.rels` file.

When you merge a standalone slide into a different deck, its layout references point to IDs (like `rId2` → `slideLayout2.xml`) that don't exist in the target deck. PowerPoint can't resolve the layout, so the slide renders as blank.

## The Lesson

**NEVER zip-merge standalone PptxGenJS slides into a different PptxGenJS-generated deck.**

The only reliable approach is to generate ALL slides from the same `pres` object:

```javascript
// ✅ CORRECT: All slides from one pres object
const pres = new pptxgen();
pres.addSlide(); // slide 1
pres.addSlide(); // slide 2 
pres.addSlide(); // slide 3 — all share same layouts, always works
```

## When This Happened

During the Cybercab deck build, slides 19 (Executive Summary) and 20 (Contingency Planning) were generated as standalone PPTXs and merged into the main deck. They appeared blank. The fix was to embed both slides directly in the main JavaScript using the same `pres` object.

## Detection

A quick way to verify after a merge: extract the PPTX and grep for content in the merged slide:

```python
import zipfile, re
with zipfile.ZipFile('deck.pptx', 'r') as z:
    s = z.read('ppt/slides/slide19.xml').decode('utf-8')
    if 'EXECUTIVE' not in s:
        print('❌ Slide is blank — layout IDs do not match')
```

## Workaround (If You Must Merge)

If you absolutely must merge standalone slides, you need to:
1. Copy all slide layouts and masters from the standalone PPTX into the main deck
2. Re-map all relationship IDs in the merged slide's XML
3. Update Content_Types.xml for all new layout/master entries

This is extremely fragile and not recommended. Always prefer generating all slides from one `pres` object.
