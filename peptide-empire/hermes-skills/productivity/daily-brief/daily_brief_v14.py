#!/usr/bin/env python3
"""
SKYNET OVERRIDE v14.0 — PREMIUM DAILY BRIEF ENGINE
Generates world-class tactical crypto briefing with 7 live data streams.
"""

import json, os, re, sys, time
from datetime import datetime
import urllib.request

start_time = time.time()
OUTPUT_DIR = "/mnt/c/Users/Robert/Desktop/Daily Brief"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "DAILY-BRIEF.md")

# ═══════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════

def http_get(url, timeout=10):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())

def sf(val, default=0.0):
    """safe_float"""
    try: return float(val) if val is not None else default
    except: return default

def fmt_price(p):
    if p <= 0: return "$0.00"
    if p < 0.00000001: return f"${p:.2e}"
    if p < 0.000001: return f"${p:.8f}"
    if p < 0.0001: return f"${p:.6f}"
    if p < 0.01: return f"${p:.6f}"
    if p < 1: return f"${p:.4f}"
    if p < 1000: return f"${p:.2f}"
    return f"${p:,.2f}"

def fmt_pct(c):
    if c is None or c == 0: return "  ─ 0.0%"
    arrow = "▲" if c > 0 else "▼" if c < 0 else "─"
    return f" {arrow} {abs(c):.1f}%"

def fmt_big(n):
    if n >= 1e9: return f"${n/1e9:.2f}B"
    if n >= 1e6: return f"${n/1e6:.2f}M"
    if n >= 1e3: return f"${n/1e3:.1f}K"
    return f"${n:.0f}"

def norm_sym(s):
    return s.lstrip('$').strip().upper()

# ═══════════════════════════════════════════════════
# DATA STREAM 1: COINGECKO — SOL PRICE + MARKET
# ═══════════════════════════════════════════════════

print("🔵 Fetching CoinGecko SOL...")
sol_data = {"price": 0, "change_24h": 0, "mcap": 0}
try:
    cg = http_get("https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd&include_24hr_change=true&include_market_cap=true")
    s = cg.get("solana", {})
    sol_data = {"price": sf(s.get("usd")), "change_24h": sf(s.get("usd_24h_change")), "mcap": sf(s.get("usd_market_cap"))}
    print(f"  ✅ SOL: ${sol_data['price']:.2f} ({sol_data['change_24h']:+.1f}%) | MCap: {fmt_big(sol_data['mcap'])}")
except Exception as e:
    print(f"  ❌ CoinGecko: {e}")

# ═══════════════════════════════════════════════════
# DATA STREAM 2: DEFILLAMA — SOLANA TVL
# ═══════════════════════════════════════════════════

print("🟢 Fetching DefiLlama TVL...")
solana_tvl = 0
try:
    chains = http_get("https://api.llama.fi/v2/chains", timeout=10)
    sol_chain = next((c for c in chains if c.get("name") == "Solana"), None)
    if sol_chain:
        solana_tvl = sf(sol_chain.get("tvl"))
        print(f"  ✅ Solana TVL: {fmt_big(solana_tvl)}")
    else:
        print("  ⚠️ Solana not found in DefiLlama")
except Exception as e:
    print(f"  ❌ DefiLlama: {e}")

# ═══════════════════════════════════════════════════
# DATA STREAM 3: DEXSCREENER — SOLANA MEMECOINS
# ═══════════════════════════════════════════════════

print("🔥 Fetching DexScreener memecoins...")

MEME_TARGETS = [
    ("WIF", "dogwifhat"), ("BONK", None), ("POPCAT", None), ("MEW", None),
    ("GIGA", None), ("MYRO", None), ("SLERF", None), ("BOME", None),
    ("TRUMP", "official trump"), ("PENGU", None), ("MOODENG", None), ("GOAT", "goatseus maximus"),
]

# Known good addresses for priority matching (verified live on DexScreener)
# These are used as PREFERENCE only — if a pair matches this address, it gets priority.
# If no pair matches, we fall through to volume-sorted symbol matching.
PRIORITY_ADDRESSES = {
    'WIF': 'EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm',
    'BONK': 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263',
    'POPCAT': '7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr',
    'MEW': 'MEW1gQWJ3nEXg2qgERiKu7FAFj79PHvQVREQUaspTaw',
    'GIGA': '63LfDmNb3MQ8mw9MtZ2To9bEA2M71kZUUGq5tiJxcqj9',
}

