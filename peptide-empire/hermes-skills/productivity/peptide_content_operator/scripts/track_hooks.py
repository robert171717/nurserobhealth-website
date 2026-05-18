#!/usr/bin/env python3
"""Track hook patterns used in recent Nurse Rob content files.

Scans content files in reverse chronological order, extracts hook metadata,
and validates rotation rules. Prevents:
  - Same hook pattern two days in a row
  - Research Contradiction, Pattern Interrupt, Vulnerability Hook, or Shocking Mechanism >1x/week
  - Banned openers slipping through on generation

Usage:
  python3 scripts/track_hooks.py /path/to/content/dir [--days N]
  python3 scripts/track_hooks.py --draft /tmp/2026-05-16_posts_draft.md [--existing-dir /path/to/content]

Flags:
  --days N          Number of past days to scan (default: 7)
  --draft FILE      Check a draft file's hooks against existing rotation
  --existing-dir DIR Directory with existing content files (default: ~/NurseRob_PeptideEmpire/content)
"""

import argparse
import os
import re
import sys
from datetime import datetime, timedelta

CAPPED_HOOKS = {"The Research Contradiction", "The Pattern Interrupt", "The Vulnerability Hook", "The Shocking Mechanism"}
MAX_PER_WEEK = 1  # Max uses per week for capped hooks

# All known hook patterns for validation
VALID_HOOKS = {
    "Contrarian Stat",
    "Credential + Myth-Bust",
    "The Unsaid Thing",
    "Direct Challenge",
    "Personal Credibility",
    "The Question Hook",
    "The Anti-Hype",
    "The Research Contradiction",
    "The Pattern Interrupt",
    "Stat Drop",
    "The Vulnerability Hook",
    "The Shocking Mechanism",
}

# Banned openers (any line starting with these is flagged)
BANNED_OPENERS = [
    "Have you heard about",
    "Let's talk about",
    "Did you know",
    "What's your #1",
]


def extract_hook_from_file(filepath: str) -> dict | None:
    """Extract hook metadata from a content file's Post 1 and Post 2 headers."""
    data = {"file": os.path.basename(filepath), "post1_hook": None, "post2_hook": None}

    with open(filepath) as f:
        content = f.read()

    # Extract date from filename or header
    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", filepath)
    data["date"] = date_match.group(1) if date_match else "unknown"

    # Find Post 1 hook
    m = re.search(r"## Post 1:.*?\n\*\*Time:.*?\*\*Hook:\*\* (.+?)(?:\s*\|\s*\*\*CTA)", content)
    if m:
        data["post1_hook"] = m.group(1).strip()

    # Find Post 2 hook
    m = re.search(r"## Post 2:.*?\n\*\*Time:.*?\*\*Hook:\*\* (.+?)(?:\s*\|\s*\*\*Pillar|\s*\|\s*\*\*CTA)", content)
    if m:
        data["post2_hook"] = m.group(1).strip()

    return data


def validate_hook_name(hook: str | None, file_label: str) -> str | None:
    """Validate a hook name. Returns error message or None."""
    if hook is None:
        return None  # No hook metadata is fine for older files
    if hook not in VALID_HOOKS:
        return f"  ⚠️ Unknown hook '{hook}' in {file_label}"
    return None


def check_consecutive(hook: str, prev_hook: str, current_day: str, prev_day: str) -> str | None:
    """Check if same hook used two days in a row."""
    if hook and prev_hook and hook == prev_hook:
        return f"  ⚠️ '{hook}' used on {prev_day} AND {current_day} — same pattern consecutive days!"
    return None


def count_hook_usage(history: list[dict], hook: str) -> int:
    """Count how many times a hook appears in the history (post1 or post2)."""
    count = 0
    for entry in history:
        if entry.get("post1_hook") == hook:
            count += 1
        if entry.get("post2_hook") == hook:
            count += 1
    return count


def check_file_pattern(content: str, issues: list):
    """Check for banned opener patterns in the content."""
    lines = content.split("\n")
    for i, line in enumerate(lines):
        stripped = line.strip()
        for banned in BANNED_OPENERS:
            if stripped.startswith(banned):
                issues.append(f"  ⚠️ Line {i+1}: Banned opener detected — '{banned}'")
                break


