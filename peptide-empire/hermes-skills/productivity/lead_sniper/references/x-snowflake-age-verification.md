# X Snowflake ID → Age Verification

Use X's tweet snowflake IDs (status IDs) to determine precise post age when
web_search snippets lack explicit dates. A far more reliable approach than
guessing from text snippets like "May 6" or "12 hours ago."

## How It Works

X status IDs are Snowflake IDs (64-bit integers, Twitter epoch: 1288834974657ms).
The timestamp is embedded in the top 41 bits:

```python
from datetime import datetime, timezone, timedelta

def snowflake_to_datetime(snowflake_id: int) -> datetime:
    twitter_epoch_ms = 1288834974657
    timestamp_ms = (snowflake_id >> 22) + twitter_epoch_ms
    return datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)

def is_within_48hrs(snowflake_id: int, now: datetime = None) -> bool:
    if now is None:
        now = datetime.now(timezone.utc)
    post_time = snowflake_to_datetime(snowflake_id)
    age = now - post_time
    return age < timedelta(hours=48)
```

## When to Use

Every degraded-mode scan. web_search results include the full X URL in the
`url` field, which contains the snowflake ID:

```
"url": "https://x.com/biohacker_joe/status/2046949562972270924"
#                                          ^-- snowflake ID: 2046949562972270924
```

## Extraction

```python
import re

def extract_snowflake_id(url: str) -> int | None:
    match = re.search(r'/status/(\d+)', url)
    return int(match.group(1)) if match else None
```

## Usage in lead_sniper Workflow

After running web_search queries, BEFORE classifying/adding leads:

1. Extract snowflake ID from each result's `url`
2. Convert to datetime via `snowflake_to_datetime(snowflake_id)`
3. If age > 48 hours → SKIP (per anti-spam rules)
4. If age ≤ 48 hours → proceed with classification

This catches edge cases that snippet-date guessing misses:
- URLs without snippet dates
- Ambiguous dates ("today is Sunday" — which Sunday?)
- Snippets echoing old content from a reshare/conversation

## Real Examples from May 11, 2026 Midday Scan

| Post | Status ID | Post Date | Age | Verdict |
|------|-----------|-----------|-----|---------|
| danfleyshman stack question | 2046949562972270924 | 2026-04-22 | 19 days | ❌ skip |
| DanielleMorrill "what's your stack?" | 2037370869971066921 | 2026-03-27 | 45 days | ❌ skip |
| buyerofponzi stack share | 2049499464100921717 | 2026-04-29 | 12 days | ❌ skip |
| Camp4 KLOW experiment | 2045617843866337642 | 2026-04-18 | 23 days | ❌ skip |
| chrissyfarr wolverine learn | 2045212323086815496 | 2026-04-17 | 24 days | ❌ skip |

All 5 potentially-interesting posts were outside the 48hr window — correctly
rejected by snowflake ID check. Without it, snippet impressions ("which company
do you trust and what Peptide Stack do you like?") would have been logged as
false-positive leads.

## Pitfalls

- **Not all X URLs contain snowflake IDs:** Profile pages (`/biohacker_joe`),
  search results pages (`/search?q=...`), and hashtag pages have no status IDs.
  Skip those — they're not individual posts.
- **x.com vs twitter.com:** Both domains work; the URL path after `/status/`
  is the same snowflake ID regardless of domain.
- **Thread posts have individual IDs:** Each reply in a thread has its own
  snowflake ID. The URL in a thread link points to the specific reply post,
  so the check is per-post, which is correct.
- **Snowflake ID date is NOT content date:** The date is when the post was
  *created*, not when it was indexed by web_search. This is exactly what we
  want for the 48hr rule — we care about post freshness, not crawl freshness.
- **Status IDs from different X API versions:** Very old tweets (pre-2010)
  may use a different ID scheme. For practical purposes, any status ID > 1e15
  (15+ digits) is a valid snowflake. If a URL has a status ID < 1e12, the post
  predates the snowflake era and is certainly older than 48 hours.
