# Nurse Rob Peptide Empire — Backup & Restore Guide
**Created: May 18, 2026 | Updated: Automatic daily**

---

## Backup System Overview

Your empire is protected by a **3-layer redundant backup system**:

| Layer | Location | Frequency | How To Restore |
|-------|----------|-----------|---------------|
| 🔴 **LOCAL** | `~/NurseRob_PeptideEmpire/backups/daily/` | Daily 2:30 AM | Copy folder back to original location |
| 🟡 **USB** | Your USB drive (when plugged in) | Daily if mounted | Copy from USB back to computer |
| 🟢 **GITHUB** | `github.com/robert171717/nurserobhealth-website` → `peptide-empire/` | Daily 2:30 AM | `git clone` then copy files |

---

## Folder Structure

```
peptide-empire/
├── hermes-skills/          ← All custom Hermes skills
│   ├── nurse-rob-x-reply-guidelines/
│   ├── peptide_content_operator/
│   ├── content-batch-generator/
│   ├── lead_sniper/
│   ├── content_scheduler/
│   └── ... (all other skills)
│
├── empire-files/           ← Core empire data
│   ├── content/
│   │   ├── master_content_rules_v1.3.md  ← THE critical file
│   │   └── YYYY-MM-DD_posts.md
│   ├── leads/
│   │   ├── lead_log.json
│   │   └── lead_dashboard.csv
│   ├── scripts/
│   │   ├── empire_backup.sh
│   │   └── sync_leads_csv.py
│   ├── dashboard/
│   │   └── metrics.json
│   ├── reports/
│   ├── pharmacy/
│   ├── affiliates/
│   └── backups/
│
├── desktop-files/          ← Desktop checklists & templates
│   ├── monetization_sprint_checklist.md
│   ├── pharmacy_contact_templates.md
│   ├── peptide_safety_quiz_funnel.md
│   └── past_post_audit_report.md
│
├── backup_log.txt          ← Latest backup log
└── BACKUP_README.md        ← This file
```

---

## How To Restore Everything

### If Your Computer Crashes (Full Restore)

1. Get a new computer with WSL2 (Ubuntu 24.04)
2. Install Hermes: `curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash`
3. Clone the repo:
   ```bash
   git clone https://github.com/robert171717/nurserobhealth-website.git ~/nurserobhealth-website
   ```
4. Restore skills:
   ```bash
   cp -r ~/nurserobhealth-website/peptide-empire/hermes-skills/* ~/.hermes/skills/
   ```
5. Restore empire files:
   ```bash
   cp -r ~/nurserobhealth-website/peptide-empire/empire-files/* ~/NurseRob_PeptideEmpire/
   ```
6. Restart Hermes: `systemctl --user restart hermes-gateway`
7. All cron jobs and automations will need to be re-created (they live in Hermes' internal database)

### If One File Gets Corrupted

```bash
# Restore a single file from backup
cp ~/NurseRob_PeptideEmpire/backups/daily/[latest-date]/empire-files/content/master_content_rules_v1.3.md \
   ~/NurseRob_PeptideEmpire/content/master_content_rules_v1.3.md
```

### If Hermes Makes a Bad Change to a Skill

```bash
# Restore from yesterday's backup
cp ~/NurseRob_PeptideEmpire/backups/daily/[yesterday-date]/hermes-skills/nurse-rob-x-reply-guidelines/SKILL.md \
   ~/.hermes/skills/social-media/nurse-rob-x-reply-guidelines/SKILL.md
```

---

## Manual Backup (USB + Google Drive)

Once a week, do a manual copy to USB and Google Drive:

1. **USB:** Plug in, copy `~/NurseRob_PeptideEmpire/` and `~/.hermes/skills/`
2. **Google Drive:** Upload same folders to `NurseRob_PeptideEmpire_Backups/`

These manual backups protect against GitHub auth failure or local corruption.

---

## Cron Job

The backup runs automatically every night at 2:30 AM MST via cron.
Check the latest backup log at: `~/NurseRob_PeptideEmpire/backups/backup_log.txt`

---

## What's NOT Backed Up (By Design)

- Hermes internal database (sessions, cron configs) — stored in `~/.hermes/` but not backed up because it can be recreated
- Large generated files — excluded to keep backups fast
- Temporary/cache files

---

*This backup system was designed for a solo RN operation. It's simple, redundant, and requires zero ongoing maintenance.*
