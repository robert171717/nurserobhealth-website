---
description: Audit available Hermes skills and map them to a project's needs, prioritizing improvements by impact, time savings, and implementation effort. Use when asked to review how skills can improve a project, optimize workflows, or identify automation opportunities.
name: project-skill-audit
trigger: audit skills for project, review skills for, how can skills improve, skill gap analysis, project optimization
---

# Project Skill Audit Guide

## When to Use
- User asks how skills can improve their project
- After updating Hermes, user wants to leverage new capabilities
- Project is stalled or needs automation
- User wants to identify time/money savings opportunities

## Audit Workflow

### Step 1: Discover Project Structure
```bash
# List project files
find /path/to/project -type f -name "*.md" -o -name "*.json" -o -name "*.yaml"

# Read key files (dashboard, README, plan, etc.)
read_file /path/to/project/DASHBOARD.md
read_file /path/to/project/README.md
```

### Step 2: List All Available Skills
```
skills_list()  # Returns all 130+ skills with descriptions
```

### Step 3: Categorize Skills by Relevance
Group skills into these categories:

**Directly Applicable** (already exist for this project type):
- Skills that match the project's domain (content, research, outreach, etc.)
- Skills already referenced in project docs

**Newly Available** (never used before):
- Skills added since project creation
- Skills in categories not previously considered

**Underutilized** (exist but not fully leveraged):
- Skills partially implemented
- Skills that could be automated via cronjob/webhook

### Step 4: Map Skills to Project Needs
For each skill, answer:
1. **What problem does it solve?** (specific to this project)
2. **How much time does it save?** (hours/week)
3. **What cost does it replace?** (tools, VA, freelancers)
4. **Implementation effort?** (low/medium/high)
5. **Dependencies?** (API keys, accounts, setup required)

### Step 5: Prioritize Improvements
Use this framework:

**HIGH IMPACT** (Implement first):
- Saves 5+ hours/week OR replaces $100+/mo cost
- Low implementation effort (< 30 minutes)
- No external dependencies

**MEDIUM IMPACT** (Implement next):
- Saves 2-5 hours/week OR replaces $50-100/mo cost
- Medium implementation effort (1-2 hours)
- Some dependencies required

**LOW IMPACT** (Implement later):
- Saves < 2 hours/week
- High implementation effort
- Multiple dependencies or complex setup

### Step 6: Generate Action Plan
Structure output as:

```
## IMMEDIATE ACTION PLAN (Priority Order)

**This Week:**
1. [Action] - [Skill] - [Expected outcome]
2. [Action] - [Skill] - [Expected outcome]

**Next Week:**
3. [Action] - [Skill] - [Expected outcome]
4. [Action] - [Skill] - [Expected outcome]

**Month 1:**
5. [Action] - [Skill] - [Expected outcome]
6. [Action] - [Skill] - [Expected outcome]
```

### Step 7: Quantify Savings
Create a table:
```
| Automation | Time Saved/Week | Cost Saved |
|------------|----------------|------------|
| [Item]     | [X] hrs        | $[Y]/mo    |
| **TOTAL**  | **[Z] hrs/week** | **$[W]/mo** |
```

## Key Skills to Always Check

### Automation
- `cronjob` - Scheduled tasks (daily/weekly/monthly)
- `webhook-subscriptions` - Event-driven workflows
- `peptide-content-operator` - Domain-specific content generation
- `content-batch-generator` - Bulk content creation

### Research
- `fda-monitor` - Regulatory monitoring
- `arxiv` - Academic papers
- `blogwatcher` - Blog/feed monitoring
- `youtube-content` - Competitor video analysis
- `llm-wiki` - Knowledge base building

### Creative
- `baoyu-infographic` - Professional infographics
- `baoyu-comic` - Educational comics
- `manim-video` - Technical animations
- `architecture-diagram` - SVG diagrams
- `inference-sh-cli` - AI image/video generation

### Social/Communication
- `xitter` / `xurl` - X/Twitter automation
- `himalaya` - Email management
- `notion` - Notion integration
- `google-workspace` - Gmail/Calendar/Drive/Sheets
- `lead-sniper` - Lead capture automation

### Data/Analysis
- `jupyter-live-kernel` - Interactive Python analysis
- `polymarket` - Market data
- `domain-intel` - Competitor intelligence

## Output Format

Always provide:
1. **Current project structure** (brief overview)
2. **High-impact improvements** (ready now)
3. **New creative capabilities** (never before available)
4. **Research/intelligence upgrades**
5. **Social media automation**
6. **Advanced automation** (webhooks, cronjobs)
7. **Immediate action plan** (prioritized timeline)
8. **Time/cost savings table**
9. **Next steps question** (ask user what to implement first)

## Pitfalls

- **Don't overwhelm**: Limit to top 10-15 recommendations max
- **Always quantify**: Every recommendation needs time/cost savings
- **Check dependencies**: Note what accounts/API keys are needed
- **Respect existing work**: Build on what's already done, don't restart
- **Prioritize automation**: Focus on skills that reduce manual work
- **Domain-specific first**: Always check for domain-specific skills before generic ones

## Example Use Cases

- "How can new skills improve my [project name]?"
- "Audit my project and suggest skill-based improvements"
- "What skills should I use for [project type]?"
- "After updating Hermes, what's new that helps my project?"
- "Find automation opportunities in my workflow"
