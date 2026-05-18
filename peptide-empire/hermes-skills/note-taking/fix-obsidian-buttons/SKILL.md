---
name: Fix Obsidian Buttons Plugin Issues
description: Troubleshoot and fix non-working buttons in Obsidian vaults using the Buttons plugin and Templates plugin - convert onclick handlers to proper command syntax
tags: [obsidian, buttons, templates, troubleshooting]
aliases: [obsidian-buttons-fix, fix-obsidian-template-buttons]
---

# Fix Obsidian Buttons Plugin Issues

## Overview

This skill covers troubleshooting and fixing non-working buttons in Obsidian vaults that use the **Buttons** plugin (by Sam Morrison), **Templater**, and core **Templates** plugin. 

**Updated 2026-04-14 (v2) after full vault engineering pass on Second-Brain-Duo-2026 + follow-up cleanup**: Added systematic Hermes Agent workflow using `search_files`, config patching (`community-plugins.json`), test-file *deletion*, precise `patch` with tool-provided before/after diffs for *every edit*, documentation updates in production files, and strict exclusion of test files. Non-trivial due to tool call failures (missing `path` param, JSON parse errors in execute_code), gray-button diagnosis (missing `class="btn btn-purple"` even with `color="purple"`), and user constraints (only delete exact 6 listed test files, never alter real content beyond buttons, always show tool diffs). Standardized fully on `type="template" action="..." color="purple" class="btn btn-purple"` when both Buttons + Templater active. Updated internal docs (e.g. Quick Capture Buttons.md) to reflect current recommended syntax. Prefer this over legacy `type="command" command="templater-insert-template-..."`.

## Systematic Vault-Wide Button Audit & Fix (Hermes Agent Workflow)

This is the reusable procedure executed for the "senior Obsidian vault engineer" task. It is non-trivial, iterative, and incorporates trial-and-error findings (plugin config missing, mixed Templater vs Buttons syntax, test files vs production).

1. **Recursive Scan**: Use `search_files` (not terminal grep) with broad pattern:
   ``` 
   search_files(pattern='button|Button|onclick|type=.*(template|command)|btn|!\[\[button|\[\[Button:', file_glob='*.md', output_mode='files_only', path=VaultPath)
   ```
   This catches HTML buttons, legacy syntax, Templater commands, callouts, etc.

2. **Environment Inspection**:
   - Read `.obsidian/community-plugins.json` (add `"buttons"` if missing via `patch`).
   - Read `.obsidian/appearance.json` (confirm `enabledCssSnippets` includes premium-buttons.css etc.).
   - `terminal("ls -la Templates/")` or `search_files` on Templates/ to verify template names match `action=` values exactly (no .md, no path, case-sensitive).

3. **Per-File Diagnosis & Fix** (production files only):
   - Use `read_file` on each (Dashboard.md, Quick Capture Buttons.md, Projects.md, Weekly Reviews.md, etc.).
   - Identify broken patterns: `type="command" command="templater-insert-template-Name"`, inline `style="background: linear-gradient..."`, `onclick=`, legacy `[[Button:`.
   - **Safe fix**: Replace with `<button type="template" action="ExactTemplateName" color="purple">Label</button>` for creation actions. Keep `<a href="..." class="btn btn-purple">` for navigation. Preserve all surrounding content, Dataview, callouts, documentation.
   - Use `patch` tool with exact multi-line `old_string` / `new_string` for precision (provides unified diff). Never use broad replace_all unless verified.
   - **Decision rule**: Leave TEST-*.md, BUTTON-*.md, BUTTON-DEBUG.md untouched — they serve as reference for old syntax.

4. **CSS & Plugin Alignment**:
   - Ensure `premium-buttons.css` exists and is enabled (it defines `.btn`, `.button-group`, `.btn-purple` gradients).
   - Buttons plugin + `color="purple"` leverages built-in styling + snippet.

