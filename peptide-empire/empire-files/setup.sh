#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
#  🏥 NURSE ROB PEPTIDE EMPIRE — ONE-COMMAND FULL SETUP (Fixed v2.2)
#  Hermes v0.11.0 | April 27, 2026
# ═══════════════════════════════════════════════════════════════════════════════
# NOTE: set -e removed — skill verification grep can return 1 if skill not in registry list

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; RED='\033[0;31m'; NC='\033[0m'
PROJECT_DIR="$HOME/NurseRob_PeptideEmpire"

echo ""
echo -e "${CYAN}╔════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  🏥 NURSE ROB PEPTIDE EMPIRE — FULL SYSTEM SETUP (FIXED)                  ║${NC}"
echo -e "${CYAN}║  Hermes v0.11.0 | 15 Skills | 15 Cron Jobs                               ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ─── STEP 1: Pre-Flight ───
echo -e "${YELLOW}━━━ STEP 1/5: Pre-Flight Checks ━━━${NC}"
command -v hermes &>/dev/null || { echo -e "${RED}❌ Hermes not found.${NC}"; exit 1; }
echo -e "  ${GREEN}✅ Hermes detected${NC}"
hermes profile list 2>/dev/null | grep -q "default" && echo -e "  ${GREEN}✅ Profiles ready${NC}" || echo -e "  ${YELLOW}⚠️  Default profile not found${NC}"

# ─── STEP 2: Directories ───
echo ""
echo -e "${YELLOW}━━━ STEP 2/5: Project Directories ━━━${NC}"
mkdir -p "$PROJECT_DIR"/{content,Content_Calendar,leads,fda_alerts,pharmacy,videos/{raw,transcripts,processed},images/{headers,carousels,stats,reels,quotes,leads},dashboard,reports,affiliates,subscribers,cron}
cat > "$PROJECT_DIR/dashboard/metrics.json" << 'EOF'
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
EOF
echo -e "  ${GREEN}✅ Directories + dashboard initialized${NC}"

# ─── STEP 3: Verify Skills ───
echo ""
echo -e "${YELLOW}━━━ STEP 3/5: Skill Verification ━━━${NC}"

SKILLS=(
    "peptide_content_operator" "content_scheduler" "lead_sniper"
    "lead_followup" "nurserob_dashboard_manager" "cron_orchestrator"
    "content_batch_generator" "image_generator" "fda_monitor"
    "video_repurposer" "nurserob_onboarding" "pharmacy_scout"
    "pharmacy_outreach_automator" "nurserob_affiliate_manager" "nurserob_analytics"
)

INSTALLED=0
for skill in "${SKILLS[@]}"; do
    if hermes skills list 2>/dev/null | grep -q "$skill"; then
        echo -e "  ${GREEN}✅${NC} $skill"
        ((INSTALLED++))
    else
        echo -e "  ${YELLOW}⚠️${NC}  $skill — NOT FOUND (create via skill_manage or Appendix A)"
    fi
done
echo -e "  Skills present: ${INSTALLED}/15"

# ─── STEP 4: Create Cron Jobs (correct CLI syntax) ───
echo ""
echo -e "${YELLOW}━━━ STEP 4/5: Creating 15 Cron Jobs ━━━${NC}"

# DAILY
hermes cron create "0 7 * * *" "Generate today's 3 Nurse Rob peptide posts using creative-mode. Save to ~/NurseRob_PeptideEmpire/content/YYYY-MM-DD_posts.md. Push to content_scheduler." --name "Daily Content Generation" --skill "peptide_content_operator" --skill "image_generator" 2>/dev/null && echo -e "  ${GREEN}✅${NC} Daily Content Generation" || echo -e "  ${YELLOW}⚠️${NC}  Daily Content Gen (may exist)"

hermes cron create "55 7 * * *" "Push morning post (8AM MST) from today's content file to X via xurl." --name "Schedule Morning Post" --skill "content_scheduler" 2>/dev/null && echo -e "  ${GREEN}✅${NC} Schedule Morning Post" || echo -e "  ${YELLOW}⚠️${NC}  Morning Post (may exist)"

hermes cron create "55 11 * * *" "Push midday post (12PM MST) from today's content file to X." --name "Schedule Midday Post" --skill "content_scheduler" 2>/dev/null && echo -e "  ${GREEN}✅${NC} Schedule Midday Post" || echo -e "  ${YELLOW}⚠️${NC}  Midday Post (may exist)"

hermes cron create "55 16 * * *" "Push evening post (5PM MST) from today's content file to X." --name "Schedule Evening Post" --skill "content_scheduler" 2>/dev/null && echo -e "  ${GREEN}✅${NC} Schedule Evening Post" || echo -e "  ${YELLOW}⚠️${NC}  Evening Post (may exist)"

hermes cron create "0 6 * * *" "Scan X and Discord for peptide questions. Auto-reply to hot leads. Push warm leads to lead_followup." --name "Lead Scan Morning" --skill "lead_sniper" 2>/dev/null && echo -e "  ${GREEN}✅${NC} Lead Scan Morning" || echo -e "  ${YELLOW}⚠️${NC}  Lead Scan AM (may exist)"

hermes cron create "0 12 * * *" "Scan X and Discord for peptide questions. Auto-reply to hot leads." --name "Lead Scan Midday" --skill "lead_sniper" 2>/dev/null && echo -e "  ${GREEN}✅${NC} Lead Scan Midday" || echo -e "  ${YELLOW}⚠️${NC}  Lead Scan Midday (may exist)"

