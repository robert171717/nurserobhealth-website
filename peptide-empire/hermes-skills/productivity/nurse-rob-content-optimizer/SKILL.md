---
name: nurse-rob-content-optimizer
description: Karpathy-pattern autonomous content quality optimizer — modifies peptide_content_operator prompts, generates test posts, scores against rubric, keeps improvements overnight
version: 1.3
author: Nurse Rob + Hermes
trigger: optimize content, content optimizer, improve content prompts, run content loop
---

# Nurse Rob Content Optimizer — Karpathy Loop (v1.3)

## v1.3 Changelog (Session Hardening — 2026-05-17)
- **New mutation category: Example Quality.** Three sub-mutations proven in the 2026-05-17 listicle integration: (1) add concrete hook examples with real study citations for ambiguous hook patterns, (2) add quality rules with specificity tests to prevent vague claims, (3) add format-specific CTA entries for new formats. All three reliably produce +1 to +2 on Hook Strength or CTA Quality.
- **New pitfall: Competitor format porting without monetization stripping.** When modeling a new format on a competitor's content, their monetization tactics (affiliate codes, shipping claims) get embedded in examples. Must strip these unless Nurse Rob has equivalent infrastructure. Added as mutation step and standalone pitfall.
- **New protected section:** FDA-sensitive language rules per v1.3 (ALL forms of heal/healing/healed BANNED — use recovery/tissue-level outcomes; never cure/treat/miracle/fix/prevent/breakthrough) are now locked from optimizer modification.

**Pattern:** Autonomous content prompt optimization using Andrej Karpathy's autoresearch loop (keep/discard, single metric, fixed budget).

**What it does:** Modifies `peptide_content_operator/SKILL.md`, generates test posts, scores them against a quality rubric, keeps changes that improve the score, discards changes that don't. Runs overnight — you wake up to better content prompts.

## v1.2 Changelog (Scoring Formula Fix — 2026-05-17)
- **Fixed scoring formula ambiguity.** COMPOSITE was specified as `AVG(Accuracy, Voice, Hook, CTA, Signature)` which produces a 0-20 scale, but all reference scores use SUM (0-100). Changed to `SUM(...)` with an explicit clarification block and worked example from the 2026-05-17 run.
- **New pitfall: AVG vs SUM scoring trap.** Added diagnostic signal: >50% first-pass discard rate likely means the wrong formula was used. Reference data from the session showed AVG → 3/15 kept vs SUM → 9/9 kept.
- **New reference entry:** Added full 2026-05-17 run data to `references/baseline-scores.md` — including the scoring bug demonstration, per-post scores, kept mutations, and process notes.

## v1.1 Changelog (Session Hardening — 2026-05-10)
- **New mutation category: Complexity Management.** Optimizer can now add Quick Reference tables when SKILL.md exceeds 300 lines or 10+ hooks + 6+ formats. Also adds rotation caps (max 1x/week) as companion mutations when introducing high-impact hooks (delta ≥ +1.0).
- **New mutation category: Short-Form Hardening.** Optimizer can add fit formulas (Body ≤N + disclaimer + CTA = 280) and format-specific pre-save checklists for whichever format scores worst on signature elements.
- **New pitfall: Rotation cap gap.** Powerful hooks (+1.0+ delta) introduced without rotation guardrails create overuse risk. Optimizer must cap or flag in report.

## Prerequisites
- `peptide_content_operator` skill loaded
- `patch` tool available for SKILL.md modifications
- Backup of SKILL.md for rollback (`cp SKILL.md SKILL.md.bak` is sufficient — no git needed. The .bak file lets you diff to verify no protected sections were touched)

## The Loop

```
LOOP for N iterations (default: 30):
  1. READ current peptide_content_operator/SKILL.md
  2. MAKE one targeted change (see "What to Change" below)
  3. GENERATE 5 test posts (1 thread, 2 engagement, 2 short-form)
  4. SCORE each post against the rubric (0-100)
  5. COMPUTE composite score (average of 5)
  6. IF composite > baseline:
       → KEEP the change, update baseline to new high
       → Log: "✓ Iteration {N}: {score} (+{delta}) — {change_description}"
  7. IF composite ≤ baseline:
       → DISCARD (git reset / re-patch)
       → Log: "✗ Iteration {N}: {score} (-{delta}) — {change_description}"
```