5. **Final Verification Pass**:
   - Re-run the exact `search_files` scan.
   - Spot-check production files with `read_file`.
   - Report: 100% working notes + any that need manual attention (usually the test files).
   - Instruct user to restart Obsidian, enable Buttons plugin, reload vault (Ctrl/Cmd+R).

**Pitfalls Discovered in This Run**:
- `community-plugins.json` missing `"buttons"` entry caused plugin to be inactive despite files present.
- Templater `command="templater-insert-template-XXX"` works but is less reliable than native Buttons `type="template"`.
- Test/reference files must be explicitly excluded to avoid breaking educational content.
# Fix Obsidian Buttons Plugin Issues (Updated 2026)

## Overview

Comprehensive workflow for auditing, diagnosing, and fixing **all** button issues in Obsidian vaults using the official **Buttons** plugin (shabegom/buttons). Prioritizes official codeblock syntax from https://buttonslovesyou.com/.

**Key Lesson from Iterative Fixes:** HTML `<button type="template">`, `type="command"`, `type="templater"` often appear to render (purple via CSS) but fail to trigger actions due to plugin parsing, mangled attributes from overlapping patches, or missing plugin registration. **Official codeblock is most reliable** for Templater integration. Always verify with full vault scan, plugin config, Templates/ folder match, and full Obsidian restart.

## When to Use This Skill
- Buttons look perfect but do nothing on click
- Mangled syntax from previous edits (`type templater`, duplicated attributes, leftover HTML fragments)
- Mixed syntax across vault (HTML, inline, old [[Button]])
- User has PARA/Second Brain vault with frequent dashboard/quick-capture buttons
- Need to delete test/debug files while preserving production content

## Root Causes Identified Across Iterations
1. **Syntax drift**: `type="template"` vs `type="templater"` vs `type="command" command="templater-insert-template-..."` — only official codeblock is parsed reliably by Buttons plugin.
2. **Patch accumulation**: Repeated `patch` calls create mangled output (e.g. `type="templater" type="templater"`).
3. **Plugin/Config gaps**: Buttons not in community-plugins.json, Templates folder mismatch, CSS snippets enabled but codeblock not used.
4. **Test pollution**: Leftover TEST-*.md / BUTTON-*.md files with experimental syntax.

## Systematic Fix Workflow (Reusable, Non-Trivial)

1. **Scan**: `search_files(pattern='<button|type templater|```button|onclick|type="command"|type="template"', file_glob='*.md', output_mode='files_only')` — identify all affected production files (exclude pure test files initially).

2. **Verify Environment**:
   - Read `.obsidian/community-plugins.json` (ensure `"buttons"` present).
   - Confirm Templates/ folder and exact filenames (case-sensitive, no .md in `action`).
   - Check `premium-buttons.css` for `.btn` / `.button-group` and `appearance.json` for enabledSnippets.
   - Use `web_extract("https://buttonslovesyou.com/")` for latest official syntax.

3. **Cleanup**:
   - Delete **only** specified test files: BUTTON-DEBUG.md, BUTTON-TEST-PAGE.md, TEST BUTTONS.md, TEST-ALL-BUTTON-TYPES.md, TEST-HTML-BUTTONS.md, TEST-LINKS.md (use `terminal` rm).
   - Never delete real notes, templates, or PARA content.

4. **Repair (Safe, Targeted)**:
   - For each button section (inside `<div class="button-group">`):
     - Replace broken/mangled HTML with **exact official codeblock**:
       ````markdown
       ```button
       name New Daily Journal
       type templater
       action Daily Journal Template
       ```
       ````
     - Map buttons to Templates/ exactly: Daily Journal Template, Task Template, Project Template, Resource Note Template, Weekly Review Template, Meeting Notes Template.
     - Preserve **all** surrounding content, div wrappers, CSS classes (`class="btn btn-purple"` if hybrid), Dataview, callouts, text, emojis.
     - Use `execute_code` with loop + `patch` for efficiency on multiple files, or individual `patch` with unique old_string for safety.
     - Show **clear before/after diff** (from tool output) for every edited file (focus on Dashboard.md and Quick Capture Buttons.md if instructed).

