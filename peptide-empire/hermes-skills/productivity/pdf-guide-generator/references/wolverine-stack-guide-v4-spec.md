# Wolverine Stack Guide v4 — Content Spec

Built May 13, 2026 using reportlab. 12-page PDF, navy/teal/gold Nurse Rob branding.

## Structure (12 Pages)

| Page | Section | Notes |
|------|---------|-------|
| 1 | Cover | Large title, gold divider, author, URL. No page number. |
| 2 | What This Guide Covers | Bullet list of contents. Context paragraph. |
| 3 | BPC-157 Deep Dive | Research summary, oral vs SubQ protocols, 250-500 mcg 1-2x/day |
| 4 | TB-500 Deep Dive | Systemic vs local mechanism, 2.5mg 2x/week protocol, half-life |
| 5 | The Wolverine Stack | Protocol summary table, injection sites, stacking logic |
| 6 | Sterile Technique | 6-step technique, supply list (insulin syringes primary) |
| 7-8 | Reconstitution & Mixing Math | Steps 1-4: supplies, how much bac water, technique, formula |
| 9-10 | Dosing Charts | BPC-157 (5mg + 10mg vials, 4 bac water volumes), TB-500 (5mg + 10mg vials, 3 bac water volumes) |
| 11 | Storage & Handling | 5-row storage table (dry powder, reconstituted, in syringe, room temp, key rules) |
| 12 | Next Steps | 4 action items, disclaimer, contact info |

## Brand Colors
- Navy: #1a2332 (backgrounds, headers)
- Teal: #0891b2 (subheadings, accents)
- Gold: #c4a43e (dividers, accents)
- Light Navy: #2a3a4f (table headers)
- Off-White: #f8f9fa (alternating table rows)
- Muted: #6b7280 (captions, secondary text)

## Dosing Protocol (Nurse Rob's personal protocol)
- **BPC-157**: 10mg vial + 2mL bac water = 5mg/mL → 5 units = 250mcg, 2x/day SubQ
- **TB-500**: 10mg vial + 1mL bac water = 10mg/mL → 25 units = 2.5mg, 2x/week SubQ

## Dosing Charts Included

### BPC-157 — 5mg Vial
Bac water volumes: 1.0, 1.5, 2.0, 2.5 mL
Dose targets: 150, 250, 350, 500 mcg

### BPC-157 — 10mg Vial
Bac water volumes: 1.0, 2.0, 3.0, 4.0 mL
Dose targets: 150, 250, 350, 500 mcg

### TB-500 — 5mg Vial
Bac water volumes: 1.0, 1.5, 2.0 mL
Dose targets: 2.0, 2.5, 5.0 mg

### TB-500 — 10mg Vial
Bac water volumes: 1.0, 2.0, 3.0 mL
Dose targets: 2.0, 2.5, 5.0 mg

## Supply List (from Step 1)
- Bacteriostatic Water (30mL standard)
- Insulin Syringes (0.3/0.5/1mL, 31G) — PRIMARY
- 3mL syringe + 22-25G needle — OPTIONAL
- Alcohol Prep Pads (70%)
- Sharps container

## Key Formula
mg/mL = mg ÷ mL
Units = (desired dose in mcg ÷ 1000) ÷ concentration in mg/mL × 100

## Rebuild Command
Use the full build script pattern from the reportlab section of pdf-guide-generator skill.
The v4 build script is at: `/tmp/build_wolverine_guide_v4.py` (may not persist across reboots).
Output paths: Desktop `Daily Brief/NurseRob_PeptideEmpire/assets/Wolverine_Stack_Guide_v4.pdf` + Linux `~/NurseRob_PeptideEmpire/assets/`

## Website Deployment
- Repo: `/mnt/c/Users/Robert/Desktop/nurserobhealth-website/`
- Copy PDF to `guide.pdf` in repo root
- `git add guide.pdf && git commit && git push`
- Vercel auto-deploys from GitHub push
- Live at: https://nurserobhealth.com/guide.pdf
- Content-length should be ~23-24KB for v4

## User Feedback from v3 → v4 Fixes
1. Major sections MUST start at page tops (use PageBreak before each)
2. No blank pages — every page has content
3. 3mL syringe marked as OPTIONAL, insulin syringes as primary
4. Formula box font must fit inside navy box without cutoff
5. Storage table spacing must be consistent — "In syringe" not "In  syringe"
6. "Next Steps" must be at top of its own page
7. Total pages doesn't matter — proper spacing over page count
