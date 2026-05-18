---
name: daily-brief
description: Generate TERMINATOR 2 world-class tactical briefing — Executive Summary, Solana memecoin table (5M/1H/24H/Vol/MCap/Liq), Pump.fun strict-filtered launches, Polymarket w/ word-boundary categories, Alpha Signals, actionable trade ideas, Market Health — auto-saved to Desktop Daily Brief folder.
version: 14.0
author: NurseRobHealth
tags: [solana, polymarket, automation, productivity, terminator, cyberpunk, pumpfun, defillama, coingecko]
related_skills: []
---

# Daily Brief - Skynet Override Premium Edition v14.0 🚀💀

## Overview

Generates a premium, actionable daily crypto briefing with **7 live data streams** and **professional-grade formatting**. Built for traders who need quick, reliable intel — not fluff.

### Data Streams

| # | Source | Data |
|---|--------|------|
| 1 | **CoinGecko** | SOL price, 24h change, market cap |
| 2 | **DefiLlama** | Solana TVL |
| 3 | **DexScreener** | 5 memecoins: price, 5M/1H/24H changes, volume, MCap, liquidity |
| 4 | **Pump.fun API** | Top 5 trending with strict filter (≥10 participants, >-95% from ATH) |
| 5 | **Polymarket Gamma** | 3 live prediction markets with word-boundary scoring + joke filter |
| 6 | **Web Search** | Alpha signals from Crypto Twitter |
| 7 | **DEX Volume Aggregate** | Broad Solana DEX activity estimate |

### Report Sections

1. **Executive Summary** — Sentiment, SOL price/TVL/DEX vol, top mover, hot Polymarket
2. **Memecoin Table** — 5 coins with 8 columns: COIN, PRICE, 5M, 1H, 24H, VOLUME, MCAP, LIQUIDITY
3. **Primary Target Analysis** — Vol/MCap ratio + situational guidance (breakout/consolidation/capitulation)
4. **Pump.fun Launchpad** — Strict-filtered trending with links
5. **Polymarket Live** — Category-diversified, visual probability bars, direct links
6. **Alpha Signals** — What Crypto Twitter is talking about
7. **Today's Play** — 3 actionable trade ideas (momentum, bounce, launch watch)
8. **Market Health** — SOL, MCap, TVL, DEX activity, health status

## When to Use

- Daily market reconnaissance (trigger: "daily brief", "brief")
- Need consolidated crypto + prediction market intel
- Pre-trade morning overview
- Automated via cron for daily delivery

## How to Run

### Via Skill (from Hermes)

Just say "daily brief" or trigger the skill. Hermes will execute `daily_brief_v14.py` via execute_code.

### Standalone (from terminal)

```bash
python3 ~/.hermes/skills/productivity/daily-brief/daily_brief_v14.py
```

Output is always saved to: `/mnt/c/Users/Robert/Desktop/Daily Brief/DAILY-BRIEF.md`

## Architecture

The engine script is at `~/.hermes/skills/productivity/daily-brief/daily_brief_v14.py`.

Key design decisions:
- **Priority address matching** — DexScreener token addresses are verified live (not hardcoded from stale data). Priority addresses bump real tokens to the top; fallback is volume-sorted symbol matching.
- **Word-boundary regex** — Polymarket scoring uses `\b` boundaries so "spain" doesn't match "ai" and "kiss" gets filtered as junk.
- **Strict Pump.fun filter** — Eliminates dead rugs: ≥10 participants AND has NOT collapsed >95% from ATH.
- **Standalone-friendly** — Alpha Signals (web_search) gracefully degrades when run outside Hermes sandbox. Everything else works standalone.
- **5M/1H/24H columns** — DexScreener `priceChange` object provides m5, h1, h6, h24. Columns show whatever is available.

## Pitfalls & Troubleshooting

| Issue | Solution |
|-------|----------|
| WIF/POPCAT not appearing | Priority addresses may be stale — run `python3 -c "import json,urllib.request; d=json.loads(urllib.request.urlopen('https://api.dexscreener.com/latest/dex/search?q=dogwifhat').read()); print([(p['baseToken']['address'],p['priceUsd']) for p in d['pairs'][:3]])"` and update PRIORITY_ADDRESSES |
| Alpha Signals empty in standalone | Expected — `hermes_tools` only available inside Hermes sandbox. Works in cron. |
| Pump.fun returns 0 coins | API rate limit — wait 30s. Or filter is too strict (market is dead). |
| Polymarket "kiss" markets | JOKE_PATTERNS list catches these. Add new patterns if garbage slips through. |
| All APIs fail | Check VPN/internet. Watchdog cron handles recovery. |
| Report not saving | Permissions check on `/mnt/c/Users/Robert/Desktop/Daily Brief/` |

## Cron Job

```
Job ID: (see cronjob list)
Schedule: 0 6 * * * (6AM MST daily)
Deliver: origin (Discord channel)
Skills: daily-brief
```

To create: `hermes cron create --name "Daily Brief v14" --schedule "0 6 * * *" --skill daily-brief --deliver origin`

## Changelog

**v14.0 (May 13, 2026) — PREMIUM REBUILD:**
- 🔥 **Complete engine rewrite** — moved from inline SKILL.md code to standalone `daily_brief_v14.py` (670 lines)
- 🟢 **NEW: CoinGecko** — SOL price, 24h change, market cap
- 🟢 **NEW: DefiLlama** — Solana TVL
- 📊 **Memecoin table upgrade** — 8 columns: COIN, PRICE, 5M, 1H, 24H, VOLUME, MCAP, LIQUIDITY
- 🎯 **Primary Target Analysis** — Vol/MCap ratio + situational guidance
- ⚡ **Pump.fun strict filter** — ≥10 participants AND >-95% from ATH
- 💀 **Polymarket word-boundary scoring** — regex `\b` boundaries + joke market filter
- 📡 **Alpha Signals** — web_search for CT intel (graceful standalone fallback)
- 🎯 **Today's Play** — 3 auto-generated trade ideas from live data
- 🏦 **Market Health** — SOL, MCap, TVL, DEX activity, health status
- 🔧 **Priority address matching** — verified live DexScreener addresses, not stale hardcoded ones
- 📈 **Sentiment calculation** — weighted score from memecoin 24h changes + SOL change
- ⚡ **4.4s execution** — 7 data streams in parallel-friendly sequential fetching

**v13.2 (April 30, 2026)** — Manual one-off with Executive Summary, table columns, Alpha Signals. Code never deployed.

**v12.0 (April 2026)** — Critical data quality fixes: symbol normalization, volume-sorted pair selection, Polymarket scoring.

**v9.0 (March 2026)** — Added Pump.fun direct API, momentum vs ATH metric, strict deduplication.
