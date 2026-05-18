# Discord Token Extraction from Hermes Config

The Hermes config at `~/.hermes/config.yaml` contains a `discord.token` field.
Reliably extracting this value is trickier than it looks — the config has
**multiple fields named `token`** (API keys, provider tokens, bot tokens), so
simple regex patterns like `r'token:\s*["\']?([^\s"\']+)["\']?'` can match the
wrong one and silently return a different credential, causing a 401 on Discord
login.

## The Gotcha

```yaml
# This is in the config — note MULTIPLE token fields at different levels:
discord:
  token: MTQ4NjA3...REAL_DISCORD_TOKEN...    # ← the one we want
providers:
  deepseek:
    token: sk-...DIFFERENT_TOKEN...          # ← NOT this one
```

A regex search for `token:` with no line context can match any of these.

## Reliable Extraction (2 methods)

### Method 1: grep + context (recommended)
```python
import subprocess, re

config_raw = subprocess.run(
    ['grep', '-n', 'token', '/home/robert/.hermes/config.yaml'],
    capture_output=True, text=True, timeout=5
)

# Preview all token lines to locate the discord one
lines = config_raw.stdout.strip().split('\n')
for line in lines:
    print(line)  # Shows line numbers, e.g. "335:  token: MTQ4..."

# Then find the line near the "discord:" section
# Or find it by searching for lines just after "discord:"
discord_line = None
config_text = subprocess.run(
    ['cat', '/home/robert/.hermes/config.yaml'],
    capture_output=True, text=True, timeout=5
).stdout

# Split on "discord:" and take the block after it
if 'discord:' in config_text:
    after_discord = config_text.split('discord:', 1)[1]
    # The token line is the first "token:" in this block
    token_match = re.search(r'token:\s*([^\s]+)', after_discord)
    if token_match:
        token = token_match.group(1).strip().strip('"').strip("'")
        print(f"Token extracted: {token[:8]}...")  # Masked for safety
```

### Method 2: Full YAML parse (requires PyYAML)
```python
import yaml, subprocess

raw = subprocess.run(
    ['cat', '/home/robert/.hermes/config.yaml'],
    capture_output=True, text=True, timeout=5
)
config = yaml.safe_load(raw.stdout)
token = config.get('discord', {}).get('token')
if token:
    print(f"Token extracted: {token[:8]}...")
```

## Verification
After extraction, verify the token starts with the expected prefix:
Discord bot tokens always start with `MT` followed by alphanumeric + dot segments.

A malformed token will produce a 401 at Discord login:
```
discord.errors.LoginFailure: Improper token has been passed.
```

## Usage
```bash
DISCORD_TOKEN="<extracted_token>" /home/robert/.hermes/hermes-agent/venv/bin/python /tmp/discord_scan.py
```
