---
name: obsidian-buttons-fenced
description: Use the Obsidian Buttons plugin's fenced code block syntax (```button ... ```) for template insertion, note creation, and cursor control with confirmation prompts and auto-scroll.
category: note-taking
tags: [obsidian, buttons, plugin, template, cursor, fenced-syntax]
---

# Obsidian Buttons Plugin — Fenced Syntax

Use the Obsidian Buttons plugin's native fenced code block syntax. Requires the **Buttons** community plugin to be enabled.

## Syntax

```markdown
```button
name Label Text
type action
action value
prompt true
cursorAt "Heading Text"
color purple
```
```

## Parameter Reference

| Parameter | Values | Purpose |
|-----------|--------|---------|
| `name` | Any text | Button label shown to user |
| `type` | `template cursor`, `template note(Name, tab)`, `command`, `link` | What the button does |
| `action` | Template name, command ID, or URL | Target of the action |
| `prompt` | `true` | Shows confirmation dialog before executing (use for cursor-type buttons!) |
| `cursorAt` | `"Exact Heading Text"` | After template insert, scrolls to and expands this heading |
| `color` | `purple`, `blue`, `green`, `yellow`, `red`, `orange`, `gray` | Button color |
| `folder` | Path like `3-Inbox` | Where to create new notes |

## Template Insertion Patterns

### Insert at cursor (inline in current note)
```button
name 🎯 Set Priorities
type template cursor
action Daily Journal Template
prompt true
cursorAt "Top 3 Priorities"
color purple
```
- `type template cursor` — inserts template at cursor position
- `prompt true` — **always use this** to prevent accidental overwrites
- `cursorAt "Heading"` — after insertion, auto-scrolls to this section

### Create new note from template
```button
name 📝 New Journal
type template note(Daily Journal, tab)
action Daily Journal Template
folder 2-Daily
color purple
```
- `type template note(Name, tab)` — creates new note named "Daily Journal" and opens it
- `folder` — where the note is created (relative to vault root)

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| Buttons don't render at all | Ensure Buttons plugin is enabled in Settings → Community plugins |
| Clicking does nothing | Check `action` value matches an exact template name (no `.md` extension) |
| Template inserts but can't find it | Template must exist in the folder specified by Settings → Core plugins → Templates → Template folder |
| No confirmation prompt | Add `prompt true` to the button block |
| Cursor goes to top after insert | Add `cursorAt "Exact Heading Text"` matching the heading in the template |
| Heading not found after insert | The `cursorAt` value must **exactly match** the heading text, including numbers and spacing |
| Section not collapsible | `cursorAt` works best with `###` (H3) headings. H1/H2 may not collapse properly |
| **Buttons render but do nothing** | Use `type templater` NOT `type template` — common typo that breaks functionality |
| **Dataview queries not working** | Ensure `dataview` is in `.obsidian/community-plugins.json` |

## Section Name Matching

The `cursorAt` value must match the heading **exactly** as it appears in the template. Common mismatches:

- Template has `### Top Priorities` but button says `cursorAt "Top 3 Priorities"` — **won't work**
- Template has `# Top 3 Priorities` but button says `cursorAt "Top 3 Priorities"` — **won't work** (heading level differs)

**Fix:** Always verify the exact heading text in the template file before setting `cursorAt`.

## Verification Steps

1. Open the note with the button in Obsidian
2. Buttons should appear as styled clickable elements (not raw markdown)
3. Click the button — a confirmation dialog should appear if `prompt true`
4. Confirm — template should insert at cursor
5. Cursor should auto-scroll to the heading specified in `cursorAt`

## Documentation Best Practice

When documenting button parameters in your vault, include these key ones:

```markdown
**Parameters:**
- `name` — Button label
- `type` — `template cursor` (inline) or `template note(Name, tab)` (new note)
- `action` — Template name from Templates/ folder
- `prompt true` — Confirmation dialog before insert (use for cursor-type!)
- `cursorAt "Heading"` — Auto-scroll to heading after insertion
- `color` — purple, blue, green, yellow, red, orange, gray
```

## When NOT to Use Fenced Buttons

| Alternative | When to use instead |
|-------------|---------------------|
| HTML `<a href>` with CSS classes | No Buttons plugin installed — simpler, no plugin dependency |
| Templater commands | Buttons plugin broken/unavailable but Templater is active |
| DataviewJS | Dynamic, query-driven interfaces |