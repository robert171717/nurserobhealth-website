---
name: hermes-agent-setup
description: Help users configure Hermes Agent — CLI usage, setup wizard, model/provider selection, tools, skills, voice/STT/TTS, gateway, and troubleshooting. Use when someone asks to enable features, configure settings, or needs help with Hermes itself.
version: 1.1.0
author: Hermes Agent
tags: [setup, configuration, tools, stt, tts, voice, hermes, cli, skills]
---

# Hermes Agent Setup & Configuration

Use this skill when a user asks about configuring Hermes, enabling features, setting up voice, managing tools/skills, or troubleshooting.

## Key Paths

- Config: `~/.hermes/config.yaml`
- API keys: `~/.hermes/.env`
- Skills: `~/.hermes/skills/`
- Hermes install: `~/.hermes/hermes-agent/`
- Venv: `~/.hermes/hermes-agent/venv/`

## CLI Overview

Hermes is used via the `hermes` command (or `python -m hermes_cli.main` from the repo).

### Core commands:

```
hermes                          Interactive chat (default)
hermes chat -q "question"       Single query, then exit
hermes chat -m MODEL            Chat with a specific model
hermes -c                       Resume most recent session
hermes -c "project name"        Resume session by name
hermes --resume SESSION_ID      Resume by exact ID
hermes -w                       Isolated git worktree mode
hermes -s skill1,skill2         Preload skills for the session
hermes --yolo                   Skip dangerous command approval
```

### Configuration & setup:

```
hermes setup                    Interactive setup wizard (provider, API keys, model)
hermes model                    Interactive model/provider selection
hermes config                   View current configuration
hermes config edit              Open config.yaml in $EDITOR
hermes config set KEY VALUE     Set a config value directly
hermes login                    Authenticate with a provider
hermes logout                   Clear stored auth
hermes doctor                   Check configuration and dependencies
```

### Tools & skills:

```
hermes tools                    Interactive tool enable/disable per platform
hermes skills list              List installed skills
hermes skills search QUERY      Search the skills hub
hermes skills install NAME      Install a skill from the hub
hermes skills config            Enable/disable skills per platform
```

### Gateway (messaging platforms):

```
hermes gateway run              Start the messaging gateway
hermes gateway install          Install gateway as background service
hermes gateway status           Check gateway status
```

### Session management:

```
hermes sessions list            List past sessions
hermes sessions browse          Interactive session picker
hermes sessions rename ID TITLE Rename a session
hermes sessions export ID       Export session as markdown
hermes sessions prune           Clean up old sessions
```

### Other:

```
hermes status                   Show status of all components
hermes updates                  Check for updates
hermes update                   Update to latest version
hermes pairing                  Manage DM authorization codes
```

### Cron jobs:

```bash
hermes cron list                List all scheduled jobs with status
hermes cron status              Check if cron scheduler is running

# Create a cron job — schedule and prompt are POSITIONAL args:
hermes cron create "0 7 * * *" "Task description here" \
  --name "Job Name" \
  --skill "skill_name"          # --skill is repeatable for multiple skills

# Examples:
hermes cron create "55 7 * * *" "Push morning post to X." \
  --name "Morning Post" --skill "content_scheduler"

hermes cron create "0 8 * * 1" "Weekly FDA scan." \
  --name "FDA Weekly" --skill "fda_monitor"

# Manage jobs:
hermes cron run [job_id]        # Run a job immediately
hermes cron pause [job_id]      # Pause a job
hermes cron resume [job_id]     # Resume a paused job
hermes cron remove [job_id]     # Delete a job
hermes cron edit [job_id]       # Edit a job's settings
```

**Gotcha:** `hermes cron create` uses positional arguments for schedule and prompt — NOT `--schedule` or `--prompt` flags. `--skill` is singular and repeatable, NOT `--skills` with a comma-separated list.

## Setup Wizard (`hermes setup`)

The interactive setup wizard walks through:
1. **Provider selection** — OpenRouter, Anthropic, OpenAI, Google, DeepSeek, and many more
2. **API key entry** — stores securely in the env file
3. **Model selection** — picks from available models for the chosen provider
4. **Basic settings** — reasoning effort, tool preferences

Run it from terminal:
```bash
cd ~/.hermes/hermes-agent
source venv/bin/activate
python -m hermes_cli.main setup
```

To change just the model/provider later: `hermes model`

## Skills Configuration (`hermes skills`)

Skills are reusable instruction sets that extend what Hermes can do.

### Managing skills:

```bash
hermes skills list              # Show installed skills
hermes skills search "docker"   # Search the hub
hermes skills install NAME      # Install from hub
hermes skills config            # Enable/disable per platform
```

### Per-platform skill control:

`hermes skills config` opens an interactive UI where you can enable or disable specific skills for each platform (cli, telegram, discord, etc.). Disabled skills won't appear in the agent's available skills list for that platform.

### Loading skills in a session:

- CLI: `hermes -s skill-name` or `hermes -s skill1,skill2`
- Chat: `/skill skill-name`
- Gateway: type `/skill skill-name` in any chat

## Voice Messages (STT)

Voice messages from Telegram/Discord/WhatsApp/Slack/Signal are auto-transcribed when an STT provider is available.

### Provider priority (auto-detected):
1. **Local faster-whisper** — free, no API key, runs on CPU/GPU
2. **Groq Whisper** — free tier, needs GROQ_API_KEY
3. **OpenAI Whisper** — paid, needs VOICE_TOOLS_OPENAI_KEY

### Setup local STT (recommended):

```bash
cd ~/.hermes/hermes-agent
source venv/bin/activate
pip install faster-whisper
```

Add to config.yaml under the `stt:` section:
```yaml
stt:
  enabled: true
  provider: local
  local:
    model: base  # Options: tiny, base, small, medium, large-v3
```

Model downloads automatically on first use (~150 MB for base).

### Setup Groq STT (free cloud):

1. Get free key from https://console.groq.com
2. Add GROQ_API_KEY to the env file
3. Set provider to groq in config.yaml stt section

### Verify STT:

After config changes, restart the gateway (send /restart in chat, or restart `hermes gateway run`). Then send a voice message.

## Voice Replies (TTS)

Hermes can reply with voice when users send voice messages.

### TTS providers (set API key in env file):

| Provider | Env var | Free? |
|----------|---------|-------|
| ElevenLabs | ELEVENLABS_API_KEY | Free tier |
| OpenAI | VOICE_TOOLS_OPENAI_KEY | Paid |
| Kokoro (local) | None needed | Free |
| Fish Audio | FISH_AUDIO_API_KEY | Free tier |

### Voice commands (in any chat):
- `/voice on` — voice reply to voice messages only
- `/voice tts` — voice reply to all messages
- `/voice off` — text only (default)

## Enabling/Disabling Tools (`hermes tools`)

### Interactive tool config:

```bash
cd ~/.hermes/hermes-agent
source venv/bin/activate
python -m hermes_cli.main tools
```

This opens a curses UI to enable/disable toolsets per platform (cli, telegram, discord, slack, etc.).

### After changing tools:

Use `/reset` in the chat to start a fresh session with the new toolset. Tool changes do NOT take effect mid-conversation (this preserves prompt caching and avoids cost spikes).

### Common toolsets:

| Toolset | What it provides |
|---------|-----------------|
| terminal | Shell command execution |
| file | File read/write/search/patch |
| web | Web search and extraction |
| browser | Browser automation (needs Browserbase) |
| image_gen | AI image generation |
| mcp | MCP server connections |
| voice | Text-to-speech output |
| cronjob | Scheduled tasks |

## Installing Dependencies

Some tools need extra packages:

```bash
cd ~/.hermes/hermes-agent && source venv/bin/activate

pip install faster-whisper    # Local STT (voice transcription)
pip install browserbase       # Browser automation
pip install mcp               # MCP server connections
```

## Adding Models & Providers

### `hermes config set` gotcha

`hermes config set KEY VALUE` appends to the **bottom** of config.yaml, but the `model:` block at the **top** takes precedence. Always verify with `hermes status` after setting:

```bash
hermes config set default_model deepseek-v4-flash
hermes config set default_provider deepseek
hermes status   # check if it actually took effect
```

If status still shows the old model, edit the `model:` block directly:

```yaml
model:
  default: deepseek-v4-flash
  provider: deepseek
```

### `hermes model` is interactive only

`hermes model` requires a real TTY — it will fail with "requires an interactive terminal" when run through pipes or subprocesses. Run it directly in your terminal.

### No `hermes router load` command

Hermes does NOT support JSON task-based routing (`hermes router load file.json` does not exist). Use the built-in routing layers instead:

| Layer | Config Key | Purpose |
|-------|-----------|---------|
| **Primary** | `model.default` | Default for all turns |
| **Smart routing** | `smart_model_routing` | Simple → cheap, Complex → strong |
| **Delegation** | `delegation` | Subagent tasks |
| **Fallback** | `fallback_model` | Error failover |

