---
name: nurserob-analytics
description: Weekly comprehensive performance report for Nurse Rob Peptide Empire — content, leads, revenue, trends, and actionable insights
version: 1.3
author: Nurse Rob
---

# NurseRob Analytics 📈

**Purpose:** Generates weekly performance report every Sunday at 6 PM MST covering all Nurse Rob Peptide Empire metrics — content performance, lead flow, revenue breakdown, trends, and next-week recommendations.

## TRIGGER
- Weekly cron: Sunday 6:00 PM MST
- Manual: "weekly report" / "analytics report"

## PROFILE ROUTING
Use `grok-mode` (grok-4.3) when available — best for data analysis and insight extraction.
If grok-4.3 is not available in the current provider routing, use the default deepseek-v4-pro or whatever the configured cron provider offers. The analytics skill works with any capable model — the key is thorough data gathering, not model selection.

## EXECUTION CONTEXT
This skill runs as a cron job every Sunday 6 PM MST. There is no user present — the agent must work silently and autonomously without asking questions or requesting clarification. The final response IS the report; do NOT use send_message or any delivery tool.

## WORKFLOW

### Step 1: Gather All Data Sources

**X Engagement (live API):** If xurl is authenticated, collect real engagement data for the week's posts:
```python
import subprocess, json

# Get follower count + user ID
whoami = json.loads(subprocess.run(['xurl', 'whoami'], capture_output=True, text=True, timeout=15).stdout)
USER_ID = whoami['data']['id']
followers = whoami['data']['public_metrics']['followers_count']

# Get recent tweets with engagement metrics (query string format — NOT -d JSON body)
result = subprocess.run(
    ['xurl', f'/2/users/{USER_ID}/tweets?max_results=30&tweet.fields=public_metrics,created_at&exclude=replies,retweets'],
    capture_output=True, text=True, timeout=15
)
tweets = json.loads(result.stdout)
# tweets['data'] is array of {id, text, created_at, public_metrics: {like_count, retweet_count, reply_count, impression_count, quote_count, bookmark_count}}
# Use pagination_token from meta.next_token to get older posts if <30 results
# This is the only reliable way to get impression count — the post_log doesn't track it
```
If xurl is not authenticated (check `xurl whoami` exit code), show "X data unavailable" and include the auth status in blockers.

**⚠️ Safe JSON I/O:** Always read JSON files using subprocess+cat, NOT `read_file`. The `read_file` tool returns line-numbered output that breaks `json.loads()`.

```python
import subprocess, json
BASE = '/home/robert/NurseRob_PeptideEmpire'

def read_json(path):
    r = subprocess.run(['cat', path], capture_output=True, text=True, timeout=5)
    return json.loads(r.stdout)

log = read_json(f'{BASE}/content/post_log.json')
```

**Data files to read:**
```
# Content metrics
→ ~/NurseRob_PeptideEmpire/content/post_log.json

# Lead metrics
→ ~/NurseRob_PeptideEmpire/leads/lead_log.json
→ ~/NurseRob_PeptideEmpire/leads/nurture_tracker.json

# Revenue metrics (from dashboard)
→ ~/NurseRob_PeptideEmpire/dashboard/metrics.json

# Affiliate report (generated 1 hour ago by nurserob-affiliate-manager at 5PM)
→ ~/NurseRob_PeptideEmpire/affiliates/affiliate_report_[YYYY-MM-DD].md
  (read for blockers, pharmacy pipeline status, trend data)

# Subscriber metrics
→ ~/NurseRob_PeptideEmpire/subscribers/subscriber_log.json

# Pharmacy metrics
→ ~/NurseRob_PeptideEmpire/pharmacy/outreach_tracker.json

# FDA alerts
→ ~/NurseRob_PeptideEmpire/fda_alerts/ (latest file)

# Cron status
→ ~/NurseRob_PeptideEmpire/cron/failure_log.json
```

### Step 2: Calculate KPIs

#### Content Performance
- Posts published this week: [X]/21 target
- Average engagement rate: [X.X]%
- Top performing post: [title] ([impressions], [engagement])
- Worst performing post: [title]
- Best content type: [Thread/Carousel/Short]
- Best posting time: [Morning/Midday/Evening]

#### Lead Flow
- New leads captured: [X]
- Hot leads: [X] | Warm leads: [X]
- Auto-replies sent: [X]
- Leads in nurture: [X]
- Leads converted (consult/product): [X]
- Conversion rate: [X.X]%

#### Revenue
- Consult revenue: $[X,XXX] ([X] consults)
- Digital products: $[XXX] ([X] units)
- Affiliate revenue: $[XXX] ([X] clicks, [X]% conversion)
- Group coaching: $[XXX] ([X] members)
- **TOTAL WEEKLY: $[X,XXX]**

#### Pharmacy Pipeline
- New pharmacies scouted: [X]
- Emails sent: [X]
- Responses received: [X]
- New partners: [X]
- Pipeline value (projected): $[est]

#### Automation Health
- Cron jobs: [X]/17 healthy
- Failures this week: [X]
- Manual interventions needed: [X]
- Automation rate: [XX]%

### Step 3: Generate Weekly Report
Save to: `~/NurseRob_PeptideEmpire/reports/weekly_report_[YYYY-MM-DD].md`

```markdown
# Nurse Rob Peptide Empire — Weekly Report
**Week of:** [Mon date] — [Sun date] 
**Generated:** Sunday, [date] 6:00 PM MST
**Profile:** grok-mode | Hermes v0.11.0

## 📊 EXECUTIVE SUMMARY
[3-4 sentence overview of the week — wins, concerns, trend direction]

## 📈 CONTENT PERFORMANCE
| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| Posts Published | [X]/21 | [Y]/21 | +/-[Z] |
| Engagement Rate | [X.X]% | [Y.Y]% | +/-[Z] |
| Top Post Impressions | [X,XXX] | - | - |

### Top 3 Posts
1. **[Title]** — [impressions] 👁️ [engagements] ❤️
   - Type: [Thread/Carousel] | Pillar: [Research/Myth/etc]
   - **Why it worked:** [analysis]
2. ...
3. ...

### Content Insights
- Best pillar: [pillar name] ([X.X]% engagement)
- Best format: [format] (avg [X] likes)
- Recommendation: [suggestion for next week]

## 🎯 LEAD PERFORMANCE
| Metric | Count |
|--------|-------|
| New Leads | [X] |
| Hot Leads | [X] |
| Auto-Replies | [X] |
| In Nurture | [X] |
| Converted | [X] |
| Conversion Rate | [X.X]% |

### Lead Insights
- Best lead source: [X/Discord/email]
- Most common question: "[question]"
- Recommendation: [suggestion]

## 💰 REVENUE BREAKDOWN
| Channel | Revenue | Units | Avg/Unit |
|---------|---------|-------|----------|
| Consults ($197-297) | $[X] | [X] | $[X] |
| Digital Products ($47-97) | $[X] | [X] | $[X] |
| Affiliate (15-30%) | $[X] | [X] clicks | $[X]/click |
| Group Coaching ($997/q) | $[X] | [X] | $[X] |
| **TOTAL** | **$[X,XXX]** | — | — |

### Revenue Insights
- Highest converting offer: [offer]
- Recommendation: [suggestion]

## 💊 PHARMACY PIPELINE
| Stage | Count |
|-------|-------|
| New (scouted) | [X] |
| Outreach Active | [X] |
| Negotiating | [X] |
| Partners | [X] |
| Declined | [X] |

## ⚙️ AUTOMATION HEALTH
| Status | Count |
|--------|-------|
| 🟢 Healthy | [X]/17 |
| 🔴 Failed | [X]/17 |
| Automation Rate | [XX]% |
| Interventions Needed | [X] |

## 🔬 FDA UPDATES
[Summary of this week's relevant FDA activity]

## 🎯 NEXT WEEK RECOMMENDATIONS
1. [Actionable recommendation based on data]
2. [Actionable recommendation]
3. [Actionable recommendation]

## 📊 30-DAY TREND (Sparklines)
Content: ▁▂▃▄█ — UP
Revenue: ▃▃▂▄▅ — UP
Leads:   ▂▁▃▃▄ — UP SLIGHTLY

---
*Report generated by NurseRob Analytics v1.0 | Hermes v0.11.0*
*Data is for internal business use. Revenue figures are estimates.*
```

### Step 4: Push Report + Update Master Content Rules (CLOSED LOOP)
- Save to reports folder: `~/NurseRob_PeptideEmpire/reports/weekly_report_[YYYY-MM-DD].md`
- Push summary to dashboard: update `~/NurseRob_PeptideEmpire/dashboard/metrics.json` by adding a `weekly_report` key with the week's KPIs
- Set `last_updated_by` to `weekly_analytics_report`
- Read previous week's report (from `reports/`) for week-over-week comparison data

**NEW — Performance Feedback Loop (Step 4B):**
After generating the report, update the Master Content Rules file with top-performing patterns:
1. Identify the top 3 posts by engagement (impressions + likes + replies)
2. Extract their hook pattern, format, content pillar, and CTA type
3. Read `/home/robert/NurseRob_PeptideEmpire/content/master_content_rules_v1.3.md`
4. Add a new `## Weekly Winners (Auto-Generated)` section at the bottom with:
   - Date and report reference
   - Top 3 winning patterns (hook + format + pillar)
   - One specific phrasing that worked (exact quote from top post)
   - "Try this pattern" recommendation for the week ahead
5. This creates a self-improving content system — every week's best performers become next week's templates
6. Both generators (daily + weekly batch) read the master rules file, so winning patterns automatically influence future content

### Step 5: Validate
- Confirm report file was saved (check existence with `os.path.exists`)
- Confirm dashboard metrics were updated (verify `weekly_report` key in dashboard JSON)

## PITFALLS
- **Skill naming mismatch:** The cron job references this skill as `nurserob_analytics` (underscores) but the installed skill is `nurserob-analytics` (hyphens). This causes a "Skill not found" notice at the start of every analytics run. Same issue affects `nurserob_affiliate_manager` (underscores in cron) vs `nurserob-affiliate-manager` (hyphens installed). If a cron job reports the skill wasn't found, this is why — check both name forms.
- Don't inflate metrics — report actual data even if down
- "No data yet" is better than made-up numbers
- Focus on actionable insights, not just data dump
- Highlight what Nurse Rob should CHANGE, not just what happened
- **Pre-launch revenue:** The report template shows realistic placeholder numbers ($380, $210) — do NOT copy those. Report actual data ($0 across channels when in pre-launch). The value of a pre-launch report is in blockers documentation and trend tracking, not revenue figures.
- **File I/O for JSON:** Use `subprocess.run(['cat', path])` for reads and `subprocess.run(['tee', path], input=json.dumps(data, indent=2))` for writes. Never use `read_file`/`write_file` — they produce line-numbered text that breaks JSON parsing.
- **Affiliate dependency:** The affiliate report runs at 5PM (1 hour before analytics). Read the just-generated affiliate report file for latest blockers and pharmacy pipeline data. If the file doesn't exist, check `tracking.json` in the affiliates directory.
- **post_log.json mixed structure:** The top level of post_log.json contains BOTH metadata keys (status, error, fix, posts_generated, days_blocked, posts[]) AND date-keyed entries ("2026-05-10": {...}). The top-level `posts` key is an array of the latest generated posts (3 objects), NOT nested under a date key. Iterating with `for key in log:` will hit metadata strings and integers alongside date dicts — always filter: `if isinstance(val, dict) and k.startswith('202')`. See the dashboard manager's `references/data-formats-and-paths.md` for full details.
- **Previous report for comparison:** Read `/home/robert/NurseRob_PeptideEmpire/reports/weekly_report_[last_week].md` to extract prior-week KPIs. Use `sorted(glob.glob(...), reverse=True)[1]` to get the last report.
- **Content file globs:** When searching for content files, use `glob.glob(f'{BASE}/content/*posts*')` in Python, NOT `subprocess.run(['ls', BASE+'/content/*posts*'])` — the latter silently fails because subprocess doesn't expand shell wildcards.
- **Dashboard update format:** When updating metrics.json, add a `weekly_report` dict — do NOT overwrite the entire file. Read first, append, write back.

## QUALITY CHECKLIST
- [ ] All data sources loaded
- [ ] KPIs calculated correctly
- [ ] Week-over-week comparisons where available (load previous report)
- [ ] At least 3 actionable recommendations
- [ ] Report saved with correct filename
- [ ] Report file confirmed on disk
- [ ] Dashboard updated with summary (metrics.json `weekly_report` key added)
- [ ] Trends direction indicated
- [ ] All data accurate — no placeholder numbers for revenue ($0 is correct in pre-launch)
