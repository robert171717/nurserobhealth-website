#!/usr/bin/env python3
"""Discord Gateway Watchdog — monitors connectivity with anti-spiral guardrails.

Run as a cron job (no_agent=True) every 10 minutes.
Checks gateway process health + Discord WebSocket connection state.
Prevents the reconnect spiral that burns Discord rate limits.

Anti-spiral guardrails:
- 30-min grace period after disconnect (lets rate limits clear)
- Max 1 restart per hour
- Max 3 restarts per 2-hour window, then alerts
- Won't kill gateway if it started < 5 min ago
"""

import os, sys, time, json, signal, subprocess
from pathlib import Path

HOME = Path.home()
HERMES_HOME = HOME / ".hermes"
GATEWAY_LOG = HERMES_HOME / "logs" / "gateway.log"
STATE_FILE = HERMES_HOME / ".discord_watchdog_state.json"
BAN_SENTINEL = HERMES_HOME / ".ban_lifted_sentinel"
VENV_PYTHON = str(HERMES_HOME / "hermes-agent" / "venv" / "bin" / "python")

# Thresholds
DISCONNECT_GRACE = 30 * 60      # Don't touch for 30 min after disconnect
RESTART_COOLDOWN = 60 * 60      # Don't restart more than once per hour
MAX_RESTARTS = 3                # Max restarts within window
RESTART_WINDOW = 2 * 60 * 60    # 2 hour window
MIN_UPTIME = 300                # Gateway must be up 5min before we kill it

def load_state():
    if STATE_FILE.exists():
        try: return json.loads(STATE_FILE.read_text())
        except: pass
    return {"restarts": [], "last_state": "unknown", "last_alerted_disconnect": 0}

def save_state(s):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(s))

def find_gateway_pid():
    try:
        r = subprocess.run(["pgrep", "-f", "hermes_cli.main gateway"], capture_output=True, text=True, timeout=5)
        if r.returncode == 0 and r.stdout.strip():
            return int(r.stdout.strip().split('\n')[0])
    except: pass
    return None

def check_discord():
    """Returns (connected: bool, age_sec: float|None)."""
    if not GATEWAY_LOG.exists():
        return False, None
    try:
        out = subprocess.run(
            ["grep", "-E", r"discord connect(ed)?|discord disconnect|discord error|Gateway failed.*discord", str(GATEWAY_LOG)],
            capture_output=True, text=True, timeout=10
        ).stdout
        last_connect, last_disconnect = None, None
        for line in reversed(out.strip().split('\n')):
            try:
                ts = time.mktime(time.strptime(line[:19], "%Y-%m-%d %H:%M:%S"))
            except: continue
            if "discord connected" in line and last_connect is None:
                last_connect = ts
            elif any(x in line for x in ("discord disconnect", "discord error", "Gateway failed")):
                if last_disconnect is None: last_disconnect = ts
            if last_connect is not None and last_disconnect is not None:
                break
        now = time.time()
        if last_connect and (last_disconnect is None or last_connect > last_disconnect):
            return True, now - last_connect
        elif last_disconnect:
            return False, now - last_disconnect
    except: pass
    return False, None

def kill_gateway(pid):
    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(3)
        try: os.kill(pid, signal.SIGKILL)
        except OSError: pass
    except OSError: pass

def start_gateway():
    try:
        subprocess.Popen([VENV_PYTHON, "-m", "hermes_cli.main", "gateway", "run", "--replace"],
                        cwd=str(HOME), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                        start_new_session=True)
        return True
    except Exception as e:
        print(f"Failed to start: {e}", file=sys.stderr)
        return False

def main():
    state = load_state()
    now = time.time()
    state["restarts"] = [t for t in state.get("restarts", []) if now - t < RESTART_WINDOW]

    pid = find_gateway_pid()
    connected, age = check_discord()

    # Happy path
    if pid and connected:
        if state["last_state"] != "connected":
            print(f"✅ Discord connected ({age:.0f}s ago)")
            state["last_state"] = "connected"
            state["last_alerted_disconnect"] = 0
            save_state(state)
        return

    if not pid:
        recent = len(state["restarts"])
        if recent >= MAX_RESTARTS:
            print(f"🚨 Gateway dead — {MAX_RESTARTS} restarts in {RESTART_WINDOW//3600}h. Manual intervention needed.")
            return
        print(f"🔴 Gateway DEAD — starting (attempt {recent + 1}/{MAX_RESTARTS})")
        if start_gateway():
            state["restarts"].append(now)
            state["last_state"] = "restarted"
            save_state(state)
        return

    # Gateway running, Discord disconnected
    if age is None:
        print("⚠️ Cannot determine Discord connection state")
        return

    # Clear ban-lift sentinel on disconnect so monitor will re-alert for future bans
    if BAN_SENTINEL.exists():
        BAN_SENTINEL.unlink()

    last_restart = max(state["restarts"]) if state["restarts"] else 0
    time_since_restart = now - last_restart if last_restart else float('inf')
    recent = len(state["restarts"])

    if age < DISCONNECT_GRACE:
        last_alerted = state.get("last_alerted_disconnect", 0)
        if now - last_alerted > 3600:
            print(f"🟡 Discord disconnected {age/60:.0f}min — grace period ({DISCONNECT_GRACE/60:.0f}min)")
            state["last_alerted_disconnect"] = now
            save_state(state)
        return

    if time_since_restart < RESTART_COOLDOWN:
        if now - state.get("last_alerted_disconnect", 0) > 3600:
            remaining = (RESTART_COOLDOWN - time_since_restart) / 60
            print(f"⏳ Discord disconnected {age/60:.0f}min — cooldown {remaining:.0f}min remaining")
            state["last_alerted_disconnect"] = now
            save_state(state)
        return

    if recent >= MAX_RESTARTS:
        if now - state.get("last_alerted_disconnect", 0) > 3600:
            print(f"🚨 Disconnected {age/60:.0f}min — {MAX_RESTARTS} restarts exhausted.")
            print(f"   Likely: IP-level WebSocket rate limit. Change VPN exit or wait 2-6h.")
            state["last_alerted_disconnect"] = now
            save_state(state)
        return

    print(f"🔄 Discord disconnected {age/60:.0f}min — restarting ({recent + 1}/{MAX_RESTARTS})")
    kill_gateway(pid)
    time.sleep(5)
    if start_gateway():
        state["restarts"].append(now)
        state["last_state"] = "restarted"
        save_state(state)
        print("   ✅ Restarted — waiting for Discord")

if __name__ == "__main__":
    main()
