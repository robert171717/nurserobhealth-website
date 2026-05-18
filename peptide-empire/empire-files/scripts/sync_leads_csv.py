#!/usr/bin/env python3
"""
Lead Sync Script — reads lead_log.json, writes formatted CSV to Desktop.
Runs every 6 hours via cron. Nurse Rob can open in Excel/Google Sheets anytime.
"""
import json
import csv
import os
from datetime import datetime, timezone
from pathlib import Path

LEAD_LOG = os.path.expanduser("~/NurseRob_PeptideEmpire/leads/lead_log.json")
OUTPUT_CSV = "/mnt/c/Users/Robert/Desktop/Daily Brief/NurseRob_PeptideEmpire/leads/lead_dashboard.csv"

def main():
    # Read lead log
    if not os.path.exists(LEAD_LOG):
        print(f"Lead log not found: {LEAD_LOG}")
        return
    
    with open(LEAD_LOG, 'r') as f:
        log = json.load(f)
    
    entries = log.get('entries', [])
    if not entries:
        print("No leads in log.")
        return
    
    # Sort by timestamp, newest first
    entries_sorted = sorted(
        entries, 
        key=lambda e: e.get('timestamp', ''), 
        reverse=True
    )
    
    # Write CSV
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    
    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Date', 'Platform', 'Username', 'Question', 
            'Classification', 'Status', 'Action Taken', 
            'Follow-up Due', 'Lead Age (Days)'
        ])
        
        now = datetime.now(timezone.utc)
        
        for e in entries_sorted:
            ts = e.get('timestamp', '')
            # Strip timezone info for display
            date_str = ts[:10] if ts else 'unknown'
            
            # Calculate lead age
            try:
                lead_dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                age_days = (now - lead_dt).days
            except:
                age_days = '?'
            
            writer.writerow([
                date_str,
                e.get('platform', 'x'),
                e.get('username', ''),
                e.get('question', '')[:200],
                e.get('classification', 'cold'),
                e.get('status', 'new'),
                e.get('action', 'pending'),
                (e.get('followup_due') or '')[:10],
                age_days
            ])
    
    print(f"Synced {len(entries_sorted)} leads to {OUTPUT_CSV}")
    
    # Also write summary stats
    hot = sum(1 for e in entries_sorted if e.get('classification') == 'hot')
    warm = sum(1 for e in entries_sorted if e.get('classification') == 'warm')
    cold = sum(1 for e in entries_sorted if e.get('classification') == 'cold')
    needs_reply = sum(1 for e in entries_sorted if e.get('action') == 'needs_reply')
    in_nurture = sum(1 for e in entries_sorted if e.get('status') == 'nurturing')
    
    print(f"  Hot: {hot} | Warm: {warm} | Cold: {cold}")
    print(f"  Needs reply: {needs_reply} | In nurture: {in_nurture}")

if __name__ == '__main__':
    main()
