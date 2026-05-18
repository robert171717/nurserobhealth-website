# Watchdog Stale Timestamp Bug — Incident Report

**Date**: May 10, 2026  
**Watchdog version**: v4.1 (buggy) → fixed in v4.2  
**Impact**: False-positive restart killing a healthy gateway

## Root Cause

The watchdog's `disconnect_since` timestamp was never cleared when the gateway reconnected normally. The happy path only cleared it on state *transition* (`last_state != "connected"`), not when the state was already "connected". This meant:

1. Gateway restarts at 09:50 (manual test)
2. Gateway connects at 09:51
3. `disconnect_since` still holds 09:50 timestamp ← **NEVER CLEARED**
4. Watchdog runs at 10:00: happy path, but `last_state` is already "connected" → `disconnect_since` STILL NOT cleared
5. Watchdog runs at 10:10: log is stale (18 min no writes) → zombie detected
6. `disconnect_duration = now - disconnect_since = 10:10 - 09:50 = 20 min`
7. 20 min > 5 min grace → **RESTART TRIGGERED on healthy gateway**

## Full Timeline

```
09:50 — Gateway stopped (manual test of startup script)
09:51 — Gateway started, Discord connected ✓
       disconnect_since = 09:50 in state file (from the stop event)
10:00 — Watchdog: happy path, returns without clearing disconnect_since
10:10 — Watchdog: log stale 18min → zombie → disconnect_duration 20min > grace → KILLS GATEWAY
10:11 — Gateway dead, systemd blocked by hung child processes
10:46 — Manual restart, bug discovered and fixed
```

## Fix (v4.2)

**Problem 1 — Happy path doesn't clear stale timestamps unconditionally:**

```python
# BEFORE (v4.1 — BUG)
if connected and svc_active:
    if state["last_state"] != "connected":  # ONLY on transition
        state["disconnect_since"] = 0
    return

# AFTER (v4.2 — FIXED)
if connected and svc_active:
    # Always clear disconnect timestamp if we're connected
    if state.get("disconnect_since", 0) != 0:
        state["disconnect_since"] = 0
        needs_save = True
    # ... rest of happy path
```

**Problem 2 — Zombie detection reuses old disconnect_since:**

```python
# BEFORE (v4.1 — BUG)
if state.get("disconnect_since", 0) == 0:
    state["disconnect_since"] = now  # Only sets if 0 — keeps old value!

# AFTER (v4.2 — FIXED)
if state.get("disconnect_since", 0) == 0 or stale or state.get("last_state") == "connected":
    state["disconnect_since"] = now  # Reset on new disconnect, zombie, or transition
```

## Manual Recovery

If this bug recurs (stale state file poisoning):

```bash
# Reset state to clean
echo '{"restarts": [], "last_state": "connected", "last_alerted": 0, "disconnect_since": 0, "vpn_failures": 0}' > ~/.hermes/.gateway_watchdog_state.json

# Kill hung child processes
pkill -f "discord_watchdog.py|safe_gateway_restart.py"

# Restart gateway
systemctl --user start hermes-gateway
```