For task-specific routing, use `/model` switches per session or configure cron jobs with per-job models.

### OAuth providers (OpenAI Codex, Nous Portal)

Some providers require OAuth login, not API keys:

```bash
hermes auth add openai-codex --type oauth    # triggers browser login
hermes auth status openai-codex              # verify: logged in / logged out
```

After OAuth, configure the provider in `config.yaml`:

```yaml
providers:
  openai-codex:
    api: https://chatgpt.com/backend-api/codex
    name: OpenAI Codex
    auth_type: oauth
    default_model: gpt-5.5-codex
```

OAuth tokens are stored in `~/.hermes/auth.json`. Check with `hermes auth status openai-codex`.

### `hermes config set` gotcha

`hermes config set KEY VALUE` appends to the **bottom** of `config.yaml`. But the `model:` block at the **top** takes precedence. Always verify with `hermes status` after setting:

```bash
hermes config set default_model deepseek-v4-flash
hermes config set default_provider deepseek
hermes status   # check if it actually took effect
```

If status still shows old model, edit the `model:` block directly:

```yaml
model:
  default: deepseek-v4-flash
  provider: deepseek
```

### No task-based routing

Hermes has **no** `hermes router load` command and no JSON-based task routing. Routing layers are:

| Layer | What it does |
|-------|-------------|
| **Primary** (`model.default`) | Default for all turns |
| **Smart routing** (`smart_model_routing`) | Simple → cheap, Complex → strong |
| **Delegation** (`delegation`) | Subagent/long-run tasks |
| **Fallback** (`fallback_model`) | Error failover |

For task-specific model assignment, use `/model` switches or per-skill model overrides.

### Adding a provider manually

Providers live under the `providers:` section of `~/.hermes/config.yaml`:

```yaml
providers:
  xai:
    api: https://api.x.ai/v1
    name: X.ai (Grok)
    api_key: xai-your-key-here
    default_model: grok-4.3
  deepseek:
    api: https://api.deepseek.com/v1
    name: DeepSeek
    api_key: sk-your-key-here
    default_model: deepseek-v4-flash
```

After editing, restart the gateway (`/restart`) or start a new CLI session.

### Adding OAuth providers (OpenAI Codex, Nous Portal)

Some providers use OAuth instead of API keys. These require the interactive `hermes model` wizard or manual auth:

```bash
# Interactive (requires TUI)
hermes model

# Check auth status
hermes auth status openai-codex
```

After OAuth login, add to `config.yaml`:

```yaml
providers:
  openai-codex:
    api: https://chatgpt.com/backend-api/codex
    name: OpenAI Codex
    auth_type: oauth
    default_model: gpt-5.5-codex
```

OAuth tokens are stored in `~/.hermes/auth.json`, not in `.env`.

### Config precedence: model block vs config set

⚠️ `hermes config set default_model X` writes to the **bottom** of config.yaml as a top-level key. But the `model:` block at the **top** takes precedence. Always verify with `hermes status` after setting:

```bash
hermes config set default_model deepseek-v4-flash
hermes status   # if still shows old model, edit model block directly
```

If the model didn't change, edit the `model:` block at top of config.yaml:

```yaml
model:
  default: deepseek-v4-flash
  provider: deepseek
  base_url: https://api.deepseek.com/v1
```

### Verify provider connectivity before configuring

Test API endpoints before adding providers:

```bash
# DeepSeek - list models
curl -s https://api.deepseek.com/v1/models \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" | \
  python3 -c "import sys,json; [print(m['id']) for m in json.load(sys.stdin)['data']]"

# xAI - list Grok models
curl -s https://api.x.ai/v1/models \
  -H "Authorization: Bearer $XAI_API_KEY" | \
  python3 -c "import sys,json; [print(m['id']) for m in json.load(sys.stdin)['data']]"
```

### OAuth providers (OpenAI Codex, Nous Portal, Gemini CLI)

Some providers require OAuth instead of API keys. These cannot be configured via `config set` alone — they need the interactive auth flow:

```bash
# OpenAI Codex (GPT-5.5)
hermes auth add openai-codex --type oauth --no-browser
# Then complete browser login when prompted

# Verify auth
hermes auth status openai-codex
```

After OAuth login, add the provider to `config.yaml`:

```yaml
providers:
  openai-codex:
    api: https://chatgpt.com/backend-api/codex
    name: OpenAI Codex
    auth_type: oauth
    default_model: gpt-5.5-codex
```

**OAuth auth stores tokens in `~/.hermes/auth.json`** — never put OAuth tokens in `.env` or `config.yaml`.

