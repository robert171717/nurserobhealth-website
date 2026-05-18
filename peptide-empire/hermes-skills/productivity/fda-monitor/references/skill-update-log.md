# Skill Update Summary — May 11, 2026

## Patched: `fda-monitor` (productivity) — May 18, 2026

**What changed:**

| # | Change | Why |
|---|--------|-----|
| 1 | Added Step 1b: Fallback Path (direct curl to FDA.gov when web_search/web_extract fail) | This session: both web_search and web_extract returned credit depletion errors. The primary path was dead — needed a working alternative |
| 2 | Added execute_code HTML processing pattern with security workaround | `curl | python3 -c` is blocked by tirith. Documented the approved workaround using `from hermes_tools import terminal` + Python file I/O |
| 3 | Added structured extraction code for Drug Shortages "New/Updated" tab | The May 18 scan successfully extracted date-grouped entries from the legacy CFM app's tab-4 HTML |
| 4 | Updated MONITORING TARGETS table with live accessibility status | FDA.gov restructured: main compounding page and PCAC pages return 404. Documented which URLs work and which are broken |
| 5 | Added 5 new pitfalls: credit depletion, security pipe blocks, FDA site restructuring, stale DB data, discrepancy watch | Each hit during the May 18 scan run |
| 6 | Added `references/fda-data-sources.md` — complete working-URL map, HTML extraction code, and shortage status table | Central reference so future scans don't rediscover URLs |
| 7 | Updated REFERENCE FILES section to point to new data sources file first | Priority ordering: operational data before historical context |

**Outstanding issue (not patched — system config):**
- The cron job still references `fda_monitor` (underscore) → gets skipped with "skill not found". The pitfall already exists in SKILL.md and this is the second scan cycle it's been an issue. Needs cron config correction outside the skill layer.

---

## Patched: `fda-monitor` (productivity) — May 11, 2026

**What changed (4 patches + 1 reference file added):**

| # | Change | Why |
|---|--------|-----|
| 1 | Profile routing: removed `grok-mode` requirement, made model-agnostic | Scan ran fine on deepseek — the searches do the work, not the model |
| 2 | Added Step 2: Deep Extract (web_extract step between search and classification) | web_search alone returns only snippets — can't classify accurately without full article text |
| 3 | Added cron fallbacks for Steps 6-7 (content scheduler + dashboard) | Cron jobs can't always call downstream integrations |
| 4 | Updated report template: removed stale `grok-mode | Hermes v0.11.0` | Old version numbers and model references are misleading |
| 5 | Updated pitfalls: skill name mismatch (underscore vs hyphen), year-hardcoded queries, web_extract necessity, separate response file | Each was a real issue hit during this session |
| 6 | Updated quality checklist: added web_extract, separate file saves, public comment template | More thorough quality gates |
| 7 | Added `references/2026-05-11-scan-findings.md` | Saves the regulatory landscape, heuristics, and effective patterns for future scans |

**Notable issue identifed (not patched — system config):**
- The cron job configuration references `fda_monitor` (underscore) but the skill is named `fda-monitor` (hyphen). This caused a "skill not found" error at the top of the session. The cron config in `cron_orchestrator` (or wherever the job is defined) should be corrected to reference `fda-monitor` instead. Added a pitfall about this so future agents try both names.
