---
description: Check and update Hermes Agent version information, including detailed commit analysis.
name: hermes-update
trigger: update hermes, upgrade hermes, hermes update
---

# Hermes Update Guide

## Check Version Info

```bash
hermes --version
```

Output shows: "Update available: X commits behind — run 'hermes update'"

### Environment Note (Native WSL2)

If you're running Hermes in **native WSL2 mode without Docker**, the `execute_code` tool won't work (it requires Docker). Instead:

1. **Ask the user to run commands directly** in their terminal
2. **Use terminal tool** if available (not execute_code)

Example workflow for native WSL2:
```bash
# Ask user to run:
hermes --version

# Or manually check commits:
cd ~/.hermes/hermes-agent
git log HEAD..origin/main --oneline --max-count=20
```

## Check Detailed Commit Information

Hermes agent code lives at: `~/.hermes/hermes-agent`

```bash
# Navigate to the hermes-agent repo
cd ~/.hermes/hermes-agent

# Check how many commits behind
git rev-list --count --left-only HEAD...origin/main

# See the commits you're missing
git log HEAD..origin/main --oneline

# See full details
git log HEAD..origin/main --oneline --max-count=50
```

## Analyze What's Changed

Categorize commits by relevance:
- **Brief-relevant**: file_tools, write actions, stale detection
- **Skills**: skill management, patch operations, size limits
- **Browser/Camofox**: web scraping, persistent sessions, VNC
- **Security**: secret redaction, path traversal, credential protection
- **Auth/Credential**: credential pools, API rotation, custom endpoints
- **CLI/UX**: terminal improvements, TUI fixes, config handling

## How to Update

```bash
# Simple update (recommended)
hermes update

# Or manual git pull
cd ~/.hermes/hermes-agent
git pull origin main
```

### Timeout Warning

`hermes update` restarts the gateway and kills running agents — this can take over 120s. If the command times out, **do not assume it failed**. The git pull and auto-stash may have already completed. Always re-check with:

```bash
hermes --version
```

If it shows the newer version, the update succeeded despite the timeout. If it still shows the old version, run `hermes update` again.

### Multi-Pass Updates (Large Jumps)

If you're hundreds of commits behind (e.g., 888+), the first `hermes update` may catch the bulk but leave a small remainder (e.g., 6 commits). Just run `hermes update` a second time to catch the leftovers. Check `hermes --version` after each pass — it'll say "Up to date" when you're done.

## Official Repo

https://github.com/NousResearch/hermes-agent

## After Updating

```bash
# Verify installation
hermes --help

# Check version again
hermes --version
```

### Config Migration

After updating — especially across version bumps — run `hermes config migrate` to pick up new config keys, env vars, and feature defaults that were introduced in the update:

```bash
hermes config migrate
```

This is non-destructive. It shows you what's new and seeds missing defaults (e.g., curator settings, plugin opt-in, new API key slots). It's not urgent — nothing breaks without it — but running it ensures you have all new features and protections. In non-interactive sessions, the update skips the migration prompt; run it manually afterward.

### Running Sessions

Active sessions (other CLI tabs, gateway chats) do **not** need to be restarted. They continue with the old binary until exited. New sessions automatically get the updated version. No mid-work interruption required.

## Common Issues

- **Not a git repo**: Ensure you're in `~/.hermes/hermes-agent`, not your home directory
- **Modified files**: Check `git status` - you may have local changes to stash
- **Permission errors**: Hermes agent is in your home directory, should have write access
- **Stale "X commits behind" message**: `hermes --version` may report you're behind (e.g., "1744 commits behind") even when `git log HEAD..origin/main` shows no new commits. This is a stale version cache. Running `hermes update` refreshes the cache and will report "Already up to date!" if current. Always run `hermes update` to get accurate status, not just `hermes --version`.