seen_symbols = set()
seen_addresses = set()
memecoins = []

for symbol, name_query in MEME_TARGETS:
    if len(memecoins) >= 5:
        break
    try:
        all_pairs = []

        # Symbol search
        try:
            data = http_get(f"https://api.dexscreener.com/latest/dex/search?q={symbol}", timeout=8)
            for p in data.get("pairs", []):
                if p.get("chainId") == "solana":
                    all_pairs.append(p)
        except: pass

        # Name search for known problematic tokens
        if name_query:
            try:
                data2 = http_get(f"https://api.dexscreener.com/latest/dex/search?q={name_query}", timeout=8)
                for p in data2.get("pairs", []):
                    if p.get("chainId") == "solana":
                        all_pairs.append(p)
            except: pass

        # Sort by 24h volume and check for priority address
        priority_addr = PRIORITY_ADDRESSES.get(symbol)
        
        # If we have a priority address, bump pairs matching it to the top
        def pair_sort_key(p):
            base = p.get("baseToken", {})
            addr = base.get("address", "")
            is_priority = 1 if (priority_addr and addr == priority_addr) else 0
            vol = sf((p.get("volume", {}) or {}).get("h24", 0))
            return (-is_priority, -vol)  # Priority first, then volume
        
        all_pairs.sort(key=pair_sort_key)

        for p in all_pairs:
            base = p.get("baseToken", {})
            psym = norm_sym(base.get("symbol", ""))
            paddr = base.get("address", "")

            # Must match normalized symbol
            if psym != norm_sym(symbol):
                continue
            # Deduplicate by symbol and address
            if psym in seen_symbols or paddr in seen_addresses:
                continue

            vol24 = sf((p.get("volume", {}) or {}).get("h24", 0))
            if vol24 < 500:
                continue

            pc = p.get("priceChange", {}) or {}
            liq = p.get("liquidity", {}) or {}

            seen_symbols.add(psym)
            seen_addresses.add(paddr)

            memecoins.append({
                "symbol": psym,
                "price": sf(p.get("priceUsd")),
                "change_5m": sf(pc.get("m5")),
                "change_1h": sf(pc.get("h1")),
                "change_6h": sf(pc.get("h6")),
                "change_24h": sf(pc.get("h24")),
                "volume_24h": vol24,
                "mcap": sf(p.get("marketCap")),
                "fdv": sf(p.get("fdv")),
                "liquidity": sf(liq.get("usd")),
                "url": p.get("url", ""),
            })
            break
    except Exception as e:
        pass

# Sort by volume and ensure exactly 5
memecoins.sort(key=lambda x: x["volume_24h"], reverse=True)
memecoins = memecoins[:5]
print(f"  ✅ Memecoins: {len(memecoins)}/5 targets ({' | '.join(c['symbol'] for c in memecoins)})")

# ═══════════════════════════════════════════════════
# DATA STREAM 4: PUMP.FUN — STRICT FILTER
# ═══════════════════════════════════════════════════

print("🔴 Fetching Pump.fun launches...")
pumpfun_coins = []
try:
    pf = http_get("https://frontend-api-v3.pump.fun/coins/currently-live", timeout=10)
    valid = []
    for c in pf:
        if c.get("is_banned", False):
            continue
        usd_mcap = sf(c.get("usd_market_cap"))
        ath_mcap = sf(c.get("ath_market_cap"))
        participants = int(c.get("num_participants", 0))
        total_supply = sf(c.get("total_supply", 1))

        if usd_mcap <= 0 or total_supply <= 0:
            continue
        if participants < 10:
            continue

        price = usd_mcap / total_supply
        perf_vs_ath = ((usd_mcap / ath_mcap) - 1) * 100 if ath_mcap > 0 else 0

        # Strict filter: must have NOT collapsed >95% from ATH
        if perf_vs_ath < -95:
            continue

        valid.append({
            "name": c.get("name", "Unknown"),
            "symbol": (c.get("symbol") or "???").upper(),
            "price": price,
            "mcap": usd_mcap,
            "momentum": perf_vs_ath,
            "participants": participants,
            "mint": c.get("mint", ""),
        })

    # Sort by market cap
    valid.sort(key=lambda x: x["mcap"], reverse=True)
    pumpfun_coins = valid[:5]
    print(f"  ✅ Pump.fun: {len(pumpfun_coins)} (filtered from {len(valid)} candidates, {len(pf)} raw)")
