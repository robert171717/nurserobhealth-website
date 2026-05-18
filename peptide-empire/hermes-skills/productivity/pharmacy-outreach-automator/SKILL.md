---
name: pharmacy-outreach-automator
description: Full automated email outreach sequences for compounding pharmacies - v1.1 Email #1 rewritten with direct affiliate ask after v1.0 vague language caused confused pharmacy responses
version: 1.1
author: Nurse Rob
---

# Pharmacy Outreach Automator 📧

**Purpose:** Manages the complete compounding pharmacy outreach pipeline — receives verified pharmacies from pharmacy-scout and runs automated 5-email sequence with tracking and partner management.

## TRIGGER
- New pharmacies pushed from pharmacy-scout
- Weekly cron: Tuesday 10:00 AM MST (check pipeline, send due emails)
- Manual: "check pharmacy outreach" / "send pharmacy emails"

## PROFILE ROUTING
Use `default` (deepseek-v4-pro) — professional business tone.

## OUTREACH PIPELINE STAGES
| Stage | Status | Next Action |
|-------|--------|-------------|
| 0 | NEW | Research + prepare intro |
| 1 | INTRO_SENT | Email #1 sent — wait 3 days |
| 2 | VALUE_SENT | Email #2 sent — wait 3 days |
| 3 | PROPOSAL_SENT | Email #3 sent — wait 7 days |
| 4 | CASE_STUDY_SENT | Email #4 sent — wait 7 days |
| 5 | FINAL_SENT | Email #5 sent — wait 14 days |
| 6 | FOLLOW_UP_DONE | Move to quarterly check-in or closed |
| 9 | PARTNER | Active partner — manage relationship |
| 99 | DECLINED | Closed — quarterly check-in |

## 5-EMAIL SEQUENCE

### Email #1: Introduction — DIRECT Affiliate Ask (Day 0)

⚠️ **CRITICAL:** Do NOT use vague partnership language ("explore a partnership," "work together"). Pharmacies receive these emails constantly and will respond confused or not at all. The affiliate ask must be in the FIRST paragraph. Pharmacies need to know exactly what you want within 10 seconds of opening the email.

```
Subject: Affiliate inquiry — Nurse Rob, RN sends educated peptide users your way

Hi [Pharmacy Name] team,

I'm Nurse Rob — a licensed RN who educates peptide users on safety,
dosing, and sourcing. My audience constantly asks: "Where do I get
quality compounded peptides from a pharmacy I can trust?"

I want to send them to you — through an affiliate partnership.

Here's the simple setup I'm proposing:
• You give me a unique tracking link or affiliate code
• I recommend [Pharmacy Name] when my audience asks where to go
• You fulfill the prescriptions — I earn a commission on referred sales
• Typical rate in this space is 15-20%, tracked monthly

I picked [Pharmacy Name] because [specific reason — PCAB accreditation,
testing transparency, GLP-1 expertise, peptide page, etc.]. I don't
recommend pharmacies I haven't personally vetted.

Would you be open to a 10-minute call to discuss structure?

Nurse Rob, RN
nurse@nurserobhealth.com
@NurseRobHealth on X
```

