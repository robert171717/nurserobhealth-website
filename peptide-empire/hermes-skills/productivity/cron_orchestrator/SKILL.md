---
name: cron_orchestrator
description: Central cron job manager for Nurse Rob Peptide Empire — 21 cron jobs with 3-layer watchdog health monitoring
version: 1.3
author: Nurse Rob
---

# Cron Orchestrator v1.2

Central manager for all 21 Nurse Rob Empire cron jobs — creation, health checks, retries, and alerts.

## Master Cron Registry (21 Jobs)

### High-Frequency Jobs (1)
| Job Name | Schedule (MST) | Skills | Priority |
|----------|---------------|--------|----------|
| Welcome Email Sender | */30 * * * * | welcome_email_sender | HIGH |

### Daily Jobs (9)
| Job Name | Schedule (MST) | Skills | Priority |
|----------|---------------|--------|----------|
| Daily Content Generation | 0 7 * * * | peptide_content_operator,image_generator | HIGH |
| Schedule Morning Post (9AM) | 55 8 * * * | content_scheduler | HIGH |
| Schedule Evening Post (5PM) | 55 16 * * * | content_scheduler | HIGH |
| Lead Scan Morning | 0 6 * * * | lead_sniper | MEDIUM |
| Lead Scan Midday | 0 12 * * * | lead_sniper | MEDIUM |
| Lead Scan Evening | 0 18 * * * | lead_sniper | MEDIUM |
| Lead Scan Overnight | 0 0 * * * | lead_sniper | LOW |
| Lead Nurture AM | 0 10 * * * | lead_followup | MEDIUM |
| Dashboard Daily Summary | 0 21 * * * | nurserob_dashboard_manager | LOW |

### Weekly Jobs (6)
| Job Name | Schedule (MST) | Skills | Priority |
|----------|---------------|--------|----------|
| FDA Weekly Scan | 0 8 * * 1 | fda_monitor | HIGH |
| Pharmacy Outreach Weekly | 0 10 * * 2 | pharmacy_outreach_automator | MEDIUM |
| Pharmacy Scout Biweekly | 0 9 * * 3 | pharmacy_scout | MEDIUM |
| Affiliate Weekly Report | 0 17 * * 0 | nurserob_affiliate_manager | LOW |
| Weekly Analytics Report | 0 18 * * 0 | nurserob_analytics | HIGH |
| Nurse Rob Content Optimizer | 0 2 * * 0 | nurse-rob-content-optimizer,peptide_content_operator | MEDIUM |

### System Jobs (3)
| Job Name | Schedule (MST) | Script | Priority |
|----------|---------------|--------|----------|
| Discord Gateway Watchdog | */10 * * * * | discord_watchdog.py | HIGH |
| Empress Recovery Watchdog | */30 * * * * | (agent, empire-recovery skill) | HIGH |
| Cron Error Alert | */30 * * * * | cron_error_alert.py | HIGH |
| Cron Health Summary | 0 9,21 * * * | cron_health_summary.py | HIGH |

### 3-Layer Watchdog Architecture
The empire monitoring system uses a split architecture to minimize Discord noise while maintaining full coverage:

| Layer | Job | Type | Deliver | Behavior |
|-------|-----|------|---------|----------|
| 🔧 Recovery | Empire Recovery Watchdog | Agent (LLM) | `local` | Silent recovery, no Discord output |
| 🚨 Alert | Cron Error Alert | `no_agent` script | `origin` | ZERO tokens, only outputs on errors |
| 📊 Summary | Cron Health Summary | `no_agent` script | `origin` | ZERO tokens, dashboard at 9AM/9PM |

**Key pattern**: `no_agent=true` scripts with empty stdout = silent. Scripts live in `~/.hermes/scripts/` and are referenced by filename only (relative path).

### Monthly Jobs (1)
| Job Name | Schedule (MST) | Skills | Priority |
|----------|---------------|--------|----------|
| Monthly Content Batch | 0 8 1 * * | content_batch_generator,image_generator | HIGH |

## Workflow

### On Startup: Health Check
1. Run `hermes cron list` to get all existing jobs
2. For each job in registry:
   - Check if job exists → if not, CREATE it using `hermes cron create`
   - Check if job is paused → alert dashboard
   - Check last run status → if failed, flag for retry