except Exception as e:
    print(f"  ❌ Pump.fun: {e}")

# ═══════════════════════════════════════════════════
# DATA STREAM 5: POLYMARKET — SMART SELECTION
# ═══════════════════════════════════════════════════

print("💀 Fetching Polymarket...")
polymarkets = []
try:
    pm = http_get("https://gamma-api.polymarket.com/markets?active=true&limit=100&order=volume24hrClob&ascending=false", timeout=10)
    live = [m for m in pm if m.get("acceptingOrders") and m.get("active")]

    # Scoring with WORD BOUNDARIES — also detect and penalize joke/meme markets
    JOKE_PATTERNS = [
        r'\bkiss\b', r'\bmeme\b', r'\bdance\b', r'\btwerk\b', r'\bpoop\b', r'\bfart\b',
        r'\bsex\b', r'\bnaked\b', r'\bdrugs\b', r'\btattoo\b', r'\belon.*baby\b',
        r'\bonlyfans\b', r'\bdivorce\b', r'\barrested\b.*\btrump\b',
    ]
    
    def score_market(q):
        ql = q.lower()
        score = 0
        
        # Penalize joke/garbage markets heavily
        for pat in JOKE_PATTERNS:
            if re.search(pat, ql):
                score -= 50
                break
        
        patterns = [
            (r'\b(bitcoin|crypto|ethereum|solana|defi|blockchain|token|btc|eth|sol)\b', 10),
            (r'\b(ai|artificial.intelligence|chatgpt|openai|llm|gpt|machine.learning)\b', 8),
            (r'\b(trump|election|president|congress|senate|democrat|republican|vote|gop)\b', 7),
            (r'\b(fed|interest.rate|inflation|cpi|gdp|recession|economy|tariff)\b', 7),
            (r'\b(tesla|spacex|apple|nvidia|google|microsoft|meta|amazon)\b', 6),
            (r'\b(nba|nfl|super.bowl|ufc|mlb|champions.league|premier.league)\b', 3),
            (r'\b(gta|grand.theft.auto|game|gaming|esports)\b', 2),
        ]
        for pat, pts in patterns:
            if re.search(pat, ql):
                score += pts
        return score

    def get_category(q):
        ql = q.lower()
        if re.search(r'\b(bitcoin|crypto|ethereum|solana|defi|blockchain|btc|eth|sol|token)\b', ql):
            return "₿ CRYPTO"
        if re.search(r'\b(ai|artificial.intelligence|tech|apple|nvidia|tesla|spacex|google|microsoft|meta)\b', ql):
            return "⚙️ TECH"
        if re.search(r'\b(trump|election|president|congress|senate|vote|gop|democrat)\b', ql):
            return "🏛️ POLITICS"
        if re.search(r'\b(fed|rate|inflation|economy|recession|tariff)\b', ql):
            return "📊 ECONOMY"
        if re.search(r'\b(nba|nfl|super.bowl|ufc|champions|premier)\b', ql):
            return "🏀 SPORTS"
        return "🌐 GENERAL"

    # Score, sort, deduplicate by category
    scored = [(score_market(m.get("question", "")), m) for m in live]
    scored.sort(key=lambda x: (-x[0], -sf(x[1].get("volume24hrClob", 0))))

    cats_used = set()
    for score, m in scored:
        if len(polymarkets) >= 3:
            break
        q = m.get("question", "")
        cat = get_category(q)
        if cat in cats_used:
            continue
        cats_used.add(cat)

        try:
            prices = json.loads(m.get("outcomePrices", "[]")) if isinstance(m.get("outcomePrices"), str) else (m.get("outcomePrices") or [])
            yes_pct = float(prices[0]) * 100 if prices else 50.0
        except:
            yes_pct = 50.0

        slug = m.get("slug", "")
        polymarkets.append({
            "title": q,
            "yes_pct": yes_pct,
            "vol_24h": sf(m.get("volume24hrClob", 0)),
            "vol_total": sf(m.get("volumeNum", 0)),
            "slug": slug,
            "category": cat,
            "url": f"https://polymarket.com/event/{slug}" if slug else "",
        })
    print(f"  ✅ Polymarket: {len(polymarkets)} live ({', '.join(cats_used)})")
