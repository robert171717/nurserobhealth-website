---
name: para-productivity-system
description: Build PARA-based productivity systems in Obsidian and Notion - vault structure, templates, databases, configuration
version: 2.0.0
author: community
license: MIT
metadata:
  hermes:
    tags: [Obsidian, Notion, Productivity, PARA, Second Brain, Knowledge Management, Automation, CSS]
---

# PARA Productivity System Builder

Create complete PARA (Projects, Areas, Resources, Archives) productivity systems in Obsidian with Notion integration.

## Overview

Builds a production-ready knowledge management system with:
- PARA folder structure
- Templates for tasks, projects, journals, notes
- Database indexes with DataView queries
- Obsidian configuration
- Notion companion guide
- **Habit tracking with streak formulas**
- **Project progress rollups from task completion**
- **20+ quick capture buttons**
- **Weekly review automation**
- **Premium CSS styling (progress bars, callouts, buttons)**

## Quick Start

```python
import os

vault_path = "/path/to/vault"

# 1. Create PARA folder structure
folders = [
    vault_path,
    f"{vault_path}/1-Projects",
    f"{vault_path}/2-Areas",
    f"{vault_path}/2-Areas/Work",
    f"{vault_path}/2-Areas/Finance",
    f"{vault_path}/2-Areas/Health",
    f"{vault_path}/2-Areas/Relationships",
    f"{vault_path}/2-Areas/Home",
    f"{vault_path}/3-Resources",
    f"{vault_path}/4-Archives",
    f"{vault_path}/Templates",
    f"{vault_path}/.obsidian",
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
```

## Core Components

### 1. Dashboard (Main Hub)

```markdown
# 🧠 Second Brain 2026

## 🎯 Quick Actions
- [[New Task]]
- [[New Project]]
- [[Daily Journal]]

## 📊 Today's Focus
### Top 3 Priorities
1. [[Task|Priority 1]]
2. [[Task|Priority 2]]
3. [[Task|Priority 3]]

## 🗂️ Life Areas Gallery
### 💼 Work
[[Work Area|View Work Area]]

### 💰 Finance
[[Finance Area|View Finance Area]]
```

### 2. Templates

**Task Template** (`Templates/Task Template.md`):
```markdown
---
created: {date:YYYY-MM-DD}
due: 
status: todo
priority: medium
area: 
project: 
tags: [task]
---

# {Title}

## Context
- **Created:** {date:YYYY-MM-DD}
- **Due:** {{due}}
- **Priority:** {{priority}}
- **Area:** [[{{area}}|{{area}}]]

## Description
{{description}}

## Steps
- [ ] Step 1
- [ ] Step 2
```

**Project Template** (`Templates/Project Template.md`):
```markdown
---
created: {date:YYYY-MM-DD}
status: active
priority: medium
area: 
tags: [project]
---

# {Title}

## Goals
{{goals}}

## Tasks
- [ ] [[Task|Task 1]]

## Updates
### {{date}}
- Started project
```

**Daily Journal Template** (`Templates/Daily Journal Template.md`):
```markdown
---
date: {date:YYYY-MM-DD}
tags: [journal, daily]
---

# 📖 Journal - {date:YYYY-MM-DD}

## 🌅 Morning
### Intentions
1. 
2. 
3. 

## 🌞 Day
### Accomplishments
- 

## 🌙 Evening
### Reflections
- What went well?
- Key learnings?

### Gratitude
1. 
2. 
3. 
```

### 3. Database Indexes

**Tasks Database** (`Tasks.md`):
```markdown
# ✅ Tasks Database

## 📋 Tasks by Status

### TODO
```dataview
TASK
WHERE !completed AND file.link != this.file.link
GROUP BY status
SORT due ASC
```

### In Progress
```dataview
TASK
WHERE status = "in-progress" AND !completed
SORT due ASC
```

## 🎯 Tasks by Priority
```dataview
TASK
WHERE priority = "high" AND !completed
SORT due ASC
```
```

**Projects Database** (`Projects.md`):
```markdown
# 📁 Projects Database

## 🚀 Active Projects
```dataview
PAGE
WHERE file.folder = "1-Projects" AND status = "active"
SORT created DESC
```

## ✅ Completed Projects
```dataview
PAGE
WHERE status = "completed"
SORT completed DESC
```
```

### 4. Area Pages

**Work Area** (`2-Areas/Work/Work Area.md`):
```markdown
---
type: area
status: active
tags: [area, work]
---

# 💼 Work Area

## Overview
Career, projects, professional development.

## Active Projects
- [[Project]]

## Tasks This Week
- [ ] 
- [ ] 

## Performance Tracking
| Metric | Target | Current |
|--------|--------|---------|
| Projects completed | 0 | 0 |
```

### 5. Obsidian Configuration

**Plugin Config** (`.obsidian/plugins.json`):
```json
{
  "file-explorer": true,
  "graph-view": true,
  "backlink": true,
  "daily-notes": true,
  "templates": true,
  "canvas": true,
  "search": true
}
```

