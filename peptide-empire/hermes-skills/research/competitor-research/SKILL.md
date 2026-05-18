---
name: competitor-research
description: Research competitors on X and the web — identify top players, analyze their positioning and content strategy, and produce structured comparison reports with prioritized recommendations.
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [competitor-analysis, research, x-twitter, market-intelligence]
    related_skills: [xitter, xurl]
prerequisites:
  commands: [xurl, curl]
  env_vars: [X_API_KEY, X_API_SECRET, X_BEARER_TOKEN, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET]
---

# Competitor Research — X + Web Methodology

Research competitors on X (Twitter) and the open web, analyze their positioning, content strategy, and market presence, then produce a structured comparison report with prioritized recommendations.

## When to use this skill

- User asks "who are my competitors?" or "how do I compare to X?"
- User wants a competitive landscape analysis in a specific niche
- Quarterly competitive audits or market intelligence reports
- Evaluating positioning, content gaps, and growth opportunities vs. peers

## Phase 1 — Discovery

Identify the top competitors. Use multiple angles — a single search misses depth.

### 1a. X (Twitter) account discovery

Use `xurl search` with varied queries to surface competitor accounts:

```bash
xurl search "peptide therapy BPC-157" -n 20
xurl search "peptide biohacking longevity health" -n 20
xurl search "BPC-157 TB-500 healing recovery peptide" -n 20
```

Extract usernames from `includes.users[]` in the JSON response. Deduplicate and rank by relevance.

### 1b. Known-account validation

Once you have candidate names/domains, verify them individually:

```bash
xurl user "@MaximusTribe"
```

Parse the JSON response for:
- `data.name` — display name
- `data.username` — handle
- `data.public_metrics.followers_count` — audience size
- `data.description` — positioning/bio text
- `data.public_metrics.tweet_count` — content volume

### 1c. X timeline analysis (content strategy)

Two approaches — use both for full coverage:

**Primary: Pull their actual tweets with metrics**
```bash
# Step 1: Get their user ID
xurl user @competitor  # → extract data.id

# Step 2: Pull recent tweets with engagement data
xurl /2/users/THEIR_USER_ID/tweets -d '{"max_results":20,"tweet.fields":"public_metrics,created_at,entities"}'
```

**Secondary: Search for content variety**
```bash
# Exclude their dominant topic to see full content mix
xurl search "from:CompetitorHandle -dominantTopic" -n 15
```

Analyze: content mix (educational vs. promotional vs. engagement), posting frequency, media types (text/video/images), engagement levels (impressions, likes, replies, bookmarks).

**Content variety technique:** When a competitor is currently running a mega-thread that dominates their recent timeline, use `xurl search "from:username -threadTopic"` to see what else they post about. Without this, you'll only see one thread and misjudge their content mix.

### 1d. Web search fallback

When Hermes native web_search is unavailable (credits, outages), use terminal curl with DuckDuckGo's HTML endpoint:

```bash
curl -s --max-time 12 -H "User-Agent: Mozilla/5.0" \
  "https://html.duckduckgo.com/html/?q=peptide+therapy+competitors" \
  | grep -oP "result__snippet[^>]*>\K[^<]+" | head -15
```

Grep pattern note: the `\K` resets the match start, so only the text AFTER the tag closing is captured. This avoids regex complexity with DDG's HTML structure.

**Important:** `web_search` and `web_extract` may fail with "Payment Required" when Firecrawl credits are exhausted. Do NOT treat this as a permanent constraint — it's transient. Fall back to curl + DDG + xurl. The skill is the fallback pattern, not the failure.

## Phase 2 — Profile Analysis

For each competitor, pull and structure:

| Dimension | Source | What to extract |
|---|---|---|
| Audience size | `xurl user` → `followers_count` | Raw reach |
| Positioning | `xurl user` → `description` | One-sentence niche claim |
| Content volume | `xurl user` → `tweet_count` | Output consistency |
| Content style | `xurl /2/users/{id}/tweets` + `xurl search "from:user"` | Educational vs. promotional vs. engagement mix |
| Content formats | Tweet analysis | Thread vs. single-tweet vs. bullet-listicle vs. reply-engagement |
| Thread structure | Thread analysis | Hook → mechanism → studies → CTA arc |
| Visual presence | Timeline scan | Video/images vs. text-only |
| Monetization path | Bio + timeline | How they convert audience → revenue (quiz, link-in-bio, affiliate codes) |
| Brand voice | Bio + tweets | Personality, warmth, authority level |
| Engagement-to-follower ratio | Impressions ÷ followers | Content resonance independent of audience size |

