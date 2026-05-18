---
name: hermes-gateway-recovery
description: Safe gateway restart protocol — stop, restart, verify Discord reconnection. Never leave the gateway dead after a restart.
---

# Hermes Gateway Recovery Protocol

## Architecture (v2.1 — May 2026)

Three components, one shared source of truth:

| File | Role |
|------|------|
| `gateway_utils.py` | Shared module — token loading, connection detection, REST helpers |
| `discord_watchdog.py` | Cron-driven monitor (v4) — detects disconnects, zombies, triggers restarts |
| `safe_gateway_restart.py` | Restart protocol (v2) — pre-flight check, stop, start, verify |
| `hermes-gateway.service` | Systemd unit with rate-limited crash recovery |
| `gateway_autostart.sh` | WSL2 bashrc hook — auto-starts gateway on first shell after boot |
| `Hermes Gateway.cmd` | Windows Startup folder — auto-starts on every Windows logon |

**Reference docs**: `references/vpn-tunnel-failures.md` (VPN silent tunnel pattern, VirtualShield quirks), `references/watchdog-stale-timestamp-bug.md` (v4.1 stale timestamp false-positive incident)

**All scripts are in `~/.hermes/scripts/`. The shared module is imported by both scripts — no duplicate logic.**

The Startup `.cmd` is at `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Hermes Gateway.cmd` and runs `wsl systemctl --user start hermes-gateway`. This is the PRIMARY reboot defense — it fires on every Windows logon, including after power outages with "always on" BIOS. The bashrc hook is a secondary safety net.

## When to use
- Gateway is dead (no process, service failed)
- Discord disconnected (grey dot, not responding)
- Zombie detected (PID alive, log silent for >10 min)
- After `hermes update` restarts the gateway
- User requests `/restart` from Discord

## Quick recovery (if gateway is running but Discord disconnected)
```bash
systemctl --user restart hermes-gateway
# Wait 40s, then check:
grep "discord connected" ~/.hermes/logs/gateway.log | tail -1
```

## Safe restart (full protocol)
```bash
cd ~/.hermes/scripts && python3 safe_gateway_restart.py
```
This will:
0. **Pre-flight**: Verify Discord REST API is reachable (aborts if network down)
1. Warn Discord users via REST API
2. Stop the systemd service + poll for process death (not hardcoded sleep)
3. Force-kill if process doesn't die within 30s
4. Start the service
5. Poll for "discord connected" in logs (up to 3 min)
6. Classify failure: startup crash vs IP rate limit vs timeout
7. Report back to Discord with root cause

## Watchdog v4.2
- Runs every 10 min via cron (`699fe4c70e62`, `no_agent=true`)
- Uses `gateway_utils.py` for connection detection — catches ALL disconnect formats
- **Zombie detection**: if service is active but log hasn't been written to in 10 min, treats as disconnected
- **Log rotation handling**: empty/fresh log gets 15-minute grace period before escalating
- **Format change detection**: if 0 timestamps parse from non-empty log → alerted after 30 min
- **Max restarts alert**: sends Discord message via REST API when giving up (not just silent stdout)
- Anti-spiral: max 3 restarts per 2 hours
- 5 min grace period after disconnect
- 30 min cooldown between restarts
- Classifies failures: `discord_connect_timeout` (rate limit) vs `service_startup_failed` (crash)
- **v4.2 fix (May 10)**: `disconnect_since` timestamp now resets unconditionally on healthy connection AND on new disconnect detection. v4.1 reused stale timestamps across gateway restarts, causing zombie detection to bypass the grace period and kill healthy gateways. See `references/watchdog-stale-timestamp-bug.md` for full incident analysis.

## Disconnect Detection Patterns (fixed in v4)
The v3 grep patterns missed these real error formats:
- `ERROR discord.client: Attempting a reconnect in Xs` ← **was MISSED** (dot, not space)
- `ERROR gateway.run: ✗ discord error: discord connect timed out`
- `ERROR gateway.run: Gateway failed to connect ...`
- `[Discord] Disconnected`

