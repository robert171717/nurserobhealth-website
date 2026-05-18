---
name: obsidian-templater-button-migration
description: Migrate from Templater inline-style buttons to CSS class-based button syntax in Obsidian vaults
version: 1.0
author: NurseRobHealth
tags: [obsidian, templater, buttons, css, vault-migration]
---

# Obsidian Templater Button Migration
## Migrate from Inline-Style Buttons to CSS Class-Based Syntax

> **Convert Templater buttons from inline `style="..."` to maintainable CSS classes**

---

## 🎯 When to Use

- Vault has buttons with inline `style="background: linear-gradient(...)"` attributes
- Buttons use `type="command" command="templater-insert-template-X"` syntax
- You want consistent styling without repeating inline CSS
- Migrating vault to CSS class-based button system

---

## 📋 Button Syntax Migration

| Old Syntax | New Syntax |
|------------|------------|
| `type="command" command="templater-insert-template-X"` | `type="template" action="Templates/X"` |
| `style="background: linear-gradient(...)"` | `color="purple" class="btn btn-purple"` |
| `<a href="..." style="...">` | `<button type="link" href="..." color="purple" class="btn btn-purple">` |

### Before (Old Format)
```html
<button type="command" command="templater-insert-template-Daily Journal Template" 
style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 24px; border-radius: 8px; border: none; cursor: pointer; font-weight: 600; transition: all 0.3s ease;">
📖 New Daily Journal
</button>
```

### After (New Format)
```html
<button type="template" action="Templates/Daily Journal Template" 
color="purple" class="btn btn-purple">
📖 New Daily Journal
</button>
```

---

## 🔧 Step-by-Step Migration Process

### Step 1: Scan Vault for Inline-Style Buttons

```python
from hermes_tools import search_files

result = search_files(
    pattern='style="background: linear-gradient',
    path='/path/to/vault/',
    limit=100
)

print(f"Found {result['total_count']} inline-styled buttons")
for match in result['matches']:
    print(f"  - {match['path'].split('/')[-1]} (line {match['line']})")
```

**Typical output:**
```
Found 40 inline-styled buttons
  - Dashboard.md (line 35)
  - Dashboard.md (line 36)
  - Quick Capture Buttons.md (line 15)
  ...
```

### Step 2: Identify Files to Migrate

Separate user-facing files from test/debug files:

```python
main_files = []
test_files = []

for match in result['matches']:
    filename = match['path'].split('/')[-1]
    if filename.startswith(('TEST', 'BUTTON-')):
        test_files.append(match)
    else:
        main_files.append(match)

print(f"Main files: {len(main_files)}")
print(f"Test files: {len(test_files)}")
```

### Step 3: Convert Buttons Using Patch Tool

For each file, use targeted replacement:

```python
from hermes_tools import patch

# Define the conversion
old_button = '''<button type="command" command="templater-insert-template-Daily Journal Template" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 24px; border-radius: 8px; border: none; cursor: pointer; font-weight: 600; transition: all 0.3s ease;">📖 New Daily Journal</button>'''

new_button = '''<button type="template" action="Templates/Daily Journal Template" color="purple" class="btn btn-purple">📖 New Daily Journal</button>'''

patch(
    mode="replace",
    path="/path/to/file.md",
    old_string=old_button,
    new_string=new_button
)
```

### Step 4: Update Button Groups

Remove inline styles from button group divs:

**Before:**
```markdown
<div class="button-group" style="display: flex; gap: 12px; flex-wrap: wrap;">
```

**After:**
```markdown
<div class="button-group">
```

The CSS for `.button-group` should be in your vault's CSS snippets.

---

## 🎨 Color Mapping

| Old Inline Style | New Color Attribute | New CSS Class |
|------------------|-------------------|---------------|
| Purple gradient | `color="purple"` | `btn btn-purple` |
| Blue gradient | `color="primary"` | `btn btn-primary` |
| Green gradient | `color="success"` | `btn btn-success` |
| Orange gradient | `color="warning"` | `btn btn-warning` |
| Red gradient | `color="danger"` | `btn btn-danger` |
| Cyan gradient | `color="info"` | `btn btn-info` |

---

## 📦 Required CSS Snippet

Ensure your vault has this CSS in `.obsidian/snippets/premium-buttons.css`:

```css
/* Premium Button Styles */
.btn {
  display: inline-block;
  padding: 10px 20px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.2s ease;
  border: none;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

/* Purple gradient - default for this vault */
.btn-purple {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

/* Button Groups */
.button-group {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}
```

**Enable the CSS snippet:**
1. Settings → Appearance → CSS snippets
2. Toggle **premium-buttons** ON
3. Reload vault (Ctrl+R)

---

## 📋 Documentation Update Pattern

When migrating, update your documentation to show both formats:

```markdown
### Button Syntax Reference

**OLD Format (Inline Styles):**
```html
<button type="command" command="templater-insert-template-X" 
style="background: linear-gradient(...)" ...>
Label
</button>
```

**NEW Format (CSS Classes - RECOMMENDED):**
```html
<button type="template" action="Templates/X" 
color="purple" class="btn btn-purple">
Label
</button>
```
```

---

## ✅ Verification Checklist

After migration:

- [ ] No `style="background: linear-gradient` remains in main files
- [ ] All buttons use `type="template"` instead of `type="command"`
- [ ] All buttons use `action="Templates/X"` instead of `command="..."`
- [ ] All buttons have `color="purple"` and `class="btn btn-purple"`
- [ ] CSS snippet is enabled in Settings → Appearance
- [ ] Test buttons by clicking them in Obsidian

---

## ⚠️ Common Pitfalls

| Issue | Solution |
|-------|----------|
| Buttons show but no hover effects | Enable CSS snippet in Appearance settings |
| Templates don't insert | Ensure `action="Templates/X"` points to real file |
| Old format still in files | Use `search_files` to find remaining instances |
| CSS not applying | Check `.obsidian/appearance.json` has `enabledSnippets` |
| **Template path wrong** | Use `action="Templates/TemplateName"` (no `.md`, no `Templates/` folder in path if it's the folder name) |

---

## 📊 Example: Full File Migration

**File: Dashboard.md**

**Before:**
```markdown
### Daily Planning
<div class="button-group" style="display: flex; gap: 12px; flex-wrap: wrap;">
<button type="command" command="templater-insert-template-Daily Journal Template" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 24px; border-radius: 8px; border: none; cursor: pointer; font-weight: 600; transition: all 0.3s ease;">📖 New Daily Journal</button>
<button type="command" command="templater-insert-template-Task Template" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 24px; border-radius: 8px; border: none; cursor: pointer; font-weight: 600; transition: all 0.3s ease;">✅ New Task</button>
</div>
```

**After:**
```markdown
### Daily Planning
<div class="button-group">
<button type="template" action="Templates/Daily Journal Template" color="purple" class="btn btn-purple">📖 New Daily Journal</button>
<button type="template" action="Templates/Task Template" color="purple" class="btn btn-purple">✅ New Task</button>
</div>
```

---

## 🔍 Search Pattern Reference

Find old buttons:
```bash
# Using search_files tool
pattern='style="background: linear-gradient'
# or
pattern='type="command" command="templater-insert-template'
```

Find new buttons:
```bash
pattern='type="template" action="Templates/'
```

---

## 📁 Files Typically Affected

- `Dashboard.md` - Main dashboard buttons
- `Quick Capture Buttons.md` - Quick action buttons
- `Projects.md` - Project management buttons
- `Weekly Reviews.md` - Review buttons
- `Habits Tracker.md` - Habit tracking buttons

---

## 💡 Pro Tips

1. **Leave test files with old format** - They serve as reference for users
2. **Update documentation** - Show both old and new formats for future reference
3. **Batch process** - Handle one file at a time, verify before moving on
4. **Test functionality** - Click buttons in Obsidian after migration
5. **Document the change** - Update your vault's README or documentation

---

## 🚀 Quick Migration Script

```python
from hermes_tools import search_files, patch

# Step 1: Find files with inline-style buttons
result = search_files(
    pattern='type="command" command="templater-insert-template',
    path='/path/to/vault/',
    limit=50
)

# Step 2: Process each file
for match in result['matches']:
    if 'TEST' in match['path'] or 'BUTTON' in match['path']:
        continue  # Skip test files
        
    filepath = match['path']
    print(f"Processing: {filepath}")
    
    # Read file content
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Apply transformations
    # (Add your specific replacements here)
    
    # Write back
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"  ✅ Done")
```

---

*Obsidian Templater Button Migration v1.0 | Created: April 2026*