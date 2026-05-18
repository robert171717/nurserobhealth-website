---
name: bulk-identifier-update
description: System-wide find-and-replace for cross-cutting identifiers (X handles, brand names, domains, emails) across the entire Hermes ecosystem — skills, project files, website repo, email templates, cron jobs
version: 1.0
author: Nurse Rob
---

# Bulk Identifier Update v1.0

**When to use:** The user changes a handle, brand name, domain, email address, or any string that appears across multiple systems (skills, files on disk, website repo, cron jobs). You need to find every reference and replace it systematically so nothing is missed.

## Trigger conditions
- User changes X/Twitter handle, GitHub username, domain, brand name
- Any string that appears in skills + project files + website needs updating everywhere
- "Update my handle across everything" or "Change @old to @new everywhere"

## Workflow

### Step 1: Search all layers simultaneously

Run these in parallel — they target different systems:

```
# Layer 1: Skills directory
grep -rn "OLD_STRING" ~/.hermes/skills/productivity/ 2>/dev/null

# Layer 2: Project files on disk (both Linux home and Windows Desktop mount)
grep -rn "OLD_STRING" ~/NurseRob_PeptideEmpire/ 2>/dev/null
grep -rn "OLD_STRING" "/mnt/c/Users/Robert/Desktop/Daily Brief/NurseRob_PeptideEmpire/" 2>/dev/null

# Layer 3: Website repo (clone fresh if needed)
grep -rn "OLD_STRING" /path/to/website-repo/ 2>/dev/null

# Layer 4: Cron jobs
hermes cron list 2>&1 | grep -i "OLD_STRING" || echo "No cron matches"
```

### Step 2: Classify hits

Group results by:
- **Skills** — patch via `execute_code` with `patch()` or manual edit
- **Disk files** — same patching approach
- **Website** — edit file, then git commit + push (may need auth)
- **Cron jobs** — usually don't reference handles directly, but verify
- **Email templates** — check welcome_email_sender and nurserob-onboarding skills specifically

### Step 3: Batch-patch skills and disk files

Use `execute_code` for efficiency. Each file gets `patch(path, old, new, replace_all=True)`:

```python
from hermes_tools import patch

files = [
    "/path/to/skill/SKILL.md",
    "/path/to/disk/file.md",
    # ...
]
for f in files:
    patch(f, "OLD_STRING", "NEW_STRING", replace_all=True)
```

### Step 4: Update website repo

```
cd /tmp/website-repo && git pull
sed -i 's|old_string|new_string|g' index.html
git add -A && git commit -m "Update handle: OLD → NEW"
git push  # may need SSH key or gh CLI auth
```

If git push fails (no auth from WSL), tell user the one-line command to run from Windows.

### Step 5: Update Fastmail signature

Fastmail signatures are NOT manageable via himalaya CLI — they live in Fastmail's web UI.
Provide the user with exact new signature text:

```
—
Name, Credential
Role · Tagline
🌐 domain.com
𝕏 @NewHandle

⚠️ Disclaimer line.
```

### Step 6: Validate OG/link preview after deploy

After website push, validate at: https://cards-dev.twitter.com/validator
Paste the domain, click Preview Card. If image doesn't appear, wait 60s and retry (X caches aggressively).

### Step 7: Update memory

Save the new handle as a memory entry so future sessions default to it.

## Pitfalls
- **Skills abstract paths** — use `~/.hermes/skills/productivity/` not relative paths. `skill_manage` can't patch skills en masse; use direct file patching.
- **Website git auth** — WSL often lacks SSH keys and `gh` CLI. If push fails, tell user the exact commands to run from Windows terminal.
- **Cron jobs usually clean** — they reference skill names, not user handles. But always verify.
- **Two copies of project files** — check both `~/NurseRob_PeptideEmpire/` (Linux home) AND `/mnt/c/Users/Robert/Desktop/Daily Brief/NurseRob_PeptideEmpire/` (Windows Desktop mount). They may be out of sync.
- **DAILY-BRIEF.md duplicates** — often exists in both `~/Desktop/` and `~/Desktop/Daily Brief/`. Patch both.
- **OG image** — if generating PNG programmatically, make sure it's at least 300×157 (Twitter minimum) and saved as PNG (NOT SVG — Twitter doesn't render SVG for cards).

## Quality checklist
- [ ] All skills patched and verified (grep for old string returns zero results)
- [ ] All disk files patched
- [ ] Website pushed and deployed
- [ ] OG image deployed and accessible at https://domain/og-image.png
- [ ] X Card Validator shows correct preview
- [ ] Fastmail signature updated
- [ ] Memory updated with new handle
- [ ] Cron jobs verified clean