5. **Verification**:
   - Re-scan vault for any remaining `<button` or mangled fragments.
   - Confirm all buttons use ```button codeblock.
   - Test in Obsidian after **full close + reopen** (not Ctrl+R — required for plugin re-init).

## Official Syntax Reference (from buttonslovesyou.com)
```button
name Button Label (with emoji)
type templater
action Exact Template Name
```
- `type templater` (not "template" or "command")
- `action` = exact filename from Templates/ (no path, no .md)
- Optional: `id` for inline referencing, `class` for styling.
- Renders as styled button; clicking runs Templater template to create new note.
- For navigation: `type link` or keep `<a class="btn btn-purple">`.

## Common Pitfalls & Lessons Learned
- **Mangling**: Always use unique, long enough `old_string` in patch; prefer `execute_code` for bulk safe replaces.
- **Plugin not triggering**: Full Obsidian restart required after config/syntax changes.
- **Styling vs Function**: CSS (`premium-buttons.css`, `.button-group`) makes them *look* good; only codeblock makes them *work*.
- **Test files**: Isolate and delete only listed test files; leave as reference if user wants.
- **User Expectations**: User wants diffs for key files (Dashboard, Quick Capture), list of fixed buttons, "close and reopen Obsidian" reminder, no content deletion.
- **Efficiency**: One `execute_code` script with search/read/patch loop minimizes tool calls while handling trial-and-error iterations.
- **CRITICAL: Button type syntax**: Use `type templater` (NOT `type template`) for Templater integration. `type template` is a common typo that causes buttons to render but do nothing on click.
- **CRITICAL: Dataview plugin**: Must be in `community-plugins.json` for all Dataview queries to work. 8+ files in Second-Brain-Duo-2026 use Dataview queries.
- **CRITICAL: Template references**: Always verify `action` values match exact template names in Templates/ folder. Placeholder names like "Template Name" break buttons.
- **CRITICAL: obsidian:// URLs**: Avoid using `obsidian://open?vault=...&file=...` for folder links. Use simple folder names like `4-Archives` instead.
- **CRITICAL: Folder references**: `type link` buttons CANNOT point to folders — they must point to files. If you need to navigate to a folder, create an index file (e.g., `3-Resources Index.md`) and point the button to that file instead.
- **Pattern: Index files for folders**: When a button needs to "open a folder", create a markdown index file in that folder with quick actions and navigation, then update the button to reference the file.

## Example Fixed Button Group
**Before (mangled):**
```html
<div class="button-group">
<button type templater action="Daily Journal Template" class="btn btn-purple">📖 New Daily Journal</button>
...
```

**After (official):**
```markdown
<div class="button-group">
```button
name New Daily Journal
type templater
action Daily Journal Template
```
...
```

## Files Typically Fixed
- Dashboard.md (main command center)
- Quick Capture Buttons.md (all action groups + docs)
- Projects.md, Weekly Reviews.md, Habits Tracker.md
- Any with `<div class="button-group">`

