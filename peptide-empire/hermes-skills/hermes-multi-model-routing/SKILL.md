---
name: hermes-multi-model-routing
description: Configure multi-model routing in Hermes Agent — smart_model_routing, fallback_model, delegation providers, auxiliary task providers, and custom provider setup. Use when building a multi-provider router config for agentic workloads.
version: 1.1.0
author: Hermes Agent
tags: [hermes, routing, multi-model, providers, fallback, delegation, smart-routing]
---

# Hermes Agent Multi-Model Routing

Configure multiple LLM providers with intelligent routing for different task types. Covers the 4-layer routing architecture: smart model routing, fallback models, delegation providers, and auxiliary task providers.

## 4-Layer Routing Architecture

| Layer | Config Key | Purpose | Triggers |
|-------|-----------|---------|----------|
| **1. Smart Model Routing** | `smart_model_routing` | Routes simple/short queries to cheap model | Message length/word count thresholds |
| **2. Fallback Model** | `fallback_model` | Auto-failover when primary fails | Rate limits (429), errors (500/502/503), auth failures (401/403), 404 |
| **3. Delegation Provider** | `delegation` | Separate model for subagents | `delegate_task` calls |
| **4. Auxiliary Providers** | `auxiliary.*` | Independent providers for side tasks | Vision, compression, session search, web extract, skills hub, MCP, approval |

## Configuration Reference

### 1. Smart Model Routing

Routes short/simple messages to a cheaper model, keeps primary for complex work.

```yaml
smart_model_routing:
  enabled: true
  max_simple_chars: 160     # Messages under this length route to cheap model
  max_simple_words: 28      # AND under this word count
  cheap_model:
    provider: deepseek       # provider name (see providers table below)
    model: deepseek-v4-flash # model ID
```

### 2. Fallback Model + Fallback Providers Chain

**`fallback_model`** — Per-turn failover. Each new user message restores primary; if primary fails, fallback_model activates for that turn only.

```yaml
fallback_model:
  provider: custom            # provider name (or xai, deepseek, etc.)
  model: Qwen3.6-27B-Base-Q4_K_M
```

### 3. Delegation Provider

Subagents use this provider instead of primary. No automatic fallback for subagents.

```yaml
delegation:
  provider: xai
  model: grok-4.3  # optimized for agent orchestration
  # base_url: ...
  # api_key: ...
  max_iterations: 50
  reasoning_effort: high
```

### 4. Auxiliary Task Providers

Each auxiliary task has its own provider resolution. Default is `"auto"` which tries: OpenRouter → Nous Portal → Custom → Codex → API-key providers.

```yaml
auxiliary:
  vision:
    provider: xai              # auto | openrouter | nous | main | anthropic | xai | deepseek | custom
    model: grok-4.3
  web_extract:
    provider: deepseek
    model: deepseek-v4-flash
  compression:
    provider: deepseek
    model: deepseek-v4-flash
  session_search:
    provider: deepseek
    model: deepseek-v4-flash
    max_concurrency: 3
  skills_hub:
    provider: deepseek
    model: deepseek-v4-flash
  mcp:
    provider: auto
    model: ""
  approval:
    provider: auto
    model: ""
```

## Supported Providers

| Provider Value | Requirements |
|---------------|-------------|
| `openrouter` | `OPENROUTER_API_KEY` |
| `anthropic` | `ANTHROPIC_API_KEY` |
| `deepseek` | `DEEPSEEK_API_KEY` |
| `xai` (alias `grok`) | `XAI_API_KEY` |
| `gemini` | `GOOGLE_API_KEY` or `GEMINI_API_KEY` |
| `nous` | `hermes auth` (OAuth) |
| `openai-codex` | `hermes model` (ChatGPT OAuth) |
| `copilot` | `COPILOT_GITHUB_TOKEN` |
| `zai` | `GLM_API_KEY` |
| `kimi-coding` | `KIMI_API_KEY` |
| `minimax` | `MINIMAX_API_KEY` |
| `huggingface` | `HF_TOKEN` |
| `custom` | `base_url` + `key_env` |
| `main` (auxiliary only) | Uses whatever provider the main agent uses |
| `auto` (auxiliary only) | Try providers in order until one works |

## Available Models by Provider (as of April 2026)

