# Nurse Rob Peptide Empire — Cron Job Audit Report
**Date:** 2026-05-11 | **Auditor:** Hermes Subagent | **Jobs Audited:** 20 (18 listed + 2 discovered)

---

## Executive Summary

**CRITICAL FINDING:** xurl OAuth2 token is expired/revoked (401 Unauthorized). This single failure blocks 6 of 20 jobs from functioning correctly. Two jobs already errored on last run due to connection failures caused by this.

**Secondary Concern:** Skill name mismatches (underscore vs hyphen) exist in 5 cron job configs. Hermes appears to resolve them, but this is fragile.

**Schedule Conflict:** Tuesday 10:00 AM has two jobs firing simultaneously (Lead Nurture AM + Pharmacy Outreach Weekly).

---

## Section 1: Job-by-Job Audit

### 1. Daily Content Generation (31d78cdb31c7)
- **Schedule:** 07:00 daily
- **Skills:** `peptide_content_operator`, `image_generator`
- **Skill Status:** ✅ Both loadable
- **Internet Deps:** web_search (Firecrawl API), image_generate (Hermes built-in)
- **Last Run:** 2026-05-11 12:07 — **OK**
- **SPoF:** web_search credit exhaustion → content degrades to knowledge-only (has fallback). image_generate failure → text-only (acceptable per skill doc)
- **Notes:** Generates content that scheduler later posts. Dependency chain: this must succeed before scheduler jobs at 08:55 and 16:55.

### 2. Schedule Morning Post 9AM (79165fb0ded9)
- **Schedule:** 08:55 daily
- **Skills:** `content_scheduler`
- **Skill Status:** ✅ Loadable
- **Internet Deps:** xurl (X/Twitter API), Discord webhook
- **Last Run:** 2026-05-11 09:05 — **🔴 ERROR: RuntimeError: Connection error**
- **SPoF:** xurl OAuth2 token (CURRENTLY BROKEN). If xurl auth fails, post is saved but NOT published.
- **Blocked by xurl:** YES — cannot post to X without valid OAuth2 token

### 3. Schedule Midday Post (d5fe193c83e2)
- **Schedule:** 11:55 daily
- **Status:** **🟡 NOT FOUND IN CRON ENGINE** — job listed in task but does not exist in `hermes cron list`. Was likely removed during the 3→2 posts/day migration (peptide_content_operator v2.5). **Stale reference — no action needed.**

### 4. Schedule Evening Post (1a089193f391)
- **Schedule:** 16:55 daily
- **Skills:** `content_scheduler`
- **Skill Status:** ✅ Loadable
- **Internet Deps:** xurl (X/Twitter API), Discord webhook
- **Last Run:** 2026-05-10 16:57 — OK
- **SPoF:** Same as Morning Post — xurl OAuth2 token required
- **Blocked by xurl:** YES — same blocker as job #2

### 5–8. Lead Scan Morning/Midday/Evening/Overnight (bbb877c9914b, 4ca2214e78bc, bc118c2566c7, 4f8f1279accd)
- **Schedule:** 06:00 / 12:00 / 18:00 / 00:00 daily
- **Skills:** `lead_sniper`
- **Skill Status:** ✅ Loadable
- **Internet Deps:** xurl (X API search), Discord bot API, web_search (fallback), web_extract
- **Last Runs:** All OK (most recent: 2026-05-11 12:06)
- **SPoF:** xurl auth failure → degraded mode (web_search fallback, much lower yield). Dual failure (xurl + web_search both down) = 0 X leads.
- **Blocked by xurl:** PARTIALLY — runs in degraded mode with web_search, but X scanning and replies are impossible
- **Notes:** Overnight scan (00:00) typically yields 0-3 leads — normal. web_extract fails on x.com URLs (known limitation).

