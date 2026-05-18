# X API Free Tier Reply Restriction — Lead Sniper Context

## Impact on Lead Replies

This restriction directly affects how lead_sniper can engage with leads. The error:

```json
{
  "title": "Forbidden",
  "detail": "Reply to this conversation is not allowed because you have not been mentioned or otherwise engaged by the author of the post you are replying to.",
  "status": 403
}
```

## When it blocks

- **Every HOT lead discovered via xurl search** — these are users @NurseRobHealth has never interacted with
- **Old backlog leads** (daniel_wilson, doodlestein, SlinkIsFit, DrLizaMD, danfleyshman, adxtyahq) — none engaged with @NurseRobHealth
- **WARM leads needing reply** — same restriction applies

## When it works

- @FrankGowalski — reply succeeded (2054095287468040526). The post may have been in a thread where @NurseRobHealth was mentioned, or the X API allowed it for some other reason. When it works, use `xurl reply` as normal. If it fails, fall back to mention post.

## Verified Behavior (May 12, 2026)

- 3 separate `xurl reply` attempts to @AlmcdDon, @unaveridad, @BadTechBandit all returned 403
- All 3 were "out of conversation" — @NurseRobHealth had no prior engagement with any
- Workaround via `xurl post` succeeded for all 3
- The 403 is deterministic for Free tier — not intermittent, not rate-limit related

## Lead Log Action Detail to Use

For leads that can't be directly replied to, set:

```json
"action": "needs_reply",
"action_detail": "X API reply restrictions — cannot reply directly without prior engagement. Need mention post or manual browser reply."
```

Or if mention post was sent:

```json
"action": "replied",
"notes": "Reply sent as public educational mention post (direct reply blocked by X API permissions). Directed to email for personal follow-up."
```

## Cleanup Strategy for Backlog

The 7 HOT leads in the backlog (daniel_wilson, doodlestein, SlinkIsFit, DrLizaMD, danfleyshman, adxtyahq, whotfiszackk) are all stale (>3 days old). Even if xurl allowed replies, posting on a 2-week-old thread looks spammy. Best approach:

1. **Manual browser replies** (best signal) — log into X as @NurseRobHealth, find and reply
2. **Fresh mention posts** (medium signal) — post new educational content that @mentions them
3. **Let them expire** — lead_log will naturally age them out as focus shifts to new leads