## Scoring Rubric (0-100 per post)

See `references/baseline-scores.md` for real scored examples from the 2026-05-08 optimization session.

Each post scored on 5 dimensions (20 pts each):

### 1. Medical Accuracy (20 pts) — NON-NEGOTIABLE
- 20: Clinically precise, cites real mechanisms, acknowledges data gaps
- 15: Generally accurate but vague
- 10: Minor inaccuracies or oversimplification
- 5: Contains misleading or unverifiable claims
- 0: Dangerous or false medical claims → **AUTO-DISCARD regardless of other scores**

### 2. Brand Voice Authenticity (20 pts)
- 20: Sounds like a real RN explaining to a patient — direct, warm, credible
- 15: Mostly on-brand, one or two off-notes
- 10: Generic "health influencer" voice creeping in
- 5: Salesy, bro-science, or impersonal
- 0: Reads like AI-generated marketing copy → auto-penalty

### 3. Hook Strength (20 pts)
- 20: "I'd stop scrolling for this" — provocative, surprising, or deeply relatable
- 15: Solid hook, genuine curiosity generated
- 10: Competent but forgettable opener
- 5: Weak or cliché ("Have you heard about peptides?")
- 0: No hook at all, or actively repelling

### 4. CTA Quality (20 pts)
- 20: Natural next step, feels helpful not pushy, clear path forward
- 15: Good CTA, slightly formulaic
- 10: Forced or generic ("DM me" without reason)
- 5: Overly aggressive ("BOOK NOW" / "DON'T MISS OUT")
- 0: Missing CTA entirely, or actively off-putting

### 5. Nurse Rob Signature Elements (20 pts)
- 20: RN credential featured naturally + disclaimer included + source cited + reads well aloud
- 15: 3 of 4 elements present
- 10: 2 of 4 elements present
- 5: 1 of 4 present
- 0: None — generic content with no brand identity

### Composite Score
```
COMPOSITE = SUM(Accuracy, Voice, Hook, CTA, Signature) 
          — 15-point penalty if Medical Accuracy < 10 (safety override)
```

⚠️ **SCORING FORMULA CLARIFICATION:** Each dimension is scored 0-20. The per-post composite is the **SUM** of the 5 dimension scores (0-100 range). Do NOT use AVG (which would give 0-20) — the report format uses 0-100. The 2026-05-17 run confirmed this trap: first attempt with AVG gave "baseline 18.1" and 12/15 discarded; corrected to SUM gave "baseline 90.4" and 9/9 kept. If your first pass has >50% discard rate, check you're using SUM not AVG.

## What to Change (Targeted Mutations)

The optimizer should try ONE of these per iteration:

### Voice & Tone (high-leverage)
- Adjust Nurse Rob voice description (more direct / warmer / more clinical)
- Add or remove specific phrases ("Here's what the research actually shows")
- Tweak the "Avoid" list (add pet peeves, remove outdated ones)
- Adjust formality level (more casual? more authoritative?)

### Thread Structure (medium-leverage)
- Modify thread template (different flow, different number of tweets)
- Change hook strategy (question vs statement vs stat vs story)
- Adjust reply structure (more/fewer numbered points)
- Add or remove structural elements (personal anecdote slot, stat card tweet)

### Engagement Posts (medium-leverage)
- Add new engagement formats (quiz, "fill in the blank", controversial-but-true)
- Rotate which formats appear on which days
- Adjust tone for engagement posts (more playful vs more clinical)

### CTA Language (high-leverage)
- Vary CTA phrasing (direct vs suggestive, urgency vs helpfulness)
- Test different monetization CTAs (link in bio vs DM vs "save for later")
- Adjust soft-sell language
- Test CTA positioning (where in the thread does it appear)

### Selection Heuristics (meta)
- Adjust content pillar weightings (40/25/20/10/5 → test other ratios)
- Add or remove content pillars
- Modify daily rotation rules

