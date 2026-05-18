#!/usr/bin/env python3
"""Cron Health Summary — twice-daily dashboard of all Nurse Rob Empire cron jobs.

Format parsed from `hermes cron list`:
  31d78cdb31c7 [active]
    Name:      Daily Content Generation
    Schedule:  0 7 * * *
    ...
    Last run:  2026-05-11T12:07:02.815494-07:00  ok

Runs: 9AM + 9PM MST via cron (no_agent=true)
Behavior: Always outputs a full health dashboard
"""

import subprocess
import sys
import re
from datetime import datetime, timezone, timedelta
from collections import Counter

MST = timezone(timedelta(hours=-7))

EXCLUDED_JOB_IDS = {
    "699fe4c70e62",  # Discord Gateway Watchdog (system job)
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
        print(f"❌ Cron Health Summary: failed to run `hermes cron list`: {e}")
        sys.exit(1)


def parse_jobs(raw_output: str) -> list[dict]:
    """Parse block-format cron list into structured job records."""
    jobs = []
    current = None
    
    for line in raw_output.split('\n'):
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
        
        name_match = re.match(r'\s+Name:\s+(.+)', line)
        if name_match:
            current["name"] = name_match.group(1).strip()
            continue
        
        sched_match = re.match(r'\s+Schedule:\s+(.+)', line)
        if sched_match:
            current["schedule"] = sched_match.group(1).strip()
            continue
        
        last_match = re.match(r'\s+Last run:\s+(\S+)\s+(\w+)', line)
        if last_match:
            current["last_run"] = last_match.group(1)
            current["status"] = last_match.group(2)
            continue
        
        next_match = re.match(r'\s+Next run:\s+(\S+)', line)
        if next_match:
            current["next_run"] = next_match.group(1)
            continue
    
    if current:
        jobs.append(current)
    
    return jobs


def parse_timestamp(ts_str: str):
    if not ts_str:
        return None
    try:
        return datetime.fromisoformat(ts_str)
    except ValueError:
        try:
            return datetime.fromisoformat(ts_str).replace(tzinfo=MST)
        except ValueError:
            return None


def fmt_ts(ts_str: str) -> str:
    """Format ISO timestamp to human-readable."""
    dt = parse_timestamp(ts_str)
    if not dt:
        return "never"
    now = datetime.now(MST).replace(tzinfo=None)
    age = now - dt.replace(tzinfo=None)
    if age < timedelta(hours=1):
        return f"{int(age.total_seconds() // 60)}m ago"
    elif age < timedelta(hours=24):
        return f"{int(age.total_seconds() // 3600)}h ago"
    else:
        return dt.strftime("%m/%d %H:%M")


def main():
    raw = run_cron_list()
    jobs = parse_jobs(raw)
    
    # Filter out excluded system jobs
    jobs = [j for j in jobs if j["id"] not in EXCLUDED_JOB_IDS]
    
    now_aware = datetime.now(MST)
    now = now_aware.replace(tzinfo=None)
    now_str = now_aware.strftime("%Y-%m-%d %H:%M MST")
    time_of_day = "🌅 Morning" if now_aware.hour < 12 else "🌙 Evening"
    
    total = len(jobs)
    statuses = Counter(j["status"] for j in jobs)
    ok_count = statuses.get("ok", 0)
    error_count = statuses.get("error", 0)
    unknown_count = statuses.get("unknown", 0)
    
    health_pct = round(ok_count / total * 100) if total > 0 else 0
    
    active_24h = 0
    for j in jobs:
        if j["last_run"]:
            last = parse_timestamp(j["last_run"])
            if last:
                age = now - last.replace(tzinfo=None)
                if age < timedelta(hours=24):
                    active_24h += 1
    
    if error_count == 0:
        overall = "🟢 HEALTHY"
    elif error_count <= 2:
        overall = "🟡 DEGRADED"
    else:
        overall = "🔴 CRITICAL"
    
    print(f"```")
    print(f"╔══════════════════════════════════════╗")
    print(f"║   🏥 CRON HEALTH SUMMARY            ║")
    print(f"║   {time_of_day} Report              ║")
    print(f"║   {now_str}                   ║")
    print(f"╠══════════════════════════════════════╣")
    print(f"║                                      ║")
    print(f"║   Overall: {overall:<24}║")
    print(f"║   Health:  {health_pct}% ({ok_count}/{total} jobs OK)    ║")
    print(f"║                                      ║")
    print(f"║   🟢 OK:       {ok_count:<3}                  ║")
    print(f"║   🔴 Errors:   {error_count:<3}                  ║")
    print(f"║   ⚪ Unknown:  {unknown_count:<3}                  ║")
    print(f"║   ⚡ Active:    {active_24h:<3} (last 24h)        ║")
    print(f"╚══════════════════════════════════════╝")
    print(f"```")
    
    print(f"\n**Job Status Detail:**\n")
    print(f"| Status | Job | Schedule | Last Run |")
    print(f"|--------|-----|----------|----------|")
    
    sorted_jobs = sorted(jobs, key=lambda x: (0 if x["status"] == "error" else 1, x["name"].lower()))
    
    for j in sorted_jobs:
        icon = "🔴" if j["status"] == "error" else "🟢" if j["status"] == "ok" else "⚪"
        name = j["name"][:35] if j["name"] else "unknown"
        sched = j["schedule"][:15] if j["schedule"] else "—"
        last = fmt_ts(j.get("last_run", "")) if j.get("last_run") else "never"
        print(f"| {icon} | {name} | {sched} | {last} |")
    
    if error_count > 0:
        print(f"\n⚠️ **Jobs in ERROR state:**")
        for j in sorted_jobs:
            if j["status"] == "error":
                print(f"   • {j['name']} (`{j['id']}`)")
        print(f"\n   Empire Recovery Watchdog scans every 30 min for auto-recovery.")


if __name__ == "__main__":
    main()
