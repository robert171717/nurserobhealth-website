---
description: Build production-ready Obsidian vaults with PARA structure, automation, premium design, and complete documentation
name: obsidian-vault-builder
version: 2.1
created: 2026-04-06
updated: 2026-05-13
tags: [obsidian, productivity, para, automation, bases, buttons]
---

# Obsidian Vault Builder

> Build production-ready Obsidian vaults with PARA structure, automation, premium design, and complete documentation.

---

## Trigger Conditions

Use this skill when:
- Building a complete Obsidian vault from scratch
- Creating productivity/knowledge management systems
- Setting up PARA (Projects, Areas, Resources, Archives) organization
- Building automated tracking systems (habits, projects, tasks)
- Creating client-ready vaults with documentation

---

## Step-by-Step Approach

### 1. Define Vault Structure (PARA Method)

```
Second-Brain-Duo-2026/
├── 1-Projects/           # Active projects with deadlines
├── 2-Areas/              # Life domains (Work, Finance, Health, etc.)
│   ├── Work Area.md
│   ├── Finance Area.md
│   ├── Health Area.md
│   ├── Relationships Area.md
│   └── Home Area.md
├── 3-Resources/          # Knowledge base
│   ├── Daily Notes/
│   ├── Weekly Reviews/
│   ├── Book Notes/
│   └── Meeting Notes/
├── 4-Archives/           # Completed work
├── Templates/            # 6+ templates
├── .obsidian/            # Configuration
├── Dashboard.md          # Main command center
├── Tasks.md              # Task database
├── Projects.md           # Project database
├── Habits Tracker.md     # Habit tracking
└── README.md             # System overview
```

**Key insight:** Use numbered folders (1-, 2-, 3-, 4-) for guaranteed sort order.

---

### 2. Create Core Templates

#### Task Template
```markdown
---
created: <% tp.file.creation_date("YYYY-MM-DD") %>
due: 
priority: medium
status: todo
project: 
area: 
---

## 📋 Task: {{task_name}}

### Description

### Steps
- [ ] 

### Notes
```

#### Project Template
```markdown
---
created: <% tp.file.creation_date("YYYY-MM-DD") %>
due: 
priority: medium
status: active
area: 
---

## 🚀 Project: {{project_name}}

### Overview

### Goals
- 

### Tasks
```dataview
TASK
FROM this.file
WHERE !completed
SORT due ASC
```

### Progress
```dataview
TABLE 
  round(count(file.tasks WHERE completed) / count(file.tasks) * 100) as "Progress %"
FROM this.file
```

### Timeline
```

#### Daily Journal Template
```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
mood: 
energy: 
focus: 
---

## 📖 Journal - <% tp.date.now("YYYY-MM-DD") %>

### 🎯 Today's Focus

### ✅ Tasks Completed

### 📝 Notes & Reflections

### 📊 Habits
```

**Key insight:** Use Templater syntax (`<% tp.file.creation_date() %>`) for auto-populated fields.

---

### 3. Build Dataview Query Library

Create comprehensive query reference with:

#### Tasks Queries
```dataview
// All active tasks
TASK
WHERE !completed
SORT due ASC
GROUP BY priority

// Tasks due today
TASK
WHERE !completed AND due = date()
SORT priority DESC

// Overdue tasks
TASK
WHERE !completed AND due < date()
SORT due ASC
```

#### Projects Queries
```dataview
// Project progress rollup
TABLE
  round(count(file.tasks WHERE completed) / count(file.tasks) * 100) as "Progress %"
FROM "1-Projects"
WHERE status = "active"
SORT due ASC

// Active projects by area
PAGE
FROM "1-Projects"
WHERE status = "active"
GROUP BY area
```

#### Habits Queries
```dataview
// Habit streaks
TABLE
  dv.streak(habit) as "Current Streak",
  dv.bestStreak(habit) as "Best Streak"
FROM "Habits"

// Monthly completion rate
TABLE
  round(count(completed WHERE completed.month = date().month) / 30 * 100) as "Monthly Rate"
FROM "Habits"
```

**Key insight:** Document ALL queries in a dedicated `Dataview-Queries.md` file organized by category (Tasks, Projects, Habits, Journal, Areas, Calendar, Advanced).

---

### 4. Implement Automation (90% Target)

#### Habit Streak Tracking
- Use `dv.streak()` for current streak
- Use `dv.bestStreak()` for best streak
- Calculate completion rates by month/week
- Create leaderboard for top performers

