# Internet Health Monitor — Design & Interpretation

## Design Philosophy

**Silent when healthy, visible only when there's a problem.** Zero tokens consumed during normal operation. Dual-path notification ensures at least one path works regardless of network state.

## Notification Design

| Scenario | Discord | Desktop Log | User Action |
|----------|---------|-------------|-------------|
| Internet UP | Nothing | Nothing | None |
| Internet goes DOWN | Delivery fails (expected) | ✅ Timestamp logged | Check Desktop log when at PC |
| Internet RECOVERS | ✅ Duration + details | ✅ Recovery logged | Review Discord notification |
| Internet stays DOWN | Nothing (no spam) | Single entry at start | Fix VPN, check log for duration |

**Key insight**: During an actual outage, there is NO way to remotely notify the user. No internet = no Discord, no email, no push notification. The Desktop log file is the only record available until the user returns to the PC.

## Script: `internet_health_monitor.py`

- **Location**: `~/.hermes/scripts/internet_health_monitor.py`
- **Cron**: `e0412520d4a5` — `*/5 * * * *`, `no_agent=true`, `deliver: origin`
- **State file**: `~/.hermes/.internet_health_state.json`
- **Log file**: `/mnt/c/Users/Robert/Desktop/Daily Brief/internet_health_log.txt`

## Check Endpoints

| Priority | Endpoint | Timeout | Purpose |
|----------|----------|---------|---------|
| 1 | `https://discord.com/api/v10/gateway` | 5s | Primary — Discord is the notification channel |
| 2 | `https://api.x.com/2/tweets` | 5s | Secondary — X posting uses this |
| 3 | `https://1.1.1.1` | 3s | Tertiary — bare IP connectivity (Cloudflare DNS) |

Any single endpoint returning a non-5xx response counts as "internet UP."

## Threshold: 2 Consecutive Failures (10 minutes)

Prevents false alarms from momentary blips. A single check failure resets the counter on next success. Two consecutive failures required before declaring DOWN.

## State Transitions

```
         ┌──────────┐
    ┌───►│  HEALTHY  │◄───┐
    │    └─────┬─────┘    │
    │          │ 2 fails  │
    │          ▼          │
    │    ┌──────────┐    │
    │    │   DOWN    │    │ recovery
    │    └─────┬─────┘    │
    │          │          │
    └──────────┘          │
     (silent)       (Discord msg)
```

- **HEALTHY → DOWN**: Output outage alert to stdout, log to Desktop. Discord delivery expected to fail.
- **DOWN → HEALTHY**: Output recovery summary (duration, fail count) to stdout. Discord delivery succeeds.
- **HEALTHY → HEALTHY**: Nothing printed, nothing logged.
- **DOWN → DOWN**: Nothing printed (no spam during extended outages).

## Interpreting the Desktop Log

```text
# Internet Health Monitor Log
# Only records outages and recoveries. No entries = everything has been fine.
[2026-05-13 05:02:00 MST] OUTAGE START: 🔴 Internet DOWN at 05:02 MST — 2 consecutive checks failed
[2026-05-13 09:06:00 MST] RECOVERY: 🟢 Internet RESTORED at 09:06 MST. Was down since 05:02 MST — 4h 4m. Consecutive failures before recovery: 49
```

**No entries** = no outages since log was created. **Multiple OUTAGE START without RECOVERY** = VPN is in zombie state (appears connected, DNS dead).
