# Obsidian .base Files for Product Vaults

> Pattern extracted from the Second-Brain-Duo-2026 v3.0 upgrade session (May 2026).
> Source: Obsidian CEO Kepano's official `obsidian-bases` agent skill (MIT licensed).

## Why .base Files Matter for Products

Obsidian 1.8+ supports native database views via `.base` files — YAML-defined views with filters, formulas, and summaries. No plugins required. This is a **differentiator** for vault products because:

- Competitors' vaults require Dataview plugin for any database-like views
- `.base` files work out of the box — zero setup for buyers
- They're live-filtered: change a frontmatter property, view updates instantly

## Template → Base Mapping Pattern

The key insight: create `.base` files that query the same properties defined in your templates. When a buyer creates a note from a template, it auto-appears in the corresponding base.

| Template Creates | Appears In |
|-----------------|------------|
| Project Template → `1-Projects/` | Project Board.base |
| Task Template → `1-Projects/` | Task Inbox.base |
| Resource Note Template → `3-Resources/` | Resource Library.base |
| Area Template → `2-Areas/` | Area Dashboard.base |
| Weekly Review Template → `3-Resources/Weekly Reviews/` | Weekly Review Archive.base |
| Daily Journal Template → `3-Resources/Daily Notes/` | Daily Journal.base |

## Standard .base File Structure

```yaml
filters:           # Which files to include
  and:             # and/or/not logic
    - 'file.folder == "1-Projects"'
    - 'status == "active"'

formulas:          # Computed fields
  days_old: '(now() - file.ctime).days.round(0)'
  status_icon: 'if(status == "active", "🟢", if(status == "completed", "✅", "⚪"))'

properties:        # Which columns/fields to show
  file.name:
    displayName: "Name"
  formula.days_old:
    displayName: "Days Old"

summaries:         # Aggregate functions per column
  days_old: Average

views:             # One or more visualization layouts
  - type: table   # table | cards | list | map
    name: "Active Projects"
    order:
      - status
      - due
    filters:       # View-specific overrides
      and:
        - 'status != "completed"'
```

## Formula Patterns Worth Copying

```yaml
# Conditional icons
status_icon: 'if(status == "active", "🟢", if(status == "on-hold", "🟡", if(status == "completed", "✅", "⚪")))'

# Priority sort order (1=high, 2=medium, 3=low)
priority_sort: 'if(priority == "high", 1, if(priority == "medium", 2, 3))'

# Due status with alerts
due_status: 'if(due, if(date(due) < today(), "⚠️ Overdue", if(date(due) == today(), "🔴 Today", if((date(due) - today()).days <= 3, "🟡 Soon", "🟢 Upcoming"))), "—")'

# Days since creation
days_active: '(now() - file.ctime).days.round(0)'

# Staleness check
needs_review: 'if((now() - file.mtime).days > 14, "🔴 Review needed", if((now() - file.mtime).days > 7, "🟡 Due soon", "🟢 Fresh"))'

# Tag list as comma-separated
tag_list: 'file.tags.join(", ")'

# File property access
file.name, file.ctime, file.mtime, file.size, file.tags, file.links, file.folder
```

## Verification

```bash
cd vault_dir/5-Bases
python3 -c "
import yaml, os
for f in os.listdir('.'):
    if f.endswith('.base'):
        with open(f) as fh:
            data = yaml.safe_load(fh)
        views = len(data.get('views', []))
        formulas = len(data.get('formulas', {}))
        print(f'✅ {f}: {views} views, {formulas} formulas')
"
```

## Key Pitfalls

- **Duration type**: date subtraction returns Duration, not number. Access `.days` before calling `.round()`. Correct: `(date(due) - today()).days.round(0)`. Wrong: `((date(due) - today()) / 86400000).round(0)`.
- **Quoting**: YAML values with colons or special chars need quoting. Use single quotes for formula expressions.
- **Folder filters**: `file.folder == "1-Projects"` matches exactly — not subfolders. Use `file.inFolder("1-Projects")` for recursive matching.
- **The `this` keyword**: In main content, refers to the base file itself. In embedded context, refers to the embedding file. In sidebar, refers to active main content file.