v4 uses 10 regex patterns covering ALL known disconnect/failure formats. See `gateway_utils.py` for the full list.

## Systemd service
- Location: `~/.config/systemd/user/hermes-gateway.service`
- **Applied May 10** — all pending fixes from May 9 audit are now live:
  - `StartLimitIntervalSec=600` (was `0` = unlimited crash loops)
  - `StartLimitBurst=5` (max 5 failures in 10 min window)
  - `RestartPreventExitStatus=77` (intentional shutdown, don't restart)
  - `TimeoutStopSec=120` (was 90)
  - `TimeoutStartSec=120` (new)
- Restart=always, RestartSec=60, RestartMaxDelaySec=300, RestartSteps=5
- RestartForceExitStatus=75 (TEMPFAIL — intentional restart)
- Reload after changes: `systemctl --user daemon-reload`

## Token management
Token is loaded from `~/.hermes/config.yaml` (`discord.token`) by `gateway_utils.py`. No hardcoded tokens in any script.

## Watchdog cron
- Job ID: `699fe4c70e62`
- Runs every 10 min
- Script: `~/.hermes/scripts/discord_watchdog.py`
- `no_agent=true` (script-only, no LLM)

## WSL2 Reboot Resilience

WSL2 user systemd services do **not** survive a Windows reboot — the user session doesn't auto-start daemons. Without a hook, the gateway stays dead until manually started.

**Fix applied**: `.bashrc` sources `gateway_autostart.sh` on every interactive shell. The script checks if the gateway is already running and starts it if not. This means the gateway comes up on the first terminal window opened after reboot.

```bash
# .bashrc entry (already in place)
/home/robert/.hermes/scripts/gateway_autostart.sh &>/dev/null &
```

Script location: `~/.hermes/scripts/gateway_autostart.sh` — idempotent, silent when already running.

**Verify after reboot**:
```bash
systemctl --user is-active hermes-gateway  # should print "active"
```

## Cold-start / reboot recovery (v2.1 additions)

Two independent auto-start mechanisms ensure the gateway comes back after a Windows reboot or power outage:

| Mechanism | Trigger | File |
|-----------|---------|------|
| Windows Startup | Windows user logon | `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Hermes Gateway.cmd` |
| bashrc hook | First WSL terminal opened | `~/.bashrc` → `~/.hermes/scripts/gateway_autostart.sh` |

The Windows Startup `.cmd` fires on every Windows logon (including after power outage with "always on" BIOS). It runs `wsl systemctl --user start hermes-gateway`. The bashrc hook is a secondary safety net — it checks if the gateway is already running before starting, so it's idempotent.

Both are needed because WSL2 user systemd services do not survive Windows reboots, and WSL2 does not auto-start its VM on boot — the Startup folder bridges this gap.

## Common failure modes
1. **Systemd timeout on stop** — TimeoutStopSec=120 (was 90).
2. **Gateway tries `systemctl --user restart` from within itself** — This creates a race condition. Use the safe_restart script instead which handles the detached lifecycle.
3. **Discord rate limit (close code 4000)** — Token-level gateway suspension. Wait or regenerate token.
4. **IP-level rate limit after reconnect storm** — Service starts fine but Discord never connects. Watchdog classifies as `discord_connect_timeout`. Wait 1-2 hours for penalty to clear.
5. **Slash command sync fails (error 30032)** — Max 100 commands reached. Non-fatal, just a warning.
6. **Zombie process** — PID alive, no log writes. Watchdog detects via `log_is_stale()` and treats as disconnected.
7. **System reboot while gateway stopped** — WSL2 user services don't survive reboot. Auto-start mechanisms (Startup folder + bashrc) handle this.
8. **VPN exit node change** — Discord WebSocket session resume fails. Watchdog's grace period absorbs most transient VPN switches.
9. **VPN silent tunnel failure (idle timeout)** — The VPN tunnel goes stale during PC idle (monitors off) without any TCP close signal. The Discord WebSocket library thinks it's connected, the gateway log says "connected", but packets can't route. **This is invisible to log-based detection.** The v4.2 watchdog catches this via active REST API probes (`discord_rest_reachable_sync()`): 3 consecutive failures (30+ min of unreachable) → auto-restart. The probe uses `discord.com/api/v10/gateway` with a browser User-Agent to avoid Cloudflare blocks (Python's default urllib UA gets 403). See `references/vpn-tunnel-failures.md` for VPN-specific fixes and VirtualShield quirks.
10. **Log file rotated (empty new file)** — Watchdog enters 15-min "undetermined" grace period, then escalates to restart.
11. **Log format changed (0 timestamps parse)** — Detected via `meta['parse_failures']`. Escalates after 30 min with Discord alert.
12. **Hermes TUI closed while gateway embedded** — The systemd gateway service runs independently. You can close `hermes --tui` anytime — Discord and cron jobs continue via the service. If the systemd service is dead and only the TUI's embedded gateway is running, closing the TUI kills the gateway. Always verify `systemctl --user is-active hermes-gateway` is `active` before closing the TUI.
12. **Watchdog stale timestamp false positive** — Zombie detection reuses old `disconnect_since` from prior disconnect events, skipping the 5-min grace period and killing a healthy gateway. Symptom: gateway was connected <20 min ago, watchdog kills it. Fix: manually clean state file (`echo '{"restarts":[],"last_state":"connected","disconnect_since":0,...}' > ~/.hermes/.gateway_watchdog_state.json`) and update watchdog to v4.2. Full analysis: `references/watchdog-stale-timestamp-bug.md`.
13. **Systemd restart blocked by hung child processes** — When the safe restart script stops the gateway, sometimes `discord_watchdog.py` or `safe_gateway_restart.py` child processes outlive the stop and prevent systemd from restarting. Symptom: `systemctl stop` succeeds, but systemd never starts a new instance. Fix: `pkill -f "discord_watchdog.py|safe_gateway_restart.py"` then `systemctl --user start hermes-gateway`.
14. **WSL2 reboot** — User systemd services don't survive Windows reboots. Covered by Windows Startup `.cmd` + bashrc autostart.
15. **Discord iOS app shows gray bubble when bot is online** — Client-side presence cache. Green on desktop + gray on iPhone = iOS cache. Force-quit and reopen.
16. **Messages sent while gateway is down are silently dropped** — Discord does NOT queue messages for offline bots. Any @mention sent while the gateway process is dead will never be delivered.

## Discord message style
- Use clean formatting: bold headers, single-line bullet points (▸), code blocks for diagrams
- Avoid raw markdown tables (if included) — Discord doesn't render them natively and they show as messy text
- Keep status reports tight: bold section headers + emoji status + one-liner details
```bash
# Service status
systemctl --user status hermes-gateway

# Recent gateway logs
tail -50 ~/.hermes/logs/gateway.log

# Discord connection events (new patterns cover all formats)
grep -E "discord|close code|websocket close|heartbeat" ~/.hermes/logs/gateway.log | tail -10

# Watchdog state
cat ~/.hermes/.gateway_watchdog_state.json

# Test shared module
cd ~/.hermes/scripts && python3 -c "from gateway_utils import *; print(check_discord_connected(), log_is_stale(), service_active())"

# Dry-run watchdog
cd ~/.hermes/scripts && python3 discord_watchdog.py

# Force restart (bypass safety — use only if safe_restart script can't run)
systemctl --user stop hermes-gateway
sleep 5
systemctl --user start hermes-gateway

# Verify Discord REST API (bypasses WebSocket)
cd ~/.hermes/scripts && python3 -c "
import asyncio
from gateway_utils import discord_rest_reachable
print(asyncio.run(discord_rest_reachable()))
"
```

## Supporting References
- `references/vpn-tunnel-failures.md` — Deep-dive on VPN silent tunnel failures: detection via REST API probe, false-positive zombie bug that was fixed, urllib User-Agent block workaround, VirtualShield-specific limitations
# Discord mobile cache check — if green on desktop but gray on iPhone:
# → Force-quit iOS Discord app and reopen (not a gateway issue)
```
