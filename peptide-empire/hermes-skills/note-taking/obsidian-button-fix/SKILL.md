---
name: obsidian-button-fix
description: Fix button rendering issues in Obsidian vaults where buttons display as raw code instead of styled clickable elements using HTML anchor tags with CSS classes
category: note-taking
tags: [obsidian, buttons, rendering, html, css]
---

# Obsidian Button Rendering Fix

Fix button rendering issues in Obsidian vaults where buttons display as raw code instead of styled clickable elements.

## Problem

When using **HTML button syntax** in Obsidian vaults, custom elements like:
- `<button type="template" action="..." color="...">` (Buttons plugin syntax)
- `![[button|Label|link|color]]` (legacy syntax)

do **not** render properly without the correct setup.

**Common symptoms:**
- Buttons display as raw HTML code
- Buttons show but don't have hover effects
- Template buttons don't trigger template creation

**Root causes:**
1. **CSS snippet not enabled** - The most common issue. Just having `premium-buttons.css` in `.obsidian/snippets/` doesn't work. It must be enabled in Settings → Appearance → CSS snippets.
2. **Buttons plugin disabled** - If using `<button type="template">` syntax, the Buttons plugin must be enabled in Settings → Community plugins.
3. **Wrong link format** - HTML anchor tags need proper paths (`.md` extension or internal link syntax `[[...]]`)

## Solution

Convert all buttons to HTML anchor format with CSS classes:

### Before (Invalid)
```markdown
![[button|New Daily Journal|Templates/Daily Journal Template.md|primary]]
```

### After (Valid)
```markdown
<a href="Templates/Daily Journal Template.md" class="btn btn-primary">📖 New Daily Journal</a>
```

## Implementation Steps

### 1. Create Button CSS Snippet

Create or update `.obsidian/snippets/premium-buttons.css`:

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