#### Project Progress Rollups
- Count completed tasks vs total tasks
- Calculate percentage: `completed / total * 100`
- Add health indicators (🟢 On Track, 🟡 At Risk, 🔴 Behind)
- Display as progress bars with CSS

#### Weekly Review Automation
- Auto-populate: tasks completed, habits completed, journal entries
- Compare to previous week (↗️/↘️ indicators)
- Generate area-by-area summary
- Create scorecard (1-10 rating per area)

#### Quarterly & Annual Review Automation
- Quarterly Review Template: goals review, area deep-dives, trend analysis, strategic insights
- Annual Plan Template: yearly theme, big 3 goals with quarterly milestones, financial plan, habit system, rewards
- Create corresponding `.base` files (Quarterly Review Archive.base, Annual Plan.base) for native database views
- Add quarterly/annual buttons to Quick Capture Buttons with blue color to distinguish from daily/weekly (purple)
- Update Templates.md, Bases Index.md, Quick Capture Buttons.md links section, README.md, and Sales-Assets.md after each addition

**Key insight:** DataView's `file.tasks` to access tasks in linked files for cross-file rollups.

---

### 5. Add Premium CSS Styling

#### Progress Bars (progress-bars.css)
```css
.progress-bar {
  background: linear-gradient(90deg, #4CAF50, #8BC34A);
  height: 20px;
  border-radius: 10px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  transition: width 0.3s ease;
}
```

#### Premium Callouts (premium-callouts.css)
```css
.callout {
  border-left: 4px solid #6C63FF;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 8px;
  padding: 12px 16px;
}
```

#### Gradient Buttons (premium-buttons.css)
```css
.quick-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  cursor: pointer;
  transition: transform 0.2s;
}

.quick-btn:hover {
  transform: translateY(-2px);
}
```

**Key insight:** CSS snippets go in `.obsidian/snippets/` and are enabled via Settings → Appearance → CSS Snippets.

---

### 6. Create Quick Capture Buttons (Modern Block Syntax)

Build 20+ one-click actions using the **Buttons plugin block syntax** (fenced code blocks). This is the modern standard — do NOT use old inline-style `[Label](templater:...)` links.

```markdown
## ⚡ Quick Capture Buttons

### Daily Actions
<div class="button-group">

```button
name 📖 New Daily Journal
type templater note(Journal, tab)
action Daily Journal Template
folder 3-Resources/Daily Notes
prompt true
color purple
```

```button
name ✅ New Task
type templater note(Task, tab)
action Task Template
folder 1-Projects
prompt true
color purple
```

</div>

### Project Actions
<div class="button-group">

```button
name 🚀 New Project
type templater note(Project, tab)
action Project Template
folder 1-Projects
prompt true
color purple
```

</div>
```

**Key insight:** Use `type templater` (NOT `type template`) when the Templater community plugin is installed. The `templater` type calls Templater's engine; `template` calls the core Templates plugin. If both are available, `templater` is preferred for its richer features.

**CRITICAL pitfall:** Never use `cursorAt "Text"` — it corrupts the YAML-like block parser and prevents the button from rendering entirely. No error, no warning — the button simply shows as raw code. This parameter is NOT supported by any version of the Buttons plugin.

---

### 6.5. Add Native Obsidian Bases (.base files)

For Obsidian 1.8+, create `.base` files that provide native database views — no plugins required. This is a **product differentiator** since most vault products require Dataview.

Create a `5-Bases/` folder with one `.base` file per data domain:

| Base File | What It Queries |
|-----------|----------------|
| `Project Board.base` | Files in `1-Projects/` filtered by status/priority/area |
| `Task Inbox.base` | Task files with overdue alerts and priority grouping |
| `Resource Library.base` | Files in `3-Resources/` with tag-based filtering |
| `Area Dashboard.base` | Life areas with review status and link counts |
| `Weekly Review Archive.base` | Reviews in `3-Resources/Weekly Reviews/` |
| `Daily Journal.base` | Daily notes with calendar-style views |

Each `.base` file is YAML with filters, formulas, properties, summaries, and views. See `references/obsidian-bases-pattern.md` for full patterns, formula recipes, and verification commands.

Also create a `5-Bases/Bases Index.md` explaining the template → base mapping and linking each base from the Dashboard Quick Links.

**Key insight:** `.base` files query the same frontmatter properties defined in your templates. When a buyer creates a note from a template, it automatically appears in the corresponding base — zero configuration.

