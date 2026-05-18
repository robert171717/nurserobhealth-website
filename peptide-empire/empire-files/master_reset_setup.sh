#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
#  🏥 NURSE ROB PEPTIDE EMPIRE — MASTER RESET SETUP
#  Hermes v0.11.0 | April 27, 2026
#
#  What this script does:
#    1. Pre-flight checks (Hermes installed, profiles configured)
#    2. Creates full project directory structure
#    3. Initializes dashboard metrics file
#    4. Verifies all 15 skills are installed
#    5. Creates all 15 cron jobs with correct CLI syntax
#    6. Runs final verification (skill count + cron count)
#
#  Usage:
#    bash master_reset_setup.sh
#    OR: chmod +x master_reset_setup.sh && ./master_reset_setup.sh
#
#  Safe to re-run — cron jobs that already exist will be skipped gracefully.
#  Skills that failed to install can be created via skill_manage (see blueprint).
# ═══════════════════════════════════════════════════════════════════════════════

# ─── Configuration ───
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'
PROJECT_DIR="$HOME/NurseRob_PeptideEmpire"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S %Z')

# ─── Banner ───
echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  🏥 NURSE ROB PEPTIDE EMPIRE — MASTER RESET SETUP               ║${NC}"
echo -e "${CYAN}║  15 Skills · 15 Cron Jobs · 95%+ Automation                     ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEP 1: PRE-FLIGHT CHECKS
# ═══════════════════════════════════════════════════════════════════
echo -e "${BOLD}${YELLOW}━━━ STEP 1/5: Pre-Flight Checks ━━━${NC}"

# Check Hermes
if ! command -v hermes &>/dev/null; then
    echo -e "  ${RED}❌ Hermes CLI not found in PATH.${NC}"
    echo -e "  ${RED}   Install Hermes v0.11.0 and ensure 'hermes' is on your PATH.${NC}"
    exit 1
fi
HERMES_PATH=$(command -v hermes)
echo -e "  ${GREEN}✅${NC} Hermes detected at ${HERMES_PATH}"

# Check profiles
if hermes profile list 2>/dev/null | grep -q "default"; then
    echo -e "  ${GREEN}✅${NC} Profiles ready (default found)"
else
    echo -e "  ${YELLOW}⚠️  Default profile not found. Some skills may need profile routing.${NC}"
    echo -e "  ${YELLOW}   Run 'hermes setup' if content generation fails.${NC}"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════
# STEP 2: PROJECT DIRECTORY STRUCTURE
# ═══════════════════════════════════════════════════════════════════
echo -e "${BOLD}${YELLOW}━━━ STEP 2/5: Project Directory Structure ━━━${NC}"

mkdir -p "$PROJECT_DIR"/{content,Content_Calendar,leads,fda_alerts,pharmacy, \
  videos/{raw,transcripts,processed}, \
  images/{headers,carousels,stats,reels,quotes,leads}, \
  dashboard,reports,affiliates,subscribers,cron}

echo -e "  ${GREEN}✅${NC} Created at ${PROJECT_DIR}"

# Initialize dashboard metrics (only if not already present)
METRICS_FILE="$PROJECT_DIR/dashboard/metrics.json"
if [ ! -f "$METRICS_FILE" ]; then
    cat > "$METRICS_FILE" << 'METRICS_EOF'
{
  "last_updated": "",
  "audience": {"x_followers": 0, "x_growth_week": 0, "email_list": 0, "email_growth_week": 0, "discord": 0},
  "revenue_mtd": {"consults": 0, "consults_count": 0, "digital": 0, "digital_count": 0, "affiliate": 0, "affiliate_clicks": 0, "coaching": 0, "coaching_members": 0},
  "content": {"posts_today": 0, "posts_week": 0, "engagement_rate": 0.0, "top_post": "N/A"},
  "leads": {"hot_today": 0, "hot_replied": 0, "warm_in_nurture": 0, "consult_inquiries_week": 0},
  "pharmacy": {"scouted_verified": 0, "outreach_active": 0, "negotiating": 0, "partners_live": 0},
  "fda": {"last_scan": "never", "alerts_found": 0, "critical_pending": 0},
  "cron_status": {}
}
METRICS_EOF
    echo -e "  ${GREEN}✅${NC} Dashboard metrics initialized"
else
    echo -e "  ${GREEN}✅${NC} Dashboard metrics already exist (preserved)"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════
# STEP 3: SKILL VERIFICATION
# ═══════════════════════════════════════════════════════════════════
echo -e "${BOLD}${YELLOW}━━━ STEP 3/5: Skill Verification ━━━${NC}"

