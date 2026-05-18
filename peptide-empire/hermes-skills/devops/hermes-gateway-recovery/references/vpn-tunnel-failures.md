# VPN Tunnel Failure — Debugging & Recovery Pattern

## The Symptom
- Discord bubble is green on PC but user's messages get no response
- Gateway log shows `✓ discord connected` but no inbound messages
- User says "internet works" because browser tabs sometimes load
- Switching VPN locations instantly fixes it

## Root Cause
VirtualShield's VPN tunnel goes stale during extended idle periods (monitors off).
The tunnel is "established" but packets don't route — TCP connections break without
FIN/RST signals, so the Discord WebSocket library never detects the drop.

This is NOT detectable via log parsing alone because the log still shows the last
successful connection event. The gateway process is alive, systemd sees it as
active, and `check_discord_connected()` returns True. Everything looks healthy
from the logs — but no messages flow.

## Detection: REST API Active Probe
Added to `gateway_utils.py` as `discord_rest_reachable_sync()`:

```python
def discord_rest_reachable_sync() -> bool:
    try:
        from urllib.request import Request, urlopen
        req = Request(
            "https://discord.com/api/v10/gateway",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except Exception:
        return False
```

Key decisions:
- Uses the **unauthenticated** gateway endpoint (no token needed)
- Requires **browser User-Agent** header — Python's default urllib UA is blocked
  by Cloudflare with HTTP 403. Without the UA, probe always returns False.
- Synchronous (urllib) — watchdog runs sync, can't use asyncio

## Watchdog Integration
The watchdog runs this probe in the happy path. If log says "connected" but
REST API is unreachable for 3 consecutive checks (30 min), it treats the
gateway as disconnected and triggers safe_restart.

Total time from VPN failure to recovery: ~30 min (detection) + 5 min (grace)
+ restart time = ~35-40 min.

## False-Positive Bug Fixed (May 10, 2026)
The zombie detection path was triggering restarts on healthy gateways because:

1. `disconnect_since` timestamp was never cleared when gateway reconnected
   (happy path only cleared it on `last_state != "connected"` transition)
2. When log staleness triggered zombie detection, the old `disconnect_since`
   made `disconnect_duration` look like 20+ minutes
3. Grace period (5 min) was bypassed → immediate restart on healthy gateway

Fix: happy path now ALWAYS clears `disconnect_since` when connected, not just
on state transition. Zombie detection now cross-checks with REST API before
treating log staleness as a zombie.

## Idle Gateway ≠ Zombie
A gateway with no inbound messages for >10 minutes has a stale log but is
healthy. The original code treated any log staleness + active service as a
zombie. Fixed: log staleness + REST API unreachable = zombie. Log staleness
+ REST API OK = idle gateway (no action needed).

## VirtualShield-Specific Notes
- "Keep Alive on Sleep" is macOS-only — not available on Windows
- Kill Switch was already disabled by user
- Split tunneling is called "Local Network Access" but only bypasses LAN devices,
  not specific apps
- No app-level split tunneling available
- Switching VPN locations forces a fresh tunnel (user's manual workaround)
- Version: 5.1.8.485 (Beta channel)
