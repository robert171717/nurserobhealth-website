---
name: xitter
description: Interact with X/Twitter via the x-cli terminal client using official X API credentials. Use for posting, reading timelines, searching tweets, liking, retweeting, bookmarks, mentions, and user lookups.
version: 1.0.0
author: Siddharth Balyan + Hermes Agent
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [uv]
  env_vars: [X_API_KEY, X_API_SECRET, X_BEARER_TOKEN, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET]
metadata:
  hermes:
    tags: [twitter, x, social-media, x-cli]
    homepage: https://github.com/Infatoshi/x-cli
---

# Xitter — X/Twitter via xurl (primary) or x-cli

Use `xurl` for X/Twitter API interactions from the terminal. `xurl` is the shorter, agent-friendly CLI that ships with Hermes and is the primary tool on this system.

When `xurl` is available, prefer it for all X operations. `x-cli` is documented below as an alternative for systems where `xurl` is not installed.

## Tool selection (this system)

On this machine: **use `xurl`**. It's installed at `/home/robert/.local/bin/xurl` and authenticated with OAuth2 (live token, expires May 2026). `x-cli` is NOT installed — skip the install steps unless `xurl` is unavailable.

### xurl quick reference (preferred)

```bash
# User lookup
xurl user "@NurseRobHealth"

# Search tweets
xurl search "peptide therapy BPC-157" -n 20

# Home timeline
xurl timeline -n 10

# Timeline for specific user
xurl timeline "@competitor" -n 10

# Post a tweet
xurl post "Tweet text here"

# Reply (chain threads by using returned ID)
xurl reply 1234567890 "Reply text"

# Whoami (own profile)
xurl whoami

# Raw API calls
xurl /2/users/me
xurl -X POST /2/tweets -d '{"text":"Hello"}'
```

### xurl output parsing

xurl returns JSON by default. Parse with python3 for structured extraction:

```bash
xurl user "@MaximusTribe" 2>&1 | python3 -c "
import json,sys
d=json.load(sys.stdin)
u=d.get('data',{})
print(f'{u.get(\"name\")} | {u.get(\"public_metrics\",{}).get(\"followers_count\",0):,} followers')
"
```

### Extracting media (images, video) from tweets

xurl's `read` command returns tweet text but not media URLs. To download images from a tweet, use the expansions API:

```bash
# Step 1: Get media URL from tweet
xurl "/2/tweets/<TWEET_ID>?expansions=attachments.media_keys&media.fields=url,width,height"
# Returns `includes.media[0].url` → e.g. https://pbs.twimg.com/media/HIXcPY1WYAAPDZf.jpg

# Step 2: Download the image
curl -sL "https://pbs.twimg.com/media/HIXcPY1WYAAPDZf.jpg?format=jpg&name=4096x4096" -o output.jpg
```

Parse with python3 to extract the URL programmatically:
```bash
MEDIA_URL=$(xurl "/2/tweets/<ID>?expansions=attachments.media_keys&media.fields=url" 2>&1 | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print(d['includes']['media'][0]['url'])")
```

**Pitfall**: Direct `curl` of `x.com/.../photo/1` returns HTML, not the image. Always use the `pbs.twimg.com` URL from the API. Some pbs.twimg.com downloads may return empty files without the right query params — use `?format=jpg&name=4096x4096` for photos.

### X Search (xAI API Tool) — Alternative to xurl

In addition to xurl (which calls the X API directly), Hermes Agent has an **X Search** tool powered by the xAI/Grok API. It's a different mechanism: Grok reasons about your search and returns X posts, users, and threads — no X API credentials needed.

### When to use X Search vs xurl

| | xurl (X API) | X Search (xAI API) |
|---|---|---|
| **Auth** | OAuth 1.0a + OAuth 2.0 (5 secrets) | `XAI_API_KEY` only |
| **Access** | Free tier (tight limits) or paid X API plan | Included with Grok/xAI API subscription |
| **Cost** | Free tier = free (but rate-limited) | Token usage at Grok rates (~$1.25/M in, $2.50/M out) |
| **Semantic search** | No (keyword only) | Yes (Grok understands intent) |
| **User/thread fetch** | Separate API calls | Built into tool |
| **Image/video understanding** | Manual extraction | Built-in (`enable_image_understanding`) |
| **Use case** | Posting, timelines, exact user lookup | Searching, discovering, research |