## Phase 3 — Gap Analysis

Compare the user's metrics against each competitor. Build a comparison grid covering:
- Followers (absolute and ratio)
- Content volume and type
- Cross-platform presence (X only vs. multi-platform)
- Monetization funnel clarity
- Niche positioning sharpness
- Visual/production quality
- Credentials and trust signals

Identify: where does the user lead? Where do competitors lead? What's the ONE biggest gap?

## Phase 4 — Report

Save to the user's preferred output path. Structure:

1. **Executive Summary** — 3-4 sentences, biggest finding first
2. **Competitor Profiles** — one section per competitor with metrics table + strengths/weaknesses + specific opportunity for the user
3. **Comparison Table** — all competitors side-by-side on key dimensions
4. **User's Gaps** — shortcomings ranked by impact
5. **User's Advantages** — unfair advantages competitors can't copy
6. **Prioritized Action Plan** — Tier 1 (this week), Tier 2 (2-4 weeks), Tier 3 (1-3 months). Each action has: what, why, estimated effort
7. **Content Strategy Insights** — specific tactics stolen from each competitor
8. **Metrics to Track** — current baseline + 30/90 day targets
9. **Caveats** — methodology notes, data source limitations, what wasn't accessible

### Report conventions

- File naming: `<project>-competitive-analysis-YYYY-MM-DD.md`
- Save location: `~/Desktop/Daily Brief/<Project>/` (Windows/WSL: `/mnt/c/Users/<user>/Desktop/Daily Brief/<Project>/`)
- Tone: Direct, no fluff, actionable. Each recommendation answers "why" and "how much effort."
- Tables for comparisons. Bullet points for insights. Avoid walls of prose.

## Pitfalls

**Web search silent failure.** `web_search` returns "Payment Required" when Firecrawl is out of credits — error may be silent or delayed. Always have the curl + DDG fallback ready. Do not treat this as "web search is broken forever" — it's a credit issue.

**X API rate limits.** Free tier X API has tight rate limits. If `xurl search` returns 0-1 results on broad queries, narrow the query or switch to individual `xurl user` lookups against known accounts.

**Timeline endpoint may return empty.** `xurl timeline` can return empty arrays even for valid accounts (rate limits, API tier restrictions). Fall back to bio + description analysis when timeline data is unavailable.

**Follower counts are point-in-time.** Note the date of data collection in every report. These numbers drift.

**One platform is not the full picture.** X data gives good signal but misses TikTok, Instagram, YouTube, podcasts, newsletters. Acknowledge the limitation in the caveats section.

**Don't over-promise competitor content analysis without timeline access.** If you can't pull actual tweets, analyze what's available (bio, positioning, follower count). Be honest about data depth in the report.

**X API v1.1 profile updates often fail.** The `update_profile.json` endpoint requires OAuth 1.0a which xurl's setup may not satisfy. When it fails, write the bio text for the user to paste manually — don't retry or treat as permanently broken. See Phase 5a.

**Thread posting: capture every returned ID.** When posting multi-tweet threads via `xurl reply`, each call returns a `data.id`. Capture it and use it as the parent for the next reply. Losing the chain mid-thread means starting over.

**`xurl whoami` does NOT reliably return the `url` field.** The API response may show `URL: ?` even when a website link is set and working on the X app. Do not report "website URL not set" based on this field — verify with the user.

**Retweets are NOT original content — filter them out.** `xurl timeline` returns retweets mixed with original posts. When analyzing a user's OWN content strategy (not competitors), always do a separate `xurl search "from:<user> <keywords>"` and filter out `RT @` posts. The raw timeline may be dominated by political/crypto retweets that don't reflect the user's actual niche content. Missing this filter leads to reporting "content drift" that isn't real.