### DeepSeek V4
| Model | Description |
|-------|-------------|
| `deepseek-v4-flash` | Fast MoE (284B total / 13B active), cheapest frontier model |
| `deepseek-v4-pro` | Premium MoE (1.6T total / 49B active), strongest DeepSeek |

### xAI / Grok
| Model | Description |
|-------|-------------|
| `grok-4.3` | 🏆 Flagship — best overall reasoning |
| `grok-4.3` | Fast variant, no chain-of-thought |
| `grok-4.3` | Optimized for agent orchestration |
| `grok-4-1-fast-reasoning` | Grok 4.1 reasoning |
| `grok-4-1-fast-non-reasoning` | Grok 4.1 fast |
| `grok-3` | Previous generation |
| `grok-3-mini` | Lightweight |
| `grok-code-fast-1` | Code-specialist |

**⚠️ Note:** Model IDs change over time. Always verify with `curl -H "Authorization: Bearer $XAI_API_KEY" https://api.x.ai/v1/models` or check provider docs. Old models like `grok-2-1212` may disappear without warning.

## Important Limitation: No Task-Based Routing

Hermes does NOT support arbitrary task-based routing (e.g., "Peptide_Content_Operator → local-qwen3.6"). It only has the 4 layers above. If you have a JSON router spec with task→model mappings, you must:

1. **Map tasks to the 4 layers**: default → primary, simple/quick → smart routing cheap model, complex/long → delegation, fast side-tasks → auxiliary
2. **Handle task-specific routing at the skill/cron level**: Each skill can use `/model` command or `hermes chat -m provider/model` to invoke a specific model
3. **Use manual `/model` switches**: Operator switches model per session based on task type

```
Your JSON router intent          → Hermes equivalent
─────────────────────────────────────────────────────
"default_daily_driver"           → model.default (primary)
"quick_scripts", "comment_replies" → smart_model_routing.cheap_model
"long_agent_runs"                → delegation.provider/model
"private_data" (local only)      → Keep local model as primary; use /model to switch back
"fallback"                       → fallback_model
Side tasks (compression, search) → auxiliary.* providers
```

## OAuth Providers (Codex, Nous Portal)

Some providers use OAuth instead of API keys. These **cannot** be configured via config.yaml alone.

### OpenAI Codex (`openai-codex`)

Codex is **not** accessible via `OPENAI_API_KEY`. It requires OAuth authentication:

```bash
hermes model        # Interactive provider selection — choose OpenAI Codex
```

**⚠️ `hermes model` requires an interactive terminal** — see the "hermes model CLI Limitations" section above for details. Cannot run via pipes, subprocess, or `hermes -z`.

```bash
hermes auth status openai-codex              # Check auth status
hermes auth add openai-codex --type oauth    # Re-authenticate if needed
```

**You cannot use Codex as a fallback or auxiliary model** — it's only available as a primary model selection via the interactive `hermes model` command or `hermes auth add openai-codex --type oauth`.

### Nous Portal (`nous`)

```bash
hermes auth add nous --type oauth     # OAuth login
hermes auth status nous               # Check status
```

### Important: `hermes model` CLI Limitations

`hermes model` is an **interactive TUI only** — it does NOT accept subcommands like `add`, `list`, `rename`, or pipe arguments.

| Command | Result |
|---------|--------|
| `hermes model` | ✅ Interactive provider/model selector |
| `hermes model add grok` | ❌ No such subcommand |
| `hermes model list` | ❌ No such subcommand |
| `hermes models` | ❌ Not a valid command |
| `hermes model \| grep ...` | ❌ Fails — requires interactive terminal |
| `hermes -m grok -z "hi"` | ✅ Use `-m model` / `-p provider` flags instead |

#### How to List Available Models from a Provider

Use the provider's API directly:

```bash
# xAI / Grok
curl -s https://api.x.ai/v1/models | python3 -m json.tool | grep '"id"'

# DeepSeek
curl -s https://api.deepseek.com/v1/models | python3 -m json.tool | grep '"id"'

# Local (LM Studio / llama.cpp)
curl -s http://localhost:8080/v1/models | python3 -m json.tool | grep '"id"'

# Z.AI
curl -s https://api.z.ai/v1/models | python3 -m json.tool | grep '"id"'
```

> ⚠️ Model IDs change over time. Always verify with the provider's `/v1/models` endpoint before configuring — old models can disappear without warning.

#### How to Add a New Provider