hermes cron create "0 18 * * *" "Scan X and Discord for peptide questions. Auto-reply to hot leads." --name "Lead Scan Evening" --skill "lead_sniper" 2>/dev/null && echo -e "  ${GREEN}✅${NC} Lead Scan Evening" || echo -e "  ${YELLOW}⚠️${NC}  Lead Scan Eve (may exist)"

hermes cron create "0 0 * * *" "Scan X and Discord for peptide questions. Lower priority overnight capture." --name "Lead Scan Overnight" --skill "lead_sniper" 2>/dev/null && echo -e "  ${GREEN}✅${NC} Lead Scan Overnight" || echo -e "  ${YELLOW}⚠️${NC}  Lead Scan Night (may exist)"

hermes cron create "0 10 * * *" "Check nurture tracker at ~/NurseRob_PeptideEmpire/leads/nurture_tracker.json. Send due follow-up messages per the 5-step sequence (Day 0/2/5/9/14)." --name "Lead Nurture AM" --skill "lead_followup" 2>/dev/null && echo -e "  ${GREEN}✅${NC} Lead Nurture AM" || echo -e "  ${YELLOW}⚠️${NC}  Lead Nurture (may exist)"

hermes cron create "0 21 * * *" "Generate daily dashboard summary. Update all metrics from today's activity across content, leads, and revenue." --name "Dashboard Daily Summary" --skill "nurserob_dashboard_manager" 2>/dev/null && echo -e "  ${GREEN}✅${NC} Dashboard Daily Summary" || echo -e "  ${YELLOW}⚠️${NC}  Dashboard Summary (may exist)"

# WEEKLY
hermes cron create "0 8 * * 1" "Run weekly FDA peptide/GLP-1 scan. Search FDA compounding, warning letters, drug shortages, and PCAC. Generate alert report. Save to ~/NurseRob_PeptideEmpire/fda_alerts/." --name "FDA Weekly Scan" --skill "fda_monitor" 2>/dev/null && echo -e "  ${GREEN}✅${NC} FDA Weekly Scan" || echo -e "  ${YELLOW}⚠️${NC}  FDA Weekly (may exist)"

hermes cron create "0 10 * * 2" "Check pharmacy outreach pipeline. Send due emails per the 5-email sequence (Intro Day 0, Value Day 3, Proposal Day 7, Case Study Day 14, Final Day 21). Update outreach tracker." --name "Pharmacy Outreach Weekly" --skill "pharmacy_outreach_automator" 2>/dev/null && echo -e "  ${GREEN}✅${NC} Pharmacy Outreach Weekly" || echo -e "  ${YELLOW}⚠️${NC}  Pharmacy Outreach (may exist)"

hermes cron create "0 9 * * 3" "Run compounding pharmacy discovery and verification. Search for GLP-1, BPC-157, NAD+ compounding pharmacies. Verify licenses and PCAB accreditation. Push new verified pharmacies to pharmacy_outreach_automator." --name "Pharmacy Scout Biweekly" --skill "pharmacy_scout" 2>/dev/null && echo -e "  ${GREEN}✅${NC} Pharmacy Scout Biweekly" || echo -e "  ${YELLOW}⚠️${NC}  Pharmacy Scout (may exist)"

hermes cron create "0 17 * * 0" "Check all affiliate links, clicks, and conversions. Update dashboard with revenue estimates by partner and category." --name "Affiliate Weekly Report" --skill "nurserob_affiliate_manager" 2>/dev/null && echo -e "  ${GREEN}✅${NC} Affiliate Weekly Report" || echo -e "  ${YELLOW}⚠️${NC}  Affiliate Report (may exist)"

hermes cron create "0 18 * * 0" "Generate comprehensive weekly performance report covering content, leads, revenue, pharmacy pipeline, and automation health. Save to ~/NurseRob_PeptideEmpire/reports/weekly_report_[date].md. Push summary to dashboard." --name "Weekly Analytics Report" --skill "nurserob_analytics" 2>/dev/null && echo -e "  ${GREEN}✅${NC} Weekly Analytics Report" || echo -e "  ${YELLOW}⚠️${NC}  Weekly Analytics (may exist)"

# MONTHLY
hermes cron create "0 8 1 * *" "Generate full 30-day content calendar for the new month using creative-mode profile. Research trending peptide topics. Produce 90 posts (3 per day) with text, image prompts, CTAs, and disclaimers. Save to ~/NurseRob_PeptideEmpire/Content_Calendar/30_Day_Calendar_[MONTH].md." --name "Monthly Content Batch" --skill "content_batch_generator" --skill "image_generator" 2>/dev/null && echo -e "  ${GREEN}✅${NC} Monthly Content Batch" || echo -e "  ${YELLOW}⚠️${NC}  Monthly Batch (may exist)"

# ─── STEP 5: Verification ───
echo ""
echo -e "${YELLOW}━━━ STEP 5/5: Final Verification ━━━${NC}"

CRON_COUNT=$(hermes cron list 2>/dev/null | grep -cE "Daily Content|Schedule|Lead Scan|Lead Nurture|Dashboard Daily|FDA Weekly|Pharmacy|Affiliate Weekly|Weekly Analytics|Monthly Content" || echo "0")
echo -e "  Cron jobs created: ${CRON_COUNT}/15"
echo ""

echo -e "${GREEN}╔════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  🏥 SETUP COMPLETE — $(date '+%Y-%m-%d %H:%M %Z')                               ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  📁 Project:  ~/NurseRob_PeptideEmpire"
echo -e "  📊 Dashboard: Load nurserob_dashboard_manager → 'show dashboard'"
echo -e "  📝 Next:     Load content_batch_generator → 'generate next 30 days'"
echo ""