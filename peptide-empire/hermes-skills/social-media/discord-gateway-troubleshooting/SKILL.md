---
name: discord-gateway-troubleshooting
description: Troubleshoot Discord gateway connection issues — reconnect spirals, rate-limit blackholes, token gateway suspensions, zombie gateway detection, and diagnostic scripts.
version: 2.0.0
author: Community
tags: [discord, troubleshooting, gateway, debugging]
---

# Discord Gateway Troubleshooting

## Common Issues and Solutions

### Issue: "expected token to be a str, received NoneType instead"

**Cause**: The environment variable name is incorrect. The code expects `DISCORD_BOT_TOKEN` but the `.env` file has `DISCORD_TOKEN`.

**Solution**: Ensure your environment file uses this exact variable name:
```bash
DISCORD_BOT_TOKEN=your_token_here
# NOT DISCORD_TOKEN=...
```

### Issue: "PrivilegedIntentsRequired" Error

**Cause**: Discord bot needs privileged intents enabled in the Developer Portal.

**Solution**:
1. Go to https://discord.com/developers/applications
2. Select your application → Bot tab
3. Enable these toggles under "Privileged Gateway Intents":
   - ✅ Message Content Intent
   - ✅ Server Members Intent (if needed)
4. Save changes and restart the gateway

### Issue: ModuleNotFoundError for 'yaml' or 'discord'

**Cause**: Missing Python dependencies in the native environment.

**Solution**: Install required packages with pip.

## Testing Discord Connection Manually

To test if your Discord setup works without running the full gateway, create a test script that loads your token and sends a message to verify connectivity.

Expected output on success:
```
✅ Logged in as Hermes Agent#3977
✅ Sent test message to channel 1484946244768895056
```

## Environment Variable Checklist

Verify your environment file has these exact variable names:

- [ ] `DISCORD_BOT_TOKEN` (not DISCORD_TOKEN)
- [ ] `DISCORD_APPLICATION_ID`
- [ ] `DISCORD_HOME_CHANNEL`

## Gateway Log Location

Check logs for detailed error messages using tail command on the gateway log file.

## Reconnect Spiral & Rate Limiting

The gateway's `run.py` auto-retries failed platform connections every 30 seconds (see `_failed_platforms` with `next_retry: now + 30`). When Discord's WebSocket is unreachable (VPN change, network blip), the gateway enters a **reconnect spiral** — each retry burns a session-start token. After 10+ attempts, Discord begins silently **blackholing IDENTIFY** on the WebSocket.

### Symptoms of Rate-Limit Blackhole

There are two distinct IDENTIFY rejection patterns — knowing which one you're in determines the fix:

**Pattern A: Silent Blackhole (IP-level rate limit)**
- Gateway log shows: `discord connect timed out after 30s` repeated every ~3 min
- Manual WebSocket test: `HELLO` received (op=10), `IDENTIFY` sent — but **no READY, no INVALID_SESSION, no close frame** — Discord silently times out
- REST API (`/api/v10/users/@me`) returns 429 rate-limit
- REST message send may still work
- **VPN change usually fixes this** (rate limit is IP-scoped)

**Pattern B: Close Code 4000 (token-level gateway suspension)**
- Manual WebSocket test: `HELLO` received, `IDENTIFY` sent — Discord responds with **close code 4000** ("Unknown Error") and cleanly closes
- Unlike the silent blackhole, Discord IS actively rejecting — just not telling you why
- **VPN change does NOT fix this** — the suspension is on the token, not the IP
- Occurs after dozens of failed IDENTIFY attempts; Discord temporarily suspends gateway access for that specific token
- Fix: wait 2-6 hours OR regenerate the bot token
- Confirming: even `intents=0` IDENTIFY gets 4000 — the token itself is gate-banned

### Breaking the Spiral
1. **Kill the gateway immediately** — `pkill -9 -f "hermes_cli.main gateway"` — don't let it keep burning tokens
2. **Diagnose the pattern** — run the diagnostic script to determine Pattern A (IP blackhole) or Pattern B (token suspension)
3. **For Pattern A (IP-level)**:
   - Change VPN exit node — new IP usually bypasses the rate limit
   - Or wait 1-3 hours for cooldown