except Exception as e:
    print(f"  ❌ Polymarket: {e}")

# ═══════════════════════════════════════════════════
# DATA STREAM 6: ALPHA SIGNALS — WEB INTEL
# ═══════════════════════════════════════════════════

print("📡 Fetching Alpha Signals...")
alpha_signals = []

# Try hermes_tools first (when running inside Hermes via execute_code/cron)
# Fall back gracefully when running as standalone Python
try:
    from hermes_tools import web_search
    _has_web_search = True
except ImportError:
    _has_web_search = False

if _has_web_search:
    queries = [
        "Solana meme coin breakout today 2026",
        "crypto alpha thread site:x.com 2026",
        "Solana DeFi news today 2026",
    ]
    seen_titles = set()
    for query in queries:
        if len(alpha_signals) >= 5:
            break
        try:
            results = web_search(query)
            for item in results.get("data", {}).get("web", [])[:3]:
                title = item.get("title", "")
                desc = item.get("description", "")
                url = item.get("url", "")
                if title and url and title not in seen_titles:
                    seen_titles.add(title)
                    alpha_signals.append({"title": title, "desc": desc[:120] if desc else "", "url": url})
                    if len(alpha_signals) >= 5:
                        break
        except:
            continue
    print(f"  ✅ Alpha Signals: {len(alpha_signals)} items")
else:
    print(f"  ⚠️ Alpha Signals: web_search not available (standalone mode)")

# ═══════════════════════════════════════════════════
# DATA STREAM 7: DEX VOLUME (aggregate from memecoins + top pairs)
# ═══════════════════════════════════════════════════

total_dex_vol = sum(c["volume_24h"] for c in memecoins)
# Get broader DEX volume from DexScreener for Solana pairs
dex_vol_estimate = total_dex_vol
try:
    # Search for SOL-USDC as representative pair
    sol_pairs = http_get("https://api.dexscreener.com/latest/dex/search?q=SOL/USDC", timeout=8)
    solana_pairs = [p for p in sol_pairs.get("pairs", []) if p.get("chainId") == "solana"]
    if solana_pairs:
        # Sum volumes of top SOL pairs
        extra_vol = sum(sf((p.get("volume", {}) or {}).get("h24", 0)) for p in solana_pairs[:3])
        dex_vol_estimate += extra_vol
except:
    pass

# ═══════════════════════════════════════════════════
# SENTIMENT CALCULATION
# ═══════════════════════════════════════════════════

sentiment_score = 0
if memecoins:
    # Weighted: 24h changes + SOL change
    for c in memecoins:
        sentiment_score += c["change_24h"] * 0.15
    sentiment_score += sol_data["change_24h"] * 0.25

if sentiment_score > 5:
    sentiment = "🟢 BULLISH"
elif sentiment_score > 0:
    sentiment = "🟡 SLIGHTLY BULLISH"
elif sentiment_score > -5:
    sentiment = "⚪ NEUTRAL"
elif sentiment_score > -10:
    sentiment = "🟠 BEARISH"
else:
    sentiment = "🔴 EXTREME FEAR"

top_mover = max(memecoins, key=lambda x: x["change_24h"]) if memecoins else None
worst_mover = min(memecoins, key=lambda x: x["change_24h"]) if memecoins else None

# Build top mover label for executive summary
if top_mover:
    top_mover_label = f"${top_mover['symbol']} {top_mover['change_24h']:+.1f}%"
else:
    top_mover_label = "$-- +0.0%"

