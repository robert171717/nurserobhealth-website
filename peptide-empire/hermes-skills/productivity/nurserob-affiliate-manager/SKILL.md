---
name: nurserob-affiliate-manager
description: Tracks all Nurse Rob affiliate links, clicks, conversions, payouts — with optimization recommendations
version: 1.1
author: Nurse Rob
---

# NurseRob Affiliate Manager 💸

**Purpose:** Centralized tracking and optimization for all Nurse Rob Peptide Empire affiliate relationships — link management, click tracking, conversion monitoring, payout reconciliation, and placement optimization.

## TRIGGER
- Weekly cron: Sunday 5:00 PM MST (before analytics report)
- Manual: "check affiliate stats" / "affiliate report"
- New affiliate partner added

## PROFILE ROUTING
Use `default` (deepseek-v4-pro) — accurate data tracking.

## DATA FILES

Two JSON files track affiliate state (both under `~/NurseRob_PeptideEmpire/affiliates/`):

### `tracking.json` — Live State (Always Exists)
Created automatically on first cron run. Tracks current period metrics. Updated every Sunday.

```json
{
  "report_generated": "2026-05-10T17:00:00-07:00",
  "total_affiliate_links": 0,
  "total_clicks_all_time": 0,
  "total_clicks_this_week": 0,
  "total_conversions": 0,
  "total_revenue_estimate": 0,
  "blockers": ["...", "..."],
  "next_steps": ["...", "..."],
  "categories": [...]
}
```

### `partner_registry.json` — Partner Contracts (Pre-Launch)
Only created when actual affiliate partnerships are active. Currently does not exist (pre-launch state). Use `tracking.json` for all weekly reporting until partners are live.

```json
{
  "partners": [
    {
      "partner_id": "aff_001",
      "name": "LabCorp OnDemand",
      "category": "lab_testing",
      "commission": "20%",
      "cookie_days": 30,
      "affiliate_link": "https://labcorp.com/r/nurserob",
      "tracking_code": "NURSEROB20",
      "status": "active",
      "joined": "2026-05-01",
      "payout_schedule": "monthly",
      "payout_method": "ACH",
      "notes": "Blood work panels — high intent audience"
    }
  ]
}
```

