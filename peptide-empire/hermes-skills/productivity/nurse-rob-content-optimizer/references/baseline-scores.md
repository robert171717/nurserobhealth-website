# Baseline Scoring Session — 2026-05-10

## Pre-Optimization Baseline: 82.2/100

### Per-Post Scores

| # | Format | Topic | Med Acc | Voice | Hook | CTA | Sig | Score |
|---|--------|-------|:-------:|:-----:|:----:|:---:|:---:|:-----:|
| 1 | Thread | BPC-157 Deep Dive | 18 | 18 | 17 | 15 | 20 | 88.0 |
| 2 | Poll | Steps to Protocol | 16 | 17 | 15 | 14 | 20 | 82.0 |
| 3 | Myth-Buster | NAD+ Bioavailability | 18 | 17 | 18 | 16 | 20 | 89.0 |
| 4 | Short Form | Survey Stats / Follow CTA | 15 | 18 | 17 | 14 | 10 | 74.0 |
| 5 | Short Form | Long-Term Safety / Save CTA | 17 | 16 | 16 | 14 | 15 | 78.0 |

### Dimension Averages
- Medical Accuracy: 16.8
- Brand Voice: 17.2
- Hook Strength: 16.6
- CTA Quality: 14.6 ← **WEAKEST**
- Signature Elements: 17.0

### Key Findings
- Thread format carries the brand well (88) — RN credential + disclaimer are automatic there.
- Short-form posts bleed signature elements (74, 78) — tight character count forces agents to cut disclaimers and RN credential.
- CTAs are functional but generic: "link in bio" and "Drop your answer" lack specificity.
- Poll posts would score higher if the CTA matched the clinical framing better.
- All posts pass safety checks; no auto-discards.

---

## Post-Optimization Result: 93.6/100 (+11.4)

15 iterations attempted, 9 kept, 6 discarded.

### Gains by Dimension

| Dimension | Before | After | Delta | What fixed it |
|-----------|:------:|:-----:|:-----:|---------------|
| CTA Quality | 14.6 | 20.0 | **+5.4** | Research Curiosity CTA, mid-thread CTA for 7+ tweets, QUIZ CTA for engagement |
| Hook Strength | 16.6 | 19.8 | **+3.2** | Research Contradiction + Pattern Interrupt + Fill-in-the-Blank hooks |
| Brand Voice | 17.2 | 18.6 | +1.4 | Anti-salesy phrases ("I'm not here to sell you"), nuance positioning |
| Signature Elements | 17.0 | 17.8 | +0.8 | Phrase additions reinforce brand identity in tight spaces |
| Medical Accuracy | 16.8 | 17.4 | +0.6 | Pillar shift 45→48% research, "cornerstone of credibility" framing |

### Kept Mutations

| # | Δ | Cat | Change |
|---|----|-----|--------|
| 1 | +2.2 | Voice | Added "Let me be direct with you" + "I'm not here to sell you anything" to USE phrases |
| 4 | +0.8 | CTA | Added Research Curiosity CTA to Short-Form section |
| 8 | +1.8 | Hook | Added The Research Contradiction hook |
| 9 | +1.4 | CTA | Added mid-thread CTA guidance for 7+ tweet threads |
| 10 | +0.6 | Pillars | Shifted pillar weights: 48/25/20/7 |
| 11 | +0.2 | Voice | Added nuance phrase to USE list |
| 12 | +0.8 | Engagement | Added Fill in the Blank as alternate Thursday format |
| 13 | +0.6 | CTA | Added QUIZ CTA to Engagement CTAs |
| 15 | +0.8 | Hook | Added Pattern Interrupt hook |

### What Failed

| # | Cat | Change | Why |
|---|-----|--------|-----|
| 2 | Voice | Added warmth to tone description | 0.0 — Current tone already strong enough |
| 3 | Hook | Pattern Interrupt (first try) | 0.0 — Wrong placement, succeeded at iter 15 with different phrasing |
| 5 | Thread | Added Real Talk tweet | -2.6 — Added structural complexity without quality gain |
| 6 | Voice | Added "biohack" to AVOID | -0.8 — AVOID list already covered this implicitly |
| 7 | Engagement | Quiz format on Wed | -1.8 — Poll/myth-buster/myth rotation already strong |
| 14 | Voice | "biohack" + supplement-ad language to AVOID | 0.0 — Duplicate of iter 6, same result |

### Process Notes
- Two-pass pattern worked: first 5 iterations (cold start) had 2 keeps, second 10 iterations (exploitation) had 7 keeps.
- Cumulative scoring was critical — evaluating mutations against original baseline (82.2) would have undercounted synergy between voice + CTA + hook changes.
- No protected sections were touched during any iteration.

---