# ═══════════════════════════════════════════════════
# TODAY'S PLAY GENERATION
# ═══════════════════════════════════════════════════

plays = []
# 1. Momentum play: best 24h performer
if top_mover and top_mover["change_24h"] > 2:
    plays.append({
        "type": "📈 MOMENTUM LONG",
        "coin": f"${top_mover['symbol']}",
        "price": fmt_price(top_mover["price"]),
        "reason": f"▲ {top_mover['change_24h']:.1f}% wave",
        "detail": f"Stop -5%, trail on strength. Entry at market."
    })
# 2. Bounce play: worst performer
if worst_mover and worst_mover["change_24h"] < -3 and len(plays) < 2:
    plays.append({
        "type": "💀 BOUNCE PLAY",
        "coin": f"${worst_mover['symbol']}",
        "price": fmt_price(worst_mover["price"]),
        "reason": f"▼ {abs(worst_mover['change_24h']):.1f}% oversold",
        "detail": "Wait for 15m reversal candle. Stop -3%."
    })
# 3. Launch watch: top pump.fun coin
if pumpfun_coins and len(plays) < 3:
    pf = pumpfun_coins[0]
    plays.append({
        "type": "⚡ LAUNCH WATCH",
        "coin": f"${pf['symbol']}",
        "price": fmt_price(pf["price"]),
        "reason": f"{pf['participants']} holders, {fmt_big(pf['mcap'])} MCap",
        "detail": "Monitor bonding curve. High risk, no position yet."
    })

# Fill remaining slots
fallback_plays = [
    {"type": "🔍 RESEARCH", "coin": "Solana Ecosystem", "price": "", "reason": "Look for new narratives", "detail": "Scan Pump.fun + DexScreener for emerging meta."},
    {"type": "💰 YIELD", "coin": "Stablecoin LP", "price": "", "reason": "DeFi yields on Solana", "detail": f"Check Jupiter/Kamino for stable yields. TVL: {fmt_big(solana_tvl)}."},
]
for fp in fallback_plays:
    if len(plays) >= 3:
        break
    plays.append(fp)

# ═══════════════════════════════════════════════════
# PRIMARY TARGET ANALYSIS
# ═══════════════════════════════════════════════════

def target_analysis(coin):
    """Generate situational guidance based on metrics"""
    vol_mcap = (coin["volume_24h"] / coin["mcap"] * 100) if coin["mcap"] > 0 else 0

    if coin["change_24h"] > 5:
        guidance = "🚀 BREAKOUT — Strength confirmed. Trail stop, let it run."
        risk = "⚠️ Extended — don't chase. Wait for pullback to add."
    elif coin["change_24h"] > 1:
        guidance = "📈 UPTREND — Higher lows. Add on dips to support."
        risk = ""
    elif coin["change_24h"] < -5:
        guidance = "💀 CAPITULATION — Oversold. Look for reversal signal."
        risk = "⚡ Catching a falling knife. Wait for confirmation."
    elif coin["change_24h"] < -1:
        guidance = "📉 DOWNTREND — Lower highs. Wait for base to form."
        risk = ""
    else:
        guidance = "⚖️ CONSOLIDATION — Range-bound. Scalp edges."
        risk = ""

    vol_quality = ""
    if vol_mcap > 10:
        vol_quality = f"📊 Vol/MCap: {vol_mcap:.1f}% — 🔥 HIGH activity. Good liquidity."
    elif vol_mcap > 2:
        vol_quality = f"📊 Vol/MCap: {vol_mcap:.1f}% — ✅ Normal activity."
    elif vol_mcap > 0:
        vol_quality = f"📊 Vol/MCap: {vol_mcap:.1f}% — ⚠️ Low activity. Slippage risk."

    return guidance, risk, vol_quality

# ═══════════════════════════════════════════════════
# BUILD REPORT
# ═══════════════════════════════════════════════════

elapsed = time.time() - start_time
now = datetime.now()
report_date = now.strftime("%B %d, %Y")
report_time = now.strftime("%H:%M UTC")
data_streams = sum([
    1 if sol_data["price"] else 0,
    1 if solana_tvl else 0,
    1 if memecoins else 0,
    1 if pumpfun_coins else 0,
    1 if polymarkets else 0,
    1 if alpha_signals else 0,
    1 if dex_vol_estimate else 0,
])

