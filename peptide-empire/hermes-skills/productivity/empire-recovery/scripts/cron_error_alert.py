#!/usr/bin/env python3
"""Cron Error Alert — silent when all jobs healthy, alerts immediately on errors.

Format parsed from `hermes cron list`:
  31d78cdb31c7 [active]
    Name:      Daily Content Generation
    Schedule:  0 7 * * *
    ...
    Last run:  2026-05-11T12:07:02.815494-07:00  ok

Runs: every 30 min via cron (no_agent=true)
Behavior:
  - All jobs OK → empty stdout → SILENT (nothing delivered)
  - Errors found → outputs alert → delivered to Discord immediately
"""

import subprocess
import sys
import re
from datetime import datetime, timezone, timedelta

MST = timezone(timedelta(hours=-7))
ALERT_WINDOW_HOURS = 6

EXCLUDED_JOB_IDS = {
    "699fe4c70e62",  # Discord Gateway Watchdog (self-recovering)
    "c038d43687db",  # Empire Recovery Watchdog (this system)
}


def run_cron_list():
    try:
        result = subprocess.run(
            ["hermes", "cron", "list"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.stdout + result.stderr
    except Exception as e:
        print(f"❌ Cron Error Alert: failed to run `hermes cron list`: {e}")
        sys.exit(1)


def parse_jobs(raw_output: str) -> list[dict]:
    """Parse block-format cron list into structured job records."""
    jobs = []
    current = None
    
    for line in raw_output.split('\n'):
        # Match job ID line: "  31d78cdb31c7 [active]"
        id_match = re.match(r'\s+([a-f0-9]{12})\s+\[(\w+)\]', line)
        if id_match:
            if current:
                jobs.append(current)
            current = {
                "id": id_match.group(1),
                "state": id_match.group(2),
                "name": "",
                "status": "unknown",
                "last_run": None,
                "next_run": None,
                "schedule": "",
            }
            continue
        
        if not current:
            continue
        
        # Name:      Daily Content Generation
        name_match = re.match(r'\s+Name:\s+(.+)', line)
        if name_match:
            current["name"] = name_match.group(1).strip()
            continue
        
        # Schedule:  0 7 * * *
        sched_match = re.match(r'\s+Schedule:\s+(.+)', line)
        if sched_match:
            current["schedule"] = sched_match.group(1).strip()
            continue
        
        # Last run:  2026-05-11T12:07:02.815494-07:00  ok
        last_match = re.match(r'\s+Last run:\s+(\S+)\s+(\w+)', line)
        if last_match:
            current["last_run"] = last_match.group(1)
            current["status"] = last_match.group(2)
            continue
        
        # Next run:  2026-05-12T07:00:00-07:00
        next_match = re.match(r'\s+Next run:\s+(\S+)', line)
        if next_match:
            current["next_run"] = next_match.group(1)
            continue
    
    if current:
        jobs.append(current)
    
    return jobs


def parse_timestamp(ts_str: str):
    """Parse ISO timestamp, handling optional timezone."""
    if not ts_str:
        return None
    try:
        return datetime.fromisoformat(ts_str)
    except ValueError:
        try:
            return datetime.fromisoformat(ts_str).replace(tzinfo=MST)
        except ValueError:
            return None


def is_recent_error(job: dict) -> bool:
    """Check if job errored within ALERT_WINDOW_HOURS."""
    if job["status"] != "error":
        return False
    if not job["last_run"]:
        return True
    
    last = parse_timestamp(job["last_run"])
    if not last:
        return True
    
    now = datetime.now(MST)
    age = now - last
    return age < timedelta(hours=ALERT_WINDOW_HOURS)


def main():
    raw = run_cron_list()
    
    # Quick check: if "error" isn't in output at all, silent
    if "error" not in raw.lower():
        return
    
    jobs = parse_jobs(raw)
    
    # Filter: exclude system jobs, only errors within window
    error_jobs = [
        j for j in jobs
        if j["id"] not in EXCLUDED_JOB_IDS and is_recent_error(j)
    ]
    
    if not error_jobs:
        return
    
    # ── ALERT! ──
    now_str = datetime.now(MST).strftime("%Y-%m-%d %H:%M MST")
    print(f"🚨 **CRON ERROR ALERT** — {now_str}")
    print(f"   {len(error_jobs)} job(s) in error state:\n")
    for j in error_jobs:
        last = j.get("last_run", "unknown")
        print(f"   🔴 **{j['name']}**")
        print(f"      ID: `{j['id']}`")
        print(f"      Schedule: {j.get('schedule', 'unknown')}")
        print(f"      Last run: {last}")
        print()
    print("   ⚡ Empire Recovery Watchdog will attempt auto-recovery.")
    print("   Check with: `hermes cron list`")


if __name__ == "__main__":
    main()
