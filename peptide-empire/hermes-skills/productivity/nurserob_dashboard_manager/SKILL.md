---
name: nurserob_dashboard_manager
description: Custom /steer dashboard tab "NurseRob_Empire_Dashboard" — 4 widgets with live metrics, cron status, quick actions, and revenue sparklines
version: 1.7
author: Nurse Rob
---

# NurseRob Dashboard Manager v1.0

Custom `/steer` dashboard tab: **"NurseRob_Empire_Dashboard"** — live business metrics, cron job status, quick actions, and revenue trends.

## Dashboard Layout (4 Widgets)

### Widget A: LIVE METRICS PANEL (Top)
```
┌──────────────────────────────────────────────────────────┐
│  🏥 NURSE ROB PEPTIDE EMPIRE — LIVE DASHBOARD             │
│  Updated: [timestamp] | Hermes v0.11.0                    │
├──────────────────────────────────────────────────────────┤
│  👥 AUDIENCE                 💰 REVENUE (MTD)            │
│  X Followers:   [X,XXX]      Consults:    $[X,XXX] ([X]) │
│    ↑ [XX] this week          Digital:     $[XXX]   ([X]) │
│  Email List:    [XXX]        Affiliate:   $[XXX]         │
│    ↑ [XX] this week          Coaching:    $[XXX]         │
│  Discord:       [XXX]        ─────────────────────       │
│                              TOTAL:       $[X,XXX]       │
│                                                           │
│  📈 CONTENT                  🎯 LEADS                    │
│  Posts Today:   [X]/3        Hot Today:   [X] replied    │
│  This Week:     [XX]/21      Warm:        [X] in nurture │
│  Engagement:    [X.X]%       Inquiries:   [X] this week  │
│  Top Post: [title preview]                               │
│                                                           │
│  💊 PHARMACY                🔬 FDA                       │
│  Verified:      [XX]         Last Scan:   [date]         │
│  In Outreach:   [X]          Alerts:      [X]            │
│  Partners:      [X]          Critical:    [X]            │
└──────────────────────────────────────────────────────────┘
```

### Widget B: CRON JOB STATUS BOARD (Middle)
```
┌──────────────────────────────────────────────────────────┐
│  ⚙️ CRON JOB STATUS        Legend: 🟢OK 🟡DUE 🔴FAIL ⚪IDLE │
├──────────────────────────────────────────────────────────┤
│  ▸ DAILY                                                 │
│  🟢 Daily Content Generation   (7:00 AM)  Last: [time]   │
│  🟢 Schedule Morning Post      (7:55 AM)  Last: [time]   │
│  🟢 Schedule Midday Post       (11:55 AM) Last: [time]   │
│  🟢 Schedule Evening Post      (4:55 PM)  Last: [time]   │
│  🟢 Lead Scan Morning          (6:00 AM)  Last: [time]   │
│  🟢 Lead Scan Midday           (12:00 PM) Last: [time]   │
│  🟢 Lead Scan Evening          (6:00 PM)  Last: [time]   │
│  🟢 Lead Scan Overnight        (12:00 AM) Last: [time]   │
│  🟢 Lead Nurture AM            (10:00 AM) Last: [time]   │
│  🟢 Dashboard Daily Summary    (9:00 PM)  Last: [time]   │
│                                                           │
│  ▸ WEEKLY                                                │
│  🟢 FDA Weekly Scan            (Mon 8AM)  Last: [date]   │
│  🟡 Pharmacy Outreach Weekly   (Tue 10AM) Due in [X]h   │
│  🟡 Pharmacy Scout Biweekly    (Wed 9AM)  Due in [X]h   │
│  🟢 Affiliate Weekly Report    (Sun 5PM)  Last: [date]   │
│  🟢 Weekly Analytics Report    (Sun 6PM)  Last: [date]   │
│                                                           │
│  ▸ MONTHLY                                               │
│  ⚪ Monthly Content Batch      (1st 8AM)  Next: [date]   │
└──────────────────────────────────────────────────────────┘
```

Status logic: 🟢 Last run OK | 🟡 Due <24h | 🔴 Last run failed | ⚪ Idle (awaiting cycle)

