---
name: nurserob-onboarding
description: Automated welcome sequence for new Nurse Rob subscribers — lead magnet delivery, trust building, and consult funnel in 5 emails
version: 1.0
author: Nurse Rob
---

# NurseRob Onboarding 🎉

**Purpose:** Welcomes new email subscribers with automated 5-email sequence delivering the Wolverine Stack Calculator lead magnet, building RN credibility, and warming toward consult.

## TRIGGER
- New email subscriber (ConvertKit/Beehiiv webhook or manual add)
- Manual: "send welcome sequence to [email]"

## PROFILE ROUTING
Use `default` (deepseek-v4-pro) — warm, welcoming tone.

## 5-EMAIL WELCOME SEQUENCE

### Email 1: Lead Magnet Delivery (Immediate)
```
Subject: Your Wolverine Stack Calculator is here 🧬

Welcome to the Nurse Rob peptide community! 🏥

Your Wolverine Stack Calculator + Guide is attached.

Here's what's inside:
📊 Personalized stack calculator (input your goals → get your protocol)
📚 12-page guide covering BPC-157, TB-500, and stacking
💉 RN injection tips you won't find on Reddit
⚠️ Safety protocols every peptide user needs

Quick intro: I'm Nurse Rob, a licensed RN who got tired of watching 
people inject things without understanding them. I read the research 
so you don't have to.

Over the next few days, I'll share some of the most important things 
I've learned as a nurse in the peptide space.

Talk soon,
Nurse Rob, RN

⚠️ Educational content from a licensed RN. Not medical advice.
```

### Email 2: Trust Builder — RN Credibility (Day 2)
```
Subject: Why an RN is different from a "biohacking guru"

Hey [name],

Quick question — when was the last time a "biohacking influencer" 
showed you their actual credentials?

Here's what I bring as a licensed RN:

🏥 Clinical training in pharmacology, physiology, and patient safety
📋 Experience reading actual research — not just abstracts
⚠️ A professional obligation to put your safety first
🩺 Real hospital experience seeing what happens when things go wrong

I'm not here to sell you peptides. I'm here to help you understand 
them — safely.

That means:
• I'll tell you what the research ACTUALLY says (even when it's not exciting)
• I'll flag risks that influencers skip over
• I'll admit when the data is thin

In tomorrow's email: the #1 mistake I see peptide users make.

- Nurse Rob, RN

⚠️ Educational content. Not medical advice.
```

### Email 3: Pain Point + Solution (Day 4)
```
Subject: The #1 mistake peptide users make

Hey [name],

After reviewing hundreds of peptide protocols, here's the pattern:

Most people have NO IDEA what their blood work means.

They're injecting BPC-157, TB-500, Ipamorelin... but they've never 
checked:
❌ Liver enzymes (ALT/AST)
❌ Kidney function (creatinine, eGFR)
❌ Inflammatory markers (CRP)
❌ Hormone panels

As a nurse, this terrifies me.

The good news: it's fixable. I built a complete Blood Work Guide 
that tells you exactly what to test and what the results mean.

→ [Link: Peptide Safety Protocol + Blood Work Guide — $47]

No pressure. But if you're serious about doing this right, 
this guide will save you months of guessing.

- Nurse Rob, RN

⚠️ Educational. Not medical advice. Consult your physician.
```

### Email 4: Social Proof (Day 7)
```
Subject: "I finally understand my protocol"

Hey [name],

Wanted to share something cool.

Someone came to me completely confused about their peptide protocol. 
They'd been piecing together Reddit advice and YouTube videos.

After a 30-minute consult, they told me:

"I finally understand what I'm taking and WHY. As a nurse, you 
explained it better than any doctor I've talked to."

This is exactly why I do 1-on-1 peptide review sessions.

$197 for 30 minutes where we go through:
✅ Your full current stack
✅ Dosing and timing optimization
✅ Safety interactions you might be missing
✅ Blood work markers that actually matter

→ [Calendly link: Book a Peptide Consultation]

Not ready? No problem. Keep learning — the free guide is a great start.

- Nurse Rob, RN

⚠️ Educational consulting. Not medical care. No provider-patient relationship.
```

### Email 5: Community + Next Steps (Day 10)
```
Subject: What's next on your peptide journey?

Hey [name],

You've got the calculator. You've read the guides. 

Here's what your next level could look like:

🔬 DEEP DIVE: 1-on-1 Consult ($197)
→ [Calendly link]

📚 COMPREHENSIVE: Peptide Safety Protocol ($47)
→ [Purchase link]

👥 COMMUNITY: Group Coaching ($997/quarter)
Monthly group calls + private Discord
→ [Application link]

Or keep it free:
• Follow @NurseRobHealth on X for daily peptide education
• Read my free safety guides
• Stay curious and stay safe

Whatever path you choose — I'm here to help.

- Nurse Rob, RN

⚠️ Educational content from Nurse Rob, RN. Not medical advice. 
Consult your physician before starting any new regimen.
```

## WORKFLOW

### Step 1: Capture New Subscriber
When new subscriber is detected (via webhook, manual add, or ConvertKit/Beehiiv):
- Log to: `~/NurseRob_PeptideEmpire/subscribers/subscriber_log.json`
- Tag: "welcome-sequence-day-0"

### Step 2: Send Email 1 (Immediate)
Personalize with subscriber name if available.
Attach lead magnet PDF (Wolverine Stack Calculator).

### Step 3: Queue Remaining Emails
Schedule automated sends for Days 2, 4, 7, 10.
Track in subscriber JSON:
```json
{
  "email": "joe@example.com",
  "name": "Joe",
  "signup_date": "2026-04-27",
  "source": "wolverine_calculator",
  "onboarding_stage": 1,
  "emails_sent": [
    {"stage": 1, "sent": "2026-04-27T14:00:00Z"},
    {"stage": 2, "sent": "2026-04-29T10:00:00Z"}
  ],
  "opened": [1, 2],
  "clicked": [2],
  "consult_booked": false,
  "product_purchased": false
}
```

### Step 4: Track Engagement
Monitor opens, clicks, conversions.
If subscriber books consult or buys product → move to "converted" tag, adjust follow-up.

### Step 5: Update Dashboard
Call `nurserob-dashboard-manager`:
"New subscriber: [name]. List now [X]. New consult booking: [Y/N]."

## LEAD MAGNET: Wolverine Stack Calculator
File: `~/NurseRob_PeptideEmpire/assets/Wolverine_Stack_Calculator.pdf`
This is the primary lead magnet — generated separately but referenced here.

Components:
- Interactive calculator (sheets/notion embed)
- 12-page PDF guide
- RN safety tips
- Stacking protocols
- Blood work schedule
- Full disclaimers

## PITFALLS
- Don't send all 5 emails at once — respect the sequence timing
- Avoid "limited time offer" urgency — keep it educational
- Every email must have disclaimer
- Track unsubscribes immediately — remove from all lists
- Don't over-automate — this sequence should feel personal

## QUALITY CHECKLIST
- [ ] Lead magnet delivered immediately
- [ ] All 5 emails personalized with subscriber name
- [ ] Each email has clear CTA and disclaimer
- [ ] Sequence timing correct (0, 2, 4, 7, 10 days)
- [ ] Subscriber log updated after each send
- [ ] Dashboard notified of new subscribers
- [ ] Conversions tracked