# Baseline Scoring Session — 2026-05-17 (v2.8 → v2.9)

## Pre-Optimization Baseline: 90.4/100

Starting from v2.8 (which already incorporated the 2026-05-10 optimizer gains).

### Per-Post Scores

| # | Format | Topic | Med Acc | Voice | Hook | CTA | Sig | Score |
|---|--------|-------|:-------:|:-----:|:----:|:---:|:---:|:-----:|
| 1 | Thread | BPC-157 tendon recovery (2025 clinical data) | 18 | 19 | 19 | 18 | 20 | 94 |
| 2 | Poll | Peptide sourcing habits | 17 | 18 | 17 | 15 | 15 | 82 |
| 3 | Myth-Buster | "More peptides = better" myth | 18 | 19 | 19 | 17 | 18 | 91 |
| 4 | Short Form | GLP-1 research gap (75% stop rate) | 17 | 19 | 19 | 18 | 18 | 91 |
| 5 | Short Form | NAD+ IV vs oral evidence gap | 18 | 20 | 20 | 18 | 18 | 94 |

### Dimension Averages
- Medical Accuracy: 17.6
- Brand Voice: 19.0
- Hook Strength: 18.8
- CTA Quality: 17.2 ← **WEAKEST**
- Signature Elements: 17.8

### Key Findings
- v2.8 was already strong. Voice and Hook were near ceiling (19.0, 18.8).
- CTA Quality (17.2) was the remaining headroom — consistent with the 05-10 session where CTA was the biggest gainer.
- Poll format (82) dragged the baseline down due to weaker CTA and missing disclaimer in signature check.

---

## Post-Optimization Result: 97.3/100 (+6.9)

9 iterations attempted, **9 kept, 0 discarded**. Early stop after 3 consecutive <0.5 delta.

### Scoring Formula Note
This was the first run where the scoring formula trap was discovered and fixed. The rubric says each dimension is 0-20, and COMPOSITE was previously specified as `AVG(...)` (0-20 scale). However, all reference scores use SUM (0-100). Using AVG produces "baseline 18.1" and false discards. Using SUM produces correct results. The optimizer SKILL.md now explicitly clarifies: **COMPOSITE = SUM of 5 dimensions (0-100), not AVG (0-20).**

### Gains by Dimension

| Dimension | Before | After | Delta | What fixed it |
|-----------|:------:|:-----:|:-----:|---------------|
| CTA Quality | 17.2 | 20.0 | **+2.8** | Clinical Curiosity CTA (Short-Form), mid-thread phrasing enhancement, Safety Check CTA (Engagement) |
| Signature Elements | 17.8 | 19.7 | **+1.9** | Premium framing directive, Reality Check tweet slot, AVOID list expansion (stack/biohack) |
| Hook Strength | 18.8 | 20.0 | +1.2 | Vulnerability Hook (with rotation cap) |
| Brand Voice | 19.0 | 20.0 | +1.0 | "Stop guessing with your health" phrase, Premium framing, AVOID list expansion |
| Medical Accuracy | 17.6 | 17.6 | ±0.0 | No accuracy-targeted mutations this run |

### Kept Mutations

| # | Δ | Cat | Change |
|---|----|-----|--------|
| 1 | +1.5 | Voice | Added "Stop guessing with your health." to Phrases to USE |
| 2 | +1.1 | Hook | Added The Vulnerability Hook with max 1x/week rotation cap |
| 3 | +2.0 | CTA | Added Clinical Curiosity CTA to Short-Form |
| 4 | +0.5 | Thread | Added "The Reality Check" tweet (position 4, data-gap slot). Extended 7→8 tweets |
| 5 | +0.9 | Engagement | Added Clinical Trial Tuesday as alternate Tuesday format |
| 6 | +0.5 | CTA | Enhanced mid-thread CTA with specific re-engagement phrasing |
| 7 | +0.1 | Voice | Added Premium framing directive (peptides = medical tools, not biohacking toys) |
| 8 | +0.2 | CTA | Added Safety Check CTA to Engagement CTAs |
| 9 | +0.1 | Voice | Strengthened AVOID list: "stack/stacking" and "biohack/biohacking" |

### What Wasn't Tried (discarded by early stop)
No iterations were discarded — all 9 were kept. The loop stopped naturally after 3 consecutive <0.5 deltas (iterations 7, 8, 9).

### Process Notes
- First-pass scoring (AVG) produced "baseline 18.1" with 12/15 discarded. Fixed to SUM → "baseline 90.4" with 9/9 kept. **Critical diagnostic: >50% discard rate → check scoring formula first.**
- All 5 mutation categories (voice, hook, CTA, thread, engagement) produced positive deltas — no cold-start losses this run.
- The Vulnerability Hook (Δ=+1.1) triggered the rotation-cap companion mutation automatically.
- Early stop fired at iteration 9 (3 consecutive <0.5 kept deltas). 9 iterations vs 15 planned — saved ~40% of runtime.
- No protected sections were touched.
- The 0 discarded mutations is unusual and likely reflects that v2.8 had ample headroom in CTA and Signature that any reasonable mutation in those categories added value. Future runs from v2.9 will likely see more discards as dimensions approach ceiling.

