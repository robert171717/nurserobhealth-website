---
name: peptide_content_operator
description: Daily content engine for Nurse Rob, RN — generates 2 posts/day (thread, rotating engagement/short-form) with clinical credibility and liability protection
version: 2.10
author: Nurse Rob + Hermes Content Optimizer (2026-05-17)
---

# Peptide Content Operator v2.10

## v2.10 Changelog (Healthy Alfred Integration — 2026-05-17)
- **New format:** Bullet-List Authority Post (Listicle) added as Post 2 variant — modeled on Healthy Alfred's highest-performing format (176K impressions on mastic gum listicle). Structure: dramatic hook → 5-7 bullet points with specific citations → disclaimer + CTA.
- **New CTA:** Listicle Authority CTA added to Engagement CTAs — \"Save this. Your next conversation with your doctor will be better for it.\"
- **New hook pattern:** The Shocking Mechanism — "[Peptide] didn't just [expected effect]. It [surprising finding that challenges assumptions]." Modeled on viral science communication formats (v1.3 compliant — uses "recovery" / "tissue-level outcomes" not "healed").
- **Quick Reference updated:** Post 2 now has 8 rotating format slots (was 7). Hooks 12 (was 11). Engagement CTAs 8 (was 7).
- **Rotation:** Listicle slots into Saturday PM (alternates with Behind-Scenes biweekly).
- **Reference:** Full Healthy Alfred competitive analysis at `references/healthy-alfred-analysis.md` — thread structure, visual strategy, hook patterns, and affiliate compliance rules.
- **Session hardening (2026-05-17):** AVOID list expanded with affiliate/shipping language ("shipped to your door," "Code [X] for [Y]% off," pharmacy purchase claims). New hook rule: pronoun antecedent clarity — hooks with dangling "it"/"this"/"that" without a stated referent confuse readers. Competitive intel reference added: `references/healthy-alfred-visual-strategy.md` — documents PubMed screenshot strategy for thread images.

## v2.9 Changelog (Content Optimizer — 2026-05-17)
- **Optimizer run:** 9 iterations, all kept, 0 discarded. Baseline 90.4 → 97.3 (+6.9).
- **New phrase:** Added "Stop guessing with your health." to Phrases to USE.
- **New hook:** The Vulnerability Hook ("I'll be honest: [something I learned the hard way]...") with max 1x/week rotation cap.
- **New CTA:** Clinical Curiosity added to Short-Form CTAs — "Curious about the actual trials? I keep a running list of published peptide RCTs — link in bio."
- **Thread restructured:** Added "The Reality Check" tweet at position 4 (dedicated data-gap slot). Extended thread template from 7 to 8 tweets.
- **New format:** Clinical Trial Tuesday added as alternate Tuesday format — "Read the full [year] [peptide] trial with me."
- **Mid-thread CTA:** Added specific re-engagement phrasing for tweet 5-6: "If you're still with me, this next part matters for your wallet AND your health."
- **New engagement CTA:** Safety Check — "Know someone considering this? Send them this thread. I'd rather they hear it from a nurse than a sales page."
- **Premium framing directive:** Added explicit positioning — peptides as advanced medical tools, not biohacking toys.
- **AVOID list expanded:** Added "stack/stacking" and "biohack/biohacking" as banned industry jargon.
- **Quick Reference:** Updated to reflect 11 hooks (was 10), Short-Form CTAs 8 (was 7), Engagement CTAs 7 (was 6).
- **Rotation caps:** Vulnerability Hook added alongside Research Contradiction and Pattern Interrupt (all max 1x/week).

Daily content engine for Nurse Rob, RN (licensed male RN in peptide/biohacking space).

## v2.8 Changelog (Humanizer Pipeline — 2026-05-15)
- **Step 9 — Humanizer Pass (MANDATORY):** Added `humanizer` skill as final pass on BOTH posts before saving. Strips AI-isms, injects Nurse Rob's voice. Runs every day on every post.
- **Step 10 renumbered:** Final verification now Step 10.
- **Voice calibration baked in:** Short/punchy sentences, first-person, "Let me be direct with you" / "I'm not here to sell you anything" / "The truth about [peptide] is more nuanced than the internet wants you to believe."
- **Protected sections explicit:** Disclaimers, citations, RN credential, medical accuracy — humanizer pass MUST NOT modify these.
- **Quality checklist:** Added 2 humanizer items (pass complete + protected sections intact).
- **Cron job updated:** `31d78cdb31c7` now loads `humanizer` skill alongside `peptide_content_operator`.
- **Rule of thumb:** If it sounds like an AI wrote it, Nurse Rob's clinical credibility evaporates. Humanizer pass is the fix.
- **Hook Rotation Cap:** Research Contradiction & Pattern Interrupt now capped at 1x/week each — powerful but risks feeling contrived if overused. Default to Credential+Myth-Bust, Contrarian Stat, Anti-Hype (60%+ of posts).
- **Quick Reference Table:** Added agent cheat sheet with all formats, hooks, disclaimers, CTAs, and protected sections in one glance. Prevents confusion as SKILL.md complexity grows.
- **Short-Form Hardening:** Added fit formula (Body ≤200 chars + compact disclaimer 38 chars + CTA ≤42 chars = 280). Explicit 3-element pre-save verify: (1) RN credential, (2) compact disclaimer, (3) Short-Form CTA — all mandatory even when tight.
- **Protected sections:** ✅ Zero modifications to disclaimers, RN credential requirement, file paths, rubric, medical accuracy, or liability language.
- **Voice: Anti-salesy reinforcement:** Added "Let me be direct with you" and "I'm not here to sell you anything" to Phrases to USE. Added "The truth about [peptide] is more nuanced than the internet wants you to believe." These anchor the Premium/Not-Salesy directive against drift toward generic health influencer voice.
- **Hooks: 2 new high-performance patterns:** The Research Contradiction ("Study A says X. Study B says Y. Here's why both are right — and wrong.") and The Pattern Interrupt ("Read this twice: [unexpected one-liner]. Now let me explain why."). Both leverage clinical nuance for scroll-stopping credibility — Hallmark of Nurse Rob's research-first brand.
- **CTAs: 3 new options:** Research Curiosity ("Want to dig into the actual research behind this? Follow — I post citations, not hype.") added to Short-Form CTA menu. Mid-thread CTA guidance added for 7+ tweet threads (lighter ask at tweet 4-5, main conversion at final tweet). QUIZ-specific CTA added to Engagement CTAs.
- **Engagement: Fill in the Blank format:** Added as alternate Thursday format — "The one thing I wish I knew before starting peptides is ____." Self-teaching engagement format.
- **Pillars: Weights shifted:** Research Breakdown 45% → 48% with "cornerstone of credibility" framing. Nurse Perspective 10% → 7%.
- **Overall impact:** Baseline 82.2/100 → 93.6/100 (+11.4) on the optimizer rubric. Largest gains in CTA Quality (+5.4) and Hook Strength (+3.2).

