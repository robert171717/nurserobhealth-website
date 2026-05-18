# Financial Stress Testing for Business Plan Decks

Use when a PPTX deck or business plan includes financial projections that need rigorous testing before presenting to stakeholders (spouse, investors, partners).

## When to Use

- User has a deck with per-unit or per-vehicle financial projections
- User asks "stress test this" or "what if X goes wrong"
- Before presenting the deck to a skeptical audience (spouse buy-in, investor pitch)
- When the plan has a stated "stress tolerance" or "risk cap" that needs quantifying

## Technique: Parameter Sweep from Implied Baseline

### Step 1: Reconstruct the implied model

Most decks present a baseline net profit number without showing the full revenue breakdown. Back-solve for gross revenue:

```
Gross = (Net + FixedCosts) / (1 - RevenueShare)
```

Example from Cybercab: $1,500 net + $385 insurance + $45 electricity, at 25% Tesla share → $2,573/mo gross per vehicle.

### Step 2: Identify stress variables

For any business model, the stress variables are:
- **Revenue split/commission** (platform takes what %?)
- **Insurance/fixed costs** (what's the floor and ceiling?)
- **Utilization/demand** (what % of theoretical capacity?)
- **CapEx** (what if the asset costs more?)
- **Energy/input costs** (what if inputs spike?)
- **Competition** (what if market saturates?)
- **Timeline delay** (opportunity cost vs alternative investments)

### Step 3: Sweep each variable independently

For each variable, test a range from optimistic to catastrophic. Show:
- Per-unit net at each level
- Annualized fleet/scale net
- Whether cash flow goes negative (break-even point)
- Whether it breaches the user's stated stress tolerance

### Step 4: Combined nightmare scenario

Test 2-3 worst-case variables simultaneously. This is the "do we survive?" scenario.

### Step 5: Score and identify vulnerabilities

Score each risk factor 1-10. The lowest scores are the real vulnerabilities. Cross-reference against the user's stated constraints (stress tolerance, debt aversion, timeline).

## Pitfalls

- **Don't trust the deck's numbers blindly.** Back-solve for implied gross revenue to confirm the math holds together. Decks often have rounding or optimism baked in.
- **The real vulnerability is usually non-financial.** In the Cybercab case, the financials survived every scenario — but the wife's stress cap of 4-5/10 was breached by moderate setbacks. Always check non-financial constraints.
- **Present the bad news clearly.** If the plan survives every scenario, say so. If it doesn't, say which one kills it and at what threshold. No sugarcoating.

## Output Format

Save results to a markdown file alongside the deck for future reference. Include a one-line bottom-line verdict.