#### Setup Guide
10-section guide covering:
- Introduction
- What you'll get
- Prerequisites
- Installation (step-by-step)
- First Steps (Day 1-3)
- Core Features
- Daily Workflow
- Weekly Review
- Troubleshooting
- Resources

#### Plugin Guide
- Core 5: DataView, Templater, Calendar, Tasks, Kanban
- Productivity: Calendar for Tasks, Reminder, QuickAdd
- Visual: CSS Snippets, Style Settings
- Installation guide with configuration tips

#### Query Reference
- Organized by category
- Copy-paste ready
- Includes common filters, sorts, groups
- Advanced queries section

**Key insight:** Create `Setup-Guide.md` in PDF-ready format for client delivery.

---

## Pitfalls & Solutions

### Pitfall 1: DataView Not Working
**Problem:** Queries show errors or don't display
**Solution:**
1. Verify DataView is installed and enabled
2. Check query syntax
3. Restart Obsidian
4. Ensure files are in correct folders

### Pitfall 2: Templates Not Populating
**Problem:** Templater variables don't insert
**Solution:**
1. Verify Templater is enabled
2. Set templates folder in Settings → Templater
3. Use correct syntax: `<% tp.file.title %>`
4. Check hotkey binding (default: Ctrl+Alt+T)

### Pitfall 3: CSS Not Applying
**Problem:** Progress bars, buttons not styled
**Solution:**
1. Settings → Appearance → CSS Snippets
2. Click refresh button (⟳)
3. Toggle on desired snippets
4. Restart Obsidian if needed

### Pitfall 4: Links Breaking
**Problem:** Internal links show as broken (red)
**Solution:**
1. Use wiki links: `[[File Name]]`
2. Check spelling matches exactly
3. Use full path if needed: `[[1-Projects/Project Name|Project Name]]`
4. File must exist first

### Pitfall 5: Buttons Render But Do Nothing
**Problem:** Buttons look correct but clicking does nothing
**Solution:**
1. `type templater` uses Templater community plugin; `type template` uses core Templates plugin. Both are valid — choose based on which engine you want. If Templater is installed, `templater` is preferred.
2. Verify Buttons plugin is enabled
3. Check `action` matches exact template name (no `.md`)
4. Restart Obsidian after syntax changes
5. **CRITICAL:** `cursorAt "Text"` silently breaks the entire button block — button won't render at all. Remove any `cursorAt` lines.

### Pitfall 6: Dataview Queries Fail Silently
**Problem:** Dataview queries show errors or blank
**Solution:**
1. Ensure `dataview` is in `.obsidian/community-plugins.json`
2. Install Dataview plugin in Obsidian
3. Enable plugin in Settings → Community plugins
4. Restart Obsidian (close and reopen, not just reload)

### Pitfall 7: Template References Broken
**Problem:** Buttons reference non-existent templates
**Solution:**
1. Scan all files for `action` values
2. Verify each template exists in Templates/ folder
3. Replace placeholder names like "Template Name"
4. Use `execute_code` to audit all references

### Pitfall 8: obsidian:// URLs Fail
**Problem:** Links using `obsidian://open?vault=...&file=...` don't work
**Solution:**
1. Avoid `obsidian://` URLs for internal navigation
2. Use simple folder names: `4-Archives` instead of `obsidian://...&file=4-Archives`
3. Use wiki links for file navigation: `[[File Name]]`

### Pitfall 10: Cross-Reference Drift After Adding Content
**Problem:** After adding new templates, bases, or guides, the index files (Templates.md, Bases Index.md, Quick Capture Buttons footer, README.md, Sales-Assets.md) become stale — missing new entries, wrong counts, outdated version numbers.
**Solution:** After ANY content addition, update ALL of these files in a single pass:
1. `Templates.md` — add new template to table, update Quick Links
2. `5-Bases/Bases Index.md` — add new base to Available Bases table + Template → Base Mapping table
3. `Quick Capture Buttons.md` — add new buttons section, update templates list, Quick Links footer, version
4. `README.md` — update vault structure tree, System Status table (counts), Roadmap, version, date
5. `Sales-Assets.md` — update bullet points (template/base counts, feature mentions), version
**Pattern:** Batch all cross-reference updates immediately after content creation so nothing ships with stale numbers. This is a product shipping to customers — every number must be accurate.
**Problem:** `type link` buttons do nothing when pointing to folders (e.g., `action 3-Resources`)
**Root cause:** Buttons plugin can only open files, not folders
**Solution:**
1. Create an index file in the folder (e.g., `3-Resources/3-Resources Index.md`)
2. Update button to point to the file: `action 3-Resources/3-Resources Index`
3. Include quick actions and navigation in the index file
**Pattern:** Always verify button `action` values point to `.md` files, not directories