def main():
    parser = argparse.ArgumentParser(description="Track hook rotation in Nurse Rob content files")
    parser.add_argument("content_dir", nargs="?", help="Path to content directory")
    parser.add_argument("--days", type=int, default=7, help="Days of history to check (default: 7)")
    parser.add_argument("--draft", help="Check a draft file's hooks against existing rotation")
    parser.add_argument("--existing-dir", help="Directory with existing content files")
    args = parser.parse_args()

    # Determine content directory
    if args.existing_dir:
        content_dir = args.existing_dir
    elif args.content_dir:
        content_dir = args.content_dir
    else:
        content_dir = os.path.expanduser("~/NurseRob_PeptideEmpire/content")

    if not os.path.isdir(content_dir):
        print(f"❌ Content directory not found: {content_dir}")
        sys.exit(1)

    # Scan existing files (reverse chronological)
    files = sorted(
        [f for f in os.listdir(content_dir) if re.match(r"\d{4}-\d{2}-\d{2}_posts\.md$", f)],
        reverse=True,
    )

    history = []
    errors = []

    for fname in files[: args.days]:
        fpath = os.path.join(content_dir, fname)
        entry = extract_hook_from_file(fpath)
        if entry.get("post1_hook") or entry.get("post2_hook"):  # Only include files with hook data
            history.append(entry)

    # If checking a draft, add it to history for validation
    draft_entry = None
    if args.draft:
        draft_entry = extract_hook_from_file(args.draft)
        if draft_entry.get("post1_hook") or draft_entry.get("post2_hook"):
            history.insert(0, draft_entry)

    # Print header
    print("=" * 60)
    print(f"  HOOK ROTATION REPORT — {len(history)} files scanned")
    print("=" * 60)

    if not history:
        print("  No hook metadata found in recent files.")
        sys.exit(0)

    # Print table
    print(f"\n  {'Date':<14} {'Post 1 Hook':<30} {'Post 2 Hook':<30}")
    print(f"  {'-'*14} {'-'*30} {'-'*30}")

    hook_counts = {}  # Track total usage of each hook across history
    prev_post1 = None
    prev_post2 = None
    prev_date = None

    for entry in history:
        d = entry["date"]
        h1 = entry.get("post1_hook") or "(none)"
        h2 = entry.get("post2_hook") or "(none)"

        marker = " ← DRAFT" if args.draft and entry == history[0] else ""
        print(f"  {d:<14} {h1:<30} {h2:<30}{marker}")

        # Validate hook names
        err = validate_hook_name(entry.get("post1_hook"), f"{d} Post 1") or \
              validate_hook_name(entry.get("post2_hook"), f"{d} Post 2")
        if err:
            errors.append(err)

        # Check consecutive rotation
        if entry.get("post1_hook") and prev_post1 and entry["post1_hook"] == prev_post1:
            err = check_consecutive(entry["post1_hook"], prev_post1, d, prev_date)
            if err:
                errors.append(err)
        if entry.get("post2_hook") and prev_post2 and entry["post2_hook"] == prev_post2:
            err = check_consecutive(entry["post2_hook"], prev_post2, d, prev_date)
            if err:
                errors.append(err)

        prev_post1 = entry.get("post1_hook")
        prev_post2 = entry.get("post2_hook")
        prev_date = d

    # Count hook usage for cap check
    for entry in history:
        for h in [entry.get("post1_hook"), entry.get("post2_hook")]:
            if h:
                hook_counts[h] = hook_counts.get(h, 0) + 1

    print("\n  --- Hook Frequency (past {} days) ---".format(min(len(history), args.days)))
    for hook in sorted(hook_counts, key=hook_counts.get, reverse=True):
        count = hook_counts[hook]
        cap_warning = ""
        if hook in CAPPED_HOOKS and count > MAX_PER_WEEK:
            cap_warning = f" ⚠️ EXCEEDS {MAX_PER_WEEK}x/week cap!"
        print(f"  {hook:<30} {count:>2}x{cap_warning}")

    # If this is just a draft check, also validate the draft file's content
    if args.draft and os.path.exists(args.draft):
        with open(args.draft) as f:
            content = f.read()
        check_file_pattern(content, errors)

    # Summary
    print(f"\n{'='*60}")
    if errors:
        print("❌ ROTATION ISSUES FOUND:")
        for err in errors:
            print(err)
        sys.exit(1)
    else:
        print("✅ ROTATION CHECK PASSED — hooks properly rotated")
        sys.exit(0)


if __name__ == "__main__":
    main()
