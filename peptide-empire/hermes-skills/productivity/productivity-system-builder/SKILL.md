---
name: productivity-system-builder
description: Build 90% automated Obsidian/Notion productivity systems using PARA method - templates, Dataview queries, habit tracking, progress rollups, quick capture buttons
version: 1.0
author: NurseRobHealth
tags: [obsidian, notion, para, productivity, automation, templates, dataview, habits, projects]
---

# Productivity System Builder
## Obsidian + Notion Vault Creation with PARA Method

> **Build 90% automated productivity systems in Obsidian/Notion using PARA method**

---

## 🎯 Trigger Conditions

Use this skill when user requests:
- "Build an Obsidian vault"
- "Create a productivity system"
- "Set up PARA method organization"
- "Build a second brain"
- "Create templates for tasks/projects/habits"

---

## 📋 User Context (Pre-Built)

```yaml
user: Robert (@NurseRobHealth)
location: Mesa, Arizona
os: Windows 10 + Ubuntu WSL2 NATIVE
save_path: /mnt/c/Users/Robert/Desktop/Daily Brief/
existing_vault: Second Brain Duo 2026 (34 files, 15 dirs)
preferences:
  - Clean 2026 aesthetic
  - Emoji-rich 🌸
  - Premium CSS design
  - 90% automation goals
  - Short actionable responses
```

---

## 🏗️ PARA Method Structure

```
1-Projects/        - Active goals with deadlines
2-Areas/           - Work, Finance, Health, Relationships, Home
3-Resources/       - Daily Notes, Weekly Reviews, Book Notes, Meeting Notes
4-Archives/        - Completed work
Templates/         - Task, Project, Journal, Weekly Review, Area, Resource
.obsidian/         - Plugin configs, CSS snippets
```

---

## 🚀 Build Process (Step-by-Step)

### Phase 1: Foundation

#### Step 1.1: Create Vault Structure
```python
import os

vault_path = "/mnt/c/Users/Robert/Desktop/Daily Brief/VAULT_NAME"
folders = [
    "1-Projects",
    "2-Areas/Work",
    "2-Areas/Finance",
    "2-Areas/Health",
    "2-Areas/Relationships",
    "2-Areas/Home",
    "3-Resources/Daily Notes",
    "3-Resources/Weekly Reviews",
    "3-Resources/Book Notes",
    "3-Resources/Meeting Notes",
    "4-Archives",
    "Templates",
    ".obsidian/plugins",
    ".obsidian/snippets"
]

for folder in folders:
    os.makedirs(os.path.join(vault_path, folder), exist_ok=True)
```

#### Step 1.2: Create Configuration Files

`.obsidian/community-plugins.json`:
```json
{
  "enabled": ["dataview", "templater", "calendar", "tasks", "kanban"],
  "enabledCommunity": true
}
```

#### Step 1.3: Create CSS Snippets (3 Files)

**progress-bars.css:**
```css
.progress-bar {
  background: linear-gradient(90deg, #10b981 0%, #3b82f6 100%);
  border-radius: 4px;
  height: 8px;
  width: 100px;
  transition: width 0.3s ease;
}

.progress-bar-container {
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
  height: 8px;
  width: 100px;
}
```

**premium-callouts.css:**
```css
.callout {
  border-left: 4px solid #3b82f6;
  background: rgba(59, 130, 246, 0.1);
  border-radius: 8px;
  padding: 12px 16px;
  margin: 8px 0;
}

.callout-tip { border-left-color: #10b981; background: rgba(16, 185, 129, 0.1); }
.callout-warning { border-left-color: #f59e0b; background: rgba(245, 158, 11, 0.1); }
.callout-danger { border-left-color: #ef4444; background: rgba(239, 68, 68, 0.1); }
```

**premium-buttons.css:**
```css
.button {
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.button-group {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
```

---

### Phase 2: Templates (6 Files)

#### Template 1: Task Template
```markdown
---
created: =date()
due: 
priority: [low|medium|high]
project: 
area: 
tags: [task]
---

# {{Task Name}}

## 📝 Description
{{Task description}}

## ✅ Action Steps
- [ ] Step 1
- [ ] Step 2

## 🔗 Related
- Project: [[Project Name]]
- Area: [[Area Name]]
```

#### Template 2: Project Template
```markdown
---
created: =date()
due: 
priority: [low|medium|high]
status: [active|on-hold|completed]
area: [work|finance|health|relationships|home]
tags: [project]
---

# {{Project Name}}

## 🎯 Goal
{{Project goal and success criteria}}

## 📋 Tasks
```dataview
TASK
FROM this.file.path
WHERE !completed
SORT due ASC
```

## 📊 Progress
- **Tasks:** {{completed}}/{{total}}
- **Progress:** {{progress_percentage}}%
- **Health:** 🟢 On Track | 🟡 At Risk | 🔴 Behind
```

