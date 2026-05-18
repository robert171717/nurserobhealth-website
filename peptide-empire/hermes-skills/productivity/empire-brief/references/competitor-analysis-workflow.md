# Competitor Analysis Workflow

Reusable workflow for competitive analysis of content creators, brands, or telehealth players in the peptide/wellness space.

## When to Use
- User asks "who are my competitors" / "analyze my competition"
- Empire strategic planning sessions
- Content gap identification
- Preceded: full empire dashboard (for baseline metrics)
- Note: This workflow generates a standalone report; the Empire Daily Brief should reference its findings rather than duplicate them.

## Step 1: Discover Competitors

### Source A: X API (primary — real follower counts, bios, recent content)
```bash
# Search for competitor accounts by topic
xurl search "peptide therapy BPC-157 longevity biohacking" -n 20

# Look up specific competitor handles
for user in maximustribe marekhealth bengreenfield JayCampbell333; do
  xurl user "@$user"
done

# Get competitor timeline for content analysis
xurl timeline "@competitor" -n 10
```

### Source B: DuckDuckGo HTML (fallback when Firecrawl is down)
```bash
curl -s --max-time 12 -H 'User-Agent: Mozilla/5.0' \
  'https://html.duckduckgo.com/html/?q=peptide+therapy+influencers+competitors' \
  | grep -oP 'result__snippet[^>]*>\K[^<]+' | head -15
```

See `references/web-search-fallback.md` for full DDG fallback details.

## Step 2: Profile Each Competitor

For each competitor, capture:
- **Handle, name, follower count** (from `xurl user`)
- **Bio/positioning** — how they describe themselves
- **Content mix** — threads, video, newsletter, podcast (from timeline + bio)
- **Monetization** — products, telehealth, books, affiliates, consultations
- **Strengths** — what they do better than Nurse Rob
- **Weaknesses/Gaps** — underserved niches, missing angles

## Step 3: Build Comparison Matrix

Create a comparison table across these dimensions:
- Followers
- Content volume / quality
- Video/visual presence
- Educational depth
- Cross-platform presence
- Monetization clarity
- Personality/brand warmth
- Niche clarity

## Step 4: Gap Analysis — Nurse Rob vs Field

Identify:
1. **Top 5 shortcomings** — ranked by impact on growth/revenue
2. **Top 5 unfair advantages** — things NRH has that competitors don't
3. **Niche opportunity** — the one-sentence lane NRH can own

Common gaps that surface (validate against actual data):
- No visual content (video, graphics)
- No off-X presence (TikTok, IG, newsletter, blog)
- Content not repurposed across platforms
- No clear monetization funnel (content → ??? → revenue)
- Niche positioning fuzzy compared to competitors

## Step 5: Build Tiered Action Plan

Format:
```
TIER 1 — Immediate (This Week)     | 4 actions, sub-hour each
TIER 2 — Near-Term (2-4 Weeks)     | 4 actions, few hours each
TIER 3 — Growth Phase (1-3 Months) | 4 actions, multi-hour each
```

Each action must have:
- **#** priority number
- **Action** — specific, executable
- **Why** — one-sentence business case
- **Effort** — estimated time

## Step 6: Save Report

Save to `/mnt/c/Users/Robert/Desktop/Daily Brief/NurseRob_PeptideEmpire/competitive-analysis-YYYY-MM-DD.md`

## Step 7: Extract Actionable Manual To-Do

Create a separate manual to-do list with:
- What Hermes completed vs what user must do manually
- Time estimates per item
- Exact instructions (paste this text, click this button)

Save to same folder as `manual-todo-list.md`.

## Pitfalls
- **Don't fabricate competitor data.** If a handle doesn't resolve via xurl, mark it NOT_FOUND. Don't guess follower counts.
- **X API free tier has limited search reach.** Competitor discovery via `xurl search` often returns 0-5 results. Use multiple query variations and supplement with DDG.
- **Bio update requires OAuth 1.0a.** xurl's OAuth2 setup can't update X bios. Mark this as a MANUAL action for the user.
- **Competitor content analysis is surface-level without web_extract.** When Firecrawl is down, you can only analyze bios and tweet previews, not full websites. Note this caveat.
- **The user prefers ACTIONABLE over ACADEMIC.** Skip methodology sections. Lead with the competitor table. Make every finding tie to a specific recommendation.