### Widget C: QUICK ACTIONS (Bottom)
```
┌──────────────────────────────────────────────────────────┐
│  ⚡ QUICK ACTIONS                                         │
├──────────────────────────────────────────────────────────┤
│  [🎨 Generate Content Now]  → Loads peptide_content_op    │
│  [🔍 Scan For Leads]        → Loads lead_sniper          │
│  [🔬 FDA Scan]              → Loads fda_monitor          │
│  [📊 Weekly Report]         → Loads nurserob_analytics   │
│  [📅 Batch 30 Days]         → Loads content_batch_gen    │
│  [💊 Pharmacy Scout]        → Loads pharmacy_scout       │
│                                                           │
│  [📂 View Lead Log] [📂 Content Calendar] [📂 Reports]    │
└──────────────────────────────────────────────────────────┘
```

### Widget D: REVENUE SPARKLINE
```
  REVENUE TREND (30-Day):
  Consults:    ▁▂▁▃▄▅▄▆███  ↑  $[X,XXX]
  Digital:     ▁▁▂▂▃▃▄▅▅▆▆  ↑  $[XXX]
  Affiliate:   ▁▁▁▂▂▃▃▄▄▅▅  →  $[XXX]
```

## Workflow

### On Dashboard Load
1. Read `~/NurseRob_PeptideEmpire/dashboard/metrics.json`
2. Poll cron job statuses via cron_orchestrator
3. Render all 4 widgets with current data
4. Highlight any 🔴 items needing attention

### On Skill Completion Update
Any skill calls: `"Update dashboard: [metric] = [value]"`
Dashboard manager updates the specific field in metrics.json.

### Daily Summary (9 PM MST)
1. Compile daily stats across all categories
2. Push summary to dashboard
3. If any 🔴 items, highlight prominently
4. Validate metrics.json with `execute_code` (not terminal `python3 -c` — blocked by security scanner)
5. **Verify content file exists**: ````python glob.glob(f'{BASE}/content/$(date +%Y-%m-%d)*posts*')```` — flag as 🔴 if missing
6. **Recalculate blocker duration from scratch**: Don't trust the stored `days_blocked` or `day_of_block` values — they drift. Compute: count calendar days from blocker start date (e.g., `May 5`) through today. Cross-check against `post_log.json.get('days_blocked')` and flag any mismatch.
7. **Recompute gap analysis fresh** (do NOT trust stored `gap_analysis` which may be stale/outdated):
   ````python
   # Check last 14 days for content files — recalculate from current date
   from datetime import timedelta
   base = datetime.date.today()
   for i in range(14):
       d = (base - timedelta(days=i)).isoformat()
       found = glob.glob(f'{BASE}/content/{d}*posts*')
       if not found: print(f"GAP: {d}")
   ````
   Always report missing days based on current scan, not stored metrics.
8. Check `~/NurseRob_PeptideEmpire/content/post_log.json` for validation issues on today's posts (missing disclaimers, char limits)
9. Cross-validate cron statuses: check post_log.json posting status vs cron engine status — they diverge when downstream tools are unauthenticated
10. **Rebuild cron_status from live `hermes cron list` output** — Do NOT trust the stored `cron_status` section in metrics.json. It WILL contain stale timestamps from days earlier because cron engine timestamps are set once on job creation and only updated on actual runs. Run `hermes --accept-hooks cron list` (note: `--accept-hooks` BEFORE `cron`, not after) and rebuild the entire `cron_status` dictionary from that output. Map display names to canonical keys:
    
    **CRITICAL: Status value format** — The `status` field in each cron_status entry MUST be the canonical raw string from the `hermes cron list` output (either `"ok"` or `"error"`), extracted via regex: `m_last.group(2)`. Do NOT store display-formatted strings like `"🟢 OK"` or `"ok 👍"` — the alerts logic checks `job.get('status') != 'ok'` and formatting strings will produce false critical alerts. If you store `"🟢 OK"`, all 18 jobs will be flagged as critical because `"🟢 OK" != "ok"`.
    
    - "Daily Content Generation" → `daily.daily_content_generation`
    - "Schedule Morning Post (9AM)" → `daily.schedule_morning_post`
    - "Schedule Evening Post" → `daily.schedule_evening_post`
    - "Lead Scan Morning" → `daily.lead_scan_morning`
    - "Lead Scan Midday" → `daily.lead_scan_midday`
    - "Lead Nurture AM" → `daily.lead_nurture_am`
    - "Welcome Email Sender" → `daily.welcome_email_sender`
    - "Dashboard Daily Summary" → `daily.dashboard_daily_summary`
    - "FDA Weekly Scan" → `weekly.fda_weekly_scan`
    - "Pharmacy Outreach Weekly" → `weekly.pharmacy_outreach_weekly`
    - "Pharmacy Scout Biweekly" → `weekly.pharmacy_scout_biweekly`
    - "Affiliate Weekly Report" → `weekly.affiliate_weekly_report`
    - "Weekly Analytics Report" → `weekly.weekly_analytics_report`
    - "Nurse Rob Content Optimizer (Weekly)" → `weekly.content_optimizer_weekly`
    - "Monthly Content Batch" → `monthly.monthly_content_batch`
    - "Discord Gateway Watchdog" → `system.discord_gateway_watchdog`
    - "Empire Recovery Watchdog" → `system.empire_recovery_watchdog`
    - "Cron Error Alert" → `system.cron_error_alert`
    - "Cron Health Summary" → `system.cron_health_summary`

    Parse each block by extracting `Name:`, `Schedule:`, `Next run:`, and `Last run:` using regex or line-matching. 
    
    **Before writing, scan for duplicates**: The old metrics.json may have the same cron job appearing in multiple places (e.g., `lead_scan_midday` under both `cron_status.daily.lead_scan_midday` AND `cron_status.lead_scan_midday` as a top-level sibling). The `daily.*` key is canonical; delete any duplicate top-level sibling with the same name. Also sweep stale artifact keys like `lead_sniper_overnight`, `jobs.*`, and anything not in the canonical name list above.

