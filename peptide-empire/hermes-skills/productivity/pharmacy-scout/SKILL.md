---
name: pharmacy-scout
description: Finds compounding pharmacies, verifies licenses and PCAB accreditation, checks FDA 503B registration, and feeds verified leads to outreach — biweekly automated pipeline
version: 3.1
author: Nurse Rob
---

# Pharmacy Scout v3.0 💊

**Purpose:** Biweekly automated discovery and verification of compounding pharmacies. Cross-references FDA 503B registration, PCAB (ACHC) accreditation, state board licenses, and FDA enforcement history. Prepares verified leads for pharmacy-outreach-automator.

## TRIGGER
- Biweekly cron: Wednesday 9:00 AM MST (every 2 weeks)
- Manual: "find new pharmacies" / "scout pharmacies" / "verify compounding pharmacy"

## PROFILE ROUTING
Use `default` (deepseek-v4-pro) — fast, accurate for structured research.

## REGULATORY CONTEXT (Current as of May 2026)

### GLP-1 Shortage Status
- **Tirzepatide shortage resolved:** Dec 19, 2024. 503A enforcement discretion ended Feb 18, 2025; 503B ended Mar 19, 2025.
- **Semaglutide shortage resolved:** Feb 21, 2025. 503A enforcement discretion ended Apr 22, 2025; 503B ended May 22, 2025.
- **Neither tirzepatide nor semaglutide is on the FDA 503B Bulks List or drug shortage list.**
- 503B facilities CANNOT legally compound these drugs from bulk substances.

### Three Remaining Legal Pathways for 503A GLP-1 Compounding
1. Documented allergy to commercial excipient (e.g., polysorbate 80)
2. Non-commercially available dose/route (microdose <2.5mg, oral, sublingual)
3. Combination formulation with documented clinically significant difference

### FDA Enforcement Stance
- FDA issued 55+ warning letters (Sep 2025) and 30 more (Mar 2026) to telehealth/GLP-1 compounders.
- FDA considers semaglutide+B12 "essentially a copy" when same route and within 10% of commercial strength.
- 503A pharmacies may fill ≤4 prescriptions/month of copies under enforcement discretion (as of Apr 1, 2026).

### FDA Regulatory Actions (May 2026)
- **FDA proposal (Apr 30, 2026):** Proposing to formally exclude semaglutide, tirzepatide, and liraglutide from the 503B bulks list. Comments due June 29, 2026.
- **14 peptides moved to FDA Category 1** (recognized as safe for 503A compounding). Includes peptides now legally compoundable.
- **FDA 503B list: 96 registered facilities** (up from 93 as of Apr 2026).

### PCAC Meeting — July 23-24, 2026 (Critical)
The Pharmacy Compounding Advisory Committee will discuss these peptides for the 503A Bulks List:

| Day | Bulk Drug Substances | Uses Evaluated |
|-----|---------------------|----------------|
| **Day 1 (Jul 23)** | BPC-157 (free base/acetate), KPV (free base/acetate), TB-500 (free base/acetate), MOTs-C (free base/acetate) | Ulcerative colitis, wound healing, obesity/osteoporosis |
| **Day 2 (Jul 24)** | Emideltide/DSIP (free base/acetate), Semax (free base/acetate), Epitalon (free base/acetate) | Opioid withdrawal, insomnia, cerebral ischemia |

**Docket:** FDA-2025-N-6895 — Public comments due July 9, 2026 for committee distribution.
**Significance:** These are the most popular research peptides. If added to the 503A Bulks List, compounding pharmacies could legally produce them from bulk substances for patient-specific prescriptions. If denied, compounding will be sharply restricted. **This is a major content/advocacy opportunity for Nurse Rob.**

## WORKFLOW