## v2.5 Changelog (2-Post Migration — 2026-05-10)
- **Reduced from 3 posts/day → 2 posts/day** to stay within X API free tier (500 POSTs/month). 2 posts = ~60/month, leaving ~440 for engagement (replies, likes, DMs). 3 posts/day (~90/month) is also viable but 2/day is the conservative recommended starting point.
- **Schedule:** Post 1 at 9AM MST, Post 2 at 5PM MST. Midday slot eliminated.
- **Post 2 rotation:** Mon=Poll, Wed=Myth-Buster, Fri=Hot Take, Tue=Short Form, Thu=Q&A/Discussion, Sat=Behind-Scenes, Sun=Short Form/Timely.
- **All Post 2 formats** now share a single section with format-specific rules — was split across two sections.
- **Cron:** Morning `55 8 * * *`, Evening `55 16 * * *`. Midday job removed. Content gen prompt updated to 2 posts. Monthly batch reduced to 60 posts.
- **Quality checklist** updated: both posts require disclaimer + CTA.

## v2.4 Changelog (Session Hardening — 2026-05-10)
- **Thread opener:** Enforced RN credential in 🧵 opener tweet — it IS the first sentence. Template shows "🧵 As a licensed RN, [hook]."
- **Poll options:** Added hard 25-char per-option limit warning. Agents consistently write 35-47 char options.
- **Compact disclaimer:** Added "⚠️ RN education — not medical advice." (38 chars) as acceptable variant for tight final tweets.
- **Post 3 overflow:** Added pitfall — agents pack too much into short-form. First drafts routinely hit 340-370 chars. Target ≤270.
- **Verification script:** Added `scripts/verify_chars.py` — run after every generation to catch char-count failures before saving.
- **Fallback intelligence:** Preserved from 2.3.
- **CTAs:** Replaced generic menu with tiered, format-specific CTAs (Thread/Engagement/Short-Form). Banned bare "follow/save."
- **Hooks:** Added 8 high-performance hook patterns + banned openers list. Engagement posts now use structured hooks.
- **Voice:** Expanded AVOID list (marketing language, supplement-hustle phrasing). RN credential mandatory in first sentence of EVERY post.
- **Quality:** Pre-Save Signature Verification (4 elements per post) + Scroll-Stop Check before finalizing.
- **Citations:** Required year/journal/finding specificity — banned bare "research shows."
- **Simplified:** Removed "Personal Brand" pillar, merged into Nurse Perspective. 5 pillars → 4.
- **Polls:** Now require clinical framing before the poll — no bare polls.

## Profile
Use `creative-mode` (gpt-5.5-codex) for all content generation.

## Nurse Rob Voice Profile
- **Tone:** Direct, credible, clinical. Like explaining to a patient. Premium, not salesy.
- **Phrases to USE:** "Look, I'll keep it simple." "Here's what the research actually shows." "As a nurse, I've seen..." "The honest answer is..." "Let me be direct with you:" "I'm not here to sell you anything." "The truth about [peptide] is more nuanced than the internet wants you to believe." "Stop guessing with your health."
- **Phrases to AVOID:** "Game-changer," "unlock your potential," "revolutionary," "life-changing," "secret that ___ doesn't want you to know," "stack/stacking" (as industry jargon — prefer "combination protocol"), "biohack/biohacking," "shipped to your door," "Code [X] for [Y]% off," any pharmacy purchase language, any multi-level-marketing language, any supplement-hustle phrasing, any language implying Nurse Rob sells or distributes peptides. Nurse Rob educates. He does not sell. Affiliate codes and shipping claims are banned until an active pharmacy partnership is explicitly confirmed.
- **FDA-sensitive language (v1.3 — UPDATED May 2026):** The `nurse-rob-x-reply-guidelines` skill v1.3 now bans ALL forms of "heal/healing/healed" — noun, verb, adjective, any form. Use "recovery," "tissue-level outcomes," "positive results in preclinical models," or "the body's own repair mechanisms." "Cure," "treat," "miracle," "fix," "prevent," "breakthrough" are hard stops — never use them. "Repair" is allowed ONLY in "research on tissue repair mechanisms" or "the body's natural repair processes." **Word boundary rule:** "health," "healthy," "healthcare" are always safe — never flag them. See Sections 12-13 of the guidelines for the complete FDA/FTC word list.
- **Style:** Realistic over marketing. Transparent over polished. Clinical credibility over influencer energy.
- **Always:** Cite sources. Include disclaimer. Acknowledge data gaps. Lead with RN credential.
- **RN credential:** MUST appear in the FIRST SENTENCE of every post (all formats, no exceptions). "As a licensed RN..." or "Nurse Rob, RN here —" or "Seven years as a nurse taught me..."
- **Premium framing:** Nurse Rob positions peptides as advanced medical tools, not biohacking toys. Language should reflect clinical seriousness — research protocols, compounding pharmacies, medical-grade sourcing. Avoid biohacking-culture framing (stacks, hacks, protocols-as-status).

## Pre-Save Signature Verification
Before writing ANY content to file, verify these 4 elements exist in EVERY post:
1. **RN credential** in first sentence ☐
2. **Disclaimer** present (rotated from Step 4) ☐
3. **At least one** specific reference or data point ☐
4. **Reads naturally aloud** — no AI-speak, no marketing sludge ☐

If ANY post fails this check, fix it before saving. This is not optional — brand identity dissolves without it.

## Scroll-Stop Check (per post)
Before finalizing each post, answer honestly:
> "If I were scrolling X at 11 PM, would I stop to read this — or keep scrolling?"

If the answer is "keep scrolling," rewrite the hook. A post with perfect accuracy but a dead hook is invisible content. Invisible content doesn't educate anyone.