**`exclude=retweets,replies` causes pagination loop on `/2/users/{id}/tweets`.** When you filter out replies/retweets from the user tweet endpoint, the `next_token` pagination loops forever — returning the same results repeatedly. This is an X API behavior, not a transient error. Workaround: use `xurl search "from:username"` instead for content mix analysis. It returns diverse results without the pagination bug.

**Multi-tweet thread analysis.** When a competitor posts a thread (chain of self-replies), analyze the arc: hook → mechanism/explanation → studies/evidence → product/affiliate CTA. The thread structure reveals their funnel strategy. Each tweet in the thread should be mapped: what job does it do? How does it advance the reader toward the CTA?

## Phase 5 — Action on Findings

When the user asks you to act on the competitive analysis (implement recommendations, post content, create assets), proceed through these sub-phases:

### 5a. Bio and profile updates

Update the user's X bio to reflect sharpened positioning discovered in the analysis. Use your best attempt first, then surface anything the API couldn't do.

```bash
# Attempt profile update via OAuth 1.0a endpoint
xurl -X POST '/1.1/account/update_profile.json' --auth oauth1 \
  -d 'description=New bio text here with CTA link'
```

**Pitfall:** The X API v1.1 `update_profile` endpoint requires OAuth 1.0a with write permissions. xurl's OAuth1 setup often fails with "Bad Authentication data" (code 215). When it does, write the exact bio text the user should paste manually and include it in the manual to-do list. Do NOT treat this as "profile updates are permanently broken" — it's an OAuth configuration issue on this specific setup.

X profile elements that require manual action (no reliable API path):
- Bio text update (OAuth 1.0a often unavailable)
- Pinning a tweet (no API v2 endpoint)
- Profile banner/header image upload
- Website URL field update

### 5b. Multi-tweet thread posting

Post educational/CTA threads using `xurl post` for the first tweet, then chain `xurl reply` using the returned tweet ID:

```bash
# Post the first tweet, capture the ID
FIRST=$(xurl post "🧵 Thread opener text here" 2>&1 | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['id'])")

# Reply to build the thread
xurl reply "$FIRST" "2/ Second tweet in thread..."
xurl reply "$PREVIOUS_ID" "3/ Third tweet..."
```

Always capture the returned `data.id` from each post and use it for the next reply. The X app displays replies in chronological order, building the thread automatically.

### 5c. Video script generation

When the competitive analysis identifies "no video content" as a gap, generate ready-to-record video scripts from the user's best-performing threads:

- Identify top threads (search `from:<user> <keywords>` via xurl, filter out RTs, rank by engagement score)
- Write timed scripts (60-90 seconds) with: hook (first 5s), explanation (3 segments), CTA (last 5s)
- Include recording tips (lighting, audio, eye contact, pacing)
- Save as `video-scripts-top-<N>-threads.md` alongside the competitive analysis report

Script format: timestamped segments with word-for-word narration text, camera directions in brackets.

### 5d. Manual to-do list generation

Generate a companion to-do file (`manual-todo-list.md`) that separates:
- What Hermes completed vs. what the human must do manually
- Tasks grouped by time commitment (Quick Wins <15min, Today 30-60min, This Week, This Month)
- Each task: what, estimated time, exact how-to steps
- A section explaining WHY any task couldn't be automated (API limitation, permission issue, requires human hands)
- Suggested weekly content rhythm (day-by-day posting schedule)

## Related skills

- `xitter` / `xurl` — X interaction and account lookups. Prefer `xurl` on this system — it's the working tool.
- `domain-intel` — passive domain reconnaissance for web presence analysis
- `duckduckgo-search` — alternative web search path
- `nurserob-analytics` — weekly performance reporting (if the user is Nurse Rob)

## Reference files

- `references/peptide-competitors-may-2026.md` — Competitor landscape as of May 2026 (tiered by follower count)
- `references/ddg-fallback-search.md` — DuckDuckGo HTML search fallback pattern
- `references/alfred-playbook-may-2026.md` — @HealthyAlfred content strategy deep-dive: 7 replicable tactics, thread formula, content mix, monetization funnel
