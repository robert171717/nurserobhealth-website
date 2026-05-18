# Past Post & Reply Audit Workflow
**Reference for nurse-rob-x-reply-guidelines | May 2026**

## When to Run
- After any major guidelines update (e.g., v1.2→v1.3 with new language rules)
- When a new forbidden word is added to Section 12
- When the user requests a liability sweep
- Proactively every 2-4 weeks

## Workflow

### Step 1: Fetch All Posts
```bash
xurl search 'from:NurseRobHealth' -n 100 > /tmp/nurserob_tweets_raw.json
```
Note: xurl search returns JSON. Pipe through python to parse if piping inline, but saving to file first avoids JSON decode errors from control characters in tweet text.

### Step 2: Filter by Date Range
Parse the JSON, filter `created_at` for the target date range. The conversation_id field links thread tweets — thread openers have `conversation_id == id`.

### Step 3: Scan Each Post Against v1.3 Checklist
Run every post through:
- Section 12 HIGH-RISK word scan (heal/cure/miracle/fix/prevent/treat/diagnose/breakthrough)
- Section 12 MEDIUM-RISK word scan (repair/support/promote/aid — check safe phrasing)
- Section 13 language scan (word boundary rules: health ≠ heal)
- Specific dose check (regex: `\d+\s*(?:mcg|mg|microgram)`)
- Personalization check (your injury, your condition, your parents, 80 yo, etc.)
- Disclaimer presence check

### Step 4: Categorize by Risk

| Tier | Criteria | Action |
|------|----------|--------|
| **DELETE TODAY** | HIGH-RISK word in thread opener or standalone tweet | Delete via `xurl -X DELETE /2/tweets/<ID>` |
| **REWRITE** | HIGH-RISK word in research citation context | Delete + repost (standalone) or leave note (thread tweet — deleting breaks chain) |
| **WORD SWAP** | MEDIUM-RISK word outside safe phrasing | Leave if in thread, rewrite if standalone |
| **ADD DISCLAIMER** | Missing disclaimer | Delete + repost (standalone only — thread tweets can't be edited) |
| **SAFE** | Passes all checks | No action |

### Step 5: Execute Deletes
```bash
xurl -X DELETE /2/tweets/<ID>
```
Verify with `"deleted":true` in response.

### Step 6: Note False Positives
Common false positives from substring matching:
- "health" / "healthy" / "healthcare" contain "heal" as substring → NOT a violation (v1.3 word boundary rule)
- "NurseRobHealth" / "nurserobhealth.com" → NOT a violation
- Use `\bheal(?:ing|ed|s)?\b` regex for accurate matching, not plain `in` substring

## X API Limitations (Critical)

- **CANNOT EDIT TWEETS** — X API v2 has no edit endpoint. Tweets are immutable after posting.
- **CAN DELETE** — `xurl -X DELETE /2/tweets/<ID>` works
- **THREAD TWEETS** — Deleting mid-thread breaks the chain. Only delete thread openers that are truly dangerous.
- **DELETE + REPOST** — For standalone tweets, delete the original and post the corrected version. But reposting changes the tweet ID and loses any engagement.

## Audit Report Format

Save to Desktop: `past_post_audit_report.md`

Structure:
1. Executive summary (total posts, flagged, safe)
2. Tier 1: DELETE TODAY (highest risk)
3. Tier 2: REWRITE (medium risk, fixable)
4. Tier 3: WORD SWAP (low risk, leave or note)
5. False positive correction (if any)
6. What's working well

Each flagged item gets: ID, date, exact text, reason flagged, risk level, recommended action.