#### Template 3: Daily Journal Template
```markdown
---
date: =date()
mood: [😔|😐|🙂|😊|🎉]
energy: [1-10]
focus: 
tags: [journal,daily]
---

# 📖 {{date}} Journal

## 🌅 Morning
### Today's Focus
1. 
2. 
3. 

### Top Priorities
- [ ] 
- [ ] 
- [ ] 

## 📝 Notes
{{Journal entries throughout day}}

## 🌙 Evening Reflection
### Accomplished
- 

### Tomorrow
- 
```

#### Template 4: Weekly Review Template
```markdown
---
week: =date().week
created: =date()
tags: [review,weekly]
---

# 📅 Weekly Review - Week {{week}}

## 📊 This Week's Stats
- **Tasks Completed:** {{count}}
- **Habits Completed:** {{count}}/{{target}}
- **Projects Progressed:** {{count}}

## ✅ Accomplishments
- 

## 🎯 Area-by-Area Review
### Work
{{Review notes}}

### Health
{{Review notes}}

## 📋 Next Week's Plan
### Top 3 Priorities
1. 
2. 
3. 

## 🏆 Scorecard
- Productivity: {{score}}/10
- Health: {{score}}/10
- Overall: {{score}}/10
```

---

### Phase 3: Database Indexes (6 Files)

#### Index 1: Dashboard.md
```markdown
# 🧠 Second Brain Duo 2026

> **Your command center. Everything at a glance.**

## ⚡ Quick Actions
<div class="button-group">
  <a class="button">✅ New Task</a>
  <a class="button">🚀 New Project</a>
  <a class="button">📖 New Journal</a>
</div>

## 🎯 Today's Focus
```dataview
TASK
WHERE !completed AND priority = "high"
LIMIT 3
```

## ✅ Active Tasks
```dataview
TASK
WHERE !completed AND due = date()
SORT priority DESC
```
```

#### Index 2: Tasks.md
```markdown
# ✅ All Tasks

## 📊 Overview
- **Pending:** {{count}}
- **Overdue:** {{count}}

## 🔥 High Priority
```dataview
TASK
WHERE !completed AND priority = "high"
SORT due ASC
```

## 📅 Due This Week
```dataview
TASK
WHERE !completed AND due >= date() AND due <= date() + dur(7 days)
SORT due ASC
```
```

#### Index 3: Projects.md
```markdown
# 🚀 All Projects

## 🎯 Active Projects
```dataview
TABLE
  status, priority, due,
  round(count(file.tasks WHERE completed) / count(file.tasks) * 100) as "Progress %"
FROM "1-Projects"
WHERE status = "active"
SORT due ASC
```

## 📈 Progress Rollup
```dataview
TABLE
  round(count(file.tasks WHERE completed) / count(file.tasks) * 100) as "Progress %"
FROM "1-Projects"
WHERE status = "active"
SORT "Progress %" DESC
```
```

#### Index 4: Habits Tracker.md
```markdown
# 📊 Habits Tracker 2026

## 🏆 Current Streaks
```dataview
TABLE
  habit,
  dv.streak(habit) as "Streak",
  count(completed WHERE completed.month = date().month) as "This Month"
FROM "Habits"
GROUP BY habit
```

## 🏅 Monthly Leaderboard
```dataview
TABLE
  habit,
  round(count(completed WHERE completed.month = date().month) / 30 * 100) as "Rate"
FROM "Habits"
GROUP BY habit
SORT "Rate" DESC
```
```

#### Index 5: Daily Journal.md
```markdown
# 📖 Journal Archive

## Recent Entries
```dataview
PAGE
FROM "3-Resources/Daily Notes"
SORT date DESC
LIMIT 7
```
```

#### Index 6: Weekly Reviews.md
```markdown
# 📅 Weekly Review Archive

## All Reviews
```dataview
PAGE
FROM "3-Resources/Weekly Reviews"
SORT created DESC
```
```

---

### Phase 4: Dataview Queries Library

Create `Dataview-Queries.md` with:

#### Tasks Queries
```dataview
// All Active Tasks
TASK WHERE !completed SORT due ASC

// Tasks Due Today
TASK WHERE !completed AND due = date()

// Tasks Due This Week
TASK WHERE !completed AND due >= date() AND due <= date() + dur(7 days)

// Overdue Tasks
TASK WHERE !completed AND due < date() SORT due ASC

// Tasks by Priority
TASK WHERE !completed GROUP BY priority

// Tasks by Area
TASK WHERE !completed GROUP BY area

// High Priority Tasks
TASK WHERE !completed AND priority = "high" SORT due ASC LIMIT 10
```

#### Projects Queries
```dataview
// Active Projects
PAGE FROM "1-Projects" WHERE status = "active" SORT due ASC

// Projects with Task Count
TABLE count(file.tasks) as "Tasks", status, priority
FROM "1-Projects" WHERE status = "active"

// Project Progress Rollup
TABLE round(count(file.tasks WHERE completed) / count(file.tasks) * 100) as "Progress %"
FROM "1-Projects" WHERE status = "active"

// Completed This Month
PAGE FROM "1-Projects" WHERE status = "completed" AND completed.month = date().month
```

