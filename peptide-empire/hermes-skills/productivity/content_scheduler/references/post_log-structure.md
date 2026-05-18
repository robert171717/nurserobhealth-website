# post_log.json — Full Schema Reference

`~/NurseRob_PeptideEmpire/content/post_log.json`

This file is a date-keyed **dict** (NOT a flat array). Access via `log.get("2026-05-12", {}).get("slots", {})`.

## Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | ISO date of most recent entry (e.g. `"2026-05-12"`) |
| `status` | string | Overall status string (e.g. `"POSTED_FULLY"`) |
| `error` | string | Last error message (used by blocked-state to show fix instructions) |
| `fix` | string | Fix command shown in blocked-state reports |
| `credentials_source` | string | URL for X developer portal credentials |
| `content_ready` | boolean | Whether content file existed on last check |
| `content_file` | string | Path to today's content file |
| `desktop_file` | string | Windows-side path (for cross-referencing) |
| `posts_generated` | integer | Total posts in content file |
| `posts` | list | *Legacy* — flat array of old post entries (from early versions before date-keyed nesting) |
| `last_error` | string | Most recent error message |
| `days_blocked` | integer | Consecutive days posting was blocked |
| `"YYYY-MM-DD"` | dict | Per-date entry (see below) — **multiple date keys coexist** |

## Per-Date Entry Fields

Keyed by ISO date string, e.g. `"2026-05-12"`.

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | ISO date |
| `day` | string | Day of week (e.g. `"Tuesday"`) |
| `mix` | string | Content mix description (e.g. `"Educational Thread + Short Form"`) |
| `status` | string | Overall status for that date (e.g. `"POSTED_FULLY"`, `"POSTED_MORNING_READY_EVENING"`, `"CONTENT_READY_AUTH_BLOCKED"`) |
| `reason` | string | Human-readable reason for current status |
| `posts_generated` | integer | Total posts generated for this date |
| `posts_posted` | integer | Total posts successfully posted |
| `auth_status` | string | Auth state at time of run (e.g. `"Authenticated (nurse-rob app)"`) |
| `content_file` | string | Path to content file |
| `desktop_file` | string | Windows-side path |
| `last_attempt` | string | ISO datetime of last attempt (e.g. `"2026-05-12T16:56:36-07:00"`) |
| `days_blocked` | integer | (optional) days_blocked at that date |
| `last_error` | string | (optional) last error at that date |
| `blocks_cleared` | boolean | (optional) true if this date resolved a blocker |
| `slots` | dict | Per-slot entries (see below) — keys: `morning`, `midday`, `evening` |

## Per-Slot Entry Fields

| Field | Type | Description |
|-------|------|-------------|
| `slot` | string | Slot name: `"morning"`, `"midday"`, `"evening"` |
| `time` | string | Scheduled time (e.g. `"2026-05-12T09:00:00-07:00"`) |
| `platform` | string | Platform (always `"x"`) |
| `content_type` | string | Type: `"thread"`, `"short_form"`, `"engagement"`, `"poll"`, `"short"` |
| `title` | string | Post title |
| `status` | string | Status: `"POSTED"`, `"READY — waiting on 5PM posting cron"`, `"READY — blocked by auth"`, `"FAILED — auth 401"` |
| `validation` | string | Validation result string (e.g. `"PASSED — 268 chars, RN credential in first sentence, compact disclaimer present"`) |
| `attempted_at` | string | ISO datetime when last attempted |
| `post_id` | string | (only when POSTED) X tweet ID |
| `url` | string | (only when POSTED) Full X URL |
| `tweet_count` | integer | (only when POSTED) Number of tweets in the thread |
| `posted_at` | string | (only when POSTED) ISO datetime of actual post |

## Access Pattern (Python / execute_code)

```python
import json, subprocess

LOG_PATH = "/home/robert/NurseRob_PeptideEmpire/content/post_log.json"
r = subprocess.run(["cat", LOG_PATH], capture_output=True, text=True)
log = json.loads(r.stdout)

# Get a specific date
today = "2026-05-12"
day_entry = log.get(today, {})
slots = day_entry.get("slots", {})

# Check morning post
morning = slots.get("morning", {})
if morning.get("status") == "POSTED":
    print(f"Morning posted: {morning['url']}")

# Check if a slot is empty
evening = slots.get("evening", {})
if not evening:
    print("Evening slot missing entirely")