| Provider Type | How to Configure |
|--------------|-----------------|
| **API-key providers** | Add to `providers` section in `config.yaml` |
| **OAuth providers** | Run `hermes model` interactively or `hermes auth add <provider> --type oauth` |

If you want to use a provider like DeepSeek, xAI, Anthropic — add it to `config.yaml` directly. If you want Codex or Nous — use the OAuth flow.

## Adding Custom Providers

Add to `providers` section in config.yaml:

```yaml
providers:
  deepseek:
    api: https://api.deepseek.com
    name: DeepSeek
    api_key: sk-your-key
    default_model: deepseek-v4-flash
    request_timeout_seconds: 1800  # optional per-provider timeout
  xai:
    api: https://api.x.ai/v1
    name: X.ai (Grok)
    api_key: xai-your-key
    default_model: grok-4.3
```

Or use `custom_providers` list for OpenAI-compatible endpoints:

```yaml
custom_providers:
  - name: DeepSeek-Flash
    base_url: https://api.deepseek.com
    api_key: sk-your-key
    model: deepseek-v4-flash
```

## Example: Multi-Provider Router Config

```yaml
# Primary model
model:
  default: deepseek-v4-flash
  provider: deepseek

providers:
  deepseek:
    api: https://api.deepseek.com
    name: DeepSeek
    api_key: sk-deepseek-key
    default_model: deepseek-v4-flash
  xai:
    api: https://api.x.ai/v1
    name: X.ai (Grok)
    api_key: xai-your-key
    default_model: grok-4.3

# Smart routing: simple queries → cheap model
smart_model_routing:
  enabled: true
  max_simple_chars: 200
  max_simple_words: 35
  cheap_model:
    provider: xai
    model: grok-4.3

# Fallback: if DeepSeek fails → Grok
fallback_model:
  provider: xai
  model: grok-4.3

# Subagents: use Grok multi-agent optimized model
delegation:
  provider: xai
  model: grok-4.3
  max_iterations: 50

# Auxiliary tasks: fast/cheap model
auxiliary:
  compression:
    provider: xai
    model: grok-4.3
  session_search:
    provider: xai
    model: grok-4.3
  web_extract:
    provider: xai
    model: grok-4.3
```

## Example: 6-Tier Production Routing

Real-world setup with primary, smart routing, delegation, fallback chain:

```yaml
model:
  default: deepseek-v4-pro      # Primary: heavy lifting
  provider: deepseek

smart_model_routing:
  enabled: true
  max_simple_chars: 300          # <300 chars → flash
  max_simple_words: 40           # <40 words → flash
  cheap_model:
    provider: deepseek
    model: deepseek-v4-flash     # Ultra-cheap for quick tasks

fallback_model:
  provider: custom               # 1st fallback: local (private)
  model: Qwen3.6-27B-Base-Q4_K_M

fallback_providers:
  - zai                          # 2nd fallback: Z.AI/GLM (last resort)

delegation:
  model: gpt-5.5-codex           # Subagents use Codex
  provider: openai-codex
```

Invocation for non-routed models:
```bash
hermes -m grok-4.3 -z "Myth-bust this..."   # xAI truth-seeking
hermes -m Qwen3.6-27B-Base-Q4_K_M -z "Sensitive data..."    # Local/private
```

## Pitfalls

