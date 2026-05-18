---
name: content-batch-generator
description: Produces 7-10 days of Nurse Rob peptide content weekly — threads, engagement posts, image prompts, v1.3 compliant
version: 2.2
author: Nurse Rob
---

# Content Batch Generator v2.2 📅

**Purpose:** Weekly content batch — generates the next 7-10 days of posts (14-20 total). Runs every Sunday 6AM MST. Outputs to date-stamped content files ready for the daily scheduler.

## v2.2 Changelog (Weekly + v1.3 — May 2026)
- Changed from 30-day monthly batch to 7-10 day weekly batch (peptide landscape moves too fast for monthly)
- Now loads Master Content Rules v1.3 as the authoritative source for voice/hooks/CTAs/FDA language
- All "heal/healing/miracle/cure" language stripped — replaced with v1.3-safe alternatives
- Brand colors updated to navy #0A1F3F / teal #00C4B4 / gold #C9A84C
- Optimizer feedback loop closed: content rules flow from optimizer → master rules file → batch generator → daily generator

## ⚠️ CRITICAL — Load Order (MUST follow this exactly)

1. **FIRST:** Load `nurse-rob-x-reply-guidelines` v1.3 (liability protection, FDA language rules, word boundaries)
2. **SECOND:** Load the Master Content Rules file at `/home/robert/NurseRob_PeptideEmpire/content/master_content_rules_v1.3.md`
3. **THIRD:** Load `peptide_content_operator` v2.10+ (voice, hooks, CTAs, thread structure)

The Master Content Rules file is the single source of truth — it overrides anything in the other skills.

## TRIGGER
- "generate next 7-10 days"
- "batch content for this week"
- Weekly cron: Sunday 6AM MST, loads v1.3 + Master Content Rules first

## PROFILE ROUTING
Use `creative-mode` (gpt-5.5-codex) — creative output + speed for batch generation.

## WORKFLOW

### Step 1: Research Phase (grok-mode for truth)
```bash
web_search "peptide research breakthroughs 2026"
web_search "FDA compounding pharmacy regulations update"
web_search "popular peptide topics trending 2026"
web_search "biohacking peptide stack protocols 2026"
```
Collect 10-15 topics for the month.

### Step 2: Build Calendar Structure
Create 30-day grid with:
- 6 Educational Threads per week (Mon-Sat)
- 1 Lead Magnet Promo per week (Sun)
- 2 Myth-Busters per week
- 3 Engagement Posts per week (polls, Q&As, hot takes)
- 1 Case Study per week
- 1 "Behind the Scenes" per week (personal brand)

### Step 3: Generate All Content
For EACH day generate EXACTLY 2 posts:
1. **Post 1** (9 AM MST): Primary thread or carousel
2. **Post 2** (5 PM MST): Rotating format (Mon=Poll, Wed=Myth-Buster, Fri=Hot Take, Tue/Thu/Sat/Sun per content_operator v2.5 rotation)

Each post includes:
- Complete text (thread formatted with 🧵 and tweet numbers)
- Image prompt for image-generator
- CTA from the tiered CTA menu in peptide_content_operator v2.3 (Thread/Engagement/Short-Form specific)
- Liability disclaimer
- RN credential in first sentence of EVERY post

### Step 4: Generate Image Prompts
For each post needing visuals:
```
Nurse Rob branding: Professional male nurse (30s), clean modern background,
navy + white + accent red color scheme, confident but approachable,
clinical aesthetic. Photorealistic, 4K.
Aspect ratios: 16:9 landscape (thread headers), 1:1 square (carousels),
9:16 portrait (Reels/stories).
```

### Step 5: Write Calendar File
Save to: `~/NurseRob_PeptideEmpire/Content_Calendar/30_Day_Calendar_[MONTH].md`

