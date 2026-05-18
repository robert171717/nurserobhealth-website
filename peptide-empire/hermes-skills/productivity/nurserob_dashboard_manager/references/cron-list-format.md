# hermes cron list — Output Format Reference

> Verified: 2026-05-13 — 19+ Empire cron jobs active and `ok`

## Command
```bash
hermes --accept-hooks cron list
```
**Important:** `--accept-hooks` must come BEFORE `cron`, not after. 
`hermes cron list --accept-hooks` ❌ (usage error)
`hermes --accept-hooks cron list` ✅

## Output Format
Block-based (not tabular). Each job is a block of key-value lines:

```
  <job_id> [active]                                  # line 1: id + status
    Name:      <Job Display Name>                    # line 2: display name
    Schedule:  <cron expression>                     # line 3: cron schedule
    Repeat:    ∞                                     # line 4: always ∞ (infinite)
    Next run:  <ISO datetime>                        # line 5: next scheduled time
    Deliver:   local | origin                        # line 6: delivery target
    Skills:    <skill1>, <skill2>                    # line 7: comma-separated skills (or missing)
    Script:    <filename>                            # line 7b: only for no-agent jobs
    Mode:      no-agent (script stdout delivered...) # line 8: only for no-agent jobs  
    Last run:  <ISO datetime>  ok|error              # line 9: last run info
```

## Typical Job Blocks

### Agent Job (with skills)
```
  31d78cdb31c7 [active]
    Name:      Daily Content Generation
    Schedule:  0 7 * * *
    Repeat:    ∞
    Next run:  2026-05-12T07:00:00-07:00
    Deliver:   local
    Skills:    peptide_content_operator, image_generator
    Last run:  2026-05-11T12:07:02.815494-07:00  ok
```

### no-agent Script Job (no skills)
```
  43dfac2a77d8 [active]
    Name:      Cron Error Alert
    Schedule:  */30 * * * *
    Repeat:    ∞
    Next run:  2026-05-11T21:30:00-07:00
    Deliver:   origin
    Script:    cron_error_alert.py
    Mode:      no-agent (script stdout delivered directly)
    Last run:  2026-05-11T21:00:49.775769-07:00  ok
```

## Parsing Tips
- Match `\s+Name:\s+(.+)` for display name
- Match `\s+Schedule:\s+(.+)` for cron expression
- Match `\s+Last run:\s+(\S+\s+\S+)` for last_run + status (e.g., `2026-05-11T12:07:02.815494-07:00  ok`)
- Status is either `ok` or `error` after the timestamp
- Job IDs are 12-char hex strings
- `[active]` is the only status shown (paused jobs are filtered out)

## Expected Fields in cron_status from hermes cron list
When rebuilding the `cron_status` section of metrics.json, use these canonical job names: `Daily Content Generation`, `Schedule Morning Post (9AM)`, `Schedule Evening Post`, `Lead Scan Morning`, `Lead Scan Midday`, `Lead Nurture AM`, `Dashboard Daily Summary`, `FDA Weekly Scan`, `Pharmacy Outreach Weekly`, `Pharmacy Scout Biweekly`, `Affiliate Weekly Report`, `Weekly Analytics Report`, `Monthly Content Batch`, `Welcome Email Sender`, `Nurse Rob Content Optimizer (Weekly)`, `Discord Gateway Watchdog`, `Empire Recovery Watchdog`, `Cron Error Alert`, `Cron Health Summary`.

**Do NOT track these additional active jobs in cron_status** (they deliver to Discord/origin, not local dashboard):
- `Daily Brief v14` — delivers origin, not local
- `GSC SEO Weekly Alert Monitor` — delivers to Discord
- `Lead Pipeline - Sheets + Discord` — delivers to Discord
- `Nurse Rob Empire Daily Brief` — delivers to Discord
- `Internet Health Monitor` — no-agent, delivers origin

These are separately monitored. Just mention them in the report as "additional active jobs" if any are in 🔴 state.

When you rebuild cron_status from `hermes cron list` output, the old metrics.json may contain stale nested keys like:
- `lead_sniper_overnight` — a flat top-level key (no prefix)
- `daily.lead_sniper_midday` — nested under a `daily` object
- `jobs.lead_scan_midday` — nested under a `jobs` object
- `lead_scan_midday` — duplicate top-level sibling alongside `daily.lead_scan_midday`

These are artifacts from older dashboard writes that used non-standard paths. **Sweep them every time cron_status is rebuilt.** Build a fresh flat dictionary using only the canonical job names from `hermes cron list`.