- **Fallback is turn-scoped**: Each new user message restores the primary model. If primary fails mid-turn, fallback activates for that turn only. Next message tries primary again.
- **Subagents don't inherit fallback**: Delegation uses its own provider. If delegation provider fails, no fallback occurs.
- **Cron jobs use fixed provider**: No automatic fallback for cron jobs. Set `provider`/`model` on the job itself.
- **Config changes require restart**: In gateway use `/restart`. In CLI, start a new session. For provider config changes, restart gateway: `systemctl --user restart hermes-gateway`, then verify with `hermes status`.
- **Tool changes require `/reset`**: Enabling/disabling tools takes effect on next session only (preserves prompt caching).
- **Provider timeouts**: Set `providers.<id>.request_timeout_seconds` for provider-wide timeouts, or `providers.<id>.models.<model>.timeout_seconds` for per-model overrides.
- **Env var names may not match config key** — Z.AI provider uses `zai:` in config.yaml but the env var is `GLM_API_KEY` (not `ZAI_API_KEY`). Use `hermes config set <key_name>` to let Hermes auto-detect the correct env var name.
- **Always use `${ENV_VAR}` syntax** — reference `.env` values with `${VAR_NAME}` (e.g. `api_key: ${GLM_API_KEY}`), never hardcode keys directly.
- **Non-built-in providers need profiles** — if a provider doesn't appear in `hermes status` "API-Key Providers", create a profile: `hermes profile create <name>` then `hermes config -p <name> set base_url/model/api_key`.
- **Duplicate env entries break resolution** — if you `hermes config set` multiple times, clean up duplicates in `.env` to prevent resolution issues.
- **Auxiliary `auto` silently burns expensive models** — leaving any auxiliary task on `provider: auto` can route overhead work (compression, session search, title generation, web extract) through Codex or other OAuth/expensive providers. The `auto` resolution order is OpenRouter → Nous → Custom → Codex → API-key providers. If you have Codex OAuth configured but no OpenRouter, compression and session search will hit Codex on every turn. **Always explicitly set provider/model for every auxiliary task** to a cheap model like `deepseek/deepseek-v4-flash`.
- **`hermes config set fallback_providers '[]'` produces a string, not a YAML list** — the CLI serializes `'[]'` as a quoted string `fallback_providers: '[]'` instead of the YAML list `fallback_providers: []`. This may cause resolution errors. After setting via CLI, verify with `hermes config` or manually patch the config file to ensure it's a proper YAML empty list.
- **Fallback chain can silently degrade to a weak model** — if `fallback_providers` includes a provider whose `default_model` is weak (e.g., `openai` → `gpt-4o-mini`), your agent can drop from a frontier primary (deepseek-v4-pro) to a mini model in two hops. Keep fallback chains short and strong — one strong fallback is better than a chain that ends with a mini model.
- **Always set `request_timeout_seconds` on every routed provider** — without timeouts, a hung API call blocks the agent until the terminal timeout (default 180s). Set generous timeouts on reasoning-capable providers (600s for DeepSeek Pro) and shorter timeouts on fast providers (300s for xAI/Z.AI).

## Provider Timeouts

```yaml
providers:
  deepseek:
    request_timeout_seconds: 1800   # Provider-wide default
    stale_timeout_seconds: 300      # Non-streaming stale-call detector
    models:
      deepseek-v4-pro:
        timeout_seconds: 600        # Longer timeout for Pro reasoning calls
```

## Routing Audit Checklist

When reviewing or troubleshooting a routing configuration, systematically check:

1. **Primary model** — Is it a frontier model appropriate for the workload? Is it API-key or OAuth (OAuth can expire silently)?
2. **Smart routing thresholds** — Are `max_simple_chars` and `max_simple_words` reasonable? Remember they're AND conditions (both must be under threshold).
3. **Auxiliary providers** — Is EVERY auxiliary task explicitly set to a cheap model? Any remaining `provider: auto` tasks may burn expensive models.
4. **Fallback model** — Is it strong enough to carry real work? Is it in the `providers` section? Is `fallback_providers` a valid YAML list (not a string)?
5. **Fallback chain strength** — Does the chain degrade gracefully? Avoid dropping from frontier → mini model. One strong fallback beats a weak chain.
6. **Delegation provider** — Does it have credentials? OAuth delegation has no fallback if the token expires.
7. **Provider timeouts** — Does every provider in the routing path have `request_timeout_seconds` set? Reasoning models need 600s; fast models need 300s.
8. **Task-based routing expectations** — If the user expects "creative work → Codex" or "truth-seeking → Grok", confirm they understand this requires profiles or `/model` switches.
9. **Cron job models** — Do cron jobs specify `model`/`provider` inline, or do they inherit the primary? Deterministic content generation should use cheap models.
10. **Config version** — Is `_config_version` current? Run `hermes config check` to see if migration is needed.

### Quick Audit Commands

```bash
hermes config                    # Full config dump
hermes config check              # Missing/outdated options
hermes doctor                    # Health + connectivity test
grep -A2 'auxiliary:' ~/.hermes/config.yaml | head -100  # Auxiliary provider audit
grep 'request_timeout' ~/.hermes/config.yaml              # Timeout coverage
grep 'fallback_providers' ~/.hermes/config.yaml           # Check for string vs list
```

After config changes:
```bash
hermes doctor              # Check config validity
hermes config              # View current settings
hermes config check        # Detect missing/outdated options
```

For auxiliary tasks with `"auto"` provider, test that at least one provider is configured and has valid credentials.