4. **For Pattern B (token suspension)**:
   - VPN change won't help — the ban is on the token
   - Wait 2-6 hours for Discord to lift the gateway suspension
   - Or regenerate bot token in Developer Portal → Bot tab → Reset Token
5. Let the watchdog (see `scripts/discord_watchdog.py`) handle restart when safe

### Gateway Auto-Retry Internals
- `gateway/run.py` line 1783: `next_retry = time.monotonic() + 30`
- `gateway/platforms/discord.py` line 828: `await asyncio.wait_for(self._ready_event.wait(), timeout=30)`
- When all platforms fail with retryable errors, gateway exits with `_exit_with_failure = True` for process supervisor restart

## Zombie Gateway Detection

A gateway process can be **alive but silently dead** — PID exists, but logging stopped hours ago.

### Detection
```bash
# Check if gateway.log is still being written to
stat ~/.hermes/logs/gateway.log | grep Modify
# If the modification time is hours old while ps shows a gateway PID → zombie

# Check process file descriptors
ls -la /proc/<PID>/fd/ | grep gateway.log
```

### Recovery
```bash
pkill -9 -f "hermes_cli.main gateway"
# Then restart or let watchdog handle it
```

## WebSocket vs REST API Split

Discord's WebSocket and REST API use **different rate limit buckets**. When the WebSocket is blackholed:
- ❌ WebSocket IDENTIFY — killed
- ❌ `GET /api/v10/users/@me` — likely rate-limited (429)
- ✅ `POST /api/v10/channels/{id}/messages` — often still works (200)
- ✅ `GET /api/v10/guilds/{id}/channels` — often still works (200)

This means you can still send messages to channels via REST API even when the bot appears offline (grey dot).

### Testing Connectivity Layers
See `references/diagnostic-steps.md` for the full diagnostic script that tests DNS, TCP, WebSocket HELLO, IDENTIFY, and REST endpoints independently.

## Watchdog Monitoring

A watchdog script at `scripts/discord_watchdog.py` prevents silent disconnects. Install via cron:

```bash
hermes cron create "Discord Gateway Watchdog" --script discord_watchdog.py --schedule "*/10 * * * *" --no-agent
```

The watchdog enforces strict anti-spiral guardrails:
- 30-min grace period after disconnect (lets rate limits clear)
- Max 1 restart per hour
- Max 3 restarts per 2-hour window, then alerts
- Checks both process health and gateway log activity
- Clears the ban-monitor sentinel on disconnect so re-alert works for future bans

## Ban Lift Monitoring

When a token-level gateway suspension (close code 4000) is confirmed, the gateway should remain **off** until the ban lifts — otherwise every restart attempt burns rate limits. The ban monitor script polls the WebSocket IDENTIFY every 5 minutes and alerts when the ban clears.

Install as cron (note: `--deliver origin` so the alert reaches you):

```bash
hermes cron create "Discord Ban Monitor" --script discord_ban_monitor.py --schedule "*/5 * * * *" --no-agent --deliver origin
```

**How it works:**
1. Every 5 minutes, tries a minimal WebSocket IDENTIFY (intents=0)
2. If close code 4000 or timeout → exit 1 (keep retrying)
3. If READY received → sends `🟢 Discord gateway ban LIFTED` to channel, creates sentinel file, exits 0
4. Sentinel file prevents duplicate alerts; watchdog clears it when a new disconnect is detected
5. **Pause the watchdog** during a token ban so it doesn't restart the gateway prematurely

**Manual check:** `python ~/.hermes/scripts/discord_ban_monitor.py` — exit 0 = ban lifted, exit 1 = still banned.

## Key Takeaway

The most common issue is using the wrong environment variable name. Always use **`DISCORD_BOT_TOKEN`** (with BOT in the middle) — not `DISCORD_TOKEN`. This was discovered through trial and error when the gateway failed to connect despite having a valid token configured.