# Nurse Rob Peptide Empire — Defense Architecture

## Five-Layer Defense Grid

```
VPN DROPS → Watchdog detects (30min) → Gateway recovers → Cron jobs resume
  → Any failed jobs → Recovery Watchdog re-runs (30min)
  → MAX DOWNTIME: ~1 hour, fully automatic
```

| Layer | Component | What It Catches | Recovery Time | Cost |
|-------|-----------|-----------------|---------------|------|
| 1 | systemd Restart=always | Gateway process crash | 60s | $0 |
| 2 | Discord Watchdog (10min) | Zombie process, silent WebSocket death, VPN tunnel failure | 10-40min | $0 |
| 3 | VPN REST API probe | Packets not routing even though tunnel "established" | 30min (3 checks) | $0 |
| 4 | Empire Recovery Watchdog (30min) | Cron jobs that errored during outage | 30-60min post-recovery | API calls |
| 5 | Windows Startup .cmd + bashrc | System reboot (WSL2 doesn't survive reboots) | On next Windows logon | $0 |

## Single Points of Failure

### xurl OAuth2 Token
ALL X/Twitter operations depend on `~/.xurl` having a valid OAuth2 token. When
the token expires or is saved to the wrong app profile, these jobs fail:
- Daily Content Generation → Morning Post → Evening Post
- Lead Scan (all 4 daily scans)
- Lead Nurture AM

**Fix:** `xurl auth oauth2 --app nurse-rob` then `xurl auth default nurse-rob`

### VPN (VirtualShield)
ALL internet-dependent operations fail when VPN tunnel is stale:
- X posting (xurl)
- Lead scanning (X API + Discord)
- Welcome emails (Fastmail SMTP)
- FDA scans / Pharmacy outreach (web_search)
- Content generation (web_search for intel, but LLM call still works)

Jobs that survive VPN failure:
- Dashboard summary (local file ops)
- Content optimizer (local file ops)

### Gateway Process
The cron scheduler runs INSIDE the gateway process. Gateway down = ALL cron dead.
Systemd + Watchdog + Recovery layers mitigate this.

## Cron Job Inventory (May 2026)

| Job ID | Name | Schedule | Internet? | Status |
|--------|------|----------|-----------|--------|
| 31d78cdb31c7 | Daily Content Gen | 07:00 daily | Yes (web_search) | Monitored |
| 79165fb0ded9 | Morning Post (9AM) | 08:55 daily | Yes (xurl) | Monitored |
| 1a089193f391 | Evening Post (5PM) | 16:55 daily | Yes (xurl) | Monitored |
| bbb877c9914b | Lead Scan Morning | 06:00 daily | Yes (xurl+Discord) | Monitored |
| 4ca2214e78bc | Lead Scan Midday | 12:00 daily | Yes (xurl+Discord) | Monitored |
| bc118c2566c7 | Lead Scan Evening | 18:00 daily | Yes (xurl+Discord) | Monitored |
| 4f8f1279accd | Lead Scan Overnight | 00:00 daily | Yes (xurl+Discord) | Monitored |
| b3f8a1c7affb | Lead Nurture AM | 09:00 daily | Yes (himalaya) | Monitored |
| c867443fbc9e | Dashboard Summary | 21:00 daily | No (local) | Monitored |
| 0116a00191b7 | FDA Weekly Scan | Mon 08:00 | Yes (web_search) | Monitored |
| b90f811c3ac0 | Pharmacy Outreach | Tue 10:00 | Yes (himalaya) | Monitored |
| b7b116c1b3de | Pharmacy Scout | Wed 09:00 | Yes (web_search) | Monitored |
| 310c9648b0de | Affiliate Report | Sun 17:00 | Yes (web) | Monitored |
| 48f0ef333cfe | Weekly Analytics | Sun 18:00 | No (local) | Monitored |
| 7e200a12172d | Monthly Content Batch | 1st 08:00 | Yes (LLM) | Monitored |
| d6cd60ff0551 | Welcome Email | */30 min | Yes (himalaya) | Monitored |
| 4e4bbf5dcb38 | Content Optimizer | Sun 02:00 | No (local) | Monitored |
| c038d43687db | Empire Recovery | */30 min | Yes (recovery) | Monitored |
| 699fe4c70e62 | Discord Watchdog | */10 min | Yes (REST probe) | no_agent |