### Requirements

- **xAI API key** (`XAI_API_KEY` in `~/.hermes/.env`) — OR —
- **X Premium+** subscription on your X account

The Grok API subscription path is simpler: one API key, no X Developer Portal setup.

### Cost

X Search has **no separate per-search fee**. It's billed as standard Grok API token usage. A typical search consumes 500–2000 tokens (fraction of a cent). You're already paying for Grok if you have `XAI_API_KEY` set — X Search just adds another tool to the toolbox.

Grok-4.3 pricing (May 2026): $1.25/M input, $0.20/M cached input, $2.50/M output.

### Availability

X Search requires a current Hermes Agent version (added ~May 2026). Verify with:
```bash
hermes tools list | grep -i x_search
```
If missing, update: `hermes update && systemctl --user restart hermes-gateway`.

The tool auto-appears when an xAI provider is configured — no manual enablement needed.

### X Premium vs Grok API subscription

These are **different things**:
- **X Premium** ($8–16/mo on X): blue checkmark, longer posts, etc. Checked via `xurl whoami` → `verified: true`.
- **Grok API subscription** (xAI console): API key for Grok models, billed per token. Your `XAI_API_KEY`.

X Search works with **either** — but the Grok API path is what most Hermes users have configured for inference anyway.

## xurl limitations

- **Profile updates:** The X API v1.1 `update_profile.json` endpoint requires OAuth 1.0a. xurl's OAuth1 auth often fails (code 215). Profile bio/avatar/banner updates must be done manually in the X app.
- **Tweet pinning:** No API v2 endpoint exists. Manual action required.
- **Rate limits:** Free tier X API has tight limits. Searches may return 0-1 results on broad queries.
- **Timeline endpoint:** `xurl timeline` may return empty even for valid accounts. Fall back to `xurl search from:<user>` or bio analysis.

## x-cli alternative (if xurl unavailable)

If `xurl` is not available, install `x-cli`:

## Important Cost / Access Note

X API access is not meaningfully free for most real usage. Expect to need paid or prepaid X developer access. If commands fail with permissions or quota errors, check your X developer plan first.

## Install

Install upstream `x-cli` with `uv`:

```bash
uv tool install git+https://github.com/Infatoshi/x-cli.git
```

Upgrade later with:

```bash
uv tool upgrade x-cli
```

Verify:

```bash
x-cli --help
```

## Credentials

You need these five values from the X Developer Portal:
- `X_API_KEY`
- `X_API_SECRET`
- `X_BEARER_TOKEN`
- `X_ACCESS_TOKEN`
- `X_ACCESS_TOKEN_SECRET`

Get them from:
- https://developer.x.com/en/portal/dashboard

### Why does X need 5 secrets?

Unfortunately, the official X API splits auth across both app-level and user-level credentials:

- `X_API_KEY` + `X_API_SECRET` identify your app
- `X_BEARER_TOKEN` is used for app-level read access
- `X_ACCESS_TOKEN` + `X_ACCESS_TOKEN_SECRET` let the CLI act as your user account for writes and authenticated actions

So yes — it is a lot of secrets for one integration, but this is the stable official API path and is still preferable to cookie/session scraping.

Setup requirements in the portal:
1. Create or open your app
2. In user authentication settings, set permissions to `Read and write`
3. Generate or regenerate the access token + access token secret after enabling write permissions
4. Save all five values carefully — missing any one of them will usually produce confusing auth or permission errors

Note: upstream `x-cli` expects the full credential set to be present, so even if you mostly care about read-only commands, it is simplest to configure all five.

## Cost / Friction Reality Check

If this setup feels heavier than it should be, that is because it is. X’s official developer flow is high-friction and often paid. This skill chooses the official API path because it is more stable and maintainable than browser-cookie/session approaches.

If the user wants the least brittle long-term setup, use this skill. If they want a zero-setup or unofficial path, that is a different trade-off and not what this skill is for.


## Where to Store Credentials

`x-cli` looks for credentials in `~/.config/x-cli/.env`.

If you already keep your X credentials in `~/.hermes/.env`, the cleanest setup is:

```bash
mkdir -p ~/.config/x-cli
ln -sf ~/.hermes/.env ~/.config/x-cli/.env
```

Or create a dedicated file:

```bash
mkdir -p ~/.config/x-cli
cat > ~/.config/x-cli/.env <<'EOF'
X_API_KEY=your_consumer_key
X_API_SECRET=your_secret_key
X_BEARER_TOKEN=your_bearer_token
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
EOF
chmod 600 ~/.config/x-cli/.env
```

## Quick Verification

```bash
x-cli user get openai
x-cli tweet search "from:NousResearch" --max 3
x-cli me mentions --max 5
```

If reads work but writes fail, regenerate the access token after confirming `Read and write` permissions.

## Common Commands

### Tweets

```bash
x-cli tweet post "hello world"
x-cli tweet get https://x.com/user/status/1234567890
x-cli tweet delete 1234567890
x-cli tweet reply 1234567890 "nice post"
x-cli tweet quote 1234567890 "worth reading"
x-cli tweet search "AI agents" --max 20
x-cli tweet metrics 1234567890
```

### Users

```bash
x-cli user get openai
x-cli user timeline openai --max 10
x-cli user followers openai --max 50
x-cli user following openai --max 50
```

### Self / Authenticated User

```bash
x-cli me mentions --max 20
x-cli me bookmarks --max 20
x-cli me bookmark 1234567890
x-cli me unbookmark 1234567890
```

### Quick Actions

```bash
x-cli like 1234567890
x-cli retweet 1234567890
```

## Output Modes

Use structured output when the agent needs to inspect fields programmatically:

```bash
x-cli -j tweet search "AI agents" --max 5
x-cli -p user get openai
x-cli -md tweet get 1234567890
x-cli -v -j tweet get 1234567890
```

Recommended defaults:
- `-j` for machine-readable output
- `-v` when you need timestamps, metrics, or metadata
- plain/default mode for quick human inspection

## Agent Workflow

1. Confirm `x-cli` is installed
2. Confirm credentials are present
3. Start with a read command (`user get`, `tweet search`, `me mentions`)
4. Use `-j` when extracting fields for later steps
5. Only perform write actions after confirming the target tweet/user and the user's intent

## Pitfalls

- **Paid API access**: many failures are plan/permission problems, not code problems.
- **403 oauth1-permissions**: regenerate the access token after enabling `Read and write`.
- **Reply restrictions**: X restricts many programmatic replies. `tweet quote` is often more reliable than `tweet reply`.
- **Rate limits**: expect per-endpoint limits and cooldown windows.
- **Credential drift**: if you rotate tokens in `~/.hermes/.env`, make sure `~/.config/x-cli/.env` still points at the current file.
- **xurl thread posting**: when building multi-tweet threads with `xurl reply`, always capture the returned `data.id` from each post and use it as the parent for the next reply. Losing the chain mid-thread means starting over. Parse with `python3 -c "import json,sys; print(json.load(sys.stdin)['data']['id'])"` to extract the ID programmatically.
- **Profile updates require manual intervention**: X API v1.1 `update_profile.json` needs OAuth 1.0a which xurl often can't satisfy. Bio changes, banner uploads, and tweet pinning must be done in the X app. Write exact copy for the user to paste.
- **`xurl whoami` does NOT reliably return the `url` field.** The API response may show `URL: ?` or empty even when the user has set a website link on their X profile and it works fine in the X app/mobile. Do not report "website URL is not set" based on `whoami` — the user may have already set it. Ask or verify via the X app UI instead.
- **X Premium ≠ Grok API subscription.** Having `XAI_API_KEY` and using Grok models does NOT mean you have X Premium (blue check). Check with `xurl whoami` → `verified: true/false`. X Premium is a separate $8–16/mo subscription on x.com. The Grok API key gives you API access to Grok models and the X Search tool, but not the X Premium badge or perks.
- **Timeline includes retweets — filter for original content.** `xurl timeline` returns the user's most recent tweets including retweets. When analyzing a user's OWN content strategy, always search for `from:<user> <niche keywords>` and filter out `RT @` tweets. The raw timeline may be dominated by retweets of trending content that don't reflect the user's actual posting strategy. Rob's timeline is heavy on political/crypto RTs but his original content is peptide education — missing this filter leads to wrong conclusions.

## Notes

- Prefer official API workflows over cookie/session scraping.
- Use tweet URLs or IDs interchangeably — `x-cli` accepts both.
- If bookmark behavior changes upstream, check the upstream README first:
  https://github.com/Infatoshi/x-cli