---

## Verification Steps

After building vault:

1. **Test DataView:**
   - Open `Dataview-Queries.md`
   - Run sample queries
   - Verify results appear

2. **Test Templater:**
   - Insert template via hotkey
   - Check auto-populated fields (date, filename)
   - Verify variables work

3. **Test CSS:**
   - Open page with progress bars
   - Verify gradient fills
   - Check button hover states

4. **Test Workflow:**
   - Create new task
   - Link to project
   - Mark task complete
   - Verify project progress updates

5. **Test Mobile:**
   - Open vault on mobile
   - Verify all features work
   - Check CSS responsiveness

---

## File Checklist

### Core Files (Must Have)
- [ ] `Dashboard.md` - Main command center
- [ ] `Tasks.md` - Task database
- [ ] `Projects.md` - Project database
- [ ] `Habits Tracker.md` - Habit tracking
- [ ] `README.md` - System overview
- [ ] `Setup-Guide.md` - Installation guide

### Templates (8 Minimum)
- [ ] `Templates/Task Template.md`
- [ ] `Templates/Project Template.md`
- [ ] `Templates/Daily Journal Template.md`
- [ ] `Templates/Weekly Review Template.md`
- [ ] `Templates/Quarterly Review Template.md`
- [ ] `Templates/Annual Plan Template.md`
- [ ] `Templates/Area Template.md`
- [ ] `Templates/Resource Note Template.md`

### Area Pages (5 Standard)
- [ ] `2-Areas/Work Area.md`
- [ ] `2-Areas/Finance Area.md`
- [ ] `2-Areas/Health Area.md`
- [ ] `2-Areas/Relationships Area.md`
- [ ] `2-Areas/Home Area.md`

### Guides (Complete Documentation)
- [ ] `Dataview-Queries.md` - Query library
- [ ] `Recommended-Plugins.md` - Plugin guide
- [ ] `CSS-Styling-Guide.md` - Customization guide
- [ ] `AI-Powered-Search.md` - Local AI vault search (enquire-mcp)
- [ ] `Mobile-Optimization-Guide.md` - Phone setup, workflows, shortcuts
- [ ] `Notion-Setup-Guide.md` - Companion Notion workspace setup

### Native Bases (Obsidian 1.8+, 8 Minimum)
- [ ] `5-Bases/Bases Index.md` - Overview and template mapping
- [ ] `5-Bases/Project Board.base` - 3 views (table, cards, completed)
- [ ] `5-Bases/Task Inbox.base` - 3 views (all, urgent, priority cards)
- [ ] `5-Bases/Resource Library.base` - 3 views (gallery, list, recent)
- [ ] `5-Bases/Area Dashboard.base` - 2 views (cards, health table)
- [ ] `5-Bases/Weekly Review Archive.base` - 2 views (history, best weeks)
- [ ] `5-Bases/Daily Journal.base` - 3 views (calendar, this week, recent)
- [ ] `5-Bases/Quarterly Review Archive.base` - 2 views (archive, best quarters)
- [ ] `5-Bases/Annual Plan.base` - 2 views (plans, browse)

### CSS Snippets (3 Premium)
- [ ] `.obsidian/snippets/progress-bars.css`
- [ ] `.obsidian/snippets/premium-callouts.css`
- [ ] `.obsidian/snippets/premium-buttons.css`

---

## Quick Start Script

Use this Python script to scaffold vault:

```python
import os

vault_path = "Second-Brain-Duo-2026"
folders = [
    "1-Projects", "2-Areas", "3-Resources/Daily Notes",
    "3-Resources/Weekly Reviews", "4-Archives", "Templates",
    ".obsidian/snippets"
]

for folder in folders:
    os.makedirs(os.path.join(vault_path, folder), exist_ok=True)

print(f"✅ Created {vault_path} with {len(folders)} folders")
```

---

## Resources

- **PARA Method:** https://fortelabs.co/blog/para/
- **DataView Docs:** https://blacksmithgu.github.io/obsidian-dataview/
- **Templater Docs:** https://silvanite.github.io/obsidian-templater/
- **Obsidian Forum:** https://forum.obsidian.md/

---

*Skill v1.0 | Created: April 2026*
*Tested with: Obsidian 1.5+, DataView 0.5+, Templater 2.0+*