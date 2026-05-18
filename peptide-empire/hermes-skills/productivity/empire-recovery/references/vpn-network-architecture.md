# VPN Network Architecture — WSL2 + Hermes Agent

## Hard Architecture Reality

```
┌─────────────────────────────────────────┐
│  WINDOWS HOST                            │
│  ┌──────────────────────────────────┐    │
│  │  VirtualShield (GUI-only)        │    │
│  │  - No CLI, no API, no scripting  │    │
│  │  - "Connect Automatically" toggle │    │
│  └──────────────────────────────────┘    │
│                    │                      │
│              Network Stack                │
│                    │                      │
│  ┌──────────────────────────────────┐    │
│  │  WSL2 (Linux)                    │    │
│  │  - Inherits Windows network      │    │
│  │  - Hermes Agent, cron jobs       │    │
│  │  - himalaya, xurl, curl          │    │
│  │  - CANNOT control Windows VPN    │    │
│  └──────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

**The boundary**: A VPN CLI running inside WSL2 (e.g., `mullvad connect`) controls the Linux network stack inside WSL2 — NOT the Windows VPN. WSL2 traffic goes through whatever tunnel Windows provides. You cannot switch VPN locations from inside WSL2 unless the VPN provider has a Windows CLI.

## Current State: VirtualShield

- **Type**: GUI-only consumer VPN, no CLI, no API
- **Recovery**: "Connect Automatically" toggle (enabled for Wi-Fi + wired)
- **Failure mode**: After network disruption (router reboot, ISP blip), reconnection can enter a "zombie" state — app shows connected, DNS resolution is dead
- **Manual fix**: Open VirtualShield, switch to a different location, reconnect
- **Automation**: None possible. No way to script a recovery.

## Upgrade Path: Mullvad VPN

**Why Mullvad**:
- Windows app has a CLI: `mullvad.exe` on Windows
- Callable from WSL2 via: `powershell.exe -Command "mullvad relay set location us"`
- Strong privacy (cash/Monero, RAM-only servers, audited)
- €5/month flat

**Bridge pattern**:
```bash
# From WSL2 terminal:
powershell.exe -Command "mullvad relay set location us"
powershell.exe -Command "mullvad connect"
```

This would enable an auto-recovery watchdog that switches VPN locations when connectivity is lost for 15+ minutes.

## Current Router Situation

- **Router**: Old, unreliable — scheduled reboots Mon/Wed/Fri at 5AM MST
- **New router**: ASUS BE6500 Dual Band RT-BE82U (on desk, not yet installed)
- **Impact**: Every router reboot forces VPN reconnection → 3 opportunities/week for zombie VPN state
- **Fix**: Install new router → cancel scheduled reboots → eliminate forced VPN reconnections

## Tailscale Note

Tailscale is a mesh overlay (device-to-device), NOT an outbound privacy VPN. It doesn't provide IP diversity for X posting or lead scanning. Not suitable as a VirtualShield replacement for this use case.