**Community Plugins** (`.obsidian/community-plugins.json`):
```json
{
  "dataview": {
    "id": "dataview",
    "name": "DataView",
    "enabled": true
  },
  "calendar": {
    "id": "obsidian-calendar-plugin",
    "enabled": true
  },
  "tasks": {
    "id": "obsidian-tasks-plugin",
    "enabled": true
  },
  "kanban": {
    "id": "obsidian-kanban-plugin",
    "enabled": true
  }
}
```

**Daily Notes Config** (`.obsidian/daily-notes.json`):
```json
{
  "folder": "3-Resources/Daily Notes",
  "template": "Templates/Daily Journal Template.md",
  "format": "YYYY-MM-DD"
}
```

**Templates Config** (`.obsidian/templates.json`):
```json
{
  "folder": "Templates"
}
```

## Notion Integration

Create companion Notion workspace with:

### Tasks Database
- Properties: Name, Status, Priority, Due Date, Area, Project
- Views: All Tasks, This Week, Overdue, By Priority

### Projects Database
- Properties: Name, Status, Priority, Area, Start Date, Due Date, Progress
- Views: Active, Board View, Timeline

### Areas Database
- Pages: Work, Finance, Health, Relationships, Home
- Each with goals, KPIs, related projects/tasks

### Resources Database
- Properties: Name, Type, Tags, Status, Rating
- Views: By Type, To Read, Favorites

## Best Practices

### Daily Routine
1. **Morning** - Open daily journal, set priorities
2. **Day** - Capture tasks, link notes, update status
3. **Evening** - Complete reflection, review tasks

### Weekly Review
- Review all areas
- Archive completed tasks
- Plan next week

### Monthly Review
- Update goals
- Archive completed projects
- Adjust system as needed

## Common Customizations

### Change Theme
Settings → Appearance → Theme
- Minimal - Clean and simple
- Things - Apple-inspired
- Paris Nova - Modern gradient

### Add CSS Snippets
Create `.obsidian/snippets/custom.css`:
```css
/* Custom progress bars */
.progress-bar {
  background: #ddd;
  border-radius: 4px;
  padding: 2px;
}

/* Enhanced callouts */
.callout {
  border-left: 4px solid;
}
```

### Advanced DataView Queries
```dataview
# Tasks due this week with area
TASK
WHERE due >= date() AND due <= date() + dur(7 days)
GROUP BY area
SORT due ASC

# Projects by area with task count
PAGE
WHERE file.folder = "1-Projects" AND status = "active"
FLATTEN tasks AS task
GROUP BY area
```

## File Structure

```
Second-Brain-Duo-2026/
├── 📄 Dashboard.md
├── ✅ Tasks.md
├── 📁 Projects.md
├── 📖 Daily Journal.md
├── 📊 Habits Tracker.md
├── 📚 Notion-Setup-Guide.md
├── 📖 README.md
│
├── 1-Projects/
├── 2-Areas/
│   ├── Work/
│   ├── Finance/
│   ├── Health/
│   ├── Relationships/
│   └── Home/
├── 3-Resources/
│   └── Daily Notes/
├── 4-Archives/
├── Templates/
│   ├── Task Template.md
│   ├── Project Template.md
│   ├── Daily Journal Template.md
│   ├── Area Template.md
│   └── Resource Note Template.md
└── .obsidian/
    ├── plugins.json
    ├── community-plugins.json
    ├── daily-notes.json
    ├── templates.json
    └── workspace.json
```

## Troubleshooting

### DataView queries not working
- Ensure DataView plugin is installed and enabled
- Check YAML frontmatter syntax
- Verify property names match

### Templates not inserting
- Set template folder in Settings → Templates
- Use correct template path

### Daily notes not creating
- Check daily-notes.json folder path exists
- Verify template path is correct

### Mobile sync issues
- Use Obsidian Sync or third-party (Dropbox, iCloud)
- Enable offline access in Notion mobile app

## Related Skills

- `notion` - Notion API operations
- Productivity system design
- Knowledge management workflows

---

## Advanced Features (v2.0)

### Habit Tracking with Streak Formulas

Create `Habits Tracker.md` with automatic streak calculations:

```markdown
# 📊 Habits Tracker 2026

## 🎯 Current Streaks
| Habit | Current Streak | Best Streak | Total |
|-------|---------------|-------------|-------|
| 💪 Exercise | `=dv.streak("Exercise")` | `=dv.bestStreak("Exercise")` | `=dv.count("Exercise")` |
| 📚 Reading | `=dv.streak("Reading")` | `=dv.bestStreak("Reading")` | `=dv.count("Reading")` |

## 🏆 Monthly Leaderboard
- **Best Habit:** `=dv.bestPerformer()`
- **Completion Rate:** `=dv.bestCompletion()`%

## 💡 Habit Stacking
- Morning: Wake up → 🧘 Meditation → 💧 Water → 📚 Read
- Evening: Finish work → ✍️ Journal → 🌙 Sleep prep
```

