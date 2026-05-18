---
description: Set up and configure Discord bot integration with Hermes Agent
name: discord-setup
related_skills: []
---

# Discord Setup & Configuration for Hermes Agent

Set up and configure Discord bot integration with Hermes Agent.

## Prerequisites

- Discord application created at https://discord.com/developers/applications
- Bot token obtained from the Bot tab in Discord Developer Portal

## Quick Start

### 1. Add Token to Config

Edit your config file and add/update the discord section:

```yaml
discord:
  token: "YOUR_BOT_TOKEN_HERE"
  require_mention: false
  auto_thread: true
  free_response_channels: []  # Leave empty for all channels, or specify ['channel-name'] to restrict
```

### 2. Invite Bot to Server

1. Go to Discord Developer Portal → Your Application → OAuth2 → URL Generator
2. Select scopes: `bot`
3. Select permissions: Send Messages, Read Message History, Embed Links, Attach Files
4. Copy generated URL and open in browser
5. Select server and authorize

### 3. Test Connection

Use the Hermes venv Python (discord.py is pre-installed there):

```python
import discord

TOKEN = "YOUR_BOT_TOKEN_HERE"
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✓ Connected as {client.user.name} (ID: {client.user.id})")
    print(f"Servers accessible: {len(client.guilds)}")
    for guild in client.guilds:
        print(f"  - {guild.name}")
    await client.close()

client.run(TOKEN)
```

Run with: `/home/robert/.hermes/hermes-agent/venv/bin/python test_discord.py`

## Channel Restrictions

To restrict bot responses to specific channels only:

```yaml
discord:
  free_response_channels: ['hermes-chat', 'bot-commands']
```

Bot will ONLY respond in listed channels. All others are ignored.

## Troubleshooting

For connection failures, disconnects, rate-limiting, and WebSocket issues, load the `discord-gateway-troubleshooting` skill which covers reconnect spirals, IP-level rate limit blackholes, zombie gateway detection, and includes diagnostic scripts and a watchdog.

### Token Not Working
- Ensure token is copied exactly (no extra spaces)
- Some setups require `bot TOKEN` prefix, others just `TOKEN`
- Check Discord Developer Portal for token validity

### discord.py Not Found
```bash
# Use the Hermes venv Python which has discord.py pre-installed
/home/robert/.hermes/hermes-agent/venv/bin/python -c "import discord; print(discord.__version__)"
```

### Bot Can't Send Messages
- Check bot role permissions in server settings
- Ensure bot has "Send Messages" permission for target channel
- Verify bot was invited with correct OAuth2 scopes

### Test Channel Restrictions
To verify `free_response_channels` is working correctly, test with a channel-specific script:

```python
import discord

TOKEN = "YOUR_TOKEN"
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        for channel in guild.text_channels:
            if channel.name == "hermes-chat":  # Target specific channel
                await channel.send("✅ Test message")
                print(f"Message sent to {channel.name}")
                await client.close()
                return

client.run(TOKEN)
```

Run with: `/home/robert/.hermes/hermes-agent/venv/bin/python test_script.py`

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `token` | required | Discord bot token from Developer Portal |
| `require_mention` | false | If true, only respond when @mentioned |
| `auto_thread` | true | Create threads for organized conversations |
| `free_response_channels` | [] | Empty = all channels; list = restrict to these |

## Security Notes

- Never commit Discord tokens to version control
- Regenerate token if accidentally exposed (Discord Developer Portal → Bot → Reset Token)
- Store sensitive tokens in config file, not in memory or logs