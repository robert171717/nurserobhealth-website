# GLP-1 Query Coverage — Rationale & Observed Yield

## Why a Separate GLP-1 Query?

GLP-1 receptor agonists (semaglutide/Ozempic/Wegovy, tirzepatide/Mounjaro/Zepbound, retatrutide) are the most commercially popular peptide class. They generate a distinct set of questions that the standard peptide-general queries miss:

| Question Type | Example (from real scans) | Why General Queries Miss It |
|--------------|---------------------------|----------------------------|
| **Adverse reactions** | Heart rate soared on reta, ER visit | "BPC-157 question OR TB-500 help" doesn't include GLP-1 names |
| **Dosing confusion** | ".4mg reta too much?" | "peptide dosage" may match, but often phrased as drug-name-specific |
| **Drug-specific switching** | "Switching from sema to tirz — what to expect?" | Uses brand/drug names, not generic "peptide" |
| **Side effect anxiety** | "Nausea on tirzepatide, should I stop?" | Mentions drug name + side effect, not "peptide help" |

## Observed Yield

### May 13, 2026 Midday Scan — Activated Catch
Query 5 (`"semaglutide OR retatrutide OR tirzepatide question OR help OR side effect"`) was first added during the May 13 midday scan. It caught the **@Vibrato444** Retatrutide adverse-reaction lead — a HOT medical-advice lead that the other 4 queries had not matched because the post used "reta" (abbreviation) and framed it as a drug-specific safety question.

### May 14, 2026 Midday Scan — 0 Results (Transient Gap)
Query 5 returned 0 results during a high-volume midday scan where Query 3 (20 results) and Query 4 (20 results) both performed normally. This confirms the same transient X search index gap behavior documented for Query 3 — the 6-hour window may simply contain no GLP-1-specific posts, or X's search index may have a brief coverage gap. This is **normal** and does NOT indicate a scan problem or query degradation.

**Handling when Query 5 returns 0:**
- Continue normally with Queries 1-4
- Do NOT fall back to degraded mode
- Do NOT fire an alert
- Report "0 results from Query 5 (normal edge case)" in the scan report

### May 17, 2026 Midday Scan — Noise Overwhelm (19 Results, 0 GLP-1 Relevant)
Query 5 returned 19 results but ZERO were GLP-1 related. All 19 were false positives from the broad OR terms:

| OR Term | What It Matches (false positives) |
|---------|----------------------------------|
| `help` | Any post containing the word "help" — sports help, cooking help, medical fundraisers, customer service |
| `side effect` | Any post about medication side effects, sports side effects, or even general "side effect" mentions in non-peptide context |
| `question` | Any post asking any question — travel questions, relationship questions, political questions |

**Root cause:** xurl's search treats each OR term independently. A post mentioning "need help" or "question about" without any GLP-1 drug name still matches. The GLP-1 drug names (semaglutide, retatrutide, tirzepatide) are specific enough that they don't generate noise — but `help`, `question`, and `side effect` are so generic they act as noise magnets.

**Impact:**
- The 19 results were all general X content: sports commentary, medical fundraisers, customer service requests, relationship advice — zero peptide content
- This is **not** a search failure nor a transient index gap — it's a structural signal-to-noise ratio problem
- When this happens, Query 5 is effectively non-functional for that scan window
- Treatment is identical to the 0-results edge case: continue with Queries 1-4, don't degrade, don't alert

**How to distinguish noise overwhelm from actual 0 results:**
- `meta.result_count = 0` → transient gap (normal)
- `meta.result_count = 15-20` but all `data[].text` lack any GLP-1 drug name → noise overwhelm
- In either case, report "0 GLP-1 relevant results from Query 5"

**Future consideration:** If noise overwhelm becomes the dominant failure mode (more common than the 0-results gap), consider restructuring Query 5 to use AND logic for GLP-1 drug names:
```
xurl search "semaglutide help" OR "semaglutide question" OR "semaglutide side effect" OR ...
``` 
This eliminates standalone `help`/`question`/`side effect` matches but requires 2x the query tokens. Not worth changing while the gap-only failure mode was observed first. Monitor and revisit if noise overwhelms >50% of scans.


## Query Design for xurl

```bash
xurl search "semaglutide OR retatrutide OR tirzepatide question OR help OR side effect" -n 20
```

**Design rationale:**
- **No exact phrase matching** — "question" and "help" are OR-d, not AND-d, so any post mentioning a GLP-1 drug plus any of these problem-indicating words matches
- **Includes all 3 major GLP-1 drugs** — semaglutide (most prescribed), tirzepatide (second most, often stacked), retatrutide (newest, most questions about side effects)
- **"-n 20"** — matches the other query's volume. If results are too noisy, reduce to -n 10

## Query Design for web_search (Degraded Mode)

```bash
web_search: site:x.com "semaglutide" OR "retatrutide" OR "tirzepatide" question help advice
```

**Design rationale:**
- web_search requires fewer operators than xurl — just space-separated OR terms
- Same drug name coverage
- "question help advice" as free terms (not quoted phrase) for maximum recall

## Future Considerations

- If GLP-1 results consistently outnumber peptide-general results, consider splitting into two GLP-1 queries: one for medical/side-effect questions and one for dosing/stacking
- When retatrutide replaces tirzepatide in market share, swap the order to prioritize the most-prescribed drug
- Brand names (Ozempic, Mounjaro, Zepbound) generate questions too — consider adding them if the active-ingredient-only query misses leads