### Step 1: Discovery — Multi-Source Search
Run ALL of these searches concurrently:
```bash
web_search "compounding pharmacy peptides GLP-1 tirzepatide 2026"
web_search "503A 503B compounding pharmacy peptide formulations"
web_search "compounding pharmacy BPC-157 NAD+ peptide GLP-1"
web_search "PCAB accredited compounding pharmacy peptide GLP-1"
web_search "telehealth compounding pharmacy peptide partner 2026"
web_search "top compounding pharmacies 503B sterile compounding peptide FDA 2026"
web_search "FDA warning letters compounding pharmacy 2026 GLP-1 enforcement actions"
web_search "compounding pharmacy BPC-157 NAD+ peptide newly opened 2026"
web_search "best online tirzepatide semaglutide compounding pharmacy 2026"
web_search "PCAB accredited compounding pharmacy telehealth partnership 2026"
```

### Step 2: Verify Each Pharmacy — FULL CREDENTIALING

For EVERY discovered pharmacy, verify ALL of the following. Use the exact URLs provided.

#### 2a. FDA 503B Registration
- Check: `https://www.fda.gov/drugs/human-drug-compounding/registered-outsourcing-facilities`
- Extract the full facility list (96 registered as of May 2026 — check current count).
- Verify if pharmacy appears. Note registration dates, inspection history, Form 483 status, warning letters, recalls.

#### 2b. PCAB Accreditation (via ACHC)
- **PRIMARY:** `https://achc.org/find-a-provider/` — Select "PCAB Compounding Pharmacy" from dropdown, filter by state.
  - ⚠️ **IMPORTANT:** This page requires interactive browser usage. It has a cookie consent banner and a multi-step dropdown filter form. `web_extract` will NOT return filtered results — you MUST use `browser_navigate` to interact with this page. If Camofox browser is not running, fall back to BACKUP sources below.
  - PCAB covers USP <795> (non-sterile), USP <797> (sterile), USP <800> (hazardous drug handling).
  - ~700 pharmacies are PCAB-accredited nationally.
- **BACKUP:** `https://a4pc.org/find-a-compounder` — APC Compounder Locator Tool. More extractable via `web_extract` — provides educational guidance on what to ask pharmacies.
- **NABP LOOKUP:** `https://nabp.pharmacy/programs/accreditations/compounding-pharmacy/accredited-compounding-pharmacies/` (form submission required).

#### 2c. State Pharmacy License
Use these state-by-state verification portals:
| State | Verification URL | Search By |
|-------|-----------------|-----------|
| Texas | `https://www.pharmacy.texas.gov/dbsearch/phy_search.asp` | Pharmacy Name, License # |
| Florida | `https://mqa-internet.doh.state.fl.us/MQASearchServices/HealthCareProviders` | License prefix + number |
| California | `https://www.pharmacy.ca.gov/about/verify_lic.shtml` | Pharmacy, Sterile Compounding, Non-Resident |
| Minnesota | `https://mn.gov/boards/pharmacy/verify.jsp` | License lookup |
| All States | `https://www.fda.gov/drugs/besaferx-your-source-online-pharmacy-information/locate-state-licensed-online-pharmacy` | State-by-state directory |

Also verify:
- **Non-resident pharmacy permits** for every state they ship to
- **Sterile compounding permit** (required for injectables in CA, FL, TX, and others)

#### 2d. FDA Enforcement History
- **Full enforcement database:** `https://www.fda.gov/drugs/human-drug-compounding/compounding-inspections-recalls-and-other-actions`
- **Warning letters:** `https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters`
- Search by pharmacy name. Note: warning letters, 483s, recalls, consent decrees.

#### 2e. Website & Business Verification
- ✅ Website active + lists compounding/peptide services
- ✅ Physical US address (not drop-ship only, not virtual office)
- ✅ Contact email/phone publicly available
- ✅ License numbers displayed (required by most states)
- ✅ Third-party testing claims verifiable (ask about COA)

### Step 3: Score & Rank (Revised)

Scoring rubric:
- License verified (home state + non-resident): +3
- PCAB accredited (verified via ACHC): +3
- FDA 503B registered: +2
- Clean FDA enforcement record (no warning letters, no open 483s): +2
- Lists peptide/GLP-1 services explicitly: +2
- Multiple peptide types (≥3): +1
- Professional website + displayed credentials: +1
- Multiple shipping states (>30): +1