11. **Recompute posts_this_week from post_log.json** — The stored `content.posts_this_week` integer drifts because it's written midway through the week and never corrected. After updating cron_status and gap analysis, count actual posts by iterating over the current week's date keys in post_log.json and tallying slots with `"POSTED"` status. For a Wednesday summary (Mon–Wed), the correct count is 6 (2×3 days). Correct the stored value if it's off — it will be.

12. **Set alerts from live lead_sniper data** — After updating cron_status and content, check `leads.lead_sniper.hot_overdue` and add a warning alert if > 0. This is the single highest-value action signal on the dashboard. Also verify `alerts.critical`, `alerts.warning`, and `alerts.good` arrays are populated with current observations — don't leave them from a previous summary.

## Metrics Data File
`~/NurseRob_PeptideEmpire/dashboard/metrics.json` — valid JSON at all times.
Fields: audience (x_followers, email_list, discord), revenue_mtd (consults, digital, affiliate, coaching), content (posts_today, posts_week, engagement_rate, top_post), leads (hot_today, hot_replied, warm_in_nurture, consult_inquiries_week), pharmacy (scouted_verified, outreach_active, needs_manual, intro_emails_sent, last_outreach, negotiating, partners_live, pipeline_note), fda (last_scan, alerts_found, critical_pending), cron_status.

### Path Discovery
The `~` in `~/NurseRob_PeptideEmpire/` resolves to `/root/` in cron context, but the actual files may be under `/home/robert/` or another user directory. The canonical path is `/home/robert/NurseRob_PeptideEmpire/` — use this directly rather than `find /home` (which times out on large directories). Only fall back to discovery if the canonical path is missing:
```bash
# Canonical path (preferred — avoids timeout):
BASE="/home/robert/NurseRob_PeptideEmpire"
# Fallback discovery (only if canonical path doesn't exist):
find /home -maxdepth 5 -name "metrics.json" -path "*/NurseRob*" 2>/dev/null
```

### Key Data File Formats (see `references/data-formats-and-paths.md` for full details)
- **post_log.json**: DICT keyed by date strings, NOT a list. Access date-keyed entries via `log.get('2026-05-14', {}).get('slots', {})` (dict of `{slot_name: slot_metadata}`). The top-level `posts` key is a separate array of most-recent posts. Slicing `post_log[-10:]` raises TypeError.
- **lead_log.json**: Single dict (most recent scan only), at `leads/lead_log.json` (NOT `dashboard/`). Historical scans are overwritten.
- **nurture_tracker.json**: LIST, not dict. At `leads/nurture_tracker.json`.
- **welcome_sent.json**: DICT with `last_run`, `sent` (array), `blocked` (array of failed email addresses), `stale_cleaned` (array of cleanup records). At `leads/welcome_sent.json`. NOT a simple `{total_sent, last_sent}` — see `references/data-formats-and-paths.md` for full structure.

