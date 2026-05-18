# Discord Gateway Diagnostic Steps

Full layered diagnostic to isolate whether a Discord connection failure is token, network, WebSocket, or rate-limit related.

## Step 1: Gateway Process Health

```bash
# Is the gateway running?
ps aux | grep "hermes_cli.main gateway"

# Is it a zombie? (alive but not logging)
stat ~/.hermes/logs/gateway.log | grep Modify
# If modification time is hours old → zombie, kill it
pkill -9 -f "hermes_cli.main gateway"
```

## Step 2: Network Layer

```bash
# DNS resolution
python -c "import socket; print(socket.getaddrinfo('gateway.discord.gg', 443, socket.AF_INET, socket.SOCK_STREAM)[0][4][0])"

# TCP connectivity
python -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)
s.connect(('gateway.discord.gg', 443))
print('TCP OK')
s.close()
"
```

## Step 3: REST API Token Validation

```python
import asyncio, aiohttp

TOKEN = "YOUR_BOT_TOKEN"
headers = {"Authorization": f"Bot {TOKEN}"}

async def test():
    async with aiohttp.ClientSession() as s:
        # Token validity
        async with s.get("https://discord.com/api/v10/users/@me", headers=headers) as r:
            if r.status == 200:
                data = await r.json()
                print(f"✅ Token valid: {data['username']}#{data['discriminator']}")
            elif r.status == 401:
                print("❌ Token INVALID — regenerate")
            elif r.status == 429:
                print(f"⏳ Rate limited: retry_after={r.headers.get('Retry-After')}")
        
        # Guild access
        async with s.get("https://discord.com/api/v10/users/@me/guilds", headers=headers) as r:
            guilds = await r.json()
            print(f"Guilds: {len(guilds)}")
            for g in guilds:
                print(f"  - {g['name']} (ID: {g['id']})")

asyncio.run(test())
```

## Step 4: WebSocket HELLO (no auth)

```python
import asyncio, aiohttp, json

async def test():
    async with aiohttp.ClientSession() as s:
        ws = await s.ws_connect('wss://gateway.discord.gg/?v=10&encoding=json')
        msg = await ws.receive(timeout=10)
        data = json.loads(msg.data)
        print(f"HELLO: op={data['op']} heartbeat={data['d']['heartbeat_interval']}ms")
        await ws.close()

asyncio.run(test())
```

## Step 5: Full IDENTIFY Handshake (with close-code detection)

This is the critical test. Discord can reject IDENTIFY in two ways:

- **Silent blackhole**: no response at all → IP-level rate limit
- **Close code 4000**: WebSocket cleanly closes with code 4000 → token-level gateway suspension

```python
import asyncio, aiohttp, json

TOKEN = "YOUR_BOT_TOKEN"

async def test():
    async with aiohttp.ClientSession() as s:
        ws = await s.ws_connect('wss://gateway.discord.gg/?v=10&encoding=json')
        hello = await asyncio.wait_for(ws.receive(), timeout=15)
        hb = json.loads(hello.data)['d']['heartbeat_interval'] / 1000
        print(f"HELLO received (hb={hb}s)")
        
        # Identify
        await ws.send_json({
            "op": 2,
            "d": {
                "token": TOKEN,
                "intents": 512,  # Minimal: GUILD_MESSAGES only
                "properties": {"os": "linux", "browser": "hermes", "device": "hermes"}
            }
        })
        print("IDENTIFY sent — waiting...")
        
        for _ in range(60):
            try:
                msg = await asyncio.wait_for(ws.receive(), timeout=1)
                raw = msg.data
                
                if raw is None:
                    print("   WebSocket closed cleanly (no close code)")
                    return
                
                if isinstance(raw, int):
                    # This is a close code
                    if raw == 4000:
                        print(f"❌ CLOSE CODE {raw} — token-level gateway suspension")
                        print("   Discord is rejecting this token. VPN change won't help.")
                        print("   Fix: wait 2-6h or regenerate token.")
                    else:
                        print(f"❌ CLOSE CODE {raw}")
                    return
                
                if isinstance(raw, str):
                    data = json.loads(raw)
                    op, t = data.get('op'), data.get('t', '')
                    if op == 0 and t == 'READY':
                        print(f"✅ READY! {data['d']['user']['username']}")
                        return
                    elif op == 9:
                        print(f"INVALID_SESSION (resumeable={data.get('d')})")
                        return
                    elif op == 1:  # Heartbeat request
                        await ws.send_json({"op": 11, "d": None})
                    elif op == 11:  # Heartbeat ACK
                        pass
                    else:
                        print(f"   op={op} t={t}")
            except asyncio.TimeoutError:
                pass
        else:
            print("❌ IDENTIFY BLACKHOLE (Pattern A)")
            print("   Discord silently ignored IDENTIFY — IP-level rate limit.")
            print("   Fix: Change VPN exit or wait 1-3h.")
        
        await ws.close()

asyncio.run(test())
```

**Close code reference:**
| Code | Meaning | Likely Cause |
|------|---------|-------------|
| 4000 | Unknown error | Token-level gateway suspension |
| 4004 | Authentication failed | Invalid token |
| 4008 | Rate limited | Too many IDENTIFY attempts |
| 4009 | Session timeout | Session expired, resume failed |
| 4013 | Invalid intent(s) | Intents not enabled in Developer Portal |

## Step 6: REST API Message Send (bypass WebSocket)

Even when WebSocket is blackholed, REST message sends often work:

```python
import asyncio, aiohttp

TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_ID = "1484946244768895056"  # hermes-chat

async def test():
    headers = {"Authorization": f"Bot {TOKEN}"}
    payload = {"content": "🔧 Test message via REST API"}
    async with aiohttp.ClientSession() as s:
        async with s.post(f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages",
                         headers=headers, json=payload) as r:
            if r.status == 200:
                data = await r.json()
                print(f"✅ Message sent! ID: {data['id']}")
            else:
                print(f"Status {r.status}: {await r.text()}")

asyncio.run(test())
```

## Decision Tree

```
Gateway process alive?
├─ No → Start gateway (watchdog handles this)
└─ Yes → Check gateway.log modification time
    ├─ Old (>1hr ago) → Zombie! Kill and restart
    └─ Recent → Run layered diagnostics:
        ├─ Step 2 (Network): TCP fails? → VPN/firewall issue
        ├─ Step 3 (REST token): 401? → Token expired, regenerate
        ├─ Step 3 (REST token): 429? → Rate limited, wait
        ├─ Step 4 (WS HELLO): Fails? → Network blocks WebSocket
        ├─ Step 5 (IDENTIFY): Silent timeout? → Pattern A (IP-level rate limit)
        │   └─ Change VPN exit or wait 1-3 hours
        ├─ Step 5 (IDENTIFY): Close code 4000? → Pattern B (token suspension)
        │   └─ VPN won't help. Wait 2-6h or regenerate token.
        ├─ Step 5 (IDENTIFY): Close code 4004? → Token invalid
        ├─ Step 5 (IDENTIFY): Close code 4008? → Explicit rate limit (rare)
        └─ Step 6 (REST send): Works? → Token valid, use REST as fallback
            while waiting for gateway ban to lift
```
