# NurseRob Data Formats & File Paths Reference

> Last verified: 2026-05-04. These quirks were discovered during dashboard summary runs.

## File Locations

| File | Expected Path (skill) | Actual Path | Notes |
|------|----------------------|-------------|-------|
| metrics.json | `~/NurseRob_PeptideEmpire/dashboard/metrics.json` | `/home/robert/NurseRob_PeptideEmpire/dashboard/metrics.json` | `~` resolves to `/root/` in cron context; actual user is `robert` |
| post_log.json | `~/NurseRob_PeptideEmpire/content/post_log.json` | `/home/robert/NurseRob_PeptideEmpire/content/post_log.json` | Same tilde issue |
| lead_log.json | (not specified in skill) | `/home/robert/NurseRob_PeptideEmpire/leads/lead_log.json` | NOT in `dashboard/` directory |
| nurture_tracker.json | (not specified) | `/home/robert/NurseRob_PeptideEmpire/leads/nurture_tracker.json` | — |
| welcome_sent.json | (not specified) | `/home/robert/NurseRob_PeptideEmpire/leads/welcome_sent.json` | Dict: `{last_run, sent[], blocked[], stale_cleaned[]}` |
| pharmacy_database.json | (not specified) | `/home/robert/NurseRob_PeptideEmpire/pharmacy/pharmacy_database.json` | — |
| outreach_tracker.json | (not specified) | `/home/robert/NurseRob_PeptideEmpire/pharmacy/outreach_tracker.json` | — |
| fda_alerts/ | (not specified) | `/home/robert/NurseRob_PeptideEmpire/fda_alerts/` | May be empty even when scan runs OK |
| affiliates/tracking.json | (not specified) | `/home/robert/NurseRob_PeptideEmpire/affiliates/tracking.json` | — |

**Path discovery command**: When files aren't found at expected paths, use:
```bash
# Targeted — limit depth to avoid timeout on large /home:
find /home -maxdepth 5 -name "metrics.json" -path "*/NurseRob*" 2>/dev/null

# Or bypass discovery entirely — the canonical path is stable:
BASE="/home/robert/NurseRob_PeptideEmpire"
# If the file isn't there, check /root/NurseRob_PeptideEmpire (cron tilde expansion)
```

## post_log.json Structure (DICT with MIXED Metadata + Date Keys)

**Critical**: post_log.json is a `dict` with **two kinds of keys**: (1) metadata keys at the top level (status, error, fix, posts_generated, posts, last_error, days_blocked, credentials_source, content_ready, content_file, desktop_file, date), and (2) date-string keys (`"2026-05-10"`) for per-day entries. It is **not a list**. Attempting to slice it (`post_log[-10:]`) raises `TypeError: unhashable type: 'slice'`.

**Date-keyed entries use `slots` (dict), NOT `posts` (list)**: Each date key maps to an entry with a `slots` field that is a dict of `{slot_name: slot_data}`, NOT a `posts` array. For example:
```json
"2026-05-14": {
  "date": "2026-05-14",
  "day": "Thursday",
  "mix": "Educational Thread (TB-500) + Q&A/Discussion",
  "posts_generated": 2,
  "posts_posted": 2,
  "auth_status": "OK — posted successfully",
  "slots": {
    "morning": {"slot": "morning", "time": "2026-05-14T09:00:00-07:00", "platform": "x",
      "content_type": "thread", "title": "TB-500 Educational Thread",
      "status": "POSTED — tweet-id-here",
      "validation": "PASSED (7 tweets, all ≤280 chars, RN credential, disclaimer)"},
    "evening": {...}
  }
}
```
The top-level `posts` array (a separate thing at root level) holds the 2 most recently posted entries with full metadata — it is NOT nested under date keys. Attempting `entry.get('posts', [])` on a date-keyed entry returns `[]` because the slot data lives in `entry['slots']` instead. Safe access:
```python
# Date-keyed entries use 'slots' dict, not 'posts' list
entry = log.get('2026-05-14', {})
slot_data = entry.get('slots', {})  # dict of {slot_name: slot_metadata}
for slot_name, slot_info in slot_data.items():
    print(f"{slot_name}: {slot_info.get('title')} — {slot_info.get('status')}")

# Top-level 'posts' is the recent post log (separate thing)
recent_posts = log.get('posts', [])  # list of dicts
```

