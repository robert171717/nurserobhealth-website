---
name: website-prompt-engineering
description: Craft specifications-grade prompts for AI code-generation models (GPT-5.5, Claude) to produce premium single-page websites. Iterative refinement from rough vision → pixel-perfect spec.
version: 1.0
author: Nurse Rob
---

# Website Prompt Engineering

Craft and iteratively refine prompts that will be fed to code-generation AI models (GPT-5.5 via Codex, Claude, etc.) to produce premium single-page websites. The skill's output is the **prompt itself** — not the website.

## When To Use

- User has a rough idea for a website and wants a prompt to feed to GPT-5.5/Codex
- User asks "improve this prompt for a better website"
- User wants to iterate on a website prompt through multiple refinement rounds
- User says "make this prompt more detailed/specific/effective"
- User is building a single-page site for a professional brand (healthcare, consulting, SaaS)

**Not for:** Actually building the website yourself — use `claude-design` or `codex` for that. This skill produces the prompt that another AI consumes.

## Relationship to Other Skills

| Skill | What It Does |
|-------|-------------|
| `website-prompt-engineering` (this) | Crafts the prompt → feeds to another AI |
| `claude-design` | Hermes IS the designer → builds HTML directly |
| `popular-web-designs` | Visual vocabulary from known brands (Stripe, Linear, etc.) |
| `codex` | The GPT-5.5-powered code generation agent that consumes the prompt |

## Prompt Structure — The 4-Element Framework

Every production-grade prompt should include these four elements in order:

### 1. Quick Reference Card (Top)
A condensed summary card placed right after the role priming. Contains: brand name, tagline, domain, email, color hexes, fonts, section order, disclaimers, and output format. This gives the model a complete mental model before diving into details — prevents models from getting lost in long prompts.

Format:
```
Brand:    Name | domain.com | email@domain.com
Tagline:  "..."
Aesthetic: ReferenceSites — clinical-luxury, zero template energy
Primary:  navy-900 #XXXXXX | Teal #XXXXXX | Gold #XXXXXX
Fonts:    Inter (400-800) + Mono (400)
Structure: Nav → Hero → Section → ... → Footer
Disclaimers: ① Section A  ② Section B  ③ Footer
Hero:     Specs...
Output:   ONE HTML file, no preamble, DOCTYPE first, /html last
```

### 2. Priority Tiers (After Rules + Quick Reference)
If the prompt is long, tell the model what to prioritize. Uses a 3-tier system:

| Tier | What | Consequence if Missed |
|------|------|-----------------------|
| **TIER 1** | Critical Rules, Hero canvas/visuals, Disclaimers, Section headings, Output format | **FAIL** — site is broken or unbranded |
| **TIER 2** | Exact color hexes, typography scale, responsive breakpoints, form behavior | Degraded — site looks off |
| **TIER 3** | Scroll animations, exact testimonial text, mobile menu polish, OG tags | Acceptable — minor polish missing |

Also add a fallback instruction immediately after the Quick Reference Card: *"If the prompt feels overwhelming, prioritize in this order: 1. Critical Rules + Tier 1 items, 2. Hero section, 3. Primary content sections (Services + Lead Magnet), 4. Footer + Disclaimers."* Placing this early — right after the condensed summary — catches the model before it gets lost in the long spec.

### 3. Full Section Specifications (Middle)
All the pixel-level detail — colors, typography, section-by-section specs, Canvas pseudocode, interactions. This is the bulk of the prompt. See the "3-Round Refinement Workflow" below for how to build this.

### 4. GPT Self-Check (Bottom)
A verification checklist at the end of the prompt that forces the model to confirm every requirement before outputting. Organized by tier. Models respond well to this — it catches 80% of missed items.

Format:
```
TIER 1 (FAIL IF MISSING):
□ One file: starts <!DOCTYPE html>, ends </html>? No preamble?
□ Hero canvas animating? Particles visible? Mouse works? Mobile count reduced?
□ Disclaimer #1 on [section]? #2 on [section]? #3 full text in Footer?
□ All section headings match exact text?

TIER 2 (DEGRADED IF MISSING):
□ Exact hex colors used? Typography correct at desktop + mobile?
□ Responsive: 375px stacked? 768px? 1440px two-column?
□ Form shows success state?

TIER 3 (POLISH):
□ Scroll animations working? Testimonial text exact?
□ ARIA labels present? OG tags, favicon, Schema.org?
```

## External AI Feedback Loop (Meta-Pattern)

For critical prompts, use a 3-pass refinement loop with an external AI grader:

1. **Round 1:** Build initial prompt with color system, typography, section specs. Feed to grader.
2. **Round 2:** Add pixel-level specs, Canvas/JS pseudocode, ASCII layout diagrams. Grader scores ~9.3/10.
3. **Round 3:** Add Priority Tiers, Quick Reference Card, GPT Self-Check, "if overwhelmed" instruction. Grader scores ~9.6-9.8/10.

The goal is not perfection — it's preventing the model from missing Tier 1 items. The final polish items (Tier 3) have diminishing returns.

## 3-Round Refinement Workflow
Take a rough prompt and add:
- Full color palette with exact hex values and usage rules
- Typography system (headings, body, monospace — weights, sizes, line heights)
- Page structure (section ordering, layout decisions)
- Reference aesthetic (name 2-3 sites the output should evoke)
- Technical constraints (single file, Tailwind CDN, vanilla JS)

