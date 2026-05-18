# Patch Tool + PptxGenJS Quoting Pitfall

## Symptom

After using the patch tool to modify a PptxGenJS `.js` source file, running the script produces:
```
SyntaxError: Invalid or unexpected token
```
Inspection of the source reveals backslash-escaped quotes like `\\\"` inside string literals.

## Root Cause

The patch tool sometimes backslash-escapes double-quote characters when inserting or replacing strings in JavaScript files. A string that should read:
```javascript
s.addImage({ path: "/tmp/photo.jpg", x: 2.5, ... });
```
becomes:
```javascript
s.addImage({ path: \\\"/tmp/photo.jpg\\\", x: 2.5, ... });
```

## Fix

1. Read the affected line immediately after patching (`read_file` with offset/limit)
2. If you see `\\\"` where regular quotes should be, re-apply the patch with the exact unescaped string
3. If the issue persists, use Python `execute_code` for bulk string replacements instead of the patch tool
4. Always re-run `node script.js` after patching to catch syntax errors early

## Prevention

- Prefer Python `write_file` + `execute_code` for multi-line changes to JS files
- Reserve patch tool for single-line replacements without special characters
- After any patch to a JS file, run a syntax check: `node --check /tmp/script.js`
