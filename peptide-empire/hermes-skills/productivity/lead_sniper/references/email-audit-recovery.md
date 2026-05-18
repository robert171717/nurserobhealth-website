# Email Audit & Recovery Protocol

When a wrong email/password/credential is discovered in public posts or templates, follow this recovery sequence:

## 1. Find the Scope
Search ALL locations for the bad value:
```bash
# Skills
search_files(pattern="badvalue", path="/home/robert/.hermes/skills", file_glob="*.md")

# Cron scripts  
search_files(pattern="badvalue", path="/home/robert/.hermes/cron", file_glob="*.py")

# Hermes scripts
search_files(pattern="badvalue", path="/home/robert/.hermes/scripts", file_glob="*.py")

# Peptide Empire project files
search_files(pattern="badvalue", path="/home/robert/NurseRob_PeptideEmpire", file_glob="*")

# Desktop-accessible files (user-facing)
search_files(pattern="badvalue", path="/mnt/c/Users/Robert/Desktop/Daily Brief", file_glob="*")

# Also search for the CORRECT value as a cross-check
search_files(pattern="correctvalue", path="/home/robert/.hermes/skills", file_glob="*.md")
```

## 2. Fix the Root Cause
Patch the skill template that caused the issue. **Never use placeholder values like `[nurserob@domain.com]` in cron-job templates** — agents hallucinate concrete values for placeholders. Use literal, verified values.

## 3. Delete Offending Posts
Use `xurl delete POST_ID` for each public post containing the bad value.

## 4. Post Public Correction
Tag all affected users with the correct value. Use `xurl post "@user1 @user2 Correction — correct value is X. Apologies."`

## 5. Reply Directly to Complainants
Users who complained get a direct reply with apology + correct value.

## 6. Pause Cron Jobs
Pause the cron job that generated the bad output until the fix is verified.

## 7. Verify the Fix
Search again for the bad value across all scopes to confirm zero matches.

## Real Incident (May 12, 2026)
- **Bad value:** `nurserob@proton.me` (hallucinated by deepseek-v4-flash from placeholder `[nurserob@domain.com]`)
- **Correct value:** `nurse@nurserobhealth.com`
- **Affected:** 6 X users who received public replies with the fake email
- **Root skill:** `lead_sniper` Step 5 reply template
- **Cron jobs paused:** Lead Scan Morning/Midday/Evening/Overnight (4 jobs)
- **Posts deleted:** 6
- **Correction posted:** 1 public tweet + 1 direct reply to complainant