---

# Targeted Listicle Pass — 2026-05-17 (v2.9 → v2.10)

## Pre-Optimization Baseline: 83.8/100

New format under test: Bullet-List Authority Post (Listicle), modeled on Healthy Alfred's 176K-impression mastic gum listicle. Targeted 5-iteration pass on the new format only.

### Per-Post Scores

| # | Format | Topic | Med Acc | Voice | Hook | CTA | Sig | Score |
|---|--------|-------|:-------:|:-----:|:----:|:---:|:---:|:-----:|
| 1 | Thread | BPC-157 Mechanism Deep Dive | 18 | 18 | 16 | 17 | 18 | 87 |
| 2 | **Listicle** | **TB-500 Unexpected Findings** | 19 | 16 | 18 | 17 | 16 | **86** |
| 3 | Short Form | NAD+ Quick Hit | 17 | 16 | 15 | 16 | 15 | 79 |
| 4 | Myth-Buster | "More Peptides = Better" | 17 | 17 | 15 | 16 | 16 | 81 |
| 5 | Hot Take | GLP-1 Peptide Ethics | 18 | 18 | 17 | 16 | 17 | 86 |

### Dimension Averages
- Medical Accuracy: 17.8
- Brand Voice: 17.0
- Hook Strength: 16.2 ← **WEAKEST**
- CTA Quality: 16.4
- Signature Elements: 16.4

### Key Findings
- The new listicle format (Post 2) scored 86 on first draft — solid debut. Voice (16) and Signature (16) were the drag.
- Listacle reads too much like a textbook page without conversational breaks between bullets.
- The Shocking Mechanism hook landed well (18) but needed concrete "wait, really?" specificity, not vague "changed everything" claims.
- CTA was functional but not memorable — "Save this. Your next conversation with your doctor will be better for it."

---

## Post-Optimization Result: ~87.5/100 (projected +3.7)

5 iterations attempted, **5 kept, 0 discarded**. Mutations focused exclusively on listicle format quality.

### Gains by Dimension

| Dimension | Before | After | Delta | What fixed it |
|-----------|:------:|:-----:|:-----:|---------------|
| Hook Strength | 16.2 | 17.6 | **+1.4** | Shocking Mechanism hook examples + quality rule (specificity test) |
| Brand Voice | 17.0 | 17.8 | +0.8 | Voice rule (conversational aside between bullets) + synthesis sentence |
| CTA Quality | 16.4 | 17.2 | +0.8 | Strengthened Listicle Authority CTA: "When your doctor asks where you learned this, you'll have the citations" |
| Signature Elements | 16.4 | 17.0 | +0.6 | Synthesis sentence rule ties bullets into nurse perspective |
| Medical Accuracy | 17.8 | 17.8 | ±0.0 | No accuracy-targeted mutations |

### Kept Mutations

| # | Δ | Cat | Change |
|---|----|-----|--------|
| 1 | +1V | Voice | Added "Voice rule" to listicle: conversational aside between bullet groups, nurse-pointing-at-chart tone |
| 2 | +1H | Hook | Added 3 Shocking Mechanism hook examples specific to listicles (BPC-157, TB-500, Semaglutide) |
| 3 | +1V/+1S | Voice+Sig | Added synthesis sentence rule: listicle must end with one memorable takeaway before disclaimer |
| 4 | +1C | CTA | Strengthened Listicle Authority CTA phrasing |
| 5 | +1H | Hook | Added Shocking Mechanism quality rule: specificity test ("wait, really?"), named mechanism requirement |

### Process Notes
- Targeted pass (listacle-only mutations) was efficient — 5 iterations vs full 15-iteration run. Saved ~67% of runtime.
- New format integration checklist: add format to Post 2 rotation, add CTA to menu, add hook to capped hooks, update Quick Reference, update track_hooks.py.
- The Shocking Mechanism hook was added to CAPPED_HOOKS in track_hooks.py alongside Vulnerability Hook, Research Contradiction, and Pattern Interrupt — all 4 capped at 1x/week.
- Pitfall discovered: agents modeling on competitor content (Healthy Alfred) will copy their monetization tactics (affiliate codes, shipping claims) even when instructed not to. Added permanent pitfall to peptide_content_operator.
- Listicle format won't fire in cron until next Saturday (biweekly with Behind-Scenes). Verify first live execution for char count compliance.
