# Credentialing Sources Reference

> Verified credentialing sources used during May 13, 2026 scout run. Maintained as a quick-reference for efficient re-verification across successive biweekly cycles.

## Source Reliability Hierarchy

| Priority | Source | URL | Coverage | Extraction Method | Notes |
|----------|--------|-----|----------|-------------------|-------|
| P1 | FDA 503B Facility List | fda.gov/drugs/human-drug-compounding/registered-outsourcing-facilities | 96 facilities (as of May 2026) | `web_extract` | Best source for 503B registration + inspection history. Table includes: facility name, city/state, initial registration, most recent registration, last inspection date, Form 483 issued?, recall conducted?, action based on last inspection. Updated weekly. |
| P2 | FDA Compounding Enforcement DB | fda.gov/drugs/human-drug-compounding/compounding-inspections-recalls-and-other-actions | All 503A + 503B facilities | `web_extract` | Alphabetical A-Z index. Each entry shows 483 issuances, warning letters, untitled letters, consent decrees, press releases, recalls. Links to PDFs of actual documents. |
| P3 | FDA Warning Letter Database | fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters | All FDA warning letters | `web_search` | Search by facility name. Warning letters are definitive enforcement actions. |
| P4 | ACHC Find a Provider (PCAB) | achc.org/find-a-provider/ | ~700 PCAB-accredited pharmacies | `browser_navigate` REQUIRED | Multi-step form: select "PCAB Compounding Pharmacy" from dropdown → select state. Cookie consent banner blocks `web_extract`. Falls back to P5/P6 when browser unavailable. |
| P5 | APC Compounder Locator | a4pc.org/find-a-compounder | APC member pharmacies | `web_extract` | Educational tool — provides guidance on what to ask pharmacies. More accessible than ACHC via extraction. |
| P6 | NABP Accreditation Lookup | nabp.pharmacy/programs/accreditations/compounding-pharmacy/accredited-compounding-pharmacies/ | NABP-accredited pharmacies | Form submission required | Not extractable programmatically. Submit form and wait for response. |
| P7 | State BOP Portals | Various (see table in SKILL.md) | State-specific | `web_extract` | FL MQA portal verified working (mqa-internet.doh.state.fl.us). TX/CA/NY portals also reliable. |

## Effective Search Queries (Discovered May 13)

These queries returned the highest-quality results during the May 13 scout:

```
"compounding pharmacy peptides GLP-1 tirzepatide semaglutide 2026"
"503A 503B compounding pharmacy peptide formulations new 2026"
"PCAB accredited compounding pharmacy peptide GLP-1 2026"
"top compounding pharmacies 503B sterile compounding peptide FDA 2026"
"FDA warning letters compounding pharmacy 2026 GLP-1 enforcement actions"
"compounding pharmacy BPC-157 NAD+ peptide newly opened 2026"
"best online tirzepatide semaglutide compounding pharmacy 2026"
"PCAB accredited compounding pharmacy telehealth partnership 2026"
```

## Self-Reported PCAB Claim Patterns

Pharmacies claim PCAB in these ways (ranked by reliability):

1. **Explicit "PCAB-Accredited" badge on website** — most reliable (e.g., MediVera: "Dual PCAB Accreditation", Strive: "PCAB/ACHC" on dedicated page)
2. **"PCAB" mentioned in about/compliance page** — reliable if cross-referenced (e.g., Enovex: ACHC/PCAB on USP 800 page)
3. **Mentioned in third-party review articles** — useful cross-reference (e.g., Epiq Scripts cited as PCAB-accredited in multiple telehealth comparison articles)
4. **Claim on provider portal page without visible badge** — least reliable; verify through ACHC or APC

## Pharmacy Discovery Pipeline (New Entries Pattern)

When discovering a new pharmacy, collect this minimum data in order:

1. **Name + Website** — verify domain resolves, active content
2. **Physical address** — cross-street via Google/OSM. Flag virtual offices or P.O. boxes
3. **License state + number** — verify via state BOP portal
4. **PCAB status** — check via ACHC browser or APC extractor. If self-reported only, note as unconfirmed
5. **FDA 503B registration** — check against FDA 503B facility list
6. **FDA enforcement history** — check enforcement database and warning letter search
7. **Contact info** — email preferred. If contact form only, flag as `CONTACT_FORM_REQUIRED`
8. **Peptide services** — extract from website. Note exact formulations offered
9. **Shipping states** — extract from FAQ or shipping policy
10. **Score** — apply scoring rubric (see SKILL.md Step 3)

## Known PCAB-Accredited Pharmacies (Verified This Scout)

| Pharmacy | PCAB Type | Verification Method | Confidence |
|----------|-----------|-------------------|------------|
| MediVera | Dual (sterile + non-sterile) | Website claim + multiple third-party sources | High |
| Strive | PCAB + NABP + LegitScript | Dedicated accreditation page | High |
| Epiq Scripts | PCAB + URAC + LegitScript | Telehealth comparison articles + pharmacy site | High |
| FarmaKeio | PCAB + IPS + ACHC | Website + multi-source | High |
| CRE8 | PCAB | Website | High |
| Hallandale | PCAB | Website | High |
| Empower | PCAB | Website + FDA references | High (despite FDA enforcement issues) |
| Enovex | PCAB/ACHC | USP 800 compliance page | Medium |
| Valor | PCAB | Website | Confirmed (now declined for peptides) |

## ACHC PCAB Bypass Strategy

When Camofox browser is unavailable and ACHC direct lookup fails:

1. Search: `"PCAB accredited" [pharmacy name]` — often returns direct accreditation pages
2. Search: `[pharmacy name] PCAB accreditation` — returns third-party verification articles
3. Check the pharmacy's "About" or "Quality/Compliance" page
4. Use APC Locator (a4pc.org) as secondary check
5. For critical decisions, note PCAB as "self-reported, unverified via ACHC" in database

## Sample Credentialing Brief Format

```
**[Pharmacy Name]** (Score: X/15)
[Type] PCAB-[accredited/confirmed/unconfirmed] | [State]-licensed [± nonresident]
FDA: [Registered/Self-reported] [± Warning Letter/483/recall]
Services: [list]
Contact: [email/phone/form]
Angle: [2-3 sentence partnership angle]
```
