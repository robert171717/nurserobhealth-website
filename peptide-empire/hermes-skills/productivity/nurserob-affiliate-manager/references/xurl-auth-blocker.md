# Xurl Auth Blocker — Reference

## Current State (as of May 10, 2026)

xurl is installed at `/home/robert/.local/bin/xurl` with two apps configured but **neither has valid OAuth2 tokens**:

```
default  [(no credentials)]
    oauth2: NurseRobHealth
    oauth1: –
    bearer: –

nurse-rob  [client_id: aW5iVFJT…]
    oauth2: (none)
    oauth1: –
    bearer: –
```

The `default` app has `oauth2: NurseRobHealth` listed but shows `[(no credentials)]` — meaning the token file is missing, expired, or was revoked. X API returns 401 on all post attempts.

## Impact on Affiliate Pipeline

- **Zero content posting** = zero impressions = zero link clicks = zero conversions
- **Zero reply capability** = 51 leads stalled, 25 overdue followups
- **Zero follower data** = no audience metrics in dashboard
- **Zero DM capability** = nurture sequences blocked

## Diagnostics

```bash
# Check auth status
xurl auth status

# Check if installed
which xurl

# Find binary location
find /home -name "xurl" -type f 2>/dev/null
```

## Fix Command

```bash
xurl auth oauth2 --app default NurseRobHealth
```
This opens a browser for OAuth2 re-authorization. Requires:
- Valid X Developer Portal app (https://developer.x.com/en/portal/dashboard)
- Minimum $5/month Basic API access credits
- Browser access on the machine (or remote browser flow)

## Alternate App (If Default Doesn't Work)

```bash
# Register a new app with client credentials from X Developer Portal
xurl auth apps add nurse-rob --client-id <CLIENT_ID> --client-secret <CLIENT_SECRET>

# Then authenticate
xurl auth oauth2 --app nurse-rob NurseRobHealth

# Set as default
xurl auth default nurse-rob
```

## History
- **Apr 28:** Day 0 — xurl installed but not authenticated (first cron runs fail)
- **May 3:** App `default` created, OAuth2 token obtained (briefly working?)
- **May 5:** Token returned 401 — Day 1 of block
- **May 10:** Day 8 of block — no change
