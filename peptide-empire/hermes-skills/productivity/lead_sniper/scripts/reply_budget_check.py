#!/usr/bin/env python3
"""
Lead Sniper Budget Checker — called at scan start to determine reply allowance.
Returns JSON with {allowance, tier, must_skip_usernames, alerts}.

Usage:
  python3 reply_budget_check.py [--reset-daily]
  
The --reset-daily flag resets today's counter if the date has changed.
Called automatically by the lead_sniper workflow.
"""
import json
import subprocess
import sys
from datetime import datetime, timezone, timedelta

BUDGET_FILE = '/home/robert/NurseRob_PeptideEmpire/leads/reply_budget.json'
REPLIED_USERS_FILE = '/home/robert/NurseRob_PeptideEmpire/leads/replied_users.json'
LEAD_LOG_FILE = '/home/robert/NurseRob_PeptideEmpire/leads/lead_log.json'

def load_json(path):
    try:
        raw = subprocess.run(['cat', path], capture_output=True, text=True, timeout=5)
        return json.loads(raw.stdout)
    except:
        return {}

def save_json(path, data):
    subprocess.run(['tee', path], 
                   input=json.dumps(data, indent=2), 
                   text=True, timeout=5)

def count_replies_today(budget):
    """Count replies from today from replied_users.json"""
    replied = load_json(REPLIED_USERS_FILE)
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    count = 0
    for user in replied.get('users', []):
        replied_at = user.get('replied_at', '')
        if replied_at.startswith(today):
            count += 1
    return count

def count_replies_this_month(budget):
    """Count replies this month from replied_users.json"""
    replied = load_json(REPLIED_USERS_FILE)
    this_month = datetime.now(timezone.utc).strftime('%Y-%m')
    count = 0
    for user in replied.get('users', []):
        replied_at = user.get('replied_at', '')
        if replied_at.startswith(this_month):
            count += 1
    return count

def get_lifetime_replies_per_user():
    """Return dict of username -> lifetime reply count"""
    replied = load_json(REPLIED_USERS_FILE)
    from collections import Counter
    counts = Counter()
    for user in replied.get('users', []):
        username = user.get('username', '').lstrip('@').lower()
        counts[username] += 1
    return counts

def get_used_posts_this_month():
    """Estimate POST operations this month from replied_users + content schedule."""
    # Content posts: 2/day * days elapsed
    now = datetime.now(timezone.utc)
    days_elapsed = now.day
    content_posts = days_elapsed * 2
    
    # Engagement posts (replies/mentions)
    engagement_posts = count_replies_this_month(None)
    
    # Add 6 deleted posts from May 12 incident
    incident_deletes = 6 if now.month == 5 and now.year == 2026 else 0
    correction_posts = 2 if now.month == 5 and now.day >= 12 and now.year == 2026 else 0
    
    total = content_posts + engagement_posts + incident_deletes + correction_posts
    return total

def determine_tier(remaining):
    """Determine budget tier based on remaining POSTs."""
    if remaining <= 0:
        return 'stop'
    elif remaining <= 50:
        return 'red'
    elif remaining <= 150:
        return 'yellow'
    return 'green'

def check_budget(reset_daily=False):
    budget = load_json(BUDGET_FILE)
    if not budget:
        print(json.dumps({"error": "budget file not found"}))
        sys.exit(1)
    
    now = datetime.now(timezone.utc)
    today_str = now.strftime('%Y-%m-%d')
    
    # Reset daily counter if date changed
    if budget.get('today_date') != today_str:
        budget['today_date'] = today_str
        budget['replies_today'] = 0
        save_json(BUDGET_FILE, budget)
    
    if reset_daily:
        budget['today_date'] = today_str
        budget['replies_today'] = count_replies_today(budget)
        budget['replies_this_month'] = count_replies_this_month(budget)
        save_json(BUDGET_FILE, budget)
    
    # Calculate remaining
    used = get_used_posts_this_month()
    cap = budget.get('monthly_cap', 500)
    remaining = cap - used
    
    # Determine tier
    tier = determine_tier(remaining)
    tier_config = budget['budget_tiers'][tier]
    
    # Per-scan allowance
    per_scan = tier_config['per_scan']
    per_day = tier_config['per_day']
    
    # Clamp by daily remaining
    daily_used = budget.get('replies_today', 0)
    daily_remaining = max(0, per_day - daily_used)
    per_scan = min(per_scan, daily_remaining)
    
    # Get users at lifetime cap
    lifetime = get_lifetime_replies_per_user()
    lifetime_cap = budget['hard_limits']['per_user_lifetime_max']
    capped_users = [u for u, c in lifetime.items() if c >= lifetime_cap]
    
    # Check for abnormal spike
    alerts = budget.get('alerts', [])
    last_count = budget.get('last_scan_lead_count', 0)
    spike_threshold = budget.get('spike_threshold', 10)
    
    result = {
        "tier": tier,
        "per_scan_allowance": per_scan,
        "per_day_allowance": per_day,
        "daily_used": daily_used,
        "daily_remaining": daily_remaining,
        "monthly_used": used,
        "monthly_remaining": remaining,
        "monthly_cap": cap,
        "lifetime_capped_users": capped_users,
        "lifetime_cap": lifetime_cap,
        "hard_limits": budget['hard_limits'],
        "alerts": alerts,
        "spike_threshold": spike_threshold,
        "last_scan_lead_count": last_count,
        "should_alert": tier in ('red', 'stop') or len(alerts) > 0,
        "can_reply": per_scan > 0
    }
    
    print(json.dumps(result, indent=2))
    return result

if __name__ == '__main__':
    reset = '--reset-daily' in sys.argv
    check_budget(reset_daily=reset)