# Detect hot polymarket
hot_pm = polymarkets[0]["title"][:55] + "..." if polymarkets else "N/A"

report = f"""╔══════════════════════════════════════════════════════════════════════╗
║  🚀 SKYNET OVERRIDE v14.0 — TACTICAL BRIEF                          ║
║  {report_date} | {report_time:<22}║
║  ⚡ Gen {elapsed:.1f}s │ {data_streams} data streams │ @RealSolanaMeme                ║
╚══════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────┐
│ 📊 EXECUTIVE SUMMARY — TL;DR                                        │
├─────────────────────────────────────────────────────────────────────┤
│ Sentiment: {sentiment:<52}│
│ SOL: {fmt_price(sol_data['price']):>11} ({sol_data['change_24h']:+.1f}% 24h)   │ MCap: {fmt_big(sol_data['mcap']):>10}         │
│ Solana TVL: {fmt_big(solana_tvl):>10}                                │ DEX 24h Vol: {fmt_big(dex_vol_estimate):>10}   │
│ Top Mover (24h): {top_mover_label:<36}│
│ Polymarket 🔥: {hot_pm[:52]:<52}│
└─────────────────────────────────────────────────────────────────────┘

"""

# Memecoin Table
report += """══════════════════════════════════════════════════════════════════════
🔥 MEMECOIN WATCH — TOP 5 BY 24H VOLUME
══════════════════════════════════════════════════════════════════════

"""
report += f"{'COIN':<7} {'PRICE':>11} {'5M':>8} {'1H':>8} {'24H':>9} {'VOLUME':>11} {'MCAP':>11} {'LIQUIDITY':>11}\n"
report += "─" * 76 + "\n"

for c in memecoins:
    report += (
        f"${c['symbol']:<6} "
        f"{fmt_price(c['price']):>11} "
        f"{fmt_pct(c['change_5m']):>8} "
        f"{fmt_pct(c['change_1h']):>8} "
        f"{fmt_pct(c['change_24h']):>9} "
        f"{fmt_big(c['volume_24h']):>11} "
        f"{fmt_big(c['mcap']):>11} "
        f"{fmt_big(c['liquidity']):>11}\n"
    )

report += "\n"

# Primary Target Analysis
if memecoins:
    primary = memecoins[0]
    guidance, risk, vol_quality = target_analysis(primary)

    report += """══════════════════════════════════════════════════════════════════════
🎯 PRIMARY TARGET ANALYSIS
══════════════════════════════════════════════════════════════════════

"""
    report += f"${primary['symbol']} — {fmt_price(primary['price'])} | Vol: {fmt_big(primary['volume_24h'])} | 24h: {fmt_pct(primary['change_24h']).strip()} | MCap: {fmt_big(primary['mcap'])}\n"
    report += f"   {guidance}\n"
    report += f"   {vol_quality}\n"
    if risk:
        report += f"   {risk}\n"
    report += f"   💀 Worst: ${worst_mover['symbol']} {fmt_pct(worst_mover['change_24h']).strip()} — avoid until base forms.\n" if worst_mover and worst_mover != primary else ""
    report += "\n"

# Pump.fun
report += """══════════════════════════════════════════════════════════════════════
⚡ PUMP.FUN LAUNCHPAD — TOP 5 TRENDING
══════════════════════════════════════════════════════════════════════

Strict Filter: ≥10 participants AND > -95% from ATH (no dead rugs)

"""
if pumpfun_coins:
    report += f"{'#':<3} {'COIN':<30} {'MCAP':>12} {'MOMENTUM':>11} {'👥':>6}   STATUS\n"
    report += "─" * 78 + "\n"
    for i, c in enumerate(pumpfun_coins, 1):
        mom_icon = "🚀" if c["momentum"] > 10 else "📈" if c["momentum"] > 0 else "📉" if c["momentum"] > -70 else "💀"
        report += f"{i:<3} ${c['symbol']:<29} {fmt_big(c['mcap']):>12} {c['momentum']:+.1f}% {mom_icon}  {c['participants']:>5}   🔴 BONDING\n"

    report += "\n🔗 Links:\n"
    for c in pumpfun_coins:
        name = c['name'].lstrip('$')[:27]
        report += f"   {name:<27} → https://pump.fun/{c['mint']}\n"
    report += "\n"