## Pitfalls
- Don't over-fetch — cache metrics and update on change events
- Dashboard must render in <2 seconds
- Metrics must be actual values, not estimates (except revenue trend)
- Financial data is local only — never leaves the machine
- Keep metrics.json valid JSON — validate before writing. Use `execute_code` tool (safe) rather than `python3 -c` in terminal, which gets blocked by the security scanner (tirith) for script execution. **CRITICAL: Do NOT use `read_file`/`write_file` hermes_tools inside `execute_code` — they return line-numbered content (`"     1|{..."`) that breaks `json.loads()`.** Instead, use subprocess for raw file I/O: read with `subprocess.run(['cat', path], capture_output=True, text=True, timeout=5)`, parse with `json.loads(raw.stdout)`, then write with `subprocess.run(['tee', path], input=json.dumps(data, indent=2), text=True, timeout=5)`. The `json.load(open('...'))` approach also works for reading but `json.loads(subprocess...)` is preferred for consistency across all JSON operations.
- **subprocess glob trap**: `subprocess.run(['ls', '/path/*glob*'])` silently returns nothing when `shell=False` — the shell never expands `*`, so `ls` receives a literal `*` character and finds no file. Use Python `glob.glob('/path/*glob*')` inside `execute_code` instead, or list the directory with `subprocess.run(['ls', '-lt', dir_path])` and parse the output. The skill's `ls ~/NurseRob_PeptideEmpire/content/*$(date +%Y-%m-%d)*posts*` commands assume a real shell — translate to `glob.glob(f'{BASE}/content/*{date}*posts*')` when inside `execute_code`.
- **Cron OK ≠ Output produced**: Several jobs (content scheduling, lead replies, pharmacy emails) report "ok" from the cron engine but fail to produce output because downstream tools are unauthenticated (xurl, himalaya). Check actual output files, not just cron status.
- **Content section goes stale between scheduler runs**: When a non-content skill (e.g., lead_sniper, fda_monitor) updates metrics.json, it only touches its own section — the `content.*` fields stay frozen at whatever they were when the last content scheduler ran. This can cause the content section to reference days-old content. After any dashboard update, check `content.last_generated` against today's date. If stale, refresh content.file, content.slots, content.block_reason, content.posting_status, and content.posts_week from the current `post_log.json` and content file.
- **days_blocked counter drifts**: The stored `days_blocked` or `day_of_block` values in post_log.json and metrics.json can be off-by-one or more. They're set by different jobs at different times and never corrected. **Always recalculate from the blocker start date**: count inclusive calendar days from `block_start` (e.g., May 5) through today. Verify: if "May 5–10" = 6 days, but stored value says 7, the stored value is wrong. Recompute fresh each summary.
- **Check for gap days — recompute fresh, don't trust stored data**: Beyond today's file, scan the last 14 days dynamically (not hardcoded to April/May). Use Python `glob.glob()` inside execute_code: `glob.glob(f'{BASE}/content/*{d}*posts*')` for each date. The stored `gap_analysis` field in metrics.json WILL go stale (observed: only checked through May 7 on May 10). Always rebuild gap analysis from current date.
- **Cron status timestamps go stale**: Daily cron jobs (Lead Scans, Schedule Post, Content Gen) may show `last_run` from May 7 even when you're generating a May 10 summary. This is because the cron engine sets these timestamps on creation, not on each run. Only the Dashboard Daily Summary job's timestamp updates every run. Note this caveat in the report — don't silently present stale timestamps as current.
- **lead_log.json uses UTC scan_date**: The scan_date field in lead_log.json is UTC-based, which may show the next calendar day for evening/overnight scans. Always use the entry timestamps (MST) for day attribution, not the top-level scan_date.
- **Content generated ≠ content publishable**: Even when a content file exists, individual posts may have quality issues. Always check `~/NurseRob_PeptideEmpire/content/post_log.json` for `validation_issues` on each post — missing disclaimers, character limit violations, or other blockers that would prevent publishing even if xurl auth is fixed. Flag them in the dashboard.
- **post_log.json is a DICT, not a list**: Access via date-keyed lookup: `log.get('2026-05-04', {}).get('posts', [])`. Attempting list indexing or slicing raises TypeError. See `references/data-formats-and-paths.md` for the full structure.
- **Silent slot drop**: A scheduler cron job may report "ok" but produce NO post_log entry for its time slot (e.g., morning scheduler at 8:17 AM reports ok, but only midday/evening entries appear in post_log). Cross-reference: compare cron run times against post_log slot entries, and check the content file's filesystem timestamp (`ls -lt content/*$(date +%Y-%m-%d)*posts*`). A content file timestamp hours after the scheduler ran suggests the file didn't exist when the scheduler triggered — possibly written later by a different scheduler. Flag any slot with a cron "ok" but missing post_log entry as 🔴 SILENT DROP.
- **FDA scan output formats**: The fda_monitor cron job produces different directory states. When NO alerts found: `fda_alerts/` exists but is empty (normal). When alerts ARE found: directory contains `YYYY-MM-DD_fda_scan.md` (full scan report) + `YYYY-MM-DD_fda_response_content.md` (ready-to-post content). Distinguish: cron `ok` + empty dir = normal (no alerts), cron `ok` + files = alerts found, `cron fail` = scan broke.
- **`which` may fail in cron context**: `which xurl` / `which himalaya` may return empty even if the tools are installed — cron has a restricted PATH. Use `find /home -name "xurl" -type f` instead for tool discovery.
- **`lead_log.json` lives in `leads/` not `dashboard/`**: Path is `~/NurseRob_PeptideEmpire/leads/lead_log.json`. It contains only the most recent scan (dict, not list) — historical scans are overwritten.
- **NEVER duplicate lead entries in metrics.json**: The `lead_sniper.last_scan.entries` block in metrics.json is a design anti-pattern. It embeds the full lead_log.json entries array, creating a redundant copy that WILL drift out of sync (the 47-entry real lead_log.json vs the 46-entry stale metrics.json copy observed May 6). The dashboard metrics.json should ONLY store summary counts (`total_pipeline`, `hot_total`, `warm_total`, `cold_total`, `overdue_followups`, `hot_overdue`, `new_this_scan`). The entries array lives exclusively in `leads/lead_log.json`. When a past scan embedded the full entries array in metrics.json, strip it out and replace with `"_entries_source": "leads/lead_log.json"` — a pointer, not a copy.\n- **Check for stale top-level `lead_sniper` key in metrics.json**: Previous scans sometimes wrote a top-level `lead_sniper` object (separate from `leads.lead_sniper`) containing `last_scan`, `xurl_status`, `web_search_status`, `x_scan_status`, `discord_scan_status`, `action_items`, `dual_failure_consecutive_scans`, and sometimes the full `entries` array. This top-level duplicate is a whole stale object — check for it after every dashboard update and `del metrics['lead_sniper']` if found. The canonical location is `leads.lead_sniper` only.
- **Check for stale sibling count fields under `leads`**: Older dashboard updates sometimes wrote pipeline counts directly under `leads.*` (e.g., `leads.total_pipeline`, `leads.hot_total`, `leads.warm_total`, `leads.cold_total`, `leads.overdue_followups`, `leads.hot_overdue`) as siblings of `leads.lead_sniper`. These are NOT the same as the top-level `lead_sniper` key — they're individual count fields that duplicate the canonical data in `leads.lead_sniper`. Because they're written separately, they inevitably drift (observed May 9: `leads.total_pipeline: 48` vs `leads.lead_sniper.total_pipeline: 51`). After every dashboard update, scan for and delete these stale sibling count fields — everything under `leads` that isn't `lead_sniper`, `xurl_installed`, `xurl_authenticated`, `xurl_note`, `web_search_status`, `dual_failure_consecutive_scans`, or `note` is drift-prone cruft. The canonical pipeline counts live ONLY in `leads.lead_sniper`.
- **Blocker-resolved state lingers in multiple fields**: When a long-running blocker (e.g., xurl 401) is finally fixed, several fields throughout metrics.json preserve the old "BLOCKED" narrative unless explicitly swept:
  - `content.block_reason`, `content.blocker`, `content.setup_command`, `content.day_of_block`, `content.posting_status` — all need clearing/updating
  - `degraded_mode` — the `xurl` and `fix_primary` fields still show the old blocker
  - `_attention` — the headline blurb still says BLOCKED
  - `alerts.critical` — the xurl OAuth2 expired entry persists
  - `degraded_note`, `degraded_fix` — both reference old blocker
  - `leads.xurl_authenticated`, `leads.lead_sniper.xurl_authenticated` — set to False
  - `days_blocked` — still at the old high number
  - `audience.x_followers` — says "N/A — xurl not authenticated"
  - `lead_followup.status` — says "BLOCKED"
  **After resolving any blocker, sweep ALL of these fields.** Don't assume a single update to `content.posts_posted` is enough — the stale "blocked" language in other sections will confuse future reads.
  
  The fields to check/update on blocker resolution:
  ```python
  # After a blocker is fixed, sweep these in metrics.json:
  sweeps = [
      ('content.block_reason', None),
      ('content.blocker', None),
      ('content.setup_command', None),
      ('content.day_of_block', 0),
      ('content.posting_blocked', False),
      ('content.posting_status', '🟢 OK — posting resumed'),
      ('degraded_mode.xurl', 'OK — fixed'),
      ('degraded_mode.fix_primary', None),
      ('degraded_mode.impact', 'Resolved'),
      ('_attention', '✅ Blocker resolved'),
      ('degraded_note', 'Blocker cleared'),
      ('degraded_fix', None),
      ('leads.xurl_authenticated', True),
      ('leads.lead_sniper.xurl_authenticated', True),
      ('days_blocked', 0),
      ('audience.x_followers', 'from xurl whoami output'),
      ('lead_followup.status', '🟢 READY — awaiting email capture from replies'),  # xurl now works, update from DEGRADED
      ('lead_followup.pipeline_stalled', False),  # clear the stalled flag
      ('lead_followup.note', 'xurl authenticated. Pipeline operational.'),  # update from stale note
  ]
  # Set each path in the nested dict. Remove from alerts.critical if xurl-related.
  metrics['alerts']['critical'] = [
      a for a in metrics['alerts']['critical'] 
      if 'xurl' not in a.lower() and 'TOKEN' not in a and '401' not in a
  ]
  ```
- **post_log.json stale top-level metadata also needs sweeping on blocker resolution**: The skill's blocker sweep above covers metrics.json exhaustively, but post_log.json at `~/NurseRob_PeptideEmpire/content/post_log.json` has the exact same problem. Its top-level keys (`status`, `error`, `fix`, `last_error`, `posts[]` array with status text, `days_blocked`) all stay frozen with the old BLOCKED narrative. Observed May 12: post_log.json still showed `status: "BLOCKED — xurl 401, re-auth needed"` even though posting had been working since May 11. After any blocker resolution, also sweep post_log.json's stale top-level metadata. The date-keyed entries (e.g., `"2026-05-12": {...}`) are usually correct — it's the top-level dict keys that rot.
  
  Sweep targets in post_log.json:
  ```python
  sweeps_pl = {
      'status': 'POSTING_OK — xurl re-authenticated [date]',
      'error': 'Resolved — [description of fix]',
      'fix': None,       # clear the old fix instruction
      'last_error': None,
      'days_blocked': 0,
  }
  # Also sweep stale status text from the top-level posts[] array
  for p in log.get('posts', []):
      if 'blocked' in p.get('status', '').lower():
          p['status'] = p['status'].replace(' — blocked by auth', '') or 'READY (from previous batch)'
  ```
  Write the post_log.json back with `subprocess.run(['tee', ...])` same as metrics.json. Do not use `read_file`/`write_file` hermes_tools (they return line-numbered content).
- **Stale cron_status nested keys**: When rebuilding `cron_status` from `hermes cron list`, the old metrics.json may contain stale nested keys from previous scan runs: `lead_sniper_overnight` (flat top-level), `daily.*` (nested under `daily`), `jobs.*` (nested under `jobs`). These are artifacts — always start fresh when rebuilding cron_status, writing only the canonical job names from `hermes cron list`. See `references/cron-list-format.md` for the full job list and parsing guide.
- **Duplicate cron entries under different nesting levels**: A single cron job like `lead_scan_midday` can appear TWICE in metrics.json's cron_status — once under `daily.lead_scan_midday` (canonical) and once as a top-level sibling under `cron_status.lead_scan_midday`. This happens when different dashboard update jobs write to different paths. When rebuilding cron_status, delete any top-level sibling that matches a nested `daily.*` key name. The `daily.*` location is canonical.
- **`hermes --accept-hooks cron list` syntax**: The `--accept-hooks` flag must go BEFORE the `cron` subcommand (`hermes --accept-hooks cron list`), not after (`hermes cron list --accept-hooks` ❌). Putting it after causes a usage error because the CLI parser expects flags before positional subcommands.
- **cron_status.status value format MUST be canonical `"ok"`/`"error"` strings, not display emoji**: When parsing `hermes cron list` output, extract the raw status from the `Last run:` line using regex group on `(ok|error)` — e.g., `m_last.group(2)`. The stored metrics.json may contain stale display-format strings like `"🟢 OK"` or `"ok 👍"` from earlier dashboard versions. If you store emoji-formatted status values, the alerts logic (`job.get('status') != 'ok'`) will flag ALL jobs as critical. **Always rebuild cron_status entirely from live `hermes cron list` output — do not copy status values from the old metrics.json even as defaults.** After rebuilding, cross-validate: all 18 jobs ok → alerts.critical should be empty. If critical is non-empty despite all jobs being ok, the status format is wrong (it's comparing `"🟢 OK" != "ok"`).
- **posts_this_week drifts**: The stored `content.posts_this_week` integer is set at various points during the week and never corrected. A value of "7" after Mon–Wed should actually be "6" (2×3=6) when the week started on Monday. Recompute from post_log.json date entries each dashboard run (see step 11 in Daily Summary workflow).
- **`hermes cron list` shows jobs not tracked in stored cron_status**: The cron engine runs additional jobs beyond the 19 canonical ones mapped in the skill (e.g., `Daily Brief v14`, `GSC SEO Weekly Alert Monitor`, `Lead Pipeline - Sheets + Discord`, `Nurse Rob Empire Daily Brief`, `Internet Health Monitor`). These are delivered to Discord or origin and not local, so they don't need tracking in the dashboard's cron_status. Just note them in the report as "additional active jobs" but don't pollute cron_status with them.
- **store `posts_this_week` as integer alongside `posts_week` string**: The `content.posts_week` field is a human-readable string (`"2 posted (May 11)"`). Also store `content.posts_this_week` as a plain integer (`2`) for numerical comparisons in widget rendering.
- **Full data format reference**: See `references/data-formats-and-paths.md` for file paths, JSON structures, and the silent-slot-drop reproduction recipe.

## Quality Checklist
- [ ] All 4 widgets populated and rendering
- [ ] Cron statuses match actual job states (check output files, not just cron engine status)
- [ ] Content file for today's date actually exists on disk
- [ ] Gap check: no missing days in last 7 days of content files
- [ ] Post quality: post_log.json checked for validation issues (disclaimers, char limits)
- [ ] **Slot coverage**: Verify all expected daily slots (typically 2-3: morning + evening, sometimes with midday) appear in post_log. A missing slot with a cron "ok" = silent drop.
- [ ] **Content file timestamp**: Compare filesystem creation time against scheduler run times. Late timestamps suggest file wasn't ready when scheduler ran.
- [ ] Quick actions functional
- [ ] Metrics.json readable, writable, and validates as valid JSON (via execute_code)
- [ ] No stale data (last_updated timestamp is recent)
- [ ] 🔴 blockers correctly identified (xurl auth, himalaya config, missing files, silent drops)
- [ ] Data file paths verified (see `references/data-formats-and-paths.md` for correct paths and formats)
- [ ] **days_blocked recalculated from blocker start date** (don't trust stored value)
- [ ] **gap_analysis recomputed fresh** (don't trust stored copy — it may only cover an earlier range)
- [ ] **cron_status rebuilt from live `hermes --accept-hooks cron list`** (don't trust stored timestamps — they're stale)
- [ ] **Duplicate cron entries removed** (check for `lead_scan_midday` appearing both in `daily.*` and as top-level sibling)
- [ ] **posts_this_week recomputed from post_log.json** (stored integer drifts — recount from actual date entries)
- [ ] **Alerts populated from live data** (especially `leads.lead_sniper.hot_overdue` for warning)
- [ ] **Alert count cross-validated**: After writing alerts, verify `alerts.critical` is sane. If all 18 cron jobs are ok but `alerts.critical` is non-empty, the cron_status status values likely have display-format strings (`"🟢 OK"`) instead of canonical `"ok"` — fix the cron_status rebuild, not the alerts.