ALL_SKILLS=(
    # Phase 1: Core Engine
    "peptide_content_operator"
    "content_scheduler"
    "lead_sniper"
    "lead_followup"
    "nurserob_dashboard_manager"
    "cron_orchestrator"
    # Phase 2: Content & Research
    "content_batch_generator"
    "image_generator"
    "fda_monitor"
    "video_repurposer"
    # Phase 3: Monetization & Growth
    "nurserob_onboarding"
    "pharmacy_scout"
    "pharmacy_outreach_automator"
    "nurserob_affiliate_manager"
    "nurserob_analytics"
)

INSTALLED=0
MISSING_SKILLS=()

for skill in "${ALL_SKILLS[@]}"; do
    if hermes skills list 2>/dev/null | grep -q "$skill"; then
        echo -e "  ${GREEN}✅${NC} $skill"
        ((INSTALLED++))
    else
        echo -e "  ${YELLOW}⚠️${NC}  $skill — NOT FOUND"
        MISSING_SKILLS+=("$skill")
    fi
done

echo ""
echo -e "  Skills present: ${INSTALLED}/15"

if [ ${#MISSING_SKILLS[@]} -gt 0 ]; then
    echo -e "  ${YELLOW}⚠️  ${#MISSING_SKILLS[@]} skill(s) missing. Create via skill_manage or use Appendix A in the blueprint.${NC}"
    echo -e "  ${YELLOW}   Missing: ${MISSING_SKILLS[*]}${NC}"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════
# STEP 4: CREATE ALL 15 CRON JOBS
# ═══════════════════════════════════════════════════════════════════
echo -e "${BOLD}${YELLOW}━━━ STEP 4/5: Creating 15 Cron Jobs ━━━${NC}"
echo ""

# Helper function
create_cron() {
    local schedule="$1"
    local prompt="$2"
    local name="$3"
    shift 3
    local skills=("$@")

    echo -ne "  ${name}... "

    # Build command
    local cmd="hermes cron create \"$schedule\" \"$prompt\" --name \"$name\""
    for s in "${skills[@]}"; do
        cmd="$cmd --skill \"$s\""
    done

    if eval "$cmd" 2>/dev/null; then
        echo -e "${GREEN}✅ CREATED${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️  (may already exist or failed)${NC}"
        return 1
    fi
}

# ── DAILY JOBS (10) ──
echo -e "  ${CYAN}── Daily Jobs (10) ──${NC}"

create_cron "0 7 * * *" \
    "Generate today's 3 Nurse Rob peptide posts using creative-mode profile. Save to ~/NurseRob_PeptideEmpire/content/YYYY-MM-DD_posts.md. Push to content_scheduler when done." \
    "Daily Content Generation" \
    "peptide_content_operator" "image_generator"

create_cron "55 7 * * *" \
    "Push morning post (8AM MST slot) from today's content file to X via xurl." \
    "Schedule Morning Post" \
    "content_scheduler"

create_cron "55 11 * * *" \
    "Push midday post (12PM MST slot) from today's content file to X." \
    "Schedule Midday Post" \
    "content_scheduler"

create_cron "55 16 * * *" \
    "Push evening post (5PM MST slot) from today's content file to X." \
    "Schedule Evening Post" \
    "content_scheduler"

create_cron "0 6 * * *" \
    "Scan X and Discord for peptide questions. Auto-reply to hot leads with value-first responses. Push warm leads to lead_followup for nurture." \
    "Lead Scan Morning" \
    "lead_sniper"

create_cron "0 12 * * *" \
    "Scan X and Discord for peptide questions. Auto-reply to hot leads." \
    "Lead Scan Midday" \
    "lead_sniper"

create_cron "0 18 * * *" \
    "Scan X and Discord for peptide questions. Auto-reply to hot leads." \
    "Lead Scan Evening" \
    "lead_sniper"

create_cron "0 0 * * *" \
    "Scan X and Discord for peptide questions. Lower priority overnight capture." \
    "Lead Scan Overnight" \
    "lead_sniper"

create_cron "0 10 * * *" \
    "Check lead nurture tracker at ~/NurseRob_PeptideEmpire/leads/nurture_tracker.json. Send any due follow-up messages per the 5-step sequence (Day 0/2/5/9/14). Update tracker after each send." \
    "Lead Nurture AM" \
    "lead_followup"

create_cron "0 21 * * *" \
    "Generate daily dashboard summary. Update all metrics from today's activity across content, leads, and revenue." \
    "Dashboard Daily Summary" \
    "nurserob_dashboard_manager"

echo ""

# ── WEEKLY JOBS (4) ──
echo -e "  ${CYAN}── Weekly Jobs (4) ──${NC}"

create_cron "0 8 * * 1" \
    "Run weekly FDA peptide/GLP-1 scan. Search FDA compounding, warning letters, drug shortages, and PCAC. Generate alert report and response content. Save to ~/NurseRob_PeptideEmpire/fda_alerts/." \
    "FDA Weekly Scan" \
    "fda_monitor"

create_cron "0 10 * * 2" \
    "Check pharmacy outreach pipeline. Send due emails per the 5-email sequence (Intro Day 0, Value Day 3, Proposal Day 7, Case Study Day 14, Final Day 21). Update outreach tracker." \
    "Pharmacy Outreach Weekly" \
    "pharmacy_outreach_automator"

create_cron "0 9 * * 3" \
    "Run compounding pharmacy discovery and verification. Search for GLP-1, BPC-157, NAD+ compounding pharmacies. Verify licenses and PCAB accreditation. Push new verified pharmacies to pharmacy_outreach_automator." \
    "Pharmacy Scout Biweekly" \
    "pharmacy_scout"

create_cron "0 17 * * 0" \
    "Check all affiliate links, clicks, and conversions. Update dashboard with revenue estimates by partner and category." \
    "Affiliate Weekly Report" \
    "nurserob_affiliate_manager"

create_cron "0 18 * * 0" \
    "Generate comprehensive weekly performance report covering content, leads, revenue, pharmacy pipeline, and automation health. Save to ~/NurseRob_PeptideEmpire/reports/weekly_report_[date].md. Push summary to dashboard." \
    "Weekly Analytics Report" \
    "nurserob_analytics"

echo ""

# ── MONTHLY JOB (1) ──
echo -e "  ${CYAN}── Monthly Job (1) ──${NC}"

create_cron "0 8 1 * *" \
    "Generate full 30-day content calendar for the new month using creative-mode profile. Research trending peptide topics. Produce 90 posts (3 per day) with text, image prompts, CTAs, and disclaimers. Save to ~/NurseRob_PeptideEmpire/Content_Calendar/30_Day_Calendar_[MONTH].md." \
    "Monthly Content Batch" \
    "content_batch_generator" "image_generator"

echo ""

# ═══════════════════════════════════════════════════════════════════
# STEP 5: FINAL VERIFICATION
# ═══════════════════════════════════════════════════════════════════
echo -e "${BOLD}${YELLOW}━━━ STEP 5/5: Final Verification ━━━${NC}"

# Skill count
SKILL_COUNT=$(hermes skills list 2>/dev/null | grep -cE "peptide_content_operator|content_scheduler|lead_sniper|lead_followup|nurserob_dashboard_manager|cron_orchestrator|content_batch_generator|image_generator|fda_monitor|video_repurposer|nurserob_onboarding|pharmacy_scout|pharmacy_outreach_automator|nurserob_affiliate_manager|nurserob_analytics" || echo "0")
echo -e "  Skills installed:  ${SKILL_COUNT}/15"

# Cron count
CRON_COUNT=$(hermes cron list 2>/dev/null | grep -cE "Daily Content Generation|Schedule Morning Post|Schedule Midday Post|Schedule Evening Post|Lead Scan Morning|Lead Scan Midday|Lead Scan Evening|Lead Scan Overnight|Lead Nurture AM|Dashboard Daily Summary|FDA Weekly Scan|Pharmacy Outreach Weekly|Pharmacy Scout Biweekly|Affiliate Weekly Report|Weekly Analytics Report|Monthly Content Batch" || echo "0")
echo -e "  Cron jobs created: ${CRON_COUNT}/15"

echo ""

# ─── SUMMARY ───
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  🏥 NURSE ROB PEPTIDE EMPIRE — SETUP COMPLETE                   ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${BOLD}📁 Project:${NC}     ${PROJECT_DIR}"
echo -e "  ${BOLD}📊 Dashboard:${NC}   Load nurserob_dashboard_manager → 'show dashboard'"
echo -e "  ${BOLD}📝 Next step:${NC}   Load content_batch_generator → 'generate next 30 days'"
echo -e "  ${BOLD}🔍 Verify cron:${NC} hermes cron list"
echo ""

if [ ${#MISSING_SKILLS[@]} -gt 0 ]; then
    echo -e "  ${YELLOW}⚠️  ${#MISSING_SKILLS[@]} skill(s) still missing. Create them via skill_manage.${NC}"
    echo -e "  ${YELLOW}   See Appendix A in NurseRob_Empire_Blueprint_v2.2.md for full prompts.${NC}"
    echo ""
fi

echo -e "  ${GREEN}Setup finished at ${TIMESTAMP}${NC}"
echo ""
