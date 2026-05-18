#!/bin/bash
# =============================================================================
# Nurse Rob Peptide Empire — 3-Layer Backup Script
# Runs daily at 2:30 AM MST via cron
# =============================================================================
# Layers:
#   1. LOCAL  — rsync to ~/NurseRob_PeptideEmpire/backups/daily/
#   2. USB    — rsync to /media/robert/*/NurseRob_PeptideEmpire_Backup/ (if mounted)
#   3. GITHUB — git commit + push to robert171717/nurserobhealth-website
# =============================================================================

set -e
TIMESTAMP=$(date +"%Y-%m-%d_%H%M")
LOG_FILE="/home/robert/NurseRob_PeptideEmpire/backups/backup_log.txt"
REPO_DIR="/home/robert/nurserobhealth-website"
BACKUP_DIR="/home/robert/NurseRob_PeptideEmpire/backups/daily/${TIMESTAMP}"

mkdir -p "$BACKUP_DIR"
mkdir -p "$(dirname "$LOG_FILE")"

echo "========================================" | tee -a "$LOG_FILE"
echo "BACKUP START: $(date)" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

# ============================================================
# LAYER 1: LOCAL BACKUP (always works, no dependencies)
# ============================================================
echo "" | tee -a "$LOG_FILE"
echo "[LAYER 1] Local backup..." | tee -a "$LOG_FILE"

# Backup skills
if [ -d "/home/robert/.hermes/skills" ]; then
    rsync -av --delete /home/robert/.hermes/skills/ "$BACKUP_DIR/hermes-skills/" 2>&1 | tee -a "$LOG_FILE"
    echo "  ✅ Skills backed up" | tee -a "$LOG_FILE"
else
    echo "  ⚠️ Skills directory not found" | tee -a "$LOG_FILE"
fi

# Backup empire files
if [ -d "/home/robert/NurseRob_PeptideEmpire" ]; then
    rsync -av --delete \
        --exclude='backups/daily/*' \
        --exclude='.git' \
        /home/robert/NurseRob_PeptideEmpire/ "$BACKUP_DIR/empire-files/" 2>&1 | tee -a "$LOG_FILE"
    echo "  ✅ Empire files backed up" | tee -a "$LOG_FILE"
else
    echo "  ⚠️ Empire directory not found" | tee -a "$LOG_FILE"
fi

# Backup Desktop files
DESKTOP_DIR="/mnt/c/Users/Robert/Desktop/Daily Brief/NurseRob_PeptideEmpire"
if [ -d "$DESKTOP_DIR" ]; then
    rsync -av --delete "$DESKTOP_DIR/" "$BACKUP_DIR/desktop-files/" 2>&1 | tee -a "$LOG_FILE"
    echo "  ✅ Desktop files backed up" | tee -a "$LOG_FILE"
else
    echo "  ⚠️ Desktop directory not found" | tee -a "$LOG_FILE"
fi

# ============================================================
# LAYER 2: USB BACKUP (only if USB is mounted)
# ============================================================
echo "" | tee -a "$LOG_FILE"
echo "[LAYER 2] USB backup..." | tee -a "$LOG_FILE"

USB_MOUNT=$(find /media/robert -maxdepth 2 -type d -name "NurseRob*" 2>/dev/null | head -1)
if [ -z "$USB_MOUNT" ]; then
    USB_MOUNT=$(find /mnt -maxdepth 3 -type d -name "NurseRob*" 2>/dev/null | head -1)
fi

if [ -n "$USB_MOUNT" ]; then
    USB_BACKUP_DIR="$USB_MOUNT/NurseRob_PeptideEmpire_Backup"
    mkdir -p "$USB_BACKUP_DIR"
    rsync -av --delete "$BACKUP_DIR/" "$USB_BACKUP_DIR/" 2>&1 | tee -a "$LOG_FILE"
    echo "  ✅ USB backup complete → $USB_BACKUP_DIR" | tee -a "$LOG_FILE"
else
    echo "  ⚠️ USB not mounted — skipped (no action needed)" | tee -a "$LOG_FILE"
fi

# ============================================================
# LAYER 3: GITHUB BACKUP (push to robert171717/nurserobhealth-website)
# ============================================================
echo "" | tee -a "$LOG_FILE"
echo "[LAYER 3] GitHub backup..." | tee -a "$LOG_FILE"

if [ ! -d "$REPO_DIR/.git" ]; then
    echo "  ⚠️ Repo not cloned locally. Attempting clone..." | tee -a "$LOG_FILE"
    git clone https://github.com/robert171717/nurserobhealth-website.git "$REPO_DIR" 2>&1 | tee -a "$LOG_FILE" || {
        echo "  ❌ Clone failed — GitHub layer skipped. Run: git clone https://github.com/robert171717/nurserobhealth-website.git ~/nurserobhealth-website" | tee -a "$LOG_FILE"
    }
fi

if [ -d "$REPO_DIR/.git" ]; then
    cd "$REPO_DIR"
    
    # Pull latest
    git pull origin main 2>&1 | tee -a "$LOG_FILE" || true
    
    # Create/update peptide-empire folder
    mkdir -p peptide-empire
    
    # Copy latest files into repo
    rsync -av --delete /home/robert/.hermes/skills/ peptide-empire/hermes-skills/ 2>&1 | tee -a "$LOG_FILE"
    rsync -av --delete \
        --exclude='backups/daily/*' \
        --exclude='.git' \
        /home/robert/NurseRob_PeptideEmpire/ peptide-empire/empire-files/ 2>&1 | tee -a "$LOG_FILE"
    
    # Add the backup log itself
    cp "$LOG_FILE" peptide-empire/backup_log.txt
    
    # Commit and push
    git add peptide-empire/ 2>&1 | tee -a "$LOG_FILE"
    git commit -m "Automated backup — ${TIMESTAMP} MST" 2>&1 | tee -a "$LOG_FILE" || echo "  (nothing new to commit)" | tee -a "$LOG_FILE"
    git push origin main 2>&1 | tee -a "$LOG_FILE" && echo "  ✅ GitHub push complete" | tee -a "$LOG_FILE" || echo "  ❌ Push failed — check git auth (gh auth login)" | tee -a "$LOG_FILE"
else
    echo "  ❌ GitHub layer skipped — repo unavailable" | tee -a "$LOG_FILE"
fi

# ============================================================
# CLEANUP: Keep last 7 daily backups, delete older
# ============================================================
echo "" | tee -a "$LOG_FILE"
echo "[CLEANUP] Removing backups older than 7 days..." | tee -a "$LOG_FILE"
find /home/robert/NurseRob_PeptideEmpire/backups/daily/ -maxdepth 1 -type d -mtime +7 -exec rm -rf {} \; 2>&1 | tee -a "$LOG_FILE"
echo "  ✅ Cleanup complete" | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "BACKUP COMPLETE: $(date)" | tee -a "$LOG_FILE"
echo "  Local: $BACKUP_DIR" | tee -a "$LOG_FILE"
echo "  GitHub: github.com/robert171717/nurserobhealth-website/tree/main/peptide-empire" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
