# Content File Freshness Check

The content file (`YYYY-MM-DD_posts.md`) can be regenerated between scheduler runs.
If the post_log.json already has an entry for today, always verify whether the
content file was *replaced* since the log entry was written.

## Detection Pattern

```python
import json, os, subprocess

BASE = "/home/robert/NurseRob_PeptideEmpire"
today = "2026-05-11"  # or fetch from datetime
content_file = f"{BASE}/content/{today}_posts.md"
log_file = f"{BASE}/content/post_log.json"

# Read post_log
r = subprocess.run(["cat", log_file], capture_output=True, text=True)
log = json.loads(r.stdout)

# Get content file mtime (Unix timestamp)
mtime = os.path.getmtime(content_file)  # seconds since epoch

# Get log entry timestamp
day_entry = log.get(today, {})
log_timestamp_str = day_entry.get("last_attempt", "")  # e.g. "2026-05-11T12:06:00-07:00"

content_stale = False
if log_timestamp_str:
    import datetime
    # Parse ISO timestamp — handle timezone offset
    log_dt = datetime.datetime.fromisoformat(log_timestamp_str)
    log_epoch = log_dt.timestamp()
    if mtime > log_epoch:
        content_stale = True
        print(f"STALE: Content file mtime ({mtime}) > log entry ({log_epoch})")
        print(f"  File was regenerated after log was written. Re-read from scratch.")
```

## Fast Shell Check

If mtime comparison is all you need and Python isn't available:

```bash
content_file="/home/robert/NurseRob_PeptideEmpire/content/2026-05-11_posts.md"
content_mtime=$(stat -c %Y "$content_file")
# Compare to the last_attempt value from post_log.json
```

## When Stale Is Detected

1. Set a run-level flag: `content_regenerated = True`
2. Re-read the entire content file — do NOT reuse cached titles/tweet counts
3. Re-validate every post from scratch (disclaimers, character counts, flagged words)
4. Overwrite the entire date entry in post_log.json (not just a field — replace the whole slots dict)
5. Update metrics.json content section with fresh titles and post counts
6. Log the regeneration in the final report

## ⚠️ Tweet Count Metadata Drift After Regeneration

When a content file is regenerated, the **header metadata** (the comment line above each code block, e.g. `**Format:** Thread (7 tweets)`) may be **stale or inaccurate** — it was written by `peptide_content_operator` at a different point in time and may reference a different version of the code block below it.

**Do NOT trust the header's tweet count.** Always parse the actual code block to determine the real tweet count.

**Observed May 17, 2026**: Content header said `**Format:** Thread (7 tweets)` but the parsed code block contained 10 tweets (opener + 7 numbered + disclaimer as separate tweet + CTA as separate tweet). Posting all 10 was correct; logging `tweet_count: 10` was correct. Using the header's "7" would have under-counted and produced a verification mismatch.

**Rules for parsing tweet count:**
```
Thread structure → count all \n\n-separated paragraphs in the code block
  - Opener (no number prefix) = tweet 1
  - 1/ through 7/ = tweets 2-8
  - ⚠️ disclaimer as standalone paragraph = tweet 9
  - 🔗 CTA as standalone paragraph = tweet 10
Single post → 1 tweet (the code block contains one paragraph)
```

**What to log:**
- `tweet_count`: the **actual parsed count** from the code block, not the header
- `validation`: reference the parsed count (e.g., `"10 tweets, all ≤280 chars"`)
- `url`: derived from the `conversation_id:` search after verification

## Why This Happens

- `peptide_content_operator` may regenerate content mid-cycle (e.g., if a user manually invokes it)
- The morning scheduler run may create the initial log entry, then the midday content batch replaces the file
- Manual edits to the content file from the desktop Windows side (`/mnt/c/Users/Robert/...`)