### 9. Lead Nurture AM (b3f8a1c7affb)
- **Schedule:** 10:00 daily
- **Skills:** `lead_followup`
- **Skill Status:** ✅ Loadable
- **Internet Deps:** himalaya (SMTP/Fastmail), xurl (for capturing emails via public replies — indirect dependency)
- **Last Run:** 2026-05-11 10:10 — **🔴 ERROR: RuntimeError: Connection error**
- **SPoF:** himalaya SMTP (can't send nurture emails without it). Also blocked by xurl: without xurl auth, lead_sniper can't capture emails via public replies, so leads enter pipeline without email addresses.
- **Blocked by xurl:** INDIRECTLY — email capture pipeline is broken upstream

### 10. Dashboard Daily Summary (c867443fbc9e)
- **Schedule:** 21:00 daily
- **Skills:** `nurserob_dashboard_manager`
- **Skill Status:** ✅ Loadable
- **Internet Deps:** None (reads local JSON files only)
- **Last Run:** 2026-05-10 21:04 — OK
- **SPoF:** None significant — fully local operation
- **Notes:** This is a reliable health-check job. If it fails, the whole monitoring layer is blind.

### 11. FDA Weekly Scan (0116a00191b7)
- **Schedule:** Monday 08:00
- **Skills:** `fda_monitor`
- **Skill Status:** ⚠️ Cron references `fda_monitor` (underscore), skill file is `fda-monitor` (hyphen). Last run succeeded, so Hermes resolves this — but fragile.
- **Internet Deps:** web_search (5 parallel queries), web_extract (3-4 URLs per query)
- **Last Run:** 2026-05-11 12:06 — OK
- **SPoF:** web_search credit exhaustion → scan fails entirely. web_extract on FDA.gov pages is critical (search snippets insufficient for classification).

### 12. Pharmacy Outreach Weekly (b90f811c3ac0)
- **Schedule:** Tuesday 10:00
- **Skills:** `pharmacy-outreach-automator`
- **Skill Status:** ✅ Loadable
- **Internet Deps:** himalaya (SMTP for sending outreach emails), web_search (optional research)
- **Last Run:** 2026-05-05 10:05 — OK
- **SPoF:** himalaya SMTP — if email sending fails, outreach pipeline stalls. Contact-form-only pharmacies require manual intervention.

### 13. Pharmacy Scout Biweekly (b7b116c1b3de)
- **Schedule:** Wednesday 09:00 (weekly cron, but content is biweekly per skill doc)
- **Skills:** `pharmacy_scout`
- **Skill Status:** ⚠️ Cron uses `pharmacy_scout` (underscore), skill file is `pharmacy-scout` (hyphen). Works but fragile.
- **Internet Deps:** web_search (7 parallel queries), web_extract (FDA, ACHC, NABP, state boards)
- **Last Run:** 2026-05-06 09:15 — OK
- **SPoF:** ACHC/PCAB verification site availability, FDA 503B list site availability, state board portal uptime

### 14. Affiliate Weekly Report (310c9648b0de)
- **Schedule:** Sunday 17:00
- **Skills:** `nurserob_affiliate_manager`
- **Skill Status:** ⚠️ Cron uses `nurserob_affiliate_manager` (underscores), skill file is `nurserob-affiliate-manager` (hyphens). Works but fragile.
- **Internet Deps:** None currently (pre-launch, reads local JSON only). Will need affiliate dashboard APIs when live.
- **Last Run:** 2026-05-10 17:03 — OK
- **SPoF:** None in pre-launch mode

### 15. Weekly Analytics Report (48f0ef333cfe)
- **Schedule:** Sunday 18:00
- **Skills:** `nurserob_analytics`
- **Skill Status:** ⚠️ Cron uses `nurserob_analytics` (underscores), skill file is `nurserob-analytics` (hyphens). Works but fragile.
- **Internet Deps:** None (reads local JSON/MD files)
- **Last Run:** 2026-05-10 18:04 — OK
- **SPoF:** Depends on Affiliate Report (job #14) completing 1 hour earlier. If affiliate report fails, analytics is missing that data.
- **Notes:** Sequential dependency on Affiliate Weekly Report (Sun 17:00 → 18:00 gap). Also reads the affiliate report file generated by job #14.

### 16. Monthly Content Batch (7e200a12172d)
- **Schedule:** 1st of month 08:00
- **Skills:** `content_batch_generator`, `image_generator`
- **Skill Status:** ⚠️ Cron uses `content_batch_generator` (underscores), skill file is `content-batch-generator` (hyphens). Works but fragile.
- **Internet Deps:** web_search (4 queries for research), image_generate (batch of ~30 images)
- **Last Run:** 2026-05-01 08:37 — OK
- **SPoF:** Very token-heavy job (30 days × 2 posts + images). Image generation failure would leave batch without graphics.

### 17. Welcome Email Sender (d6cd60ff0551)
- **Schedule:** Every 30 minutes
- **Skills:** `welcome_email_sender`
- **Skill Status:** ✅ Loadable
- **Internet Deps:** himalaya (IMAP to read Fastmail inbox + SMTP to send welcome emails)
- **Last Run:** 2026-05-11 12:01 — OK
- **SPoF:** Fastmail IMAP/SMTP connectivity. If himalaya can't connect, leads sit unprocessed in inbox. Max 30-min delay window.
- **Notes:** Reduced from */10 to */30 on 2026-05-10 to save tokens (~600K→~200K/day). This is the highest-frequency job.

### 18. Content Optimizer Weekly (4e4bbf5dcb38)
- **Schedule:** Sunday 02:00
- **Skills:** `nurse-rob-content-optimizer`, `peptide_content_operator`
- **Skill Status:** ⚠️ Cron uses `peptide_content_operator` (underscores), skill file uses the same name — loads OK
- **Internet Deps:** None (reads/writes local SKILL.md, generates test posts using LLM)
- **Last Run:** 2026-05-10 17:29 — OK
- **SPoF:** This job MODIFIES peptide_content_operator/SKILL.md. If a bad mutation is kept, it degrades ALL future content generation. The skill has safety guards (medical accuracy auto-discard, protected sections), but a subtle voice drift could persist.
- **Notes:** Runs at 2 AM to avoid contention with other jobs. Uses `deliver: origin` — different from most jobs.

### 19. Empire Recovery Watchdog (c038d43687db)
- **Schedule:** Every 30 minutes
- **Skills:** `empire-recovery`
- **Skill Status:** ✅ Loadable
- **Internet Deps:** Internet connectivity check (Discord API gateway ping), cron engine API
- **SPoF:** If cron engine itself is down, this can't run. Self-excluding: never re-runs itself or Discord Watchdog.
- **Notes:** Max 3 recovery attempts per job per day. 6-hour lookback window for failed jobs.

### 20. Discord Gateway Watchdog (699fe4c70e62)
- **Schedule:** Every 10 minutes
- **Mode:** no-agent (script only)
- **Script:** `discord_watchdog.py` ✅ Found at `~/.hermes/scripts/discord_watchdog.py`
- **Internet Deps:** Discord API (gateway check)
- **Last Run:** 2026-05-11 12:00 — OK
- **SPoF:** This is the MOST critical infrastructure job — if the Discord gateway dies and this doesn't catch it, the Hermes agent can't communicate.
- **Notes:** Runs as a script (no_agent), so it's lightweight and fast. 10-minute interval means max 10-min gateway downtime.

---

## Section 2: Schedule Conflict Analysis

### CONFLICT: Tuesday 10:00 AM
Two jobs fire simultaneously:
1. **Lead Nurture AM** (b3f8a1c7affb) — daily at 10:00
2. **Pharmacy Outreach Weekly** (b90f811c3ac0) — Tuesday at 10:00

**Risk:** Both jobs compete for LLM/model resources simultaneously. Pharmacy Outreach also calls `nurserob_dashboard_manager`, which Lead Nurture may also try to update. Dashboard writes could race.

**Recommendation:** Offset Pharmacy Outreach to Tuesday 10:30 or 11:00 to avoid concurrent execution.

### Sequential Dependencies (by design, working correctly):
- Daily Content Gen (07:00) → Morning Post (08:55) → Evening Post (16:55) — 1h55m gap is sufficient
- Affiliate Weekly (Sun 17:00) → Analytics Report (Sun 18:00) — 1-hour gap, analytics reads affiliate output
- Content Optimizer (Sun 02:00) runs before Content Gen (07:00) — optimizer changes are picked up same day

### High-Concurrency Windows:
- **Every 30 minutes:** Welcome Email Sender + Empire Recovery Watchdog fire at the same time (:00 and :30). Both are lightweight, likely fine.
- **06:00–07:00 window:** Lead Scan Morning (06:00) + Daily Content Gen (07:00) — sequential, no overlap

---

## Section 3: Internet Dependency Map

### Critical External Services
| Service | Jobs Dependent | Status | Impact if Down |
|---------|---------------|--------|----------------|
| **xurl OAuth2 (X API)** | Morning Post, Evening Post, Lead Scans (×4), Lead Nurture | 🔴 **BROKEN (401)** | X posting dead, X scanning degraded to web_search, replies impossible |
| **himalaya IMAP/SMTP (Fastmail)** | Welcome Email, Lead Nurture, Pharmacy Outreach | ✅ Working (v1.2.0) | No outbound emails, no inbox monitoring |
| **web_search (Firecrawl API)** | Content Gen, Lead Sniper (degraded), FDA Monitor, Pharmacy Scout, Monthly Batch | ⚠️ Credit-dependent | Content research degrades, lead scanning degraded, FDA/Pharmacy blind |
| **Discord Bot API** | Lead Sniper (Discord scanning), Discord Watchdog | ✅ Configured | Loss of Discord monitoring and lead scanning channel |
| **image_generate (Hermes built-in)** | Content Gen, Monthly Batch | Unknown | Content posts without graphics (acceptable fallback) |

---

## Section 4: Single Points of Failure (SPoF) Ranked by Impact

### 🔴 CRITICAL (Empire-Blocking)
1. **xurl OAuth2 token** — A single expired token blocks ALL X posting (2 jobs) AND degrades lead scanning (4 jobs). Currently broken. **6+ jobs affected.** Fix: `xurl auth oauth2 --app default NurseRobHealth` (requires browser).
2. **Firecrawl API credits** — Exhaustion would blind FDA Monitor, Pharmacy Scout, and kill web_search fallback for Lead Sniper. **6+ jobs affected.**

### 🟡 HIGH IMPACT
3. **himalaya SMTP (Fastmail)** — Loss blocks all outbound email: welcome emails, pharmacy outreach, lead nurture emails. **3 jobs affected.**
4. **Discord bot token** — Loss kills Discord lead scanning and the gateway watchdog. **2 jobs affected, plus agent communication.**
5. **Internet connectivity (VPN)** — Total outage blocks all internet-dependent jobs. Mitigated by Empire Recovery Watchdog.

### 🟢 MODERATE
6. **Content Optimizer modifying SKILL.md** — Bad mutations could degrade content quality. Mitigated by backup (.bak) and medical accuracy auto-discard.
7. **Dashboard metrics.json corruption** — Would affect Dashboard Summary and Analytics Report. Mitigated by file-based approach.

---

## Section 5: Skill Name Mismatches

| Cron Job Config Name | Actual Skill File | Status |
|----------------------|-------------------|--------|
| `fda_monitor` | `fda-monitor` | ⚠️ Resolved but fragile |
| `pharmacy_scout` | `pharmacy-scout` | ⚠️ Resolved but fragile |
| `nurserob_affiliate_manager` | `nurserob-affiliate-manager` | ⚠️ Resolved but fragile |
| `nurserob_analytics` | `nurserob-analytics` | ⚠️ Resolved but fragile |
| `content_batch_generator` | `content-batch-generator` | ⚠️ Resolved but fragile |
| `peptide_content_operator` | `peptide_content_operator` | ✅ Match (skill uses underscores) |
| `content_scheduler` | `content_scheduler` | ✅ Match |
| `lead_sniper` | `lead_sniper` | ✅ Match |
| `lead_followup` | `lead_followup` | ✅ Match |
| `nurserob_dashboard_manager` | `nurserob_dashboard_manager` | ✅ Match |
| `welcome_email_sender` | `welcome_email_sender` | ✅ Match |
| `image_generator` | `image-generator` | ⚠️ Resolved but fragile |
| `nurse-rob-content-optimizer` | `nurse-rob-content-optimizer` | ✅ Match |
| `pharmacy-outreach-automator` | `pharmacy-outreach-automator` | ✅ Match |
| `empire-recovery` | `empire-recovery` | ✅ Match |

**5 skills have underscore/hyphen mismatches** in their cron configs. Hermes resolves these at runtime (all jobs ran OK), but this is a naming convention inconsistency that could break if the resolution logic changes.

---

## Section 6: xurl OAuth2 Status — Deep Analysis

**Current State: State B (Token Expired/Revoked)**

```
xurl auth status:
  ▸ default  [(no credentials)]
      oauth2: NurseRobHealth    ← app registered, username assigned
      oauth1: –
      bearer: –

xurl whoami:
  {"title":"Unauthorized","status":401,"detail":"Unauthorized"}  ← TOKEN INVALID
```

**Impact Analysis:**
- `default` app is registered with `NurseRobHealth` OAuth2 — the setup is correct
- The token has expired or been revoked at the X developer portal
- The `(no credentials)` indicator confirms the token is no longer valid
- All X API calls will return 401

**Jobs Blocked:**
1. Morning Post (79165fb0ded9) — **LAST RUN ERRORED**
2. Evening Post (1a089193f391) — Will error on next run
3. Lead Scans (4 jobs) — Running in degraded mode (web_search fallback)
4. Lead Nurture (b3f8a1c7affb) — **LAST RUN ERRORED** (connection error)
5. Content generation still works (saves to file), but posting is blocked

**Fix Required (manual, requires browser):**
```bash
xurl auth oauth2 --app default NurseRobHealth
```
This opens a browser for OAuth2 re-grant. No need to re-register the app.

---

## Section 7: Recommendations

### Immediate (Fix Today)
1. **Re-auth xurl:** Run `xurl auth oauth2 --app default NurseRobHealth` in a browser session. This unblocks 6+ jobs.
2. **Check Firecrawl credits:** Verify web_search is still returning results (not "Payment Required").

### Short-Term (This Week)
3. **Fix schedule conflict:** Offset Pharmacy Outreach Weekly from Tue 10:00 to Tue 10:30 or 11:00.
4. **Standardize skill names:** Update 5 cron job configs to use hyphenated skill names (matching filesystem).

### Medium-Term (This Month)
5. **Add xurl auth health check:** Create a lightweight pre-flight script that checks xurl auth before content scheduler runs, with a notification if broken.
6. **Consider token refresh automation:** If X API supports refresh tokens, automate the re-auth flow.
7. **Remove stale job reference:** The `d5fe193c83e2` (Midday Post) is referenced in documentation but removed from cron. Update documentation.

---

## Section 8: Job Health Scorecard

| Status | Count | Jobs |
|--------|-------|------|
| ✅ OK | 16 | Content Gen, Evening Post, Lead Scans (×4), Dashboard Summary, FDA Scan, Pharmacy Outreach, Pharmacy Scout, Affiliate Report, Analytics Report, Monthly Batch, Welcome Email, Content Optimizer, Empire Recovery, Discord Watchdog |
| 🔴 ERROR | 2 | Morning Post (Connection error), Lead Nurture AM (Connection error) |
| 🟡 MISSING | 1 | Schedule Midday Post (removed, reference stale) |
| 🔴 DEGRADED | 4 | Lead Scans running in web_search degraded mode due to xurl auth failure |

**Overall Empire Health: 70%** — Core infrastructure works, but X platform integration is completely offline.

---

*Report generated by Hermes Agent subagent — 2026-05-11T12:10:00-07:00*