### Complexity Management (meta — v1.1)
- **Add Quick Reference table** when SKILL.md exceeds 300 lines or has 10+ hook patterns + 6+ engagement formats + tiered CTAs. The v2.6→v2.7 transition proved agents get confused without one. Test: generate 3 posts with and without the table, score for format-rule compliance (not voice/hook/CTA). A table that reduces format errors by ≥1 post is a keep.
- **Add rotation caps** when introducing high-impact hooks (delta +1.0 or higher). The "Research Contradiction" hook scored +1.8 on voice but had no rotation guardrail — by iteration 15, an agent could easily overuse it. Companion mutation: when a new hook is kept, immediately test adding a "max 1x/week" cap. Score on voice consistency (does it prevent contrived-feeling repetition?).

### Short-Form Hardening (format-specific)
- **Add fit formula** for short-form posts (Body ≤N chars + disclaimer M chars + CTA K chars = 280). The v2.6 optimizer found short-form was the weakest format (avg 14.5/20 on signature elements) because agents couldn't fit disclaimer+credential. Test: generate 5 short-form posts with vs without fit formula, score on signature elements (20 pts) — if +3 or higher, keep.
- **Add explicit pre-save checklist** for the weakest format (whichever scores lowest on signature elements). The optimizer should detect which format loses the most credential/disclaimer points and add a 3-element mandatory check for that format specifically.

### Example Quality (high-leverage — v1.3)
- **Add concrete hook examples** for ambiguous hook patterns. Hooks like "The Shocking Mechanism" and "The Pattern Interrupt" are structurally defined but agents generate weak examples unless shown what success looks like. Providing 3 concrete peptide-specific examples (with real study citations) reliably improves Hook Strength by +1 to +2. The 2026-05-17 listicle run proved this: adding 3 Shocking Mechanism examples with real peptide/study pairings immediately improved Hook scores.
- **Add quality rules to hook patterns.** When a hook is defined with a pattern template but no quality gate, agents fall back to vague claims ("changed everything we know"). Adding a specificity test (e.g., "must name the study or mechanism that makes it surprising") prevents this. Test: generate 3 hooks with vs without quality rule, score on Hook Strength. Expected: +1 to +2.
- **Add explicit CTAs for new formats.** New formats (listicle, Clinical Trial Tuesday) without their own CTA entries in the CTA menu cause agents to default to bare "Follow for more" — the worst possible outcome. Adding a format-specific CTA entry with concrete phrasing improves CTA Quality by +1 to +2.

## What NOT to Change (Protected)