## AFFILIATE CATEGORIES (Tracker)
The tracking.json uses these 5 categories (aligned with what's actually tracked):

| Category | Label | Commission Range | Status |
|----------|-------|------------------|--------|
| peptide_suppliers | Peptide Suppliers (Research Chemical Cos) | 15-30% | not_configured |
| lab_testing | Lab Testing Services (Blood Work Panels) | 15-30% | not_configured |
| supplements | Supplement Brands (NAC, NAD+, Magnesium) | 15-30% | not_configured |
| biohacking_gear | Biohacking Gear (Red Light Therapy, Cold Plunge) | 15-30% | not_configured |
| pharmacy_partners | Pharmacy Affiliate Partnerships | 15-30% | not_configured |

## PRE-LAUNCH / ZERO-DATA MODE

When no affiliate partnerships exist (pre-launch state), the weekly cron still runs and must produce a valid report. All metrics will be $0 with blockers documented. The report still serves value as a weekly status checkpoint.

### Step 0: Detect Mode
Read `tracking.json` — if `total_affiliate_links === 0` across all categories, you're in pre-launch mode.

**Reading JSON files safely (always use execute_code with subprocess):**
```python
import subprocess, json
r = subprocess.run(['cat', f'{BASE}/affiliates/tracking.json'], capture_output=True, text=True, timeout=5)
tracking = json.loads(r.stdout)
```
Do NOT use `read_file` — it returns line-numbered text that breaks `json.loads()`.

### Step 0b: Check Blockers
In pre-launch mode, EVERY weekly report should re-check these blockers and update their language:

1. **xurl auth status** — Check if posting is blocked (`xurl auth status` via terminal). If the app shows `oauth2: NurseRobHealth` but `(no credentials)`, the token expired. Update day count.
2. **Partner registry** — Does `partner_registry.json` exist?
3. **Pharmacy pipeline** — Have any pharmacies reached Stage 3+ (partnership proposal)?
4. **Monetization setup** — Is Stripe/Gumroad/ConvertKit configured?

### Step 0c: Generate Report Even When $0
The report must be saved even with zero data. It provides:
- Week-over-week tracking of how long the program has been dormant
- Blocker documentation for Nurse Rob to review
- Pharmacy pipeline status as a leading indicator of future partnerships
- Accountability metric: "Day X of zero content posting"

### Step 0d: Pre-Launch Report Generation
When in pre-launch mode, replace Steps 1-4 below with this condensed workflow:

1. **Read tracking.json** — Load from `~/NurseRob_PeptideEmpire/affiliates/tracking.json`
2. **Update week counters** — Reset `total_clicks_this_week` to 0, update `report_generated` timestamp
3. **Update blockers** — Refresh the blockers array with current state (check xurl auth status, days blocked)
4. **Update next_steps** — Refresh with priority-ordered next steps
5. **Write updated tracking.json** — `subprocess.run(['tee', path], input=json.dumps(data, indent=2))`
6. **Update dashboard metrics.json** — Update `metrics.json` fields:
   - `revenue_mtd.affiliate` — reset to $0
   - `affiliate_dashboard` — update blockers, day count, week count, report_week range
   - `cron_status.Affiliate Weekly Report` — update last_run timestamp, note
   - Write via `subprocess.run(['tee', path], input=json.dumps(data, indent=2))`
7. **Generate report markdown** — Save to `affiliate_report_[YYYY-MM-DD].md`
8. **Validate** — Confirm both JSON files parse correctly with `json.loads()`

## WORKFLOW

### Step 1: Collect Click Data
For each affiliate link, check click metrics:
- X bio link clicks (analytics)
- Email click tracking
- Content post link clicks

### Step 2: Track Conversions
- Check affiliate dashboards for each partner
- Log conversion events: `purchase`, `signup`, `trial_start`
- Calculate: conversion_rate = conversions / clicks

### Step 3: Calculate Revenue
- Revenue = conversions × average_order_value × commission_rate
- Track per-partner revenue
- Track trend: week-over-week, month-over-month

### Step 4: Optimize Placements
Analyze which placements drive the most conversions:
- X bio link
- Content thread "link in bio"
- Email nurture sequences
- Lead magnet PDF
- Consult follow-up materials
- Dashboard quick links

### Step 5: Generate Affiliate Report
Save to: `~/NurseRob_PeptideEmpire/affiliates/affiliate_report_[YYYY-MM-DD].md`

```markdown
# Nurse Rob Affiliate Report — Week of [date]
**Generated:** Sunday, [date] 5:00 PM MST

## 💰 AFFILIATE REVENUE SUMMARY
| Partner | Clicks | Conversions | Conv Rate | Revenue | Trend |
|---------|--------|-------------|-----------|---------|-------|
| LabCorp | 145 | 8 | 5.5% | $174 | ↑ |
| [Partner] | [X] | [X] | [X.X]% | $[X] | → |
| **TOTAL** | **340** | **12** | **3.5%** | **$380** | ↑ |

## 📊 PERFORMANCE BY CATEGORY
| Category | Revenue | % of Total |
|----------|---------|------------|
| Lab Testing | $380 | 55% |
| Supplements | $210 | 30% |
| Biohacking Gear | $105 | 15% |

## 🔗 TOP PERFORMING LINKS
1. **[Link Name]** — [X] clicks, [X] conversions, $[X] revenue
   - Placement: [where]
   - Recommendation: [increase/decrease/keep]

## ⚠️ UNDERPERFORMING LINKS
1. **[Link Name]** — [X] clicks, 0 conversions
   - Recommendation: [move placement / replace partner / test new CTA]

## 🎯 NEXT WEEK OPTIMIZATIONS
1. [Actionable change]
2. [Actionable change]

## 📈 30-DAY TREND
Week 1: $280 → Week 2: $310 → Week 3: $350 → Week 4: $380 📈

---
*All revenue figures are estimates based on reported clicks and average conversion rates.*
```

### Step 6: Update Dashboard
Call `nurserob-dashboard-manager`:
"Affiliate update: $[X] revenue this week, [X] total clicks, [X] conversions"

## AFFILIATE LINK PLACEMENT STRATEGY

### High-Intent Placements (Convert Best)
1. **Consult follow-up email** — "Here's the lab I use and trust"
2. **Lead magnet PDF** — "Recommended testing services"
3. **Direct reply to "where to buy" questions** — "I recommend [partner]"

### Medium-Intent Placements
4. **Educational thread (soft mention)** — "I use [partner] for my own blood work"
5. **Email nurture (Day 4)** — Value-first, then mention
6. **Dashboard quick links**

### Brand-Building Placements (Low Conversion, High Trust)
7. **X bio** — "Lab testing I use: [link]"
8. **Content footer** — "Tools I use and trust → link in bio"

## DISCLAIMER REQUIREMENTS
Every affiliate placement MUST include:
```
"Affiliate link — I may earn a commission at no extra cost to you. 
I only recommend products I've personally vetted as a licensed RN."
```

## PITFALLS
- The cron job references skill name `nurserob_affiliate_manager` (underscores) but the installed skill is `nurserob-affiliate-manager` (hyphens). If `skill_view` fails, check both name formats.
- Never promote products you haven't personally vetted
- Don't over-saturate — max 1 affiliate mention per content piece
- Track which partners actually pay out — some have terrible reporting
- Keep affiliate relationship transparent — it builds MORE trust
- Don't let affiliate revenue drive content — content drives affiliate
- **Pre-launch:** When `total_affiliate_links === 0`, don't skip the report — generate it anyway. The blockers documentation is the most valuable output.
- **File I/O:** Always use `subprocess.run(['cat', path])` and `subprocess.run(['tee', path], input=json.dumps(...))` for reading/writing JSON files. Do NOT use `read_file`/`write_file` Hermes tools — they return line-numbered content that breaks `json.loads()`.
- **Pharmacy pipeline in report:** Track pharmacy pipeline progress even though it's not affiliate revenue yet — Hallandale and Valor at Stage 1 (intro sent) are the closest to becoming affiliate partners.

## QUALITY CHECKLIST
- [ ] All active partner links working
- [ ] Click data collected for all partners
- [ ] Conversions tracked where possible
- [ ] Revenue calculated (estimates flagged)
- [ ] Top/bottom performers identified
- [ ] Optimization recommendations made
- [ ] Report saved and dashboard updated
- [ ] All affiliate mentions have disclaimer
- [ ] **Pre-launch:** Blockers refreshed with current xurl auth state and day count
- [ ] **Pre-launch:** tracking.json and metrics.json both updated with report timestamp
- [ ] **Pre-launch:** Pharmacy pipeline status included in report even if $0 affiliate revenue
- [ ] **Pre-launch:** `affiliate_report_[date].md` saved even when all metrics are zero
- [ ] **Pre-launch:** Report includes "next steps" section with priority-ordered actions for Nurse Rob