**Maximum score: 15**

### Step 4: Red Flag Detection

🚩 **Immediate rejection triggers:**
- Pharmacy name not disclosed by telehealth provider
- No license numbers displayed on website
- No PCAB/NABP/ACHC accreditation visible
- 503B claiming to compound semaglutide/tirzepatide from bulk (post-shortage)
- Marketing claims implying FDA approval of compounded products
- Pricing far below market (e.g., <$200/mo for GLP-1 equivalents without transparency)
- Active FDA Warning Letter or open Form 483 observations
- No physical US address listed
- Deals in controlled substances without DEA registration
- "Research chemical" or "not for human consumption" labeling on clearly therapeutic products

### Step 5: Save Verified List
Save to: `~/NurseRob_PeptideEmpire/pharmacy/pharmacy_database.json`
```json
{
  "scout_date": "2026-04-29",
  "regulatory_snapshot": "Post-shortage: tirzepatide & semaglutide resolved. 503B cannot compound from bulk. 503A limited to 3 legal pathways.",
  "fda_503b_count": 93,
  "total_found": 15,
  "verified": 12,
  "rejected": 3,
  "pharmacies": [
    {
      "name": "ABC Compounding Pharmacy",
      "website": "https://...",
      "email": "info@...",
      "phone": "555-...",
      "address": "...",
      "license_state": "CA",
      "license_number": "PHY...",
      "nonresident_states": ["TX","FL","NY"...],
      "pcab_accredited": true,
      "pcab_source": "achc.org",
      "type": "503B",
      "fda_registration_date": "2024-06-15",
      "fda_inspections": "Last inspected 3/15/2025, no 483 issued",
      "fda_warning_letters": 0,
      "peptide_services": ["Tirzepatide", "Semaglutide", "BPC-157", "NAD+"],
      "score": 14,
      "red_flags": [],
      "status": "NEW",
      "discovered": "2026-04-29"
    }
  ]
}
```

### Step 6: Generate Pharmacy Profile Brief
For each TOP-10 scored pharmacy, generate a 1-paragraph brief with credentialing detail:
```
**ABC Compounding Pharmacy** (Score: 14/15)
503B FDA-registered (since 6/2024) | PCAB-accredited (verified via ACHC) | CA-licensed + 38 nonresident permits
Last FDA inspection 3/15/2025 — no 483 issued. Zero warning letters.
Services: Tirzepatide, Semaglutide, BPC-157, NAD+
Contact: info@abcpharmacy.com | 555-0123
Angle: Clean FDA record + broad licensing + PCAB. Strong fit for Nurse Rob audience.
```

### Step 7: Initiate Outreach
Call `pharmacy-outreach-automator`:
"New pharmacy batch ready. Load `~/NurseRob_PeptideEmpire/pharmacy/pharmacy_database.json` latest entries and begin Day 0 research phase."

### Step 8: Update Dashboard
Log to `nurserob-dashboard-manager`:
`Pharmacy scout: [X] found, [Y] verified, [Z] rejected, [W] pushed to outreach`

## TARGET PHARMACY PROFILE
- 🔍 **Ideal:** 503B + PCAB-accredited, clean FDA record, multiple peptides, >30 states, transparent pricing
- ✅ **Good:** 503A + PCAB, single peptide type, active website, displayed credentials
- ⚠️ **Caution:** Unverified license, no physical address, "too good to be true" pricing, undisclosed pharmacy by telehealth partner, minor FDA 483 history (closed)
- ❌ **Skip:** No license info, active FDA warning letter, 503B illegally compounding post-shortage GLP-1s, spammy/MLM feel, controlled substances without DEA registration

## KEY RESOURCES (Quick Reference)