**Headless/WSL environments:** Use `--no-browser` flag, then paste the device code URL into your browser manually.

### Config precedence gotcha

When using `hermes config set KEY VALUE`, values are appended to the **bottom** of `config.yaml`. But the `model:` block at the **top** of the file takes precedence. Always verify with `hermes status` after changes:

```bash
hermes config set default_model deepseek-v4-flash
hermes status   # Verify it actually took effect
```

If the model didn't change, edit the `model:` block at the top directly:

```yaml
model:
  default: deepseek-v4-flash
  provider: deepseek
  base_url: https://api.deepseek.com/v1
```

### Discovering available models

Query the provider's `/v1/models` endpoint to list all available model IDs:

```bash
# xAI (Grok)
curl -s https://api.x.ai/v1/models \
  -H "Authorization: Bearer $XAI_API_KEY" | \
  python3 -c "import sys,json; [print(m['id']) for m in json.load(sys.stdin)['data']]"

# DeepSeek
curl -s https://api.deepseek.com/v1/models \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" | \
  python3 -c "import sys,json; [print(m['id']) for m in json.load(sys.stdin)['data']]"
```

### Multi-model routing architecture

Hermes supports 4 layers of model routing — not task-based JSON routing, but you can approximate it:

| Layer | Config Key | Use Case |
|-------|-----------|----------|
| **Primary** | `model.default` | Default model for all turns |
| **Smart routing** | `smart_model_routing` | Simple → cheap model, Complex → strong model |
| **Delegation** | `delegation` | Subagent/long-run tasks |
| **Fallback** | `fallback_model` | Error failover (429, 503, connection) |

```yaml
# Smart routing: cheap model for short/simple messages
smart_model_routing:
  enabled: true
  max_simple_chars: 160
  max_simple_words: 28
  cheap_model:
    provider: deepseek
    model: deepseek-v4-flash

# Delegation: stronger model for subagents
delegation:
  model: deepseek-v4-pro
  provider: deepseek

# Fallback: safety net when primary fails
fallback_model:
  provider: custom
  model: Qwen3.6-27B-Uncensored
```

### Switching models in a session

- **CLI/TUI:** `/model grok-4.3` or `/model --provider xai`
- **Command line:** `hermes -m grok-4.3 --provider xai`

## Config File Reference

The main config file is `~/.hermes/config.yaml`. Key sections:

```yaml
# Model and provider
model:
  default: anthropic/claude-opus-4.6
  provider: openrouter

# Agent behavior
agent:
  max_turns: 90
  reasoning_effort: high    # xhigh, high, medium, low, minimal, none
```

Edit with `hermes config edit` or `hermes config set KEY VALUE`.
  enabled: true
  provider: local           # local, groq, openai
tts:
  provider: elevenlabs      # elevenlabs, openai, kokoro, fish

# Display
display:
  skin: default             # default, ares, mono, slate
  tool_progress: full       # full, compact, off
  background_process_notifications: all  # all, result, error, off
```

Edit with `hermes config edit` or `hermes config set KEY VALUE`.

## Gateway Commands (Messaging Platforms)

| Command | What it does |
|---------|-------------|
| /reset or /new | Fresh session (picks up new tool config) |
| /help | Show all commands |
| /model [name] | Show or change model |
| /compact | Compress conversation to save context |
| /voice [mode] | Configure voice replies |
| /reasoning [effort] | Set reasoning level |
| /sethome | Set home channel for cron/notifications |
| /restart | Restart the gateway (picks up config changes) |
| /status | Show session info |
| /retry | Retry last message |
| /undo | Remove last exchange |
| /personality [name] | Set agent personality |
| /skill [name] | Load a skill |

## Troubleshooting

### Voice messages not working
1. Check stt.enabled is true in config.yaml
2. Check a provider is available (faster-whisper installed, or API key set)
3. Restart gateway after config changes (/restart)

### Tool not available
1. Run `hermes tools` to check if the toolset is enabled for your platform
2. Some tools need env vars — check the env file
3. Use /reset after enabling tools

### Model/provider issues
1. Run `hermes doctor` to check configuration
2. Run `hermes login` to re-authenticate
3. Check the env file has the right API key

### Changes not taking effect
- Gateway: /reset for tool changes, /restart for config changes
- CLI: start a new session

### Skills not showing up
1. Check `hermes skills list` shows the skill
2. Check `hermes skills config` has it enabled for your platform
3. Load explicitly with `/skill name` or `hermes -s name`
