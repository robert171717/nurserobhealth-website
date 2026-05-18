#!/usr/bin/env python3
"""Discord Gateway Ban Monitor — polls WebSocket IDENTIFY. Alerts once when ban lifts.

Run as a cron job (no_agent=True, deliver=origin) every 5 minutes.
Uses a sentinel file to prevent re-alerting. The watchdog clears it on disconnect
so the monitor will re-alert for future bans.

When the ban lifts:
- Prints alert to cron output (delivered to origin chat)
- Sends a Discord message to the configured channel via REST API
- Exits 0 silently on subsequent runs (sentinel exists)
"""

import asyncio, aiohttp, json, sys, os
from pathlib import Path

TOKEN = "YOUR_BOT_TOKEN_HERE"
CHANNEL_ID = "YOUR_CHANNEL_ID_HERE"
SENTINEL = Path.home() / ".hermes" / ".ban_lifted_sentinel"

async def try_identify():
    session = aiohttp.ClientSession()
    try:
        ws = await session.ws_connect(
            'wss://gateway.discord.gg/?v=10&encoding=json',
            timeout=aiohttp.ClientTimeout(total=10)
        )
        hello = json.loads((await asyncio.wait_for(ws.receive(), timeout=10)).data)
        
        await ws.send_json({
            "op": 2, "d": {
                "token": TOKEN, "intents": 0,
                "properties": {"os": "linux", "browser": "hermes", "device": "hermes"}
            }
        })
        
        for _ in range(10):
            try:
                msg = await asyncio.wait_for(ws.receive(), timeout=1)
                raw = msg.data
                if raw is None or isinstance(raw, int):
                    await ws.close(); await session.close()
                    return False
                if isinstance(raw, str):
                    data = json.loads(raw)
                    if data.get('op') == 0 and data.get('t') == 'READY':
                        username = data['d']['user']['username']
                        await ws.close(); await session.close()
                        return True
                    elif data.get('op') == 9:
                        await ws.close(); await session.close()
                        return False
                    elif data.get('op') == 1:
                        await ws.send_json({"op": 11, "d": None})
            except asyncio.TimeoutError:
                pass
        
        await ws.close(); await session.close()
        return False
    except:
        await session.close()
        return False

async def send_discord(msg: str):
    try:
        async with aiohttp.ClientSession() as s:
            headers = {"Authorization": f"Bot {TOKEN}"}
            async with s.post(
                f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages",
                headers=headers, json={"content": msg},
                timeout=aiohttp.ClientTimeout(total=10)
            ) as r:
                return r.status == 200
    except:
        return False

async def main():
    # Already alerted — stay silent
    if SENTINEL.exists():
        sys.exit(0)
    
    ok = await try_identify()
    
    if ok:
        msg = "🟢 **Discord gateway ban LIFTED** — gateway reconnecting now. Green dot incoming."
        await send_discord(msg)
        SENTINEL.write_text("ban_lifted")
        print(msg)
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