### Round 2: Pixel-Level Specification
Make every section buildable without guesswork:
- **ASCII layout diagrams** for each section showing exact element placement
- **Exact copy** for headings, subheadlines, CTAs — no placeholder text like "add your headline here"
- **CSS specifications** for special elements (glassmorphism nav, particle canvas, cards)
- **Interaction specifications** — hover states, transitions, scroll behaviors, mobile menu behavior
- **Canvas/JS pseudocode** if the design includes procedural elements (particles, animations). Include actual JavaScript code snippets (initParticles, animate, mouse tracking, touch support, debounce). Don't just describe — show the model exactly how to implement it. This is the #1 failure point in AI-generated websites — descriptive specs produce broken canvases; pseudocode produces working ones.

### Round 3: Production Hardening
Add everything needed for a real deployment:
- Tailwind config with custom colors, fonts, animations
- `<head>` meta tags (title, description, OG, Twitter card, favicon)
- Schema.org markup (commented)
- Accessibility checklist (WCAG 2.1 AA)
- Performance targets
- Responsive breakpoint specifications
- Form behavior (success states, validation)
- SEO tags
- Exact verification instructions for the output

## Key Principles

### Be Exacting, Not Vague
❌ "Use a nice blue" → ✅ "Teal #00C4B4 for CTAs and accents"
❌ "Professional typography" → ✅ "Inter 800 at 4.5rem, tracking-tight, line-height 1.05"
❌ "Make it look premium" → ✅ "Reference aesthetic: Levels Health, InsideTracker, Parsley Health"

### Specify Non-Negotiables
- Disclaimers (healthcare: must be in 3+ locations)
- Legal requirements
- Brand elements that cannot be changed
- Technical constraints (single file, no frameworks)

### Use Structure That AI Models Follow Well
- Numbered sections with exact headings
- Code blocks for color tokens, Tailwind config, CSS
- ASCII diagrams for layout (models parse spatial instructions from ASCII well)
- Checklists at the end (models respond well to checklist verification)

### Reference Real Examples
Name 2-3 real websites the output should reference. This anchors the model's aesthetic sense better than abstract descriptions.

## Voice and Framing for the Prompt

The prompt should tell the model:
1. **Who they are:** "You are an elite web designer..." (role priming)
2. **What the output must feel like:** "indistinguishable from a $15,000-$20,000 custom agency build"
3. **Exactly what success looks like:** A visitor thinks X, Y, Z within 3 seconds
4. **The first and last line rule:** Output starts with `<!DOCTYPE html>`, ends with `</html>`, nothing else
5. **Anti-patterns — explicitly tell it what NOT to do:** Add an "ANTI-PATTERNS — DO NOT DO THESE" section with 6-8 specific prohibitions (e.g., "Do not use CSS background-image for hero — must be Canvas with JS", "Do not use <br> for spacing", "Do not hardcode pixel widths — use grid utilities", "Do not skip the skip-to-content link"). Models perform significantly better with negative constraints alongside positive ones. This reduces common failure modes by ~30%.

## Canvas/Pseudocode: The 5-Block Format

When the design includes procedural elements (particle canvas, WebGL, complex animations), format the implementation spec as numbered, self-contained blocks — not a single wall of code:

```
1. Initialize — canvas setup, context, particle array, resize handler
2. Create — particle factory function with count, properties, randomization
3. Animate — requestAnimationFrame loop: clear, update, draw, connect
4. Mouse/Touch — event listeners with getBoundingClientRect positioning
5. Utilities — debounce, throttle, or other helper functions
```

Each block should be small enough that it cannot fail independently. If the model messes up block 3, blocks 1, 2, 4, and 5 still work. This is significantly more effective than describing the animation in prose or dumping a single monolithic code block. Include actual working JavaScript within each block — do not just describe the behavior.

## Common Patterns

### Healthcare Professional Site
- Must have: credentials display, disclaimer in 3+ places, trust signals, booking integration
- Color: dark navy + single vibrant accent (teal/blue) + gold warmth sparingly
- Tone: clinical authority without coldness, genuine care

### SaaS Landing Page
- Must have: hero with product visual, feature grid, pricing, social proof, CTA
- Color: often dark theme with gradient accents
- Tone: confident, clear, benefit-driven

### Personal Brand / Consulting
- Must have: about section with story, services with pricing, testimonials, contact
- Color: clean with warmth signals
- Tone: approachable authority

## Pitfalls
- Don't build the website — build the prompt. The output is markdown text, not HTML.
- Don't stop at one round of improvement. The first pass adds structure, the second adds precision.
- Don't leave placeholder text like "[Your headline here]" — write the actual copy.
- Don't skip the Canvas/JS specs if the design calls for procedural elements.
- Don't forget accessibility, SEO, meta tags, and responsive behavior in the final round.

## Quality Checklist
- [ ] Color palette has exact hex values with usage rules
- [ ] Typography specifies fonts, weights, sizes, line heights for mobile+desktop
- [ ] Every section has an ASCII layout diagram or exact element specification
- [ ] All copy is actual text, not placeholders
- [ ] Interactive elements have behavior specifications (hover, transition, scroll)
- [ ] Technical constraints clearly stated (single file, Tailwind CDN, vanilla JS)
- [ ] Accessibility requirements specified (WCAG level, contrast, focus, semantic HTML)
- [ ] Output instructions are exact (first line, last line, no preamble)
- [ ] Reference aesthetic named (2-3 real sites)
- [ ] Non-negotiables listed (disclaimers, legal, brand lock)
