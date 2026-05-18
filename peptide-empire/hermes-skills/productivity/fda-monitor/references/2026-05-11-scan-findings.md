# Scan Reference — May 11, 2026

## Key Regulatory Landscape (as of May 2026)

### GLP-1 Compounding: The Big Squeeze
- **April 30, 2026:** FDA proposed excluding semaglutide, tirzepatide, and liraglutide from 503B bulks list
- **Public comment deadline:** June 29, 2026
- **Context:** Tirzepatide shortage resolved Dec 2024, semaglutide shortage resolved Feb 2025
- **Only active shortages:** Dulaglutide (Trulicity), Liraglutide (Victoza/Saxenda) — only GLP-1s still legally compoundable under shortage exception
- **503A safe harbor:** Up to 4 Rx/month of "essentially copy" products before FDA enforcement
- **Combo products (e.g., semaglutide + B12):** Still count as "essentially copy" if each API within 10% of branded strengths

### Peptide Reclassification (Biohacker Peptides)
- **PCAC meeting:** July 23-24, 2026 — 7 peptides up for 503A Category 1 review
  - Day 1: BPC-157, KPV, TB-500, MOTs-C
  - Day 2: DSIP/Emideltide, Semax, Epitalon
- **Second PCAC meeting:** Before Feb 2027 — GHK-Cu, Melanotan II, LL-37, Dihexa, PEG-MGF
- **Political driver:** HHS Secretary Kennedy made reversing 2023 restrictions a personal priority; Section 503A(c) emergency authority is a wildcard
- **Timeline reality:** Even if PCAC recommends inclusion, notice-and-comment rulemaking takes 12+ months

### Enforcement
- **March 31, 2026:** Coordinated warning letters to Gram Peptides, Mile High Compounds, Prime Sciences
- **Pattern:** FDA explicitly rejects "research use only" disclaimers when marketing + bacteriostatic water sales + clinical claims establish intent for human use

## Effective Search + Extraction Pattern

1. **web_search all 5 queries in parallel** (limit=8 per query)
2. **Identify key URLs from each result set:**
   - fda.gov pages → ALWAYS extract (press releases, warning letters, drug alerts)
   - Advisory committee calendar → ALWAYS extract
   - Law firm analyses (FDALawBlog, Foley, JD Supra) → extract for legal context
   - Industry news (RAPS, Drug Topics, Pharmacy Times) → extract for clinical angle
   - Blog/media (Amanecia, Newtropin, Reddit r/medicine) → optional, good for public sentiment
3. **Run web_extract on identified URLs** (batch parallel when possible)
4. **Classify from full content, not snippets**

## Severity Classification Heuristics

| Signal | Severity |
|--------|----------|
| FDA press release / proposed rule | 🔴 CRITICAL |
| Coordinated warning letter blitz (2+ firms same day) | 🔴 CRITICAL |
| PCAC meeting announcement | 🟡 IMPORTANT |
| Official clarification / guidance update | 🟡 IMPORTANT |
| Shortage status change | 🟡 IMPORTANT |
| Industry commentary on existing policy | 🟢 NOTABLE |
| Single warning letter (non-coordinated) | 🟢 NOTABLE |
| Pipeline updates | 🟢 NOTABLE |

## Report File Structure
```
fda_alerts/
├── YYYY-MM-DD_fda_scan.md              # Full scan report with analysis
├── YYYY-MM-DD_fda_response_content.md   # Ready-to-post threads + comment templates
└── references/                          # Reference files (this dir)
```