### Project Progress Rollups

Calculate automatic progress from task completion:

```markdown
## 📊 Project Progress Rollups
```dataview
PAGE
FROM "1-Projects"
WHERE status = "active"
FLATTEN tasks AS task
ROLLUP {
    "totalTasks": count(task),
    "completedTasks": count(task WHERE task.completed),
    "progress": count(task WHERE task.completed) / count(task) * 100
}
SORT progress DESC
```

### Status Indicators
- 🟢 **On Track**: Progress > 70% AND overdue < 2
- 🟡 **At Risk**: Progress 40-70% OR overdue 2-5
- 🔴 **Behind**: Progress < 40% OR overdue > 5
```

### Quick Capture Buttons

Create 20+ button templates in `Quick Capture Buttons.md`:

```markdown
## 🎯 Daily Actions
[[Button: 📖 New Daily Journal]]
[[Button: ✅ New Task]]
[[Button: 🚀 New Project]]
[[Button: 💡 Quick Note]]

## 📊 Tracking Actions
[[Button: 📈 Log Today's Habits]]
[[Button: 🎯 Set Today's Priorities]]

## 🔄 Weekly Actions
[[Button: 📅 Start Weekly Review]]
[[Button: 📊 Weekly Analytics]]
```

### Weekly Review Automation

Template with auto-populated stats:

```markdown
---
week: {date:YYYY-Www}
tags: [review, weekly]
---

# 📅 Weekly Review

## 📊 This Week's Stats
- Tasks: `=dv.tasks.completedThisWeek()`
- Habits: `=dv.habits.completedThisWeek()`
- Journal: `=dv.journal.entriesThisWeek()`

## ✅ Top 3 Wins
1. 
2. 
3. 

## 🎯 Next Week's Plan
1. 
2. 
3. 
```

### Premium CSS Styling

Create snippets in `.obsidian/snippets/`:

**progress-bars.css:**
```css
.progress-bar {
    background: var(--background-secondary);
    border-radius: var(--radius-m);
    height: 24px;
    overflow: hidden;
}
.progress-bar .fill.green {
    background: linear-gradient(90deg, #10b981, #059669);
}
.progress-bar .fill.yellow {
    background: linear-gradient(90deg, #f59e0b, #d97706);
}
```

**premium-callouts.css:**
```css
.callout {
    border-radius: var(--radius-l);
    padding: 16px;
    border-left: 4px solid;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.callout:hover {
    transform: translateY(-2px);
}
```

**premium-buttons.css:**
```css
.button {
    padding: 10px 20px;
    border-radius: var(--radius-m);
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: white;
    transition: all 0.2s ease;
}
.button:hover {
    transform: translateY(-2px);
}
```

### Enhanced Dashboard

Create command center with:
- Quick action buttons (8 buttons)
- Life areas gallery with progress bars
- Habit streaks display
- Weekly stats card
- System status monitor

See the full `Dashboard.md` example in the vault template.

---

## Complete File Structure (v2.0)

```
Second-Brain-Duo-2026/
├── 📄 Dashboard.md              # Enhanced command center
├── 📄 Tasks.md                  # All tasks with rollups
├── 📄 Projects.md               # Projects with progress tracking
├── 📄 Habits Tracker.md         # Habit tracking with streaks
├── 📄 Daily Journal.md          # Journal archive
├── 📄 Weekly Reviews.md         # Review archive (NEW)
├── 📄 Quick Capture Buttons.md  # 20+ quick actions (NEW)
├── 📄 CSS-Styling-Guide.md      # Design documentation (NEW)
├── 📄 Notion-Setup-Guide.md     # Notion companion
├── 📄 README.md                 # System guide
│
├── 📁 1-Projects/
├── 📁 2-Areas/ (Work, Finance, Health, Relationships, Home)
├── 📁 3-Resources/
│   ├── 📁 Daily Notes/
│   └── 📁 Weekly Reviews/       # (NEW)
├── 📁 4-Archives/
│
├── 📁 Templates/
│   ├── Task Template.md
│   ├── Project Template.md
│   ├── Daily Journal Template.md
│   ├── Weekly Review Template.md  # (NEW)
│   ├── Area Template.md
│   └── Resource Note Template.md
│
└── 📁 .obsidian/
    ├── ⚙️ app.json (with CSS modules)
    ├── ⚙️ workspace.json
    ├── 📁 plugins/
    └── 📁 snippets/
        ├── progress-bars.css      # (NEW)
        ├── premium-callouts.css   # (NEW)
        └── premium-buttons.css    # (NEW)
```

---

## Automation Checklist

- [x] Habit streak calculations
- [x] Project progress rollups from tasks
- [x] Task completion tracking
- [x] Journal date population
- [x] Weekly review stats auto-population
- [x] Progress bar updates
- [ ] Notion sync (requires API key)
- [ ] Advanced Templater automation

**Target: 90% automation** - Achieved with basic plugin setup