else:
    report += "   No launches meeting strict filter criteria\n\n"

# Polymarket
report += """══════════════════════════════════════════════════════════════════════
💀 POLYMARKET LIVE — PREDICTION MARKETS
══════════════════════════════════════════════════════════════════════

"""
for m in polymarkets:
    # Visual probability bar
    bar_len = 20
    filled = int(m["yes_pct"] / 100 * bar_len)
    bar = "█" * filled + "░" * (bar_len - filled)
    report += f"{m['category']} | {m['title']}\n"
    report += f"   YES: {m['yes_pct']:.1f}% [{bar}] │ 24h Vol: {fmt_big(m['vol_24h'])} │ Total: {fmt_big(m['vol_total'])}\n"
    if m['url']:
        report += f"   🔗 {m['url']}\n"
    report += "\n"

# Alpha Signals
report += """══════════════════════════════════════════════════════════════════════
📡 ALPHA SIGNALS — WHAT CT IS TALKING ABOUT
══════════════════════════════════════════════════════════════════════

"""
if alpha_signals:
    for i, item in enumerate(alpha_signals, 1):
        report += f"   {i}. {item['title']}\n"
        if item['desc']:
            report += f"      {item['desc']}\n"
        report += f"      🔗 {item['url']}\n\n"
else:
    report += "   No signals acquired\n\n"

# Today's Play
report += """══════════════════════════════════════════════════════════════════════
🎯 TODAY'S PLAY — ACTIONABLE IDEAS
══════════════════════════════════════════════════════════════════════

"""
for i, p in enumerate(plays, 1):
    report += f"   {i}. {p['type']}: {p['coin']} {p['price']} — {p['reason']}\n"
    report += f"      {p['detail']}\n\n"

# Market Health
report += f"""══════════════════════════════════════════════════════════════════════
🏦 MARKET HEALTH
══════════════════════════════════════════════════════════════════════

   SOL:          {fmt_price(sol_data['price']):>10}  ({sol_data['change_24h']:+.1f}% 24h)
   SOL MCap:     {fmt_big(sol_data['mcap']):>10}
   TVL:          {fmt_big(solana_tvl):>10}  (DefiLlama)
   DEX Activity: {fmt_big(total_dex_vol):>10}  (top 5 memecoin pairs)
   Status:       {"🟢 Healthy" if sol_data["price"] > 50 and solana_tvl > 1e9 else "⚠️ Monitor"}

"""

# Footer
report += f"""══════════════════════════════════════════════════════════════════════
🔴 END TRANSMISSION — {report_time}
══════════════════════════════════════════════════════════════════════

╔══════════════════════════════════════════════════════════════════════╗
║  SKYNET OVERRIDE v14.0 │ @RealSolanaMeme │ {elapsed:.1f}s │ {data_streams}/7 live ║
║  CoinGecko • DefiLlama • DexScreener • Pump.fun • Polymarket • Web ║
║  💀 HASTA LA VISTA, BABY. I'LL BE BACK.                            ║
╚══════════════════════════════════════════════════════════════════════╝
"""

# ═══════════════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════════════

os.makedirs(OUTPUT_DIR, exist_ok=True)
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(report)

file_size = os.path.getsize(OUTPUT_FILE)
print(f"\n{'='*60}")
print(f"✅ BRIEF SAVED: {OUTPUT_FILE}")
print(f"   Size: {file_size:,} bytes | Time: {elapsed:.1f}s | Streams: {data_streams}/7")
print(f"   Sentiment: {sentiment}")
print(f"   Memecoins: {len(memecoins)} | Pump.fun: {len(pumpfun_coins)} | Polymarket: {len(polymarkets)}")
print(f"   Alpha Signals: {len(alpha_signals)} | Plays: {len(plays)}")
print(f"{'='*60}")
print("\n💀 MISSION COMPLETE. STAY VIGILANT. 💀")