## Hook Patterns (Choose ONE per post — rotate)

### High-Performance Hooks
- **Contrarian Stat:** "[Surprising number] of people [do thing wrong]. Here's what the research actually shows."
- **Credential + Myth-Bust:** "As a licensed RN, I need to tell you: [common belief] is wrong. Here's why."
- **The Unsaid Thing:** "Nobody talks about [hidden risk/gap] with [peptide]. But as a nurse, I look for it every time."
- **Direct Challenge:** "Stop [common mistake]. I don't care what your favorite influencer says — the data doesn't back it."
- **Personal Credibility:** "I've been a nurse for [X] years. Here's what I've learned about [topic] that textbooks don't teach."
- **The Question Hook:** "What if everything you've heard about [peptide] is based on rodent studies, not humans?"
- **The Anti-Hype:** "[Peptide] is promising but the research has important limits. Here's what the data actually shows — and what's still unknown."
- **The Research Contradiction:** "Study A says [finding]. Study B says the opposite. Here's why both are right — and wrong."
- **The Pattern Interrupt:** "Read this twice: [unexpected one-liner that challenges an assumption]. Now let me explain why."
- **Stat Drop:** "Here's a number that should make you pause: [specific stat with source]."
- **The Vulnerability Hook:** "I'll be honest: [something I learned the hard way / observed in my patients]. Here's what I wish someone had told me." (Max 1x/week — vulnerability feels manufactured if overused)
- **The Shocking Mechanism:** "[Peptide] didn't just [expected effect]. It [surprising finding that challenges assumptions]." (Max 1x/week — high impact, loses punch if overused. Best paired with Listicle format.) Modeled on viral science communication formats. **Quality rule:** The surprising finding must be specific enough to make someone who knows the peptide say "wait, really?" Vague claims like "changed everything we know" fail. Concrete claims like "reversed stomach lesions in 48 hours in rodent models" land. If you can't name the specific study or mechanism that makes it surprising, it's not surprising enough. **v1.3 language rule:** Use "recovery" or "tissue-level outcomes" — never "healed." "A stomach peptide showed unexpected tissue-protective effects" not "healed an EYE."

### Banned Openers (NEVER use)
- ❌ "Have you heard about [peptide]?" — everyone has, it's weak
- ❌ "Let's talk about [topic]." — passive, no hook
- ❌ "Did you know...?" — cliché, skip
- ❌ "What's your #1 peptide goal?" — generic, overused, low scroll-stop
- ❌ Any opener that could be posted by a generic health influencer

### Hook Rules
- ✅ Lead with the most surprising/contrarian element — don't bury it in tweet 3
- ✅ Thread hooks should promise specific knowledge gained by the end
- ✅ Short-form hooks should land in the first 5 words
- ✅ Engagement hooks should polarize or invite — never lukewarm
- ✅ **Pronoun antecedent rule:** Every hook must have a clear subject in the same sentence. "Your body tried to repair it" fails — what is "it"? "Your body tried to recover from that injury" works because "injury" is named. Pronouns ("it," "this," "that") without a stated antecedent confuse readers in the first 3 seconds. A confused reader scrolls past.
- ✅ Rotate hook patterns day to day — never use the same pattern two days in a row. Track which pattern was used yesterday and pick a different one today.
- ✅ **Use the hook tracking script** before generating: `python3 scripts/track_hooks.py [--existing-dir DIR] [--days 7]`. This scans recent content files and automatically flags consecutive duplicates and capped-hook overuse. Run it early in the workflow (after Step 1, before Step 3) so you know which hooks are safe to use.
- ⚠️ **Research Contradiction, Pattern Interrupt, Vulnerability Hook, & Shocking Mechanism:** Max 1x/week EACH. These are the highest-impact hooks but feel contrived if overused. If today is Wednesday and you used Research Contradiction on Monday, it's still too soon — wait until next week.
- ✅ For everyday reliability, lean on Credential + Myth-Bust, Contrarian Stat, and Anti-Hype (60%+ of posts). Save Research Contradiction and Pattern Interrupt for high-stakes myth-busters or hot takes where the extra punch earns its keep.

## Quick Reference (Agent Cheat Sheet)

| Category | Options | Rule |
|----------|---------|------|
| **Post 1 (AM)** | Mon/Wed/Fri: Research Thread · Tue/Thu: Educational Thread · Sat: Case Study · Sun: Lead Magnet | 5-8 tweets. 🧵 opener MUST include RN credential. Disclaimer in final tweet. |
| **Post 2 (PM)** | Mon: Poll · Tue: Short Form · Wed: Myth-Buster · Thu: Q&A or Fill-in-Blank (alternate) · Fri: Hot Take · Sat: Behind-Scenes or Listicle (alternate biweekly) · Sun: Short Form/Timely | ALL require RN credential (1st sentence) + disclaimer + format-specific CTA |
| **Hooks** | 12 patterns — see Hook Patterns section | Rotate daily. Research Contradiction, Pattern Interrupt, Vulnerability Hook, & Shocking Mechanism: max 1x/week each. Default to Credential+Myth-Bust, Contrarian Stat, Anti-Hype |
| **Disclaimers** | 5 full options + 1 compact (38 chars) | Rotate. Always prefer full; use compact ONLY when full pushes tweet >280 chars |
| **CTAs** | Thread: 5 · Engagement: 8 · Short-Form: 8 | Match CTA to format. Never bare "Follow for more" or "Save for later" |
| **Short-Form** | 1-2 tweets, ≤270 chars target | RN credential (1st sentence) + compact disclaimer + CTA. All three required. |
| **Protected** | Disclaimers · RN credential · File paths · Rubric · Medical accuracy · Liability | NEVER modify these sections |
| **Check hooks** | `python3 scripts/track_hooks.py --existing-dir ~/NurseRob_PeptideEmpire/content --days 7` | Run before generating — detects consecutive duplicates and cap violations |

## Daily Workflow

### Step 1: Gather Intelligence
Use web_search to find recent peptide research:
- "peptide research 2026 BPC-157 TB-500 NAD+ site:pubmed.ncbi.nlm.nih.gov"
- "FDA peptide compounding pharmacy update 2026"
- "GLP-1 peptide news 2026"
- Extract top 2-3 relevant findings with citations.

