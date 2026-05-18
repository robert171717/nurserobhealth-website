---
name: hoa-architectural-proposal
description: "Write formal proposals to HOA architectural review committees for home improvement projects — legal research, statute citation, structured arguments that minimize denial risk."
version: 1.0.0
---

# HOA Architectural Proposal

Write persuasive, legally-grounded proposals for HOA Architectural Control Committee (ACC) approval of home improvement projects. Maximizes approval odds by addressing every likely objection before the committee raises it.

**When to use:** Any time the user needs to submit an ACC/HOA design review request for a property improvement — EV charging, solar, concrete/hardscape, fencing, exterior modifications.

## Workflow

### 1. Research the legal landscape FIRST

Before writing, determine what laws apply. This prevents citing wrong statutes (a common and embarrassing mistake).

**Checklist:**
- [ ] Does the state have a specific right-to-charge law? (Check [Plug In America's policy tracker](https://pluginamerica.org/policy/right-to-charge-policies/))
- [ ] Does the state have a solar/energy device protection statute? (Almost all do — these set precedent for energy infrastructure)
- [ ] What does the state's planned community/HOA act say about architectural review standards? (Look for "shall not unreasonably withhold" language)
- [ ] What do the specific community's CC&Rs say about hardscape, exterior modifications, and utilities?

**Critical pitfall:** Never trust a statute number from an old plan or memory. Verify the actual text of each statute you cite. Use `curl` to fetch from the state legislature website if web_search credits are depleted.

### 2. Structure the proposal

Every ACC proposal needs these sections in this order:

```
1. PROJECT DESCRIPTION — What, where, scope. Be specific about dimensions.
2. VISUAL IMPACT & MITIGATION — Lead with "minimally visible." Address every
   aesthetic concern: curb appeal, street visibility, neighboring properties,
   lighting, signage, landscaping. Show it's invisible or innocuous.
3. LEGAL BASIS FOR APPROVAL — Cite specific statutes with quoted text.
   Lead with the approval standard ("shall not unreasonably withhold"),
   then precedent statutes, then federal policy.
4. PROFESSIONAL INSTALLATION — Licensed, bonded, insured contractors.
   City permits. Code compliance. This neutralizes the "safety" objection.
5. REQUESTED ACTION — What you want the committee to DO. Be explicit.
6. SUPPORTING DOCUMENTATION — What's attached/enclosed.
7. APPENDIX: PERSONAL STATEMENT — Why this matters. Community member
   history. Good-faith framing.
```

### 3. Argument strategy

**Lead with "this costs you nothing."** HOAs fear liability, expense, and precedent. Explicitly state: no HOA funds, no common area impact, no liability to the association.

**Address visual impact FIRST, before legal arguments.** Committees care more about aesthetics than law. Show it's invisible from the street. Compare to already-approved modifications (driveway extensions, patios).

**Use the "routine home improvement" frame.** Frame the project as functionally identical to something the HOA already approves routinely. A charging pad = a concrete pad. A solar array = a roof modification.

**Cite laws as backup, not as threats.** The legal section is there so they know you know your rights — but the tone should be cooperative, not adversarial.

### 4. Common pitfalls

| Pitfall | Fix |
|---------|-----|
| Citing wrong statute number | Verify EVERY citation's actual text before writing. Past sessions or plans may have incorrect numbers. Always re-verify with `curl` to the legislature site. |
| Web search credits depleted mid-research | Fall back to `terminal`: `curl -sL "https://www.azleg.gov/ars/33/01817.htm" 2>/dev/null | sed -n 's/<[^>]*>//gp' | sed '/^$/d' | head -100`. The `sed -n` strips HTML tags, `sed '/^$/d'` removes blank lines, `head` limits output. Adapt the URL for your state's legislature site. |
| Leading with legal threats | Legal basis goes AFTER visual mitigation, not before |
| Vague project description | Include dimensions, materials, exact location on property |
| No contractor details | Even if undecided, state "licensed/bonded/insured" and commitment to permits |
| Aggressive tone | Frame as "I welcome the committee's input" not "you can't stop me" |
| Missing visual mitigation | This is the #1 thing committees care about. Don't skip it. |

### 5. After submission

- Track the review clock. Most states have a deemed-approved deadline (often 60 days).
- If denied: appeal citing the "shall not unreasonably withhold" standard.
- Have a backup plan ready before submitting (commercial lot, alternate location).
- Save the approved proposal as a template for future submissions.

## Reference Files

- `references/arizona-ev-statutes.md` — Arizona-specific EV/HOA legal research (2026)
- `templates/acc-proposal-template.md` — Full proposal template with all sections