## Post-Fix Summary Template
- Files fixed: [list]
- All buttons now use correct ```button codeblock syntax with exact template matches.
- Reminder: fully close and reopen Obsidian (not just reload).

This updated skill encodes the full iterative workflow that succeeded after multiple syntax attempts. Use on any Second-Brain or PARA vault with button issues.

### Step 3: Convert Navigation Buttons

**Wrong (broken):**
```html
<button onclick="document.location='Habits Tracker';">📈 Log Habits</button>
```

**Correct (works):**
```html
<a href="Habits Tracker" class="btn btn-purple">📈 Log Habits</a>
```

### Step 4: Verify Template Configuration

Check `.obsidian/core-plugins-mapping/templates.json`:

```json
{
  "folder": "Templates",
  "templateFolderPath": "Templates"
}
```

### Step 5: Verify Plugins Enabled

Check `.obsidian/core-plugins.json` has:
```json
"templates": true
```

Check `.obsidian/community-plugins.json` has:
```json
"buttons"
```

## Common Patterns

### Template Button Examples

```html
<button type="template" action="Daily Journal Template" color="purple">📖 New Daily Journal</button>
<button type="template" action="Project Template" color="purple">🚀 New Project</button>
<button type="template" action="Task Template" color="purple">✅ New Task</button>
```

### Link Button Examples

```html
<a href="Habits Tracker" class="btn btn-purple">📈 Log Habits</a>
<a href="Projects" class="btn btn-purple">📊 Update Progress</a>
<a href="4-Archives" class="btn btn-purple">🗂️ Archive</a>
```

### Button Groups (CSS styling)

```html
<div class="button-group" style="display: flex; gap: 12px; flex-wrap: wrap;">
  <button type="template" action="Daily Journal Template" color="purple">📖 New Daily Journal</button>
  <button type="template" action="Task Template" color="purple">✅ New Task</button>
</div>
```

## Troubleshooting

### Issue: Buttons don't create new notes

**Cause:** Using `onclick="document.location='...'` which just navigates to the file

**Fix:** Use `type="template" action="..."` syntax

### Issue: Buttons show as raw HTML

**Cause:** Buttons plugin not enabled or syntax wrong

**Fix:** Enable Buttons plugin, verify syntax matches examples above

### Issue: Template button creates note but doesn't populate template

**Cause:** Template folder not configured

**Fix:** Check `.obsidian/core-plugins-mapping/templates.json`

### Issue: Mixed button types (some work, some don't)

**Cause:** Inconsistent syntax across vault

**Fix:** Audit all buttons with search:
```bash
grep -r 'button onclick' vault/
grep -r 'command="templates' vault/
```

### Issue: Buttons have no purple color

**Cause:** Missing `color="purple"` attribute

**Fix:** Add `color="purple"` to template buttons:
```html
<button type="template" action="..." color="purple">Label</button>
```

### Issue: Buttons look unstyled or plain (no color, no hover effects)

**Cause:** CSS snippets not enabled in Settings → Appearance

**Fix:** 
1. **Settings** → **Appearance**
2. **Scroll down** to "CSS snippets" section
3. **Click the refresh button** (↻)
4. **Enable these snippets** (toggle ON):
   - `premium-buttons.css`
   - `premium-callouts.css`
   - `progress-bars.css`
5. **Reload Obsidian** when prompted

**Note:** Even if the Buttons plugin is enabled, the buttons won't have proper styling without these CSS snippets active.

### Issue: Buttons plugin enabled but buttons still don't work

**Cause:** Plugin not actually enabled or CSS snippets missing

**Fix:** Verify in Obsidian:
1. **Settings** → **Community plugins** → **Buttons** should show **"Disable"** (not "Enable")
2. **Settings** → **Appearance** → **CSS snippets** → All premium snippets **toggled ON**
3. **Reload Obsidian**

## Verification

After fixing buttons, verify:

1. **Template buttons** create new notes (not just open files)
2. **Link buttons** navigate to existing notes
3. All buttons have consistent styling (e.g., `btn btn-purple`)

## Files Modified

When fixing a vault, typically update:
- `Dashboard.md` - main quick actions
- `Quick Capture Buttons.md` - additional buttons
- `Habits Tracker.md` - habit tracking buttons
- `Projects.md` - project management buttons
- `Weekly Reviews.md` - review buttons

## Notes

- **Buttons plugin syntax** is different from standard HTML buttons
- Template names in `action` must match exactly (case-sensitive, no path/extension)
- Use `type="template"` for Buttons plugin template buttons
- Use `color="purple"` (or "blue", "green", "red", "yellow", "orange") for button styling
- The Buttons plugin has built-in color classes: `button.button-default.purple`
- Read the plugin's `main.js` source code to understand how it parses buttons
- Template button syntax evolved: `command="templates:insert-template"` was an incorrect assumption; the correct syntax is `type="template" action="TemplateName"`