#### Habits Queries
```dataview
// Habit Completion This Week
TABLE count(completed WHERE completed.week = date().week) as "This Week"
FROM "Habits" GROUP BY habit

// Habit Streak Calculation
TABLE dv.streak(habit) as "Streak", dv.bestStreak(habit) as "Best Streak"
FROM "Habits"

// Habit Completion Rate
TABLE round(count(completed WHERE completed.month = date().month) / 30 * 100) as "Rate"
FROM "Habits" GROUP BY habit
```

---

### Phase 5: Area Pages (5 Files)

#### Work Area.md
```markdown
# 💼 Work Area

## 🎯 Active Projects
```dataview
PAGE FROM "1-Projects" WHERE status = "active" AND area = "work" SORT due ASC
```

## ✅ Pending Tasks
```dataview
TASK WHERE !completed AND area = "work" SORT due ASC
```
```

(Repeat for Finance, Health, Relationships, Home)

---

### Phase 6: Quick Capture Buttons

Create `Quick Capture Buttons.md` with 20+ actions:

```markdown
# ⚡ Quick Capture Buttons

## Daily Actions
- 📖 New Journal Entry
- ✅ New Task
- 💡 Quick Note
- 📝 Log Meeting

## Project Actions
- 🚀 New Project
- 📊 Update Progress
- 🗂️ Archive Project
- 📋 Add Milestone

## Tracking Actions
- 📈 Log Habits
- 🎯 Set Priorities
- ⏰ Time Block
- 💰 Log Expense

## Weekly Actions
- 📅 Start Weekly Review
- 📊 View Analytics
- 📝 Plan Next Week
- 🏆 Update Scorecard

## System Actions
- 🧹 Cleanup Old Notes
- 🔄 Sync Vault
- 📚 Create Resource
- ⚙️ Configure Settings
```

---

## ⚡ Automation Patterns (90% Goal)

### Habit Streaks
```dataview
dv.streak(habit)  // Current streak
dv.bestStreak(habit)  // Best streak
```

### Project Progress
```dataview
round(count(file.tasks WHERE completed) / count(file.tasks) * 100)
```

### Task Completion Tracking
```dataview
count(file.tasks WHERE completed) as "Completed"
count(file.tasks) as "Total"
```

### Weekly Review Stats
```dataview
count(tasks WHERE completed AND completed.week = date().week)
```

### Progress Bars
```css
width: {{progress}}%  // Dynamic width based on completion
```

---

## 🚫 Common Pitfalls

1. **Plugin Order:** Install DataView before Tasks
2. **CSS Snippets:** Must refresh after enabling (⟳ button)
3. **Template Paths:** Use relative paths from vault root
4. **Dataview Syntax:** Check for typos in query blocks
5. **File Naming:** Use spaces or hyphens consistently

---

## ✅ Verification Checklist

After build, verify:
- [ ] All 15 directories created
- [ ] 6 templates working (test each)
- [ ] 5 area pages populated
- [ ] 6 database indexes functional
- [ ] CSS snippets enabled and working
- [ ] Dataview queries returning data
- [ ] Quick capture buttons clickable
- [ ] Habit tracking with streaks
- [ ] Project progress rollups calculating
- [ ] Weekly review template auto-populating

---

## 📊 Deliverables

**Minimum Viable Vault:**
- PARA structure (4 folders)
- 3 templates (Task, Project, Journal)
- Dashboard.md, Tasks.md, Projects.md

**Complete Vault:**
- All 6 templates
- 5 area pages
- 6 database indexes
- 3 CSS snippets
- Dataview queries library
- Quick capture buttons (20+)
- README + Setup Guide

**Premium Vault:**
- Notion companion guide
- Sales assets (video script, screenshots)
- Advanced automation scripts
- Custom CSS themes
- Mobile optimization notes

---

## 📚 Resources

- **PARA Method:** https://fortelabs.co/blog/para/
- **Obsidian Docs:** https://help.obsidian.md
- **DataView:** https://blacksmithgu.github.io/obsidian-dataview/
- **Templater:** https://silvanite.github.io/obsidian-templater/
- **Community Plugins:** https://obsidian.md/plugins

---

## 🔧 File Editing Best Practices

When editing existing markdown files in the vault:

1. **Always read current content first** - Don't assume text matches exactly
2. **Case-sensitive matching** - "90% automated" ≠ "90% Automated"
3. **Include whitespace** - Markdown formatting (spaces, newlines) matters
4. **Verify after changes** - Read file back and confirm changes applied
5. **Use exact string replacement** - Match the full context including markdown syntax

**Example:**
```python
# WRONG: Assume text is simple
content.replace("90% automated", "Highly automated")

# RIGHT: Match exact formatting including markdown
content.replace(
    "> **Notion + Obsidian PARA Vault** | Premium Productivity System | 90% Automated",
    "> **Notion + Obsidian PARA Vault** | Premium Productivity System | Highly automated with DataView + Templater"
)
```

---

*Productivity System Builder v1.1 | Last updated: April 2026*