Format:
```markdown
# Nurse Rob 30-Day Content Calendar — [Month Year]
*Generated: [Date] | Hermes v0.11.0 | creative-mode*

## Week 1: Foundation & Trust

### Day 1 — Monday, [Date]
**Theme:** [Pillar tag]
**Post 1 (9AM):** Thread — [Title]\n[Full thread content with tweet numbers]\n**Image:** [image prompt]\n**CTA:** [CTA text]\n**Disclaimer:** [disclaimer text]\n---\n**Post 2 (5PM):** [Format] — [Description]\n[Full content]\n---
*...repeat for all 30 days...*
```

### Step 6: Push to Content Scheduler
```bash
# After generation, feed to scheduler
"Load ~/NurseRob_PeptideEmpire/Content_Calendar/30_Day_Calendar_[MONTH].md 
into content_scheduler for daily auto-posting"
```

## 30-DAY CONTENT THEMES (Rotating)

### Week 1: Foundation & Trust
| Day | Topic Theme | Pillar |
|-----|------------|--------|
| 1 | "Why an RN is your best peptide guide" | Nurse Perspective |
| 2 | BPC-157 research deep dive | Research |
| 3 | Blood work basics for peptide users | Research |
| 4 | "Bro-science vs clinical reality" | Myth Busting |
| 5 | Tirzepatide vs Semaglutide breakdown | Research |
| 6 | Weekend peptide Q&A | Engagement |
| 7 | Wolverine Stack Calculator promo | Lead Magnet |

### Week 2: Deep Science
| Day | Topic Theme | Pillar |
|-----|------------|--------|
| 8 | NAD+ and cellular aging | Research |
| 9 | Ipamorelin + CJC-1295 dosing | Research |
| 10 | "Your peptide source might be dangerous" | Myth Busting |
| 11 | Blood work markers deep dive | Research |
| 12 | GLP-1s: the nurse's perspective | Nurse Perspective |
| 13 | Weekend case study | Case Study |
| 14 | "Why I left bedside nursing" | Nurse Perspective |

### Week 3: Optimization
| Day | Topic Theme | Pillar |
|-----|------------|--------|
| 15 | Peptide storage and handling | Research |
| 16 | "Debunking: peptides are steroids" | Myth Busting |
| 17 | Lab testing: what to actually test | Research |
| 18 | Stacking protocols explained | Research |
| 19 | FDA compounding update | Regulatory |
| 20 | Weekend Q&A + case study | Engagement |
| 21 | Peptide Safety Protocol promo | Digital Product |

### Week 4: Action & Offers
| Day | Topic Theme | Pillar |
|-----|------------|--------|
| 22 | Injection technique (RN tips) | Nurse Perspective |
| 23 | "5 peptide myths I debunk weekly" | Myth Busting |
| 24 | Affiliate: "What I actually use" | Affiliate |
| 25 | Cycling protocols explained | Research |
| 26 | Consult testimonials (anonymized) | Social Proof |
| 27 | Weekend engagement poll | Engagement |
| 28 | Group coaching promo | Monetization |

*(Days 29-30: Overflow / trending topics / news-jacking)*

## MONETIZATION CALENDAR (Integrated)
| Week | Offer | Frequency |
|------|-------|-----------|
| 1 | Wolverine Stack Calculator (lead magnet) | 2x |
| 2 | Peptide Safety Protocol ($47) | 1x |
| 3 | 1-on-1 Consults ($197) | 1x |
| 4 | Group Coaching ($997/quarter) + Affiliate | 2x |

## QUALITY CHECKLIST (v2.3 compatible)
- [ ] All 30 days have 2 posts each (60 total)
- [ ] RN credential in first sentence of EVERY post (see peptide_content_operator v2.3)
- [ ] Every post has disclaimer
- [ ] Image prompts included for visual posts
- [ ] CTAs from tiered CTA menu — no bare "follow/save"
- [ ] Hooks from pattern menu — no banned openers
- [ ] Nurse Rob voice consistent across all posts — no marketing language
- [ ] Research claims have source references (year, journal, finding)
- [ ] Calendar file properly formatted
- [ ] Content pillars balanced across month (4 pillars: Research 45%, Myth 25%, Regulatory 20%, Nurse 10%)
- [ ] Each post passes Scroll-Stop Check: "Would I stop scrolling?"