**Why this template works (contrast with failed v1.0):**
- The affiliate ask is in **sentence three** (v1.0 buried it in Email #3, a full week later)
- Pharmacy knows exactly what's being proposed (affiliate tracking link, 15-20% commission)
- They see what's in it for them: educated customers they didn't pay to acquire
- It's 3 short paragraphs — skimmable in 15 seconds
- The specific compliment ("PCAB accreditation") proves you actually researched them

### Email #2: Value Add (Day 3)
```
Subject: What your potential patients are asking me about peptides

Hi [Contact Name],

Following up on my previous note. 

I thought it might be valuable to share what I'm hearing from 
the peptide community — these are questions your future patients 
are asking right now:

1. "Is my compounding pharmacy actually 503B certified?"
2. "What testing does this pharmacy do on their peptides?"
3. "How do I know the dosing is accurate?"

As a nurse, I help them understand what to look for. And when 
they're ready to move forward, I want to point them to a 
pharmacy I trust.

I think [Pharmacy Name] fits that profile — especially because 
of [specific strength].

Open to a quick chat?

- Nurse Rob, RN
```

### Email #3: Partnership Proposal (Day 7)
```
Subject: A potential partnership structure

Hi [Contact Name],

I've put together a few ways we could work together:

1. AFFILIATE PARTNERSHIP (15-20%)
   • I send educated patients → you fulfill
   • Tracked via unique link/code
   • Monthly reporting

2. SPONSORED EDUCATION (flat rate)
   • I create clinical content featuring your pharmacy
   • Thread/post/video with Nurse Rob's clinical lens
   • Full disclaimers + compliance

3. CO-BRANDED PATIENT EDUCATION
   • "How to Read Your Peptide Label" guides
   • Injection technique videos
   • Safety protocol checklists

I'm flexible on structure — let's find what works for both of us.

Can we schedule a 15-minute call this week?

- Nurse Rob, RN

⚠️ All content includes appropriate disclaimers. All partnerships 
are educational in nature, not medical endorsements.
```

### Email #4: Case Study (Day 14)
```
Subject: Real results from peptide education

Hi [Contact Name],

Wanted to share something that highlights why I do this work.

Recently, someone came to me confused about their peptide protocol. 
They had [common issue] and didn't know [basic safety step].

After going through my educational materials, they:
✓ Understood proper dosing
✓ Identified a potential interaction they'd missed
✓ Found a reputable pharmacy (this could be you)

This is the gap I fill — clinical education between the patient 
and the pharmacy. 

If you're open to exploring how we can work together, I'd love 
to connect.

- Nurse Rob, RN
```

### Email #5: Final Follow-Up (Day 21)
```
Subject: Last note from me

Hi [Contact Name],

I've reached out a few times about potential partnership — 
completely understand if the timing isn't right.

My door stays open. If things change or you want to explore 
this later, just reply to this email.

In the meantime, I'll continue educating peptide users on safety 
and best practices. If [Pharmacy Name] ever wants to collaborate 
on patient education, I'm here.

All the best,
Nurse Rob, RN
```

## WORKFLOW

### Step 1: Load Pharmacy Database
Read `~/NurseRob_PeptideEmpire/pharmacy/pharmacy_database.json`
Filter pharmacies with status "NEW" — these need Email #1.

### Step 2: Send Due Emails
For each pharmacy at a stage where next email is due:
- Generate personalized email using template
- Personalize with: pharmacy name, specific strength, contact name
- Send via `himalaya` CLI configured at `~/.config/himalaya/config.toml`
- Sending address: `Nurse Rob, RN <nurse@nurserobhealth.com>`
- Email send command:
```bash
cat << 'EOF' | himalaya template send
From: Nurse Rob, RN <nurse@nurserobhealth.com>
To: [pharmacy_email]
Subject: [subject]
[body]
--
Nurse Rob, RN | nurse@nurserobhealth.com | nurserobhealth.com
EOF
```

### Step 2b: Handle Contact Form Pharmacies
⚠️ Many compounding pharmacies only expose contact forms — no direct email.
When `contact_channel` is `"contact_form"` and `email` is `null`:
- Do NOT skip them. Mark as `status: "needs_manual"` in outreach_tracker.json
- Set `next_action` to: `"⚠️ MANUAL: Submit Intro Email via contact form at [URL]. Phone: [phone] as backup."`
- Include the contact form URL and phone number so Nurse Rob can copy-paste the template
- Update the pharmacy_database.json `status` field to `"CONTACT_FORM_REQUIRED"` (not OUTREACH_STAGE_1)
- Count these pharmacies under `pharmacy.needs_manual` in dashboard metrics
- These pharmacies still need manual outreach — the pipeline tracks them separately from emailed ones

### Step 2c: Overdue Pipeline Handling
When the cron fires and `next_action_date` is in the past (pipeline sat idle):
- Send ONLY the next pending stage — never batch-send multiple stages at once (defeats the drip sequence purpose)
- Set the new `next_action_date` relative to TODAY, not the original schedule
- Example: If Stage 1 was due April 29 but today is May 5, send Stage 1 NOW and set Stage 2 due May 8 (today + 3 days)

### Step 3: Update Pipeline
Save to: `~/NurseRob_PeptideEmpire/pharmacy/outreach_tracker.json`
```json
{
  "pharmacy_id": "pharm_001",
  "name": "ABC Compounding",
  "current_stage": 2,
  "stage_history": [
    {"stage": 1, "sent": "2026-04-27", "template": "intro"},
    {"stage": 2, "sent": "2026-04-30", "template": "value_add"}
  ],
  "contact_name": "John Smith",
  "contact_email": "john@abcpharmacy.com",
  "responded": false,
  "response_notes": "",
  "partner_status": null,
  "revenue_generated": 0
}
```

### Step 4: Handle Responses
- **Positive reply** → Mark as NEGOTIATING, flag for Nurse Rob review
- **"Not interested"** → Mark as DECLINED, move to quarterly check-in
- **Question** → Answer professionally, advance to next stage
- **No response** → Continue sequence per schedule

### Step 5: Partner Onboarding (When PARTNER status)
- Generate unique affiliate code/link
- Add to nurserob-affiliate-manager tracking
- Schedule monthly partner check-in
- Update dashboard with new partner count

### Step 6: Update Dashboard
Call `nurserob-dashboard-manager`:
"Pharmacy outreach: [X] emails sent, [Y] negotiating, [Z] new partners"

## PITFALLS
- Never imply Nurse Rob can prescribe or dispense
- Don't claim to have patients — say "audience" or "the people I educate"
- Maintain professional boundaries — RN is educator, not sales rep
- Track opt-outs and never email them again
- **VAGUE LANGUAGE IN EMAIL #1 = CONFUSED RESPONSES:** The original v1.0 Email #1 used "explore a partnership" without specifying affiliate, and buried the actual ask in Email #3. Result: pharmacies responded confused because they didn't know what was being asked. The affiliate type, commission range, and value prop must be in the FIRST paragraph of Email #1. See the rewritten template (v1.1).
- Keep affiliate terms vague until real negotiation with Nurse Rob
- **Contact form pharmacies**: Do NOT skip or fail silently. Mark as `needs_manual` with the contact form URL and phone number. These are often the highest-scored pharmacies — Empower, CRE8, FarmaKeio were all 10/10 score with no direct email.
- **Overdue pipeline**: If `next_action_date` is in the past (e.g., pipeline sat idle between scout and first cron run), send only the NEXT pending stage. Never batch-send Stage 1+2+3 all at once — it defeats the drip sequence. Set future dates relative to TODAY.
- **Dashboard staleness**: Before reporting "himalaya not installed" or similar blocker, verify with `which himalaya && himalaya --version`. The dashboard's cron_status.pharmacy_outreach field may carry stale data from a prior run — always update it to reflect current reality.
- **Metrics file**: Use `execute_code` with `subprocess.run(['cat', path])` for reading/writing dashboard metrics.json — NOT `read_file`/`write_file` hermes tools (they return line-numbered content that breaks `json.loads()`).

## QUALITY CHECKLIST
- [ ] Each email personalized (not generic blast)
- [ ] Pharmacy-specific details included
- [ ] All emails include Nurse Rob RN signature
- [ ] Outreach tracker updated after each action
- [ ] Responses flagged for Nurse Rob review
- [ ] New partners onboarded to affiliate system
- [ ] Dashboard metrics updated