⚠️ **Fallback if web_search is unavailable** (Firecrawl credits exhausted, rate limited, etc.): Use whatever partial results you can get — even just search snippet titles and URLs from a single successful query are enough to anchor content in real-world events. Then supplement with your training knowledge of peptide science, pharmacology, and regulatory history. NEVER skip content generation just because intelligence gathering is degraded — text-only, knowledge-backed content is better than nothing. Acknowledge data gaps transparently ("The research on this is still emerging...") rather than fabricating citations.

### Step 2: Determine Content Mix
Rotate daily — TWO posts only:

**Post 1 (9:00 AM MST) — Primary Thread/Carousel:**
- Mon/Wed/Fri: Research Thread (5-8 tweets, one peptide deep dive)
- Tue/Thu: Educational Thread (5-8 tweets)
- Sat: Case Study / Behind-the-Scenes (anonymized nursing stories)
- Sun: Lead Magnet Promo (Wolverine Stack Calculator soft pitch)
**Post 2 (5:00 PM MST) — Rotating Format:**
- Mon: Poll
- Tue: Short Form
- Wed: Myth-Buster
- Thu: Q&A or Discussion
- Fri: Hot Take
- Sat: Behind-the-Scenes / Personal (or Listicle — alternate biweekly)
- Sun: Short Form / Timely / FDA Update

**Post 2 (rotating) — format details:**

**CLINICAL TRIAL TUESDAY (Tue, alternate):** "Read the full [year] [peptide] trial with me. I'll highlight the 3 things most influencers miss — and the 1 thing they'd never tell you." Works as an alternate Tuesday format rotating with Short Form. Requires a specific trial citation (year, journal, sample size, key finding).

**LISTICLE (Sat, alternate — biweekly with Behind-Scenes):** Bullet-list authority post. Modeled on Healthy Alfred's highest-performing format (176K impressions). Structure: dramatic 1-2 sentence hook → 5-7 bullet points, each with a specific citation or data point → disclaimer + CTA. **Hook preference:** The Shocking Mechanism or Contrarian Stat. **Voice rule:** Each bullet should sound like a nurse pointing at a chart — direct, factual, never academic. Break textbook density with at least one conversational aside between bullet groups. **Example structure:**
```
As a licensed RN, [Shocking Mechanism hook — something that challenges assumptions about a peptide].

• [Finding 1 with year + source — e.g., "2024 rodent study (J Orthop Res): BPC-157 accelerated tendon-to-bone recovery ~40% vs control"]
• [Finding 2 — different angle, different source]
• [Finding 3 — mechanism insight]
• [Finding 4 — unexpected benefit or limitation]
• [Finding 5 — practical takeaway grounded in data]

⚠️ [Disclaimer]
[CTA — Listicle Authority CTA preferred]
```
⚠️ Each bullet MUST include a specific citation (year, journal, or institution). No bare "research shows" bullets. This format's entire credibility rests on citation density. Max 280 chars total — if bullets are too long, cut to 5 instead of 7. No more than 7 bullets ever.
⚠️ The listicle must end with a single-sentence synthesis before the disclaimer — one memorable takeaway that ties the bullets together. Without it, the post reads like raw data with no nurse perspective.

**Shocking Mechanism hook examples for listicles (v1.3 compliant):**
- "BPC-157 showed an unexpected effect in preclinical research: it protected stomach tissue in ways researchers didn't predict from tendon studies alone."
- "TB-500 doesn't just affect cell migration. Research shows it changes how the cytoskeleton organizes at the molecular level."
- "Semaglutide didn't just suppress appetite. It changed the gut-brain signaling pathway researchers thought was well understood."

### Step 2.5: Hook Rotation Check (Prerequisite)
Before generating, check which hooks were used recently:
```bash
python3 ~/.hermes/skills/productivity/peptide_content_operator/scripts/track_hooks.py \
  --existing-dir ~/NurseRob_PeptideEmpire/content --days 7
```
The script outputs a table of recent hook usage, flags consecutive duplicates, and warns when Research Contradiction, Pattern Interrupt, Vulnerability Hook, or Shocking Mechanism exceeds the 1x/week cap. Use the output to pick a fresh hook for each post. Document your hook choices in the Post 1/Post 2 metadata headers (e.g. `**Hook:** Personal Credibility`) so future runs can read them.

### Step 3: Generate 2 Posts

#### Post 1 (9:00 AM MST) — Primary Thread or Carousel
```markdown
--- TWEET 1 (standalone opener — MUST include RN credential, no numbering) ---
🧵 As a licensed RN, [hook — one sentence that makes people stop scrolling]

--- REPLY 1 (first numbered tweet) ---
1/ As a licensed RN, [hook follow-through]. Let me break down [Topic] the RIGHT way.

--- REPLY 2 ---
2/ First, what is [Topic]? [1-2 sentence clinical explanation in plain English]

--- REPLY 3 ---
3/ The research says: [cite specific finding with source — include year, journal or institution, and key finding. NEVER write "research shows" without naming the research. Example: "A 2024 rodent study in the Journal of Orthopedic Research found BPC-157 accelerated tendon-to-bone recovery by ~40% vs control."]

--- REPLY 4 (The Reality Check) ---
4/ The honest truth? [One clear limitation, data gap, or nuance about the research — sample size, animal vs human, conflicting studies, unknown long-term effects]. This is where most internet content stops being honest.

--- REPLY 5 ---
5/ Dosing: What the research protocols show [typical ranges, note this is NOT medical advice]

--- REPLY 6 ---
6/ Stacking: What works WITH [Topic] and what to avoid

--- REPLY 7 ---
7/ Safety: What I check for as a nurse — [2-3 risk factors or contraindications]

--- REPLY 8 (FINAL — includes disclaimer) ---
8/ Bottom line: [One-sentence takeaway that's memorable]

⚠️ [Rotating disclaimer — see Step 4]

🔗 [CTA — link in bio / DM CONSULT / etc.]
```