These are locked — the optimizer must NEVER modify:
- ❌ Disclaimer text (legal protection)
- ❌ Required RN credential mention
- ❌ File save paths (Desktop + Linux backup)
- ❌ The scoring rubric itself (avoids Goodhart's law collapse)
- ❌ Medical accuracy requirements
- ❌ "Never give dosing advice" rules
- ❌ Liability section
- ❌ FDA-sensitive language rules per nurse-rob-x-reply-guidelines v1.3 (ALL forms of heal/healing/healed BANNED — use recovery/tissue-level outcomes; never cure/treat/miracle/fix/prevent/breakthrough; word boundary rules: health ≠ heal)

## Scoring Pass (Baseline)

Before the optimization loop, run a SCORING PASS on current output:

```
1. Load current peptide_content_operator
2. Generate 5 test posts using CURRENT prompts
3. Score each against rubric
4. Record BASELINE = average composite score
5. Report: "Baseline: {score}/100 — Areas to target: {weakest dimensions}"
```

This establishes the floor. All subsequent improvements are measured against this (or the running high-water mark).

⚠️ **IMPORTANT: Cumulative scoring.** After the baseline, each mutation's composite MUST be calculated by simulating its effect ON TOP OF all previously kept changes — not independently from the original baseline. A common scoring bug: evaluating mutation X as if it were the only change, then comparing its score to the running baseline. This undercounts the mutation's true contribution because it ignores the synergy with earlier kept changes. Instead, model the full state (original + all kept changes + this mutation's delta), score that, and compare to the running baseline.

## Run Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Iterations | 15 | ~30-45 min. Structural wins happen in first 5-10; beyond that you're tuning phrasing. Stop at 3 consecutive **kept** with <0.5 delta. |
| Posts per iteration | 5 | 1 thread + 2 engagement + 2 short-form |
| Model for generation | creative-mode (gpt-5.5-codex) | Consistent with content_operator |
| Model for scoring | Any capable model | Scoring is reasoning, not creative |
| Auto-discard threshold | Medical Accuracy < 10 | Safety override |

### Two-Pass Pattern
When the first several mutations all get discarded, don't stop early — switch to **second-pass mode**. The first pass narrows the mutation space (reveals what doesn't work), while the second pass exploits the open space (tries better mutations in untouched sections). In the 2026-05-10 run, the first 4 iterations yielded 0 keeps, but the remaining 11 iterations kept 9 — the cold start pattern is normal. Implement as:

1. **First pass (iterations 1-5):** Try each category once (voice, hook, cta, thread, engagement). Track which categories produce positive deltas and which produce negative.
2. **Second pass (iterations 6+):** Stack mutations only in winning categories. Avoid re-targeting sections that produced negative deltas. Mutations in fresh sections (pillars, hook variants, CTA variants) have the highest hit rate.
3. Only early-stop after the second pass is yielding <0.5 kept changes consecutively.

### Early Stop Rule
Stop the loop early when 3 consecutive **kept** iterations produce <0.5 composite delta. This means 3 consecutive kept changes that each add <0.5 points — structural improvements are captured and further tuning is diminishing. 

**Do NOT count discarded iterations (negative or zero deltas) toward the early stop.** Negative deltas mean the wrong type of mutation was tried, not that the space is exhausted. The early stop signals diminishing returns on the *right* mutations, not running out of bad ideas.

A 10-iteration run that nets +14 is better than a 30-iteration run that nets +15 with 20 wasted calls.

## Output Report

After the loop completes, generate:

```markdown
# Content Optimizer Report — {Date}
...report content...
```

Save to: `/mnt/c/Users/Robert/Desktop/Daily Brief/NurseRob_PeptideEmpire/optimizer/YYYY-MM-DD_report.md`

## Step 11: Update Master Content Rules (CLOSED-LOOP FEEDBACK)

After every successful optimizer run, update the Master Content Rules file at `/home/robert/NurseRob_PeptideEmpire/content/master_content_rules_v1.3.md`:

1. Read the current master rules file
2. Apply any changes that were KEPT during this optimizer run (hook pattern improvements, CTA refinements, voice adjustments)
3. Update the "Last Updated" date
4. NEVER modify: FDA language rules section, disclaimer text, protected content section, word boundary rules
5. The master rules file is the bridge between optimizer improvements and both generators (daily + weekly batch)
6. Both generators load this file before producing content — so optimizer improvements automatically flow into future content

### Improvements Kept:
| # | Delta | What Changed |
|---|-------|--------------|
| 3 | +8.4 | Changed hook strategy from statement to question |
| 7 | +5.2 | Added "Look, I'll keep it simple" to standard opener |
| 12 | +12.1 | Removed "game-changer" from vocabulary — massive voice improvement |
| ... | ... | ... |

### Weakest Dimensions (target for next run):
- {dimension}: {score}/20 avg
- {dimension}: {score}/20 avg

### Patches Applied to peptide_content_operator/SKILL.md:
[summary of what was permanently changed]

### Suggested Manual Review:
- {any changes the optimizer is uncertain about}
```

Save to: `/mnt/c/Users/Robert/Desktop/Daily Brief/NurseRob_PeptideEmpire/optimizer/YYYY-MM-DD_report.md`

## Usage

### One-shot overnight run
```
"Run content optimizer for 30 iterations"
```

### Targeted optimization
```
"Optimize only hook strength — 20 iterations"
"Optimize CTAs — focus on soft-sell language"
"Optimize voice to be more clinical, less casual"
```

### Cron (weekly)
```
cronjob: "0 2 * * 0" (Sunday 2 AM) → content optimizer → 30 iterations
```

## Pitfalls

- ❌ Don't let the optimizer modify the rubric itself — that's Goodhart's law bait (optimizing for what's easy to measure, not what matters)
- ❌ Medical accuracy auto-discard MUST fire — a post scoring 100 on voice but 5 on accuracy is dangerous
- ❌ Don't optimize past the point of diminishing returns — if 3 consecutive *kept* iterations show < 0.5 delta, stop early. Negative deltas (discards) do NOT count toward early stop
- ❌ **Cumulative scoring bug.** When scoring a mutation, evaluate its effect ON TOP of all previously kept changes, not independently from the original baseline. If you evaluate each mutation against the original baseline independently, you'll undercount synergy and miss legitimate improvements. The 2026-05-10 run caught this in the first pass — mutations that stacked on previous keeps were getting lower deltas than they deserved because they were scored against the original, not the running state. Fix: maintain an accumulated `current_posts` state and apply each mutation's deltas to that, not to `baseline_posts`.
- ❌ **Mutation deduplication.** Never try the same target twice. If mutation A added "biohack" to the AVOID list and was discarded, mutation B that also adds "biohack" to the AVOID list (with slightly different phrasing) will also be discarded — same target, same result. Track which SKILL.md sections you've already mutated (voice profile, hook list, CTA list, pillar weights, rotation rules) and move to a fresh section each iteration.
- ❌ The optimizer may discover "cheese" — phrasings that score well on the rubric but sound unnatural to humans. If delta is suspiciously large (>20 pts in one iteration), flag for manual review
- ❌ Never remove the disclaimer or weaken legal protections for score gains — these are locked
- ❌ Voice optimization can drift toward generic "good copywriting" — the explicit Nurse Rob phrases ("as a nurse," "look, I'll keep it simple") are anchors, don't let the optimizer delete them all
- ❌ **Powerful hooks without rotation caps.** If a new hook pattern scores a +1.0 or higher delta on Hook Strength, it's powerful enough to feel contrived on repeat. The optimizer MUST either add a rotation cap in the same iteration or flag it as "needs rotation guardrail" in the report. The v2.6→v2.7 manual fix (capping Research Contradiction at 1x/week) is an example of what the optimizer should do autonomously.
- ❌ **AVG vs SUM scoring trap.** The rubric dimensions are 0-20 each, but the composite score is the SUM (0-100), not the AVG (0-20). Using AVG produces a baseline of ~18/100 instead of ~90/100, causing nearly all mutations to be falsely discarded. **Diagnostic: if >50% of your first-pass mutations are discarded, check your scoring formula first** — before concluding the mutations themselves are bad. The 2026-05-17 run demonstrated this cleanly: AVG → 3 kept / 12 discarded, SUM (correct) → 9 kept / 0 discarded.
- ❌ **Competitor format porting without stripping monetization.** When modeling a new format on a competitor's content (e.g., Healthy Alfred's listicle), the competitor's monetization tactics (affiliate codes, "shipped to your door," discount offers) will be embedded in their examples. The new format instructions must explicitly forbid these unless Nurse Rob has equivalent infrastructure. The 2026-05-17 listicle integration confirmed this — the initial draft copied Alfred's "Code X for 10% off" pattern despite Nurse Rob having no pharmacy partnerships. Solution: when porting a competitor format, add a monetization-stripping step to the mutation: identify what the competitor is selling, remove it, replace with Nurse Rob's actual CTAs (guide pages, DM consult, follow).

## Verification

After running:
1. Spot-check 3 generated posts from the optimized SKILL.md
2. Confirm they still sound like Nurse Rob (not generic health influencer)
3. Verify disclaimer present on all posts
4. Check that the optimizer didn't touch protected sections
5. Read the best-scoring and worst-scoring post aloud — does the human ear agree with the rubric?

## Related Skills
- `peptide_content_operator` — the skill being optimized
- `content-batch-generator` — monthly batch can inherit improvements
- `content_scheduler` — posts the optimized output
- `humanizer` — can be called mid-loop for additional voice checking
