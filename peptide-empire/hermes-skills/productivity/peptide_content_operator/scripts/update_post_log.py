#!/usr/bin/env python3
"""Append a day's content generation entry to post_log.json.

Usage: pipe a JSON day-entry to stdin. The entry is merged into the file,
preserving all existing data and updating the summary fields at the bottom.

Example:
  python3 scripts/update_post_log.py << 'EOF'
  {
    "date": "2026-05-11",
    "day": "Monday",
    "mix": "Research Thread + Poll",
    "posts_generated": 2,
    "posts_posted": 0,
    "auth_status": "BLOCKED — xurl 401",
    "slots": {
      "morning": {
        "slot": "morning",
        "time": "2026-05-11T09:00:00-07:00",
        "platform": "x",
        "content_type": "thread",
        "title": "FDA's Peptide Pivot",
        "status": "READY — blocked by auth",
        "validation": "PASSED (10 tweets, all ≤232 chars)",
        "attempted_at": "2026-05-11T12:06:00-07:00"
      },
      "evening": {
        "slot": "evening",
        "time": "2026-05-11T17:00:00-07:00",
        "platform": "x",
        "content_type": "poll",
        "title": "Where Do You Get Your Peptide Info?",
        "status": "READY — blocked by auth",
        "validation": "PASSED (243 chars tweet + 4 poll options ≤25 chars)",
        "attempted_at": "2026-05-11T12:06:00-07:00"
      }
    },
    "content_file": "/home/robert/NurseRob_PeptideEmpire/content/2026-05-11_posts.md",
    "desktop_file": "/mnt/c/Users/Robert/Desktop/Daily Brief/NurseRob_PeptideEmpire/content/2026-05-11_posts.md",
    "last_attempt": "2026-05-11T12:06:00-07:00"
  }
  EOF

The script:
  1. Reads post_log.json from ~/NurseRob_PeptideEmpire/content/post_log.json
  2. Inserts the new day entry under its date key
  3. Updates summary fields at the bottom (last_error, days_blocked)
  4. Writes back with consistent formatting (sort_keys=False, indent=2)
  5. Prints PASS or the specific validation failure

Summary fields auto-computed:
  - days_blocked: incremented if auth_status contains BLOCKED or FAILED, else 0
  - last_error: set from the --error field if provided, or auto-derived from auth_status
"""

import json
import sys
import os
from datetime import datetime, timezone, timedelta

LOG_PATH = os.path.expanduser("~/NurseRob_PeptideEmpire/content/post_log.json")
MST = timezone(timedelta(hours=-7))


def mst_now() -> str:
    """Return current time as ISO 8601 string in MST."""
    return datetime.now(MST).strftime("%Y-%m-%dT%H:%M:%S-07:00")


def load_log(path: str) -> dict:
    """Load post_log.json, creating a minimal structure if missing."""
    if os.path.exists(path):
        try:
            with open(path) as f:
                data = json.load(f)
            if not isinstance(data, dict):
                data = {}
        except (json.JSONDecodeError, OSError):
            data = {}
    else:
        data = {}
    return data


def save_log(path: str, data: dict):
    """Write post_log.json with consistent formatting."""
    with open(path, "w") as f:
        json.dump(data, f, indent=2, sort_keys=False)
        f.write("\n")
    print(f"✅ Wrote {path} ({len(data)} top-level keys)")


def validate_entry(entry: dict) -> list[str]:
    """Validate required fields exist. Returns list of missing field names."""
    required_date = ["date", "day", "mix", "posts_generated", "slots"]
    required_slot = ["slot", "time", "platform", "content_type", "title", "status", "validation"]

    issues = []
    for field in required_date:
        if field not in entry:
            issues.append(f"missing top-level field: {field}")

    if "slots" in entry:
        for slot_name, slot_data in entry["slots"].items():
            if not isinstance(slot_data, dict):
                issues.append(f"slot '{slot_name}' is not a dict")
                continue
            for field in required_slot:
                if field not in slot_data:
                    issues.append(f"slot '{slot_name}' missing field: {field}")

    return issues


def compute_summary(data: dict) -> tuple[str, int]:
    """Compute last_error and days_blocked from all entries."""
    days_blocked = 0
    last_error = ""
    for key, val in data.items():
        if not isinstance(val, dict):
            continue
        if "date" not in val:
            continue
        auth = val.get("auth_status", "")
        reason = val.get("reason", "")
        if "401" in auth or "BLOCKED" in auth or "FAILED" in auth:
            days_blocked += 1
            if reason:
                last_error = reason
            elif auth:
                last_error = auth

    if last_error:
        # Append day count
        if "Day" not in last_error:
            last_error = f"{last_error} (Day {days_blocked} blocked)"
    return last_error, days_blocked


def main():
    entry = json.load(sys.stdin)

    issues = validate_entry(entry)
    if issues:
        print("❌ VALIDATION FAILED:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)

    date_key = entry.get("date", "")
    if not date_key:
        print("❌ No 'date' field in entry")
        sys.exit(1)

    # Set last_attempt if not provided
    if "last_attempt" not in entry:
        entry["last_attempt"] = mst_now()

    data = load_log(LOG_PATH)

    # Remove old entry for same date if it exists
    data.pop(date_key, None)

    # Insert new entry sorted among existing date entries
    # Collect non-date keys and date keys separately
    date_keys = []
    non_date_keys = []
    for k in data:
        if isinstance(data.get(k), dict) and "date" in data.get(k, {}):
            date_keys.append(k)
        else:
            non_date_keys.append(k)

    date_keys.append(date_key)
    date_keys.sort()

    # Rebuild: non-date keys first (in original order), then sorted date keys
    new_data = {}
    for k in non_date_keys:
        new_data[k] = data[k]
    for k in date_keys:
        if k == date_key:
            new_data[k] = entry
        else:
            new_data[k] = data[k]

    # Compute / update summary fields
    last_error, days_blocked = compute_summary(new_data)
    new_data["last_error"] = last_error
    new_data["days_blocked"] = days_blocked

    save_log(LOG_PATH, new_data)
    print(f"✅ post_log.json updated — {date_key}: {entry.get('mix', 'N/A')} | Days blocked: {days_blocked}")


if __name__ == "__main__":
    main()