/* Gradient Colors */
.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-secondary {
  background: linear-gradient(135deg, #607d8b 0%, #78909c 100%);
  color: white;
}

.btn-success {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  color: white;
}

.btn-warning {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.btn-danger {
  background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
  color: white;
}

.btn-info {
  background: linear-gradient(135deg, #12c2e9 0%, #c471ed 100%);
  color: white;
}

.btn-purple {
  background: linear-gradient(135deg, #8e44ad 0%, #9b59b6 100%);
  color: white;
}

/* Button Groups */
.button-group {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}
```

### 2. Enable CSS Snippet (Critical!)

The CSS snippet must be **enabled in Obsidian's settings** for buttons to render with styles:

**Option A: Via UI**
1. Open Obsidian → Settings → Appearance
2. Scroll to "CSS snippets" section
3. Click refresh button (↻)
4. Toggle **premium-buttons** ON

**Option B: Via JSON (for automation)**
Edit `.obsidian/appearance.json`:
```json
{
  "theme": "obsidian",
  "cssTheme": "Minimal",
  "enabledSnippets": [
    "premium-buttons.css",
    "premium-callouts.css",
    "progress-bars.css"
  ]
}
```

**Troubleshooting:** If buttons still don't render:
- Check `.obsidian/appearance.json` has `"enabledSnippets"` array
- Ensure snippet filename is exact (case-sensitive)
- Reload vault (`Ctrl+R` / `Cmd+R`)

### 3. Convert Existing Buttons (Bulk Fix)

Use Python script to convert all invalid button syntax:

```python
import re
import os

def convert_buttons_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Pattern 1: ![[button|Label|link|color]]
    pattern1 = r'\!\[\[button\|([^|]+)\|([^|]+)\|([^]]+)\]\]'
    
    # Color mapping
    color_map = {
        'primary': 'btn-primary',
        'secondary': 'btn-secondary',
        'success': 'btn-success',
        'warning': 'btn-warning',
        'danger': 'btn-danger',
        'info': 'btn-info',
        'purple': 'btn-purple'
    }
    
    def replace_button(match):
        label = match.group(1)
        link = match.group(2)
        color = match.group(3).lower()
        css_class = color_map.get(color, 'btn-primary')
        return f'<a href="{link}" class="btn {css_class}">{label}</a>'
    
    new_content = re.sub(pattern1, replace_button, content)
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    
    return True

# Process all markdown files in vault
vault_path = "/path/to/vault"
for root, dirs, files in os.walk(vault_path):
    for file in files:
        if file.endswith('.md'):
            filepath = os.path.join(root, file)
            convert_buttons_in_file(filepath)
```

### 4. Button Syntax Reference

| Type | Syntax | Example |
|------|--------|---------|
| Primary | `<a href="link" class="btn btn-primary">Label</a>` | Main actions |
| Success | `<a href="link" class="btn btn-success">Label</a>` | Positive actions |
| Warning | `<a href="link" class="btn btn-warning">Label</a>` | Caution actions |
| Info | `<a href="link" class="btn btn-info">Label</a>` | Informational |
| Danger | `<a href="link" class="btn btn-danger">Label</a>` | Delete/warning |

### 5. Button Groups

For multiple buttons on one line:

```markdown
<div class="button-group" style="display: flex; gap: 12px; flex-wrap: wrap;">
  <a href="link1" class="btn btn-primary">Button 1</a>
  <a href="link2" class="btn btn-success">Button 2</a>
  <a href="link3" class="btn btn-info">Button 3</a>
</div>
```

## Verification

1. Open file in Obsidian
2. Buttons should render as **clickable, styled elements**
3. If still showing as code:
   - Reload vault (`Ctrl+R` / `Cmd+R`)
   - Toggle Buttons plugin off/on
   - Check CSS snippet is enabled

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| Buttons show as raw code | Enable CSS snippet in Appearance settings |
| No hover effects | Check browser cache, reload page |
| Links not working | Ensure relative paths are correct |
| Gradient not showing | Check CSS snippet file is saved |
| **Buttons don't create templates** | **Enable Buttons plugin + Templates plugin in Settings** |
| **Error: template not found** | Verify template file exists in Templates folder |
| **Nothing happens on click** | Reload Obsidian (Ctrl+R), check plugin is enabled |

## Troubleshooting Broken Buttons

When buttons don't work, follow this diagnostic flow:

1. **Check Plugin Status**
   - Settings → Community plugins → Is "Buttons" enabled?
   - Settings → Core plugins → Is "Templates" enabled?

2. **Verify Template Files Exist**
   - Check `Templates/` folder for the referenced templates
   - Template name in button must match actual file name

3. **Test with Simple Button**
   - Create a test file with a simple button
   - If it works, the issue is with your original file

4. **Reload Obsidian**
   - Press Ctrl+R (Cmd+R on Mac)
   - Or close and reopen Obsidian

5. **Check CSS Snippets**
   - Settings → Appearance → CSS snippets
   - Enable any premium button styling snippets
| **Buttons plugin installed but buttons broken** | Plugin being in `community-plugins.json` doesn't mean it's enabled. Use HTML anchor syntax instead (no plugin required) |
| **CSS snippet not applying** | Check `.obsidian/appearance.json` has `"enabledSnippets"` array with exact filename |
| **Template buttons don't create new notes** | HTML anchor tags (`<a href="...">`) are for **navigation links**. Use `<button type="template" action="...">` syntax for **template creation** (requires Buttons plugin enabled) |

## Critical: Button Type Selection

**Choose the right button type for your use case:**

| Use Case | Recommended Syntax | Why |
|----------|-------------------|-----|
| **Navigation links** (view pages, jump to sections) | `<a href="Page.md" class="btn btn-purple">Label</a>` | Works without plugins, has premium styling |
| **Template creation** (create new notes from templates) - **Buttons plugin enabled** | `<button type="template" action="TemplateName" color="purple">Label</button>` | Only Buttons plugin can create new notes |
| **Template creation** (create new notes from templates) - **Buttons plugin DISABLED** | `<button type="command" command="templater-insert-template-TemplateName" class="btn btn-purple">Label</button>` | Uses Templater commands directly, no Buttons plugin required |
| **External links** (open websites) | `<a href="https://example.com" class="btn btn-purple">Label</a>` | Standard HTML anchor behavior |

**The Buttons plugin is NOT required for HTML anchor buttons**, but you DO need:
1. The `premium-buttons.css` snippet enabled in Settings → Appearance → CSS snippets
2. The `.obsidian/appearance.json` file must have `"enabledSnippets": ["premium-buttons.css"]`

**⚠️ IMPORTANT: Buttons Plugin vs Templater Commands**

When the **Buttons plugin is uninstalled or disabled**:
- ❌ `<button type="template" action="Templates/TemplateName" ...>` buttons **BREAK**
- ❌ `<button type="link" href="..." ...>` buttons **BREAK**
- ✅ `<button type="command" command="templater-insert-template-..." class="btn btn-purple">` **WORKS** (uses Templater)
- ✅ `<a href="..." class="btn btn-purple">` **WORKS** (standard HTML)

**Conversion from Buttons Plugin to Templater:**

| OLD (Buttons Plugin Required) | NEW (Templater Only) |
|------------------------------|---------------------|
| `<button type="template" action="Templates/Daily Journal Template" ...>` | `<button type="command" command="templater-insert-template-Daily Journal Template" class="btn btn-purple">` |
| `<button type="link" href="Habits Tracker.md" ...>` | `<a href="Habits Tracker.md" class="btn btn-purple">` |

## Troubleshooting: Buttons Don't Work

### Scenario 1: Buttons show as raw HTML code
**Cause:** CSS snippet not enabled
**Fix:** Enable in Settings → Appearance → CSS snippets → Toggle "premium-buttons" ON

### Scenario 2: Buttons styled but clicking doesn't create new note
**Cause:** Using HTML anchor tag for template creation
**Fix:** Use `<button type="template" action="TemplateName" color="purple">Label</button>` syntax

### Scenario 3: Buttons plugin enabled but buttons broken
**Cause:** Template name doesn't match actual template filename
**Fix:** Ensure `action="TemplateName"` matches exactly (case-sensitive, no `.md` extension)

### Scenario 4: CSS doesn't apply at all
**Cause:** `enabledSnippets` missing from `appearance.json`
**Fix:** Add to `.obsidian/appearance.json`:
```json
{
  "enabledSnippets": ["premium-buttons.css"]
}
```

### Scenario 5: Buttons plugin shows as "Enabled" but nothing happens on click
**Cause:** Plugin files exist but plugin isn't properly initialized
**Diagnosis:**
1. **Test button type** - Try clicking Command buttons (`type="command"`), Link buttons (`type="link"`), and Template buttons (`type="template"`)
2. **Test both modes** - Try in Edit Mode (Ctrl+Shift+M) and Reading Mode
3. **Test HTML** - If even HTML links (`<a href="...">`) don't work, you might be in Reading Mode

**Fix:**
1. **Disable Buttons plugin** in Settings → Community plugins
2. **Wait 2 seconds**
3. **Enable Buttons plugin** again
4. **Reload Obsidian** (click OK when prompted)
5. **Test again**

**If STILL broken:** Use HTML anchor syntax instead (no plugin required):
```markdown
<a href="Templates/Daily Journal Template.md" class="btn btn-purple">Label</a>
```

## When to Use This

- ✅ Creating interactive dashboards
- ✅ Quick capture pages
- ✅ Navigation hubs
- ✅ Productivity systems with multiple action points

## Alternative Approaches

### Option 1: Buttons Plugin Native Syntax
```markdown
!button[New Journal] Templates/Daily Journal Template.md
```
- **Pros**: Simpler syntax
- **Cons**: Limited styling, no gradients

### Option 2: Callout Buttons
```markdown
> [!INFO] Actions
> [[New Journal|New Journal]] | [[New Task|New Task]]
```
- **Pros**: Built into Obsidian
- **Cons**: Takes more vertical space

### Option 3: Dataview Queries
```dataview
LIST WITHOUT id
WHERE contains(tags, "action")
```
- **Pros**: Dynamic content
- **Cons**: Requires Dataview plugin

---

## YAML-Style Block Syntax (Buttons Plugin)

The Buttons plugin also supports a YAML-style block syntax inside fenced code blocks. This is the format used in modern dashboards (e.g., Second-Brain-Duo-2026).

### Valid Block Syntax
```button
name 📖 New Daily Journal
type template note(Journal, tab)
action Daily Journal Template
folder 3-Resources/Daily Notes
prompt true
color purple
```

### Block Syntax Parameters

| Parameter | Valid Values | Required? | Description |
|-----------|-------------|-----------|-------------|
| `name` | Any text with emojis | Yes | Button label |
| `type` | `template`, `templater`, `link`, `command` | Yes | Button behavior. Use `template` for core Templates plugin, `templater` for Templater community plugin, `link` for navigation, `command` for Obsidian commands |
| `note(Title, tab)` | Any title string | For templates | Creates new note with title, opens in tab |
| `action` | Template name or URL | Yes | Target template/page/command |
| `folder` | Folder path | Optional | Where to create new note |
| `prompt` | `true` / `false` | Optional | Ask for confirmation before action |
| `color` | `purple`, `blue`, `green`, `red`, `orange` | Optional | Button color |

### ⚠️ Critical: Invalid Parameters That BREAK Buttons

The Buttons plugin ignores *some* unknown parameters silently — but others corrupt the YAML-like block parser and **prevent the button from rendering at all**. No error, no warning, the button just shows as raw code or disappears entirely.

| Invalid Parameter | Severity | Why It Fails | Fix |
|-------------------|----------|-------------|-----|
| `type template cursor` | 🔴 BREAKS | `cursor` is not a valid type suffix — parser rejects the entire block | Use `type template note(Title, tab)` |
| `cursorAt "Top 3 Priorities"` | 🔴 BREAKS | Quoted value with spaces **corrupts the YAML-like block parser** — button won't render at all. This is the #1 cause of "some buttons purple, this one raw code" in production vaults. | Remove the line entirely. Cursor positioning after template insertion is not supported by any syntax. |
| `cursor: true` | 🟡 Silent fail | YAML-style colon not recognized by Buttons parser — silently ignored, no button breakage | Use `cursor true` (space, no colon) or remove |
| `prompt: true` | 🔴 BREAKS | Colons break YAML parsing in button blocks — entire block fails | Use `prompt true` (space, no colon) |
| `scrollTo` | 🟡 Silently ignored | Not a supported parameter | Remove |
| `position` | 🟡 Silently ignored | Not a supported parameter | Remove |

**Key distinction:** `cursorAt` with a quoted string value is **NOT silently ignored** — it corrupts the block parser. The button will not render at all. This is the single most common cause of "some buttons look purple but others don't" in production vaults.

**Key distinction:** `cursorAt` with a quoted string is NOT silently ignored — it corrupts the block parser. This is the #1 cause of "some buttons render purple but this one shows as raw code" in production vaults.

### Block Syntax: Template Button Pattern

**Working pattern** (copy this):
```button
name 🎯 Button Label
type template note(Note Title, tab)
action Template Name
folder path/to/folder
prompt true
color purple
```

**Broken pattern** (common mistake):
```button
name 🎯 Button Label
type template cursor        ← INVALID: not a recognized type
action Template Name
cursorAt "Section Name"     ← INVALID: silently ignored
prompt true
color purple
```

### Block Syntax: Link Button Pattern
```button
name 📈 Log Habits
type link
action obsidian://open?vault=VaultName&file=PageName
color purple
```

### Block Syntax: Command Button Pattern
```button
name ⚡ Run Command
type command
action some-obsidian-command-id
color purple
```

---

### Debugging Broken Block Syntax Buttons

When a block-syntax button does nothing on click:

1. **Check `type` parameter** — Must be `template`, `link`, or `command`. `cursor` alone is invalid.
2. **Check for `note(Title, tab)`** — Template buttons MUST use `note(Title, tab)` suffix, not `cursor`.
3. **Remove unknown params** — `cursorAt`, `scrollTo`, `position` are NOT supported.
4. **Verify `action` matches** — Template name must exactly match the file in Templates folder (no `.md` extension).
5. **Check `folder` path** — Must be a valid relative path from the vault root.
6. **Compare to working buttons** — Copy the exact pattern from another working button in the same file.

## Vault-Wide Button Audit Workflow

When asked to fix broken buttons across a vault, use this systematic approach:

### Step 0: Run the automated validator (recommended first pass)

```bash
python3 scripts/validate-buttons.py /path/to/vault
## Vault-Wide Button Audit Workflow

When asked to fix broken buttons across a vault, use this systematic approach:

### Step 0: Run the automated validator (recommended first pass)

```bash
python3 scripts/validate-buttons.py /path/to/vault
```

This single script checks: missing params, `cursorAt` breakage, `type template cursor` breakage, template existence, folder existence, and link target validity. Fix everything it reports, then re-run to confirm zero issues.

### Step 1: Extract ALL button blocks from the vault
```bash
VAULT="/path/to/vault"
grep -rln '```button' "$VAULT" --include='*.md'
grep -rA 10 '```button' "$VAULT" --include='*.md'
```

### Step 2: Check for known-invalid parameters
```bash
# Find buttons with BREAKING cursorAt or cursor usage
grep -rA 8 '```button' "$VAULT" --include='*.md' | grep -i 'cursorat\|type template cursor'
```

### Step 3: Verify all template references exist
```bash
# List all template names (without .md extension)
ls "$VAULT/Templates/" | sed 's/\\.md$//'

# Check each button's action against known templates
# Any action NOT in the template list is broken
```

### Step 4: Verify all folder references exist
```bash
# Check each button's folder path
# Any folder NOT found by `test -d` is broken
```

### Step 5: Fix and verify
- Fix all broken buttons using the correct patterns above
- **Remove all `cursorAt` lines entirely** — they BREAK buttons
- Re-run Step 0 (`validate-buttons.py`) to confirm zero issues remain
- Check documentation sections that describe button syntax — remove references to invalid parameters like `cursorAt`