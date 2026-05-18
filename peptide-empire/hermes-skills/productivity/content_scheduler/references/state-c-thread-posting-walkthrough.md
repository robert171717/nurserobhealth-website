# State C Thread Posting Walkthrough

Live-tested May 14, 2026 — first successful end-to-end post from this cron system.

## Initial Auth Verification

```bash
xurl auth status
```
Shows:
```
default  [(no credentials)]
      oauth2: NurseRobHealth
      oauth1: –
      bearer: –

▸ nurse-rob  [client_id: aW5iVFJT…]
      oauth2: NurseRobHealth
      oauth1: –
      bearer: –
```

**Interpretation:** Default app (▸) = `nurse-rob` with active oauth2. The `default` app entry is stale — ignore it.

```bash
xurl whoami
```
Returns 200 with user profile → **State C confirmed.**

## Thread Posting (7 tweets)

### Step 1: Post opener
```bash
xurl post '🧵 As a licensed RN, [hook text...]'
```
→ Save `id` from output (`data.id`). This is `OPENER_ID`.

### Step 2: Reply all numbered tweets to OPENER_ID
```bash
sleep 10
xurl reply $OPENER_ID '1/ [first numbered tweet...]'
sleep 10
xurl reply $OPENER_ID '2/ [second numbered tweet...]'
# ...repeat for all N tweets
```

**CRITICAL:** Every `xurl reply` targets the OPENER_ID. Do NOT chain (reply to tweet 1 with tweet 2). X threading works by replying to root, not chaining.

### Thread Timing
- 7 tweets (opener + 6 replies): ~70 seconds total (10s delay × 6 replies + ~10s for posting opener)
- 5 tweets: ~50 seconds
- 8 tweets: ~80 seconds
- Well within X rate limits (50 posts/day, 300 posts/3hr window)

## Post-2 (Single Tweet)

No chaining needed — just:
```bash
xurl post '[single tweet text with RN credential, disclaimer, CTA]'
```

## Post-Posting Cleanup

### Update post_log.json
```python
# In execute_code:
import subprocess, json
log = json.loads(open(path).read())

# 1. Update today's entry with POSTED status + tweet IDs + URLs
log["2026-05-14"]["posts_posted"] = N
log["2026-05-14"]["auth_status"] = "OK — posted successfully"
log["2026-05-14"]["slots"]["morning"]["status"] = "POSTED"
log["2026-05-14"]["slots"]["morning"]["post_id"] = "OPENER_ID"
log["2026-05-14"]["slots"]["morning"]["tweet_count"] = 7
log["2026-05-14"]["slots"]["morning"]["url"] = "https://x.com/NurseRobHealth/status/OPENER_ID"
log["2026-05-14"]["slots"]["evening"]["status"] = "POSTED"
log["2026-05-14"]["slots"]["evening"]["post_id"] = "POST2_ID"

# 2. Sweep stale BLOCKED top-level metadata
log["days_blocked"] = 0
log["last_error"] = ""
log["status"] = "POSTING_OK — xurl authenticated, content posted"
log["error"] = "Resolved — xurl working as of [date]"

# Write back
subprocess.run(["tee", path], input=json.dumps(log, indent=2), text=True, timeout=5)
```

### Cross-post to Discord
```bash
DISCORD_TOKEN="$(grep -A20 '^discord:' ~/.hermes/config.yaml | grep -E '^\s+token:' | head -1 | awk '{print $2}')"
curl -s -X POST "https://discord.com/api/v10/channels/1484946244768895056/messages" \
  -H "Authorization: Bot $DISCORD_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"📢 Content Posted: [title] — [X URL]"}'
```

### Sweep dashboard metrics.json
Update: `content.posts_today`, `content.posts_posted`, `content.posting_status`, `content.block_reason` (clear), `alerts.good` (add success), `alerts.critical` (remove xurl entries), `degraded_mode.xurl` (set to OK), `days_blocked` (reset to 0), `leads.xurl_authenticated` (set True).

See content_scheduler SKILL.md → Pitfalls → "Post-block dashboard cleanup required" for the full sweep list.
