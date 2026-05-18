---
name: obsidian-button-syntax-fix
description: Fix broken button syntax in Obsidian vaults - scan for old patterns, convert to modern Buttons plugin syntax, organize into groups
version: 1.0
author: NurseRobHealth
tags: [obsidian, buttons, vault-maintenance, plugin-fix]
---

# Obsidian Button Syntax Fix
## Scan & Convert Broken Buttons to Modern Syntax

> **Fix broken button syntax in Obsidian vaults using the Buttons plugin by Sam Morrison**

---

## 🎯 When to Use

- Converting vaults with outdated button syntax (`[[Button: ...]]`)
- Fixing broken plugin references after plugin updates
- Modernizing vaults with HTML buttons (`<a href="..." class="button">`)
- Converting custom button formats to standard plugin syntax

---

## 📋 Button Syntax Evolution

| Old Syntax | New Syntax |
|------------|------------|
| `[[Button: Label]]` | `![[button\|Label\|link\|color]]` |
| `<a href="..." class="button">` | `![[button\|Label\|...]]` |
| `<div class="button-group">` | `<div class="button-group">` (keep) |

---

## 🔧 Step-by-Step Fix Process

### Step 1: Scan Vault for Button Patterns

```python
import os
import re

vault_path = "/path/to/vault"

# Find all markdown files
all_files = []
for root, dirs, files in os.walk(vault_path):
    for file in files:
        if file.endswith('.md'):
            all_files.append(os.path.join(root, file))

# Search for button patterns
button_patterns = [
    r'\[\[Button:',      # Old [[Button: syntax
    r'\[\[button:',      # Old [[button: syntax  
    r'<div class="button-group">',  # HTML button group
    r'<a class="button">',  # HTML anchor button
    r'<button',  # HTML button tag
]

files_with_buttons = {}

for filepath in all_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for pattern in button_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            if filepath not in files_with_buttons:
                files_with_buttons[filepath] = {}
            files_with_buttons[filepath][pattern] = len(matches)

print(f"Found {sum(len(v) for v in files_with_buttons.values())} buttons in {len(files_with_buttons)} files")
```

### Step 2: Read Files with Buttons

```python
for filename, patterns in files_with_buttons.items():
    print(f"\n📄 {filename}")
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'button' in line.lower():
            print(f"   Line {i+1}: {line[:100]}")
```

### Step 3: Convert to New Syntax

**Pattern 1: Simple Button Conversion**
```python
old_buttons = [
    ("[[Button: New Project]]", "![[button|🚀 New Project|Templates/Project Template.md|primary]]"),
    ("[[Button: New Task]]", "![[button|✅ New Task|Templates/Task Template.md|success]]"),
]

for old, new in old_buttons:
    content = content.replace(old, new)
```

**Pattern 2: Button Groups (Keep CSS, Fix Buttons)**
```python
# Old HTML group with broken buttons
old_section = """<div class="button-group">
  <a href="..." class="button">Label</a>
</div>"""

# New group with proper syntax
new_section = """<div class="button-group" style="display: flex; gap: 12px;">
![[button|Label|link|color]]
</div>"""
```

### Step 4: Write & Verify

```python
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
with open(filepath, 'r', encoding='utf-8') as f:
    new_content = f.read()

old_count = new_content.count("[[Button:")
new_count = new_content.count("![[button|")

print(f"✅ Old: {old_count}, New: {new_count}")
```

---

## 🎨 Button Syntax Reference

### Basic Button
```markdown
![[button|Label|link|color]]
```

### Parameters
| Parameter | Description | Examples |
|-----------|-------------|----------|
| `Label` | Text shown (use emojis!) | `🚀 New Project` |
| `link` | Page or template path | `Templates/Project Template.md` |
| `color` | Button color | `primary, success, warning, info, secondary` |

### Colors
- **primary** (🔵 Blue) - Main actions, new items
- **success** (🟢 Green) - Positive actions, tracking
- **warning** (🟡 Yellow) - Important/urgent actions
- **info** (🔷 Light Blue) - Informational, views
- **secondary** (⚫ Gray) - Secondary actions

---

## 📦 Button Groups

### Styled Button Group
```markdown
<div class="button-group" style="display: flex; gap: 12px; flex-wrap: wrap;">
![[button|📖 New Journal|Templates/Daily Journal Template.md|primary]]
![[button|✅ New Task|Templates/Task Template.md|success]]
![[button|💡 Quick Note|Templates/Resource Note Template.md|warning]]
</div>
```

### Footer Button Group
```markdown
<div class="button-group" style="display: flex; gap: 16px; justify-content: center; margin-top: 32px;">
![[button|⚡ Quick Capture|Quick Capture Buttons|primary]]
![[button|📅 Weekly Review|Templates/Weekly Review Template.md|info]]
![[button|📈 Track Habits|Habits Tracker|success]]
</div>
```

---

## 📊 Example: Full File Fix

**Before:**
```markdown
# Quick Actions

**Daily Planning**
- 🗓️ **New Daily Journal**
- ✅ **New Task**

[[Button: Log Today's Habits]]
```

**After:**
```markdown
# Quick Actions

### Daily Planning
<div class="button-group" style="display: flex; gap: 12px;">
![[button|📖 New Daily Journal|Templates/Daily Journal Template.md|primary]]
![[button|✅ New Task|Templates/Task Template.md|success]]
</div>

<div class="button-group" style="display: flex; gap: 12px;">
![[button|📈 Log Today's Habits|Habits Tracker|success]]
</div>
```

---

## ⚠️ Common Pitfalls

| Issue | Solution |
|-------|----------|
| Old syntax not found | Use `.replace()` on exact strings from file |
| Button group CSS missing | Add `display: flex; gap: 12px; flex-wrap: wrap;` |
| Links not working | Use relative paths (`Templates/...`) not absolute |
| Colors not applying | Check spelling: `primary` not `Primary` |

---

## ✅ Verification Checklist

After fixing buttons:

- [ ] No `[[Button:` syntax remains
- [ ] All buttons use `![[button|...]]` format
- [ ] Button groups have CSS styling
- [ ] Links point to valid pages/templates
- [ ] Colors match button purpose
- [ ] Emojis added for visual appeal

---

## 📁 Files Typically Affected

- `Dashboard.md` - Quick actions section
- `Quick Capture Buttons.md` - All quick actions
- `Projects.md` - Project management buttons
- `Habits Tracker.md` - Habit tracking buttons
- `Tasks.md` - Task management buttons
- `Templates/` - Template buttons

---

*Obsidian Button Syntax Fix v1.0 | Created: April 2026*