```json
{
  // Top-level metadata keys (coexist with date keys)
  "date": "2026-05-10",
  "status": "BLOCKED — xurl 401, re-auth needed",
  "error": "xurl app 'default' has oauth2 token but it returns 401 — expired/revoked token",
  "fix": "Re-auth: xurl auth oauth2 --app default NurseRobHealth (opens browser for OAuth2 grant)",
  "credentials_source": "https://developer.x.com/en/portal/dashboard (min $5 API credits)",
  "content_ready": true,
  "content_file": "/home/robert/NurseRob_PeptideEmpire/content/2026-05-10_posts.md",
  "desktop_file": "/mnt/c/Users/Robert/Desktop/Daily Brief/NurseRob_PeptideEmpire/content/2026-05-10_posts.md",
  "posts_generated": 3,
  "posts": [                    // Latest posts (3 objects, the READY but unpublished ones)
    {
      "slot": "morning",
      "time": "2026-05-06T08:00:00-07:00",
      "platform": "x",
      "content_type": "thread",
      "title": "FDA Peptide Compounding Update — July 2026 PCAC Meeting",
      "status": "READY — blocked by auth",
      "likes": 0, "reposts": 0, "replies": 0, "views": 0, "impressions": 0
    }
  ],
  "last_error": "xurl auth app 'default' has oauth2 token but it returns 401 — expired/revoked token",
  "days_blocked": 7,
  
  // Date-keyed entries (sporadic — only dates with content activity)
  "2026-05-10": {
    "status": "CONTENT_READY_AUTH_BLOCKED",
    "reason": "xurl OAuth2 token on 'default' app returns 401 — expired/revoked, re-auth required",
    "date": "2026-05-10",
    "day": "Sunday",
    "mix": "Lead Magnet Promo — Wolverine Stack Calculator (thread)...",
    "posts_generated": 3,
    "posts_posted": 0,
    "auth_status": "401"
  },
  "2026-05-09": { ... },
  "2026-05-07": { ... }
}
```

**Safe access pattern**:
```python
import json, subprocess, datetime
r = subprocess.run(['cat', f'{BASE}/content/post_log.json'], capture_output=True, text=True, timeout=5)
log = json.loads(r.stdout)  # returns dict

# Access top-level metadata
blocker_status = log.get('status', 'unknown')
days_blocked = log.get('days_blocked', 0)
fix_command = log.get('fix', 'N/A')

# Access latest posts (top-level "posts" key — NOT nested under a date)
latest_posts = log.get('posts', [])
for p in latest_posts:
    print(p.get('slot'), p.get('content_type'), p.get('title')[:50])

# Access a specific date's entry — uses 'slots' dict, NOT 'posts' list
today = datetime.date.today().isoformat()
today_data = log.get(today, {})
slot_data = today_data.get('slots', {})  # dict of {slot_name: slot_metadata}
for slot_name, slot_info in slot_data.items():
    print(f"  {slot_name}: {slot_info.get('title')} — {slot_info.get('status')}")

# Iterate all date keys (skip metadata keys)
for key in sorted(log.keys()):
    if key.startswith('202') and len(key) == 10 and isinstance(log[key], dict):
        status = log[key].get('status', '?')
        generated = log[key].get('posts_generated', 0)
        posted = log[key].get('posts_posted', 0)
        slots = log[key].get('slots', {})
        slot_names = list(slots.keys()) if isinstance(slots, dict) else []
        print(f"  {key}: gen={generated}, posted={posted}, slots={slot_names}, status={status}")
```

**Metadata keys to expect at top level** (as of May 2026):
`date`, `status`, `error`, `fix`, `credentials_source`, `content_ready`, `content_file`, `desktop_file`, `posts_generated`, `posts` (array of latest post objects), `last_error`, `days_blocked`

## lead_log.json Structure

Lead log is a single dict (one entry for the most recent scan), NOT a list of scan entries:

```json
{
  "scan_date": "2026-05-10",
  "scan_time": "2026-05-10T19:01:00-07:00",
  "scan_type": "degraded_web_search",
  "leads_found": 51,
  "hot": 6,
  "warm": 23,
  "cold": 22,
  "replied": 0,
  "new_consults": 0,
  "entries": [
    {
      "platform": "x",
      "username": "@daniel_wilson",
      "post_url": "https://x.com/daniel_wilson",
      "question": "Asking where to buy peptides and pros/cons — directly soliciting sources",
      "classification": "hot",           // Values: "hot" | "warm" | "cold"
      "action": "needs_reply",
      "action_detail": "Cannot reply — xurl CLI not authenticated. Needs manual setup.",
      "timestamp": "2026-04-28T07:04:35Z",
      "followup_due": "2026-04-30",
      "notes": "HOT: asking 'where to buy'. Per workflow: public reply with education + disclaimer."
    },
    { ... }  // 51 total entries
  ]
}
```

**CRITICAL**: The declared counts (`hot`, `warm`, `cold`, `replied`) ARE the authoritative numbers. Do NOT recount from the `entries` array. The entries use `classification` field (values: `"hot"`, `"warm"`, `"cold"`) — NOT `temperature`. If you filter on the wrong field, you'll get 0 matches.

**Entry fields**: `platform`, `username`, `post_url`, `question`, `classification` (hot/warm/cold), `action`, `action_detail`, `timestamp`, `followup_due`, `notes`

**New fields discovered May 10**: `scan_time` (full timestamp), `scan_type` (e.g. "degraded_web_search", "scheduled_1800_mst"), `new_consults` (cumulative consult signups from leads)

Only one scan is retained — each new scan overwrites. Historical scans are lost.

## toolbox.json (Cron) May Not Exist

When running as a cron job, `which xurl` and `which himalaya` may return empty even if the tools are installed elsewhere. The cron environment has a restricted PATH. Check installation via:
```bash
# Use -maxdepth to avoid timeout on large /home:
find /home -maxdepth 5 -name "xurl" -type f 2>/dev/null
find /home -maxdepth 5 -name "himalaya" -type f 2>/dev/null
# For xurl specifically, the canonical install path is ~/.local/bin/xurl (~ resolves to user home)
ls -la /home/robert/.local/bin/xurl /home/robert/.local/node_modules/.bin/xurl
```

## subprocess glob trap

`subprocess.run(['ls', '/path/*glob*'])` with `shell=False` (the default) silently returns nothing — the shell never expands `*`, so `ls` receives a literal `*` character and finds no file matching that literal name. **All `ls` commands with wildcards in this reference assume a real shell**. When running inside `execute_code` (Python), translate to:

```python
# WRONG — silently returns empty:
subprocess.run(['ls', f'{BASE}/content/*{date}*posts*'])

# RIGHT — use Python glob:
import glob
files = glob.glob(f'{BASE}/content/*{date}*posts*')

# ALSO RIGHT — list directory and parse:
subprocess.run(['ls', '-lt', f'{BASE}/content/'], capture_output=True, text=True)
````

## Silent Slot Drop Pattern (NEW — discovered May 4)

**Symptom**: Cron engine reports "ok" for a scheduled job, but the expected output in post_log.json is missing for that time slot. The content file's filesystem timestamp is later than the job's run time.

**Example (May 4, 2026)**:
- `Schedule Morning Post` ran at 8:17 AM MST → cron: "ok"
- post_log.json had NO entry for the morning slot (only midday and evening)
- `2026-05-04_posts.md` filesystem timestamp: 12:02 PM MST (4 hours AFTER morning scheduler)
- The content file was likely created/overwritten by the midday scheduler's run

**Root cause hypothesis**: The content file didn't exist when the morning scheduler ran (it was created at 12:02 PM). Either:
1. Content generation (7:18 AM) produced the file but morning scheduler triggered before the file was fully written
2. Content generation failed silently and midday scheduler re-ran generation
3. Morning scheduler found no content file and silently skipped

**Detection checklist**:
1. Check cron run times vs content file creation time
2. Cross-reference post_log.json slot entries vs cron scheduler runs
3. If a scheduler ran but no corresponding slot appears in post_log, flag as 🔴 SILENT DROP
4. Check filesystem timestamps: `ls -lt content/*$(date +%Y-%m-%d)*posts*`

## FDA Scan Output

The FDA scan cron job (Mon 8AM) may report "ok" even when `fda_alerts/` directory is empty. An empty directory means "no alerts found" — this is normal, not a failure. Distinguish:
- **Empty directory + cron OK** = scan ran, zero alerts (normal)
- **No directory + cron OK** = scan may not have written output
- **Cron FAIL** = scan itself failed

## welcome_sent.json Structure

Not a simple `{total_sent, last_sent}` dict. Actual structure (May 2026):

```json
{
  "last_run": "2026-05-11T01:01:31Z",
  "sent": [],                    // {} or [] — list of successfully sent emails
  "blocked": [                   // Emails that were attempted but blocked
    "nurse@nurserobhealth.com",
    "mundellrobert84@gmail.com"
  ],
  "stale_cleaned": [             // Records of old/duplicate entries cleaned
    {
      "run_at": "2026-05-04T04:22:28Z",
      "ids_cleaned": [7, 9, 10, 11, 12, 13, 16],
      "emails": ["nurse@nurserobhealth.com", "mundellrobert84@gmail.com", ...]
    }
  ]
}
```

## pharmacy_database.json Structure

Path: `/home/robert/NurseRob_PeptideEmpire/pharmacy/pharmacy_database.json`

```json
{
  "scout_date": "2026-05-13",
  "regulatory_snapshot": "...",
  "fda_503b_count": 0,
  "total_found": 10,
  "verified": 10,
  "rejected": 0,
  "pharmacies": [
    {
      "name": "...",
      "address": "...",
      "phone": "...",
      "verified": true,
      "pcab_certified": true,
      "fda_registered": true,
      "licensed_states": ["AZ", "CA", ...],
      "source": "scout"
    }
  ]
}
```

Key fields: `scout_date` (last scout date), `verified` (count of verified pharmacies), `total_found` (total found including unverified), `pharmacies` (array of pharmacy objects), `fda_503b_count`, `rejected`.

## subscriber_log.json

Path: `/home/robert/NurseRob_PeptideEmpire/subscribers/subscriber_log.json`
May be absent if no real subscribers exist yet. When present, expected array of subscriber objects with email, name, signup_date, source, onboarding_stage, emails_sent, etc.

## Content File Naming Pattern

Content files follow the pattern: `YYYY-MM-DD_posts.md`
Examples: `2026-05-14_posts.md`, `2026-05-13_posts.md`

Each file contains 2-3 posts in sections. Typical patterns:
```
# Nurse Rob Content — [Day], [Date]
## Post 1: [Type] — [Title]
## Post 2: [Type] — [Title]
## Post 3: [Type] — [Title]   (optional — some days use 2-slots only)
```

Common slot configurations:
- **2-slot days** (increasingly common): morning thread + evening short form/Q&A
- **3-slot days** (original pattern): morning thread + midday poll + evening short form

Files are created by the Daily Content Generation cron (7 AM). A missing file for a date = gap day.

## Affiliate Report Naming Pattern

Affiliate reports follow: `affiliate_report_YYYY-MM-DD.md`
Path: `/home/robert/NurseRob_PeptideEmpire/affiliates/affiliate_report_YYYY-MM-DD.md`

Generated by the nurserob-affiliate-manager cron (Sun 5 PM, 1 hour before the analytics report).
Structure: Executive summary table (This Week vs Last Week vs Change), then detailed sections.

Also present: `/home/robert/NurseRob_PeptideEmpire/affiliates/tracking.json` — a metrics dict with total_affiliate_links, total_clicks_all_time, total_clicks_this_week, total_conversions, total_revenue_estimate, blockers[].

## Weekly Report Naming Pattern

Analytics reports go to: `reports/weekly_report_YYYY-MM-DD.md`
Path: `/home/robert/NurseRob_PeptideEmpire/reports/weekly_report_YYYY-MM-DD.md`

Previous reports remain in the directory for week-over-week comparison. Load via:
```python
import glob
reports = sorted(glob.glob(f'{BASE}/reports/weekly_report_*.md'), reverse=True)
last_week = reports[1] if len(reports) > 1 else None
```