| Resource | URL | Purpose |
|----------|-----|---------|
| FDA 503B Facility List | `fda.gov/drugs/human-drug-compounding/registered-outsourcing-facilities` | Verify 503B registration + inspection history |
| ACHC Find a Provider | `achc.org/find-a-provider/` | Verify PCAB accreditation (PRIMARY) |
| APC Compounder Locator | `a4pc.org/find-a-compounder` | Search compounding pharmacies |
| NABP Accreditation | `nabp.pharmacy/programs/accreditations/compounding-pharmacy/accredited-compounding-pharmacies/` | Verify NABP accreditation |
| FDA Warning Letters | `fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters` | Check enforcement history |
| FDA Compounding Enforcement | `fda.gov/drugs/human-drug-compounding/compounding-inspections-recalls-and-other-actions` | Full enforcement database |
| FDA 503B Bulks List | `fda.gov/drugs/human-drug-compounding/bulk-drug-substances-used-compounding-under-section-503b-fdc-act` | Verify legal APIs for 503B |
| FDA GLP-1 Policy | `fda.gov/drugs/drug-alerts-and-statements/fda-clarifies-policies-compounders-national-glp-1-supply-begins-stabilize` | Current compounding policy |
| BeSafeRx State Lookups | `fda.gov/drugs/besaferx-your-source-online-pharmacy-information/locate-state-licensed-online-pharmacy` | State license portals |

## OUTREACH ANGLE (For Pharmacy Outreach Automator)
```
Subject: Partnership Inquiry — Nurse Rob, RN (Peptide Education)

Hi [Pharmacy Name] team,

I'm Nurse Rob, a licensed RN who educates thousands of biohackers 
and peptide users on safe, evidence-based peptide protocols.

My audience regularly asks me: "Where can I get high-quality, 
properly compounded peptides?" I only recommend pharmacies I've 
personally vetted — and [Pharmacy Name] caught my attention.

I'd love to explore:
• Affiliate partnership (I send educated patients your way)
• Sponsored educational content (my audience trusts my clinical lens)
• Co-branded patient education materials

Would you be open to a 15-minute call this week?

Best,
Nurse Rob, RN
[Contact info]
```

## PITFALLS
- Don't claim to "prescribe" or "dispense" — RNs don't have prescribing authority
- Verify licenses independently — don't trust self-reported claims
- Distinguish 503A (patient-specific prescriptions only) from 503B (office-use, subject to CGMP, cannot compound non-bulk-list APIs post-shortage)
- ACHC Find a Provider is the primary PCAB verification source — not a generic pcab.org lookup
- The FDA 503B list updates weekly; always re-extract for current data
- Avoid pharmacies that market "for human use" on clearly research peptides
- Never engage with pharmacies selling Schedule III/IV substances without verifying DEA registration
- GLP-1 compounding legality is in active litigation — flag pharmacies still compounding at scale
- **Real-world example — Empower Pharmacy:** Previously scored 10/15. On re-scout, discovered: FDA Warning Letter (4/2/2025), Form 483 issued 11/14/2025 (still open), prior Warning Letter (10/15/2021), active Eli Lilly litigation. Score downgraded to 7/15 and outreach deferred. **Always re-check the FDA enforcement database for existing pharmacies on each scout run** — enforcement status can change between biweekly cycles.
- The ACHC Find a Provider (`achc.org/find-a-provider/`) cannot be verified via `web_extract` alone — it's a multi-<wbr>step form with cookie consent. Use `browser_navigate` or fall back to secondary sources.

## QUALITY CHECKLIST
- [ ] At least 5 search sources used (Step 1)
- [ ] FDA 503B list extracted and cross-referenced
- [ ] Every pharmacy run through ACHC Find a Provider for PCAB
- [ ] Home state license verified via state BOP portal
- [ ] FDA enforcement database checked for each pharmacy
- [ ] Red flags documented with rationale for rejections
- [ ] Database file properly formatted JSON with all fields
- [ ] Top 10 scored with credentialing briefs
- [ ] Outreach initiated for new verified pharmacies
- [ ] Dashboard updated
- [ ] Regulatory context note included in database