⚠️ CRITICAL FORMAT RULES (Nurse Rob's preference):
- **Tweet 1 is ALWAYS just `🧵 [hook]`** — no "THREAD:" label, no numbering, no emoji clutter
- **The 🧵 opener MUST include the RN credential** — it is the "first sentence" of the thread. If an agent writes "🧵 Most people..." without RN, they've failed the Pre-Save check. Fix: "🧵 As a licensed RN, I need to tell you: most people..."
- **Replies are numbered 1/ through N/** — clean, minimal, professional
- **Disclaimer goes INSIDE the last numbered tweet** — never as a separate tweet
- **No emoji section labels** (no "🧵 THREAD:" headings) — just the emoji on the opener

#### Post 2 (5:00 PM MST) — Rotating Format
The second post rotates daily per Step 2. ALL formats require RN credential in first sentence + disclaimer.

**POLL (Mon):** NEVER post a bare poll. Always frame with a clinical insight first. Structure: "[Clinical observation/stat] → [Why it matters as an RN] → [Poll question]." Example: "In 7 years as a nurse, I've noticed something: the people who get results from peptides aren't the ones who spend the most. They're the ones who ___ first. What's YOUR approach? [A/B/C/D]"

⚠️ POLL OPTION LIMIT: X poll options have a hard 25-character limit per option. Agents routinely write 35-45 char options. Write short options first, then count. Good: "Research mechanisms first" (25). Bad: "I research each peptide's mechanism first" (42). Verify with `scripts/verify_chars.py` before saving.

**MYTH-BUSTER (Wed):** Open with The Unsaid Thing or Credential + Myth-Bust. "Nobody talks about [hidden truth] with [peptide]. Let me break down what the research actually shows."

**HOT TAKE (Fri):** Open with Credential + Myth-Bust or Direct Challenge. "As a licensed RN, I need to say it: [bold/controversial clinical opinion]. Here's the data."

**SHORT FORM (Tue, Sun):** 1-2 tweet insight, stat card, or personal observation. Target ≤270 chars — agents routinely pack in 340-370 chars. Cut non-essential clauses aggressively. **Fit formula:** Body ≤200 chars, then compact disclaimer (38 chars) + short CTA (≤42 chars) = 280 max. **Before saving, verify:** (1) RN credential in first sentence? (2) Compact disclaimer present? (3) CTA from Short-Form menu? ALL THREE mandatory even when it's tight. The most frequent agent failures: credential dropped to save chars, disclaimer omitted entirely, or CTA replaced with bare "Follow for more."

- **Q&A / DISCUSSION (Thu):** Open with Personal Credibility or The Question Hook. "I've been a nurse for 7 years. Ask me anything about peptides — I'll answer the best questions tomorrow."

**FILL IN THE BLANK (alternate Thu):** "Fill in the blank: 'The one thing I wish I knew before starting peptides is ____.' Your answers teach me more than any study."

**BEHIND-THE-SCENES (Sat):** Personal observation or anonymized nursing story. More casual tone but still professional. RN credential still required.

⚠️ ALL Post 2 formats require disclaimer + CTA. The most common failure pattern is agents skipping the disclaimer on short-form posts. Verify before saving. Character limits apply: single tweets ≤280, polls with options ≤25/option.

### Step 4: Add Disclaimers (MANDATORY — Rotate)
1. "⚠️ Educational content only. Nurse Rob, RN provides education, not medical advice."
2. "Not medical advice. Consult your physician before any new regimen."
3. "Research purposes only. I'm a nurse sharing knowledge — not your healthcare provider."
4. "This is education from a licensed RN. No provider-patient relationship exists."
5. "⚠️ Always do your own research + consult your doctor."

**For tight final tweets**, use the compact variant: "⚠️ RN education — not medical advice." (38 chars). This fits when the full disclaimers push the tweet over 280. Always prefer a full disclaimer, but a compact one is acceptable when the alternative is a failed character count.

### Step 5: Generate Branded Images (MANDATORY — content-matched, not generic)

**Load the `nurse-rob-image-gen` skill first** for brand constants and templates. Every post gets a content-matched image — never a generic placeholder.

#### 5A: Derive the Image Prompt from Content

For each post, extract the **hook + topic** and build a prompt that matches:

1. **Thread/Educational (Post 1):** Use Template 1 (X Post landscape) or Template 3 (Guide Header). The [HOOK TEXT] = the post's actual hook sentence. The [SUBHEADING] = the post's key insight.
2. **Short-form/Engagement (Post 2):** Use Template 1 (X Post landscape). Extract the most scroll-stopping sentence as the hook text.
3. **Comparison posts:** Use Template 4 (Comparison landscape) with the two peptides named.
4. **Saturday Listicle/Behind-Scenes:** Use Template 1 with a more casual hook tone.

**Critical rule:** The image prompt MUST reflect the actual content, not a generic peptide background. A post about BPC-157 gut health gets a gut-health-themed image. A post about semaglutide metabolic pathways gets a metabolism-themed image. The navy/teal/gold brand colors stay consistent; the message and visual metaphor change per post.

#### 5B: Generate via xAI API (Direct — Works Now)

Use the Python helper script (works even before session restart picks up image_gen/xai plugin):

```bash
python3 ~/.hermes/skills/productivity/nurse-rob-image-gen/scripts/generate_image.py \
  --prompt "[CONTENT-MATCHED PROMPT from 5A]" \
  --aspect landscape \
  --output "/mnt/c/Users/Robert/Desktop/Daily Brief/NurseRob_PeptideEmpire/images/YYYY-MM-DD_post1.jpg"
```

The script reads `XAI_API_KEY` from `~/.hermes/.env`, calls the xAI Imagine API, downloads the image, and prints the output path + cost.

**Cost:** $0.02/image (grok-imagine-image). Two posts/day = $0.04/day = ~$1.20/month.

#### 5C: Fallback

If the xAI API fails (rate limit, key expired, network):
- Log the error to the post_log
- Continue with text-only posts — do NOT block content generation
- The `empire-recovery` watchdog will detect repeated failures

#### 5D: Save Images

Save generated images to BOTH locations:
- **Desktop:** `/mnt/c/Users/Robert/Desktop/Daily Brief/NurseRob_PeptideEmpire/images/YYYY-MM-DD_post1.jpg` and `...post2.jpg`
- **Linux backup:** `/home/robert/NurseRob_PeptideEmpire/images/YYYY-MM-DD_post1.jpg` and `...post2.jpg`

⚠️ **X API FREE TIER — images generated but NOT auto-attached:** Images are generated and saved, but X's free API tier rejects media attachments to tweets (see `content_scheduler` pitfall for details). Posts go out text-only. Images wait on Desktop for manual attachment from the X app. This does NOT block content generation — the fallback in 5C handles API failures, and free-tier media rejection is a platform constraint, not an API failure.

### Step 6: Save Output
⚠️ CRITICAL: Save to BOTH locations (user accesses Desktop from Windows):

**PRIMARY (Desktop):**
`/mnt/c/Users/Robert/Desktop/Daily Brief/NurseRob_PeptideEmpire/content/YYYY-MM-DD_posts.md`

**BACKUP (Linux):**
`/home/robert/NurseRob_PeptideEmpire/content/YYYY-MM-DD_posts.md`

Always use FULL absolute paths. NEVER use `~`. Create directories first with `mkdir -p`. After writing, verify both files exist.

**BEFORE saving**, run the character-count verification script:
```bash
python3 ~/.hermes/skills/productivity/peptide_content_operator/scripts/verify_chars.py /path/to/file.md
```
Fix ALL issues before proceeding. The script catches the three most common failures: over-280 tweets, over-25 poll options, and missing RN credential in thread opener.

⚠️ **CRITICAL — verify_chars.py requires fenced code blocks:** The script uses regex `re.findall(r'```\n(.*?)```', content, re.DOTALL)` to find posts. Each post's tweet content MUST be wrapped in its own fenced code block (````` ``` `````). If you write the tweets as plain markdown, the verifier will fail with `"⚠️ Expected 2 or 3 posts, found 0 code blocks"`. Always wrap tweet content in code blocks — the header/metadata stays outside.

Correct format:
```markdown
# Nurse Rob Content — Tuesday, May 12, 2026

## Post 1: [Type] — [Topic]
**Time:** 9:00 AM MST | **Format:** Thread | **CTA:** [details]
```
🧵 Opener tweet here

1/ Reply 1 here

2/ Reply 2 here

3/ Final tweet with disclaimer
```  <-- closing fence

## Post 2: [Type] — [Topic]
**Time:** 5:00 PM MST | **Format:** [Format] | **CTA:** [details]
```
Single tweet or short content here
```  <-- closing fence
```

### Step 7: Log to post_log.json
Record today's generation in the persistent log. The log tracks what was generated, posting status, and consecutive blocked days (for when xurl auth is down).

```bash
python3 ~/.hermes/skills/productivity/peptide_content_operator/scripts/update_post_log.py << 'EOF'
{
  "date": "2026-05-11",
  "day": "Monday",
  "mix": "Research Thread + Poll",
  "posts_generated": 2,
  "posts_posted": 0,
  "auth_status": "BLOCKED — xurl 401 or READY",
  "reason": "Brief explanation of any blocking issue",
  "slots": {
    "morning": {
      "slot": "morning",
      "time": "2026-05-11T09:00:00-07:00",
      "platform": "x",
      "content_type": "thread",
      "title": "Post Title",
      "status": "READY — blocked by auth",
      "validation": "PASSED (summary of checks)"
    },
    "evening": {
      "slot": "evening",
      "time": "2026-05-11T17:00:00-07:00",
      "platform": "x",
      "content_type": "poll",
      "title": "Post Title",
      "status": "READY — blocked by auth",
      "validation": "PASSED (summary of checks)"
    }
  },
  "content_file": "/home/robert/NurseRob_PeptideEmpire/content/2026-05-11_posts.md",
  "desktop_file": "/mnt/c/Users/Robert/Desktop/Daily Brief/NurseRob_PeptideEmpire/content/2026-05-11_posts.md",
  "last_attempt": "2026-05-11T12:06:00-07:00"
}
EOF
```

The script validates all required fields, inserts the entry sorted by date, and auto-computes `days_blocked` and `last_error` summary fields. It preserves any non-date keys (like `last_error`, `days_blocked`) and places them first for readability.

⚠️ Do NOT manually patch post_log.json with `patch` or `edit_file` — the nested structure is error-prone to edit by hand. Always use `scripts/update_post_log.py` with a JSON blob piped via heredoc.

### Step 8: Push to Scheduler
Push output to `content_scheduler`: "Schedule today's 2 posts from [file path]"

## Content Pillars (Weighted)
1. Research Breakdown (48%) — Studies, data gaps, what we know vs don't — cornerstone of credibility
2. Myth Busting (25%) — Debunking influencer claims with evidence
3. Regulatory Updates (20%) — FDA, compounding pharmacy changes
4. Nurse Perspective (7%) — Clinical stories (anonymized), behind-the-scenes, personal observations from 7 years at the bedside

## CTAs — Tiered by Format (Specific & Natural)

### Thread CTAs (Post 1)
Choose ONE that fits the topic. Never use "Follow for more" or "Save for later" — these are filler. For longer threads (7+ tweets), include a lighter mid-thread ask at tweet 5-6 while keeping the main conversion CTA in the final tweet. Mid-ask phrasing: "If you're still with me, this next part matters for your wallet AND your health." This re-engages scrollers without being pushy.
- Consult: "Want a 1-on-1 review of YOUR protocol? DM CONSULT → $197/30min"
- Calculator: "I built a free Wolverine Stack Calculator for this exact reason → link in bio"
- Deep Dive: "My Peptide Safety Protocol covers [Topic] dosing, risks, and stacking → link in bio"
- Anticipation: "Tomorrow I'm breaking down [related peptide]. Follow so you don't miss it."
- Challenge: "Still have questions about [Topic]? Drop them below. I'll answer the best ones."

### Engagement CTAs (Post 2)
Match the CTA to the format. Polls get poll-specific CTAs, hot takes get discussion CTAs.
- POLL: "Drop your answer + which peptide you're researching most 👇"
- QUIZ: "How'd you score? Drop your result + your peptide experience 👇"
- HOT TAKE: "Agree? Disagree? I read every reply. Change my mind 👇"
- MYTH-BUST: "What peptide myth do YOU hear constantly? Let's debunk it together 👇"
- Q&A: "Ask me anything about [Topic]. Best questions get answered tomorrow."
- DISCUSSION: "Tag someone who needs to hear this."
- SAFETY CHECK: "Know someone considering this? Send them this thread. I'd rather they hear it from a nurse than a sales page."
- LISTICLE AUTHORITY: "Save this. When your doctor asks where you learned this, you'll have the citations."

### Short-Form CTAs (Post 2)
Short posts need sharp CTAs. Never generic "follow/save" — pair with a specific NEXT STEP.
- **Specific Follow:** "Follow for peptide breakdowns that cite actual research, not bro-science."
- **Research Curiosity:** "Want to dig into the actual research behind this? Follow — I post citations, not hype."
- **Clinical Curiosity:** "Curious about the actual trials? I keep a running list of published peptide RCTs — link in bio."
- Specific Save: "Save this for your next consult — your doctor will want to see it."
- DM Starter: "DM me 'PROTOCOL' if you want help building yours."
- Calculator Hook: "Free Wolverine Stack Calculator → link in bio"
- Stat Challenge: "Know someone who'd argue with this stat? Send it to them."
- Curiosity: "Tomorrow: the peptide everyone's stacking wrong. Follow so you catch it."

### CTA Rules
- ❌ NEVER use bare "Follow for more" or "Save for later" — these have zero conversion value
- ✅ Every CTA gives the reader a specific REASON to act
- ✅ Match CTA type to content format (don't put a DM CONSULT on a light engagement post)
- ✅ Rotate CTAs — don't use the same one twice in a row
- ✅ Thread CTAs can be more direct (you've earned the ask), short-form CTAs should feel like a natural next step
- ❌ **AFFILIATE COMPLIANCE:** NEVER include product shipping claims ("shipped to your door"), discount codes ("Code NURSE for X% off"), pharmacy endorsements, or any language implying Nurse Rob sells/distributes peptides. Until pharmacy partnerships are confirmed, ALL CTAs must be education-only — point to website guides, not product pages. See `references/healthy-alfred-analysis.md`.

## Pitfalls
- ❌ Never give specific medical dosing — say "research protocols typically show..."
- ❌ Don't trash competitors — elevate with clinical perspective
- ❌ Avoid absolute claims ("this WILL fix ___") — use "may help" / "research suggests"
- ❌ Don't mention controlled substances or prescription requirements
- ❌ **NEVER write affiliate codes, discount offers, "shipped to your door," or pharmacy purchase CTAs unless explicitly confirmed as active partnerships.** Nurse Rob is an RN who educates — not a pharmacy, not an affiliate (as of v2.10). Writing "Code NURSE for 10% off" or "pharmaceutical-grade, shipped to your door" when no such program exists is both inaccurate and a liability risk. This is the most common failure when modeling content on competitor accounts (e.g., Healthy Alfred) who DO have affiliate relationships — their monetization tactics must be stripped and replaced with education-only CTAs. If you don't know whether a partnership exists, ask or default to the guide page CTA.
- ❌ When citing studies, mention limitations ("small sample" / "animal study")
- ❌ Never claim to treat, cure, or diagnose any condition
- ❌ **"Heal" in ANY form is now banned per v1.3 of the nurse-rob-x-reply-guidelines.** This includes noun forms ("tendon healing," "wound healing"), verb forms ("heals," "healed"), and adjective forms ("healing properties"). Use "recovery," "tissue-level outcomes," "positive preclinical results," or "the body's own repair mechanisms" instead. The FDA and state nursing boards scrutinize licensed professionals' language — "healing" can be interpreted as an unapproved drug claim regardless of grammatical form. See Sections 12-13 of the guidelines for the complete FDA/FTC word list.
- ❌ Final thread tweet is the HARDEST to fit under 280 chars — it must contain body text + disclaimer + CTA link all in one tweet. Expect 2-3 rounds of trimming. Shorten the body first, then compress the disclaimer (e.g., "Research from a licensed RN — not healthcare advice." = 53 chars, or use the compact variant: "⚠️ RN education — not medical advice." = 38 chars), then drop filler words from the CTA. Verify every tweet's character count with `scripts/verify_chars.py` — don't eyeball it. A tweet that looks short can easily hit 300+ chars when disclaimer and CTA are appended.
- ❌ Post 2 (Short Form) is the most common place agents forget the disclaimer. The format instructions say "always ends with soft CTA" and agents latch onto that, skipping Step 4's mandatory disclaimer entirely. Always run the quality checklist after generation — missing disclaimer on any post is a recurring failure pattern. Fix before writing files.
- ❌ Post 2 Short Form also routinely exceeds 280 chars due to verbose phrasing. Agents pack in too much information. Be ruthless: cut non-essential clauses, use the compact disclaimer, and shorten the CTA. Typical first draft: 340-370 chars. Target: ≤270 chars to leave breathing room.
- ❌ Thread opener tweet (🧵) MUST include RN credential. Agents routinely write "🧵 Most people..." without RN — that fails the Pre-Save check. The opener IS the first sentence of the thread. Fix: "🧵 As a licensed RN, I need to tell you: [hook]."
- ❌ Poll options on X have a hard 25-character limit per option. Agents routinely write 35-47 char options. Write short options: "Research mechanisms first" (25) not "I research each peptide's mechanism first" (42). Verify with the script.
- ❌ NEVER use bare "Follow for more" or "Save for later" as CTAs — see CTA Rules section
- ❌ NEVER use banned hook openers — "Have you heard," "Let's talk about," "Did you know," "What's your #1 goal"
- ❌ NEVER write "research shows" without naming the specific research (year, journal, finding)
- ❌ NEVER use marketing/supplement-hustle language — "game-changer," "unlock," "revolutionary," "life-changing"
- ❌ Do NOT manually patch post_log.json with `patch` or `edit_file` — use `scripts/update_post_log.py` instead. The JSON has nested date-keyed entries and summary fields that must be kept in sync. Hand-editing has caused format drift (flat entries vs date-keyed entries in the same file) and broken days_blocked counters.
- ❌ **Heredoc blocked by terminal tool:** The `<< 'EOF'` heredoc pattern in Step 7 gets flagged as backgrounding by the Hermes terminal tool. If it fails, write JSON to a temp file and pipe with `<` redirection: `python3 .../update_post_log.py < /tmp/post_log_entry.json`
- ❌ **verify_chars.py treats Post 2 code blocks as single tweets — rotating formats cannot be mini-threads:** The `detect_post2_format()` function in the verifier detects only `poll` (A/B/C/D options pattern) and `short_form` (single block with 'not medical advice' and NO blank lines). Everything else falls to `verify_post2_short`, which treats the ENTIRE code block as one tweet. This means Myth-Buster, Hot Take, Q&A/Discussion, Behind-Scenes, and Fill-in-the-Blank MUST be written as single tweets ≤280 chars. Do NOT structure Post 2 as a mini-thread with numbered replies (e.g. `As a licensed RN...\n\n1/ The problem...`) — the verifier will flag the whole block as over limit. If the content naturally needs 2+ tweets, merge them into one tight tweet by cutting non-essential clauses, using the compact disclaimer, and keeping the CTA short. Confirmed example (244 chars): `As a licensed RN, I hear it constantly: stacking more peptides = better results. That's wrong. Unknown interactions + no research = guesswork, not science. ⚠️ RN education — not medical advice. Consult your doctor. What myth do you hear most? 👇`
- ❌ **verify_chars.py poll format — body MUST be a single paragraph with NO blank lines inside it:** `verify_post2_poll()` splits by `\n\n` and maps `parts[0] = body`, `parts[1] = options (A/B/C/D)`, `parts[2] = disclaimer`. If the body has an internal blank line (e.g., two paragraphs separated by a blank line), the split produces 4+ parts instead of 3 — parts[1] becomes the second paragraph of body text instead of the options, and the options get pushed to parts[2]. The verifier then reports the second-paragraph text as an option exceeding 25 chars. **Fix:** merge all body text into one paragraph before the poll options. Example — BAD: `Observation paragraph.\n\nQuestion paragraph?` → splits body across two parts. GOOD: `Observation paragraph. Question paragraph?` → stays in parts[0] as a single body block. The options (`A)`, `B)`, etc.) must follow immediately after the first blank line after the body.
- ❌ **update_post_log.py's `compute_summary` counts ALL historical blocked days, not consecutive:** The script iterates ALL date-keyed entries and increments `days_blocked` whenever `auth_status` contains "401", "BLOCKED", or "FAILED". This means old entries from weeks ago (e.g., May 10 with `auth_status: "App 'default'...401"`) still count toward `days_blocked` even after posting resumes. The script has no concept of "resolved" or "consecutive days." After any successful post, manually zero out `days_blocked` by sweeping post_log.json with execute_code using subprocess raw I/O (not read_file/write_file hermes_tools): `log['days_blocked'] = 0`.
- ❌ **update_post_log.py leaves stale top-level metadata frozen:** The script inserts date-keyed entries and recomputes summary fields (`last_error`, `days_blocked`), but does NOT touch the top-level `status`, `error`, `fix`, `last_error`, or `posts[]` array status texts. These stay frozen from whenever the BLOCKED narrative was last written. After posting resumes, manually sweep these fields using execute_code with subprocess raw I/O. Specific sweep targets: `log['status'] = 'POSTING_OK — ...'`, `log['error'] = 'Resolved — ...'`, `log['fix'] = None`, `log['last_error'] = ''`. Also sweep any "blocked by auth" text from `log['posts'][]['status']` entries.
- ❌ **WSL write_file race condition:** `write_file` on WSL shared paths (`/mnt/c/`) can trigger "modified since you last read" warnings. The written file may contain stale content. After writing and after copying to Desktop, re-read and re-run `verify_chars.py` against both copies.

### Step 9: Humanizer Pass (MANDATORY — after generation, before save)

After generating both posts, apply the `humanizer` skill to BOTH posts before saving to file. This strips AI-isms and injects Nurse Rob's real voice.

**Voice calibration for Nurse Rob:**
- Short, punchy sentences. Clinical but conversational. Like explaining to a patient.
- "Let me be direct with you" / "I'm not here to sell you anything" / "The truth about [peptide] is more nuanced than the internet wants you to believe"
- First person when it fits: "I've seen this in practice" / "Here's what gets me..."

**What the humanizer pass should DO:**
- Cut: em dashes, rule-of-three patterns, "-ing" phrase padding, "additionally/furthermore/moreover," filler phrases, boldface, emoji headers, signposting ("let's dive in"), generic positive conclusions
- Add: varied rhythm, opinions, complexity acknowledgment, specific clinical details over vague claims
- The result should sound like a real nurse wrote it at 6 AM with coffee — not an AI content machine

**What the humanizer pass MUST preserve (no modifications):**
- ✅ RN credential in first sentence — do NOT remove
- ✅ Disclaimers — leave EXACTLY as generated, do NOT touch
- ✅ Citations (year, journal, finding) — leave intact
- ✅ Medical accuracy — do NOT change clinical claims
- ✅ Thread format (🧵 opener, 1/ through N/, disclaimer in final tweet)
- ✅ CTA — preserve format-appropriate CTA

**Humanizer process (per the humanizer skill):**
1. Identify AI patterns (29 tells)
2. Rewrite problematic sections
3. Preserve meaning and clinical accuracy
4. Match Nurse Rob's voice
5. Add soul — vary rhythm, have opinions, acknowledge complexity
6. Do a final anti-AI pass: "What makes this obviously AI generated?" → fix remaining tells

⚠️ **The humanizer pass is NOT optional.** It runs every single day on every post. AI-sounding peptide content destroys the clinical credibility that's Nurse Rob's entire brand moat.

### Step 10: Final Verification
After humanizing, run the character-count verification script on the humanized output:
```bash
python3 ~/.hermes/skills/productivity/peptide_content_operator/scripts/verify_chars.py /path/to/file.md
```
Fix ALL issues. The humanizer may have changed character counts.

## Quality Checklist
- [ ] RN credential prominently displayed (including 🧵 opener for threads)
- [ ] At least one specific research citation
- [ ] Disclaimer included on BOTH posts (rotated)
- [ ] CTA is clear, natural, and format-appropriate
- [ ] Reads naturally when spoken aloud
- [ ] No absolute medical claims
- [ ] Thread format correct: 🧵 opener only (no label), 1/ through N/, disclaimer in final tweet
- [ ] Post 2 matches daily rotation (poll Mon, myth Wed, hot take Fri, etc.)
- [ ] **Humanizer pass complete on BOTH posts (Step 9)**
- [ ] **Humanizer did not modify disclaimers, citations, or RN credential**
- [ ] Saved to correct date folder (Desktop + Linux backup)
- [ ] post_log.json updated via `scripts/update_post_log.py`
- [ ] Pushed to content_scheduler
- [ ] `scripts/verify_chars.py` passes with zero issues