### Create Jobs Command Template
```bash
# CORRECT Hermes v0.11.0 syntax — schedule and prompt are positional args:
hermes cron create "[cron expression]" "[task description]" \
  --name "[Job Name]" \
  --skill "[skill1]" \
  --skill "[skill2]"       # --skill is repeatable for multiple skills

# Examples from working setup:
hermes cron create "0 7 * * *" "Generate today's 2 Nurse Rob peptide posts (v2.5 format)." \
  --name "Daily Content Generation" \
  --skill "peptide_content_operator" \
  --skill "image_generator"

hermes cron create "55 8 * * *" "Push morning post (9AM MST) to X via xurl." \
  --name "Schedule Morning Post (9AM)" \
  --skill "content_scheduler"

# Verify:
hermes cron list         # Shows all jobs with [active] status
hermes cron status       # Check if scheduler is running
```

### Failure Recovery
1. Log failure to `~/NurseRob_PeptideEmpire/cron/failure_log.json`
2. Retry after 30 minutes (max 3 retries)
3. If all retries fail → alert dashboard with 🔴 status
4. HIGH priority failures: also attempt fallback with `glm` profile

### Health Check Report
```
┌────────────────────────────────────┐
│  ⚙️ CRON ORCHESTRATOR STATUS       │
│  Checked: [timestamp]              │
├────────────────────────────────────┤
│  Total Jobs:    17                 │
│  🟢 Running:    [X]                │
│  🟡 Due:        [X]                │
│  🔴 Failed:     [X]                │
│  ⚪ Idle:       [X]                │
│                                    │
│  Last 24h:                         │
│  • Executions:   [X]               │
│  • Successes:    [X] ([XX]%)       │
│  • Retries:      [X]               │
│  • Failures:     [X]               │
└────────────────────────────────────┘
```

## Pitfalls
- Don't create duplicate cron jobs — check registry before creating
- ALL times MUST be MST (America/Phoenix)
- Don't retry jobs that fail due to rate limits — wait for next cycle
- Monitor for job overlap: if job takes >15 min, skip next instance
- Rotate failure_log.json weekly to prevent bloat
- **no_agent script paths**: Must be relative to `~/.hermes/scripts/`. Absolute paths (e.g. `/home/robert/.hermes/scripts/foo.py`) are rejected. Use just the filename: `--script "cron_error_alert.py"`.
- **no_agent output behavior**: Empty stdout = silent (nothing delivered). Non-empty stdout = delivered to `--deliver` target. This is the key to zero-token monitoring.
- **`hermes cron list` format**: Block-based, not a table. Parse with regex on `\s+Name:\s+(.+)`, `\s+Schedule:\s+(.+)`, `\s+Last run:\s+(\S+\s+\w+)`. See `nurserob_dashboard_manager/references/cron-list-format.md` for full format reference with examples.
- **Silent ERROR with no delivery_error:** When a job shows `last_status: "error"` but `last_delivery_error: null`, the agent failed mid-execution (not the cron system). The cron engine fired, the agent started, but it hit a tool failure, model timeout, or unrecoverable step. The fix is NOT restarting the cron — it's updating the prompt. Recovery pattern:
  1. Read the cron's current prompt via `cronjob list` with the job_id
  2. Identify weak points: missing fallback instructions, no auth pre-check, ambiguous "generate 3 posts" vs "generate 2 posts"
  3. Hardened prompt must include: explicit step count, auth check as Step 0, fallback for every tool (`if X fails, use Y instead`), and a "never skip" directive
  4. Update the cron with `cronjob action=update` — the job_id stays the same, so the schedule and history are preserved
  5. For HIGH priority jobs: also downgrade the model (pro→flash) to reduce timeout risk
  6. Verify the job's `next_run_at` is in the future — a job stuck in the past won't fire
- **Prompt drift:** The cron's prompt_preview may say "2 posts" but the skill it loads may still describe 3 posts (or vice versa). When updating a skill (e.g., peptide_content_operator v2.3→v2.5), also update ALL cron jobs that reference that skill. A mismatch between the cron prompt and the skill produces dead content (extra posts never scheduled) or confused agents.

## Quality Checklist
- [ ] All 21 cron jobs created and registered
- [ ] Each job has correct schedule, skills/dependencies, priority
- [ ] 3-layer watchdog active: recovery (local) + error alert (origin) + health summary (origin)
- [ ] Health check runs on every orchestrator load
- [ ] Failure recovery logic active (retry 3x, then escalate)
- [ ] Dashboard receives status updates for every job
- [ ] Timezone confirmed MST for all schedules
