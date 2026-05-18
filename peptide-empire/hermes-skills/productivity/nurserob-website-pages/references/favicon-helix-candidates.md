# Favicon Helix Candidates — Nurse Rob

Generated May 17, 2026. All 5 use navy #0A1F3F bg with rounded rectangle container (rx=18). Designed to read at 16×16, 24×24, and 32×32 favicon sizes.

## V1 — Diagonal Flow
Sweeping diagonal with depth shadow (second strand at lower opacity).
```
viewBox="0 0 100 100"
Background: rect 100×100 rx=18 fill=#0A1F3F
Strand 1 (front): path M18 88 Q40 70 50 50 Q60 30 82 12, stroke=#C9A84C 2.5px
Strand 2 (back): path M12 92 Q38 72 48 52 Q58 32 88 10, stroke=#C9A84C 1.2px opacity=0.5
Nodes: 4 circles r=1.8 at (28,74), (41,58), (54,42), (67,26)
```

## V2 — 3D Twist
Classic sine-wave vertical helix with faint rung lines for depth.
```
viewBox="0 0 100 100"
Background: rect 100×100 rx=18 fill=#0A1F3F
Strand 1 (left wave): path M25 5 Q55 30 25 55 Q-5 80 25 100, stroke=#C9A84C 3.5px round
Strand 2 (right wave): path M75 5 Q45 30 75 55 Q105 80 75 100, stroke=#C9A84C 1.5px opacity=0.5
Rungs: lines at y=20 (x30→70), y=45 (x28→72), y=70 (x30→70), stroke=#C9A84C 2px opacity=0.4
```

## V3 — Minimal Elegant
Two interlocking simple curves, no rungs. Clean luxury aesthetic.
```
viewBox="0 0 100 100"
Background: rect 100×100 rx=18 fill=#0A1F3F
Curve 1: path M30 12 Q60 40 30 68, stroke=#C9A84C 3px round
Curve 2: path M70 88 Q40 60 70 32, stroke=#C9A84C 3px round
Accent nodes: circles at (36,30) and (64,70) r=2
```

## V4 — Bold Premium
Thick dominant front strand with thin back strand. Center node.
```
viewBox="0 0 100 100"
Background: rect 100×100 rx=18 fill=#0A1F3F
Front: path M22 90 Q48 70 50 50 Q52 30 78 10, stroke=#C9A84C 4px round
Back: path M78 90 Q52 70 50 50 Q48 30 22 10, stroke=#C9A84C 1.5px round
Center: circle cx=50 cy=50 r=3 fill=#C9A84C
```

## V5 — Dual Color
Teal + gold interlocking strands. The user's full brand palette in one icon.
```
viewBox="0 0 100 100"
Background: rect 100×100 rx=18 fill=#0A1F3F
Gold strand: path M22 90 Q45 70 48 50 Q52 30 78 10, stroke=#C9A84C 3px round
Teal strand: path M78 90 Q55 70 52 50 Q48 30 22 10, stroke=#00C4B4 3px round
Center dot: circle cx=50 cy=50 r=2.5 fill=#FFFFFF opacity=0.9
```

## Preview Pattern
To let the user compare, build an HTML file with a grid of cards. Each card shows the SVG at 16px, 24px, 32px, plus a Google search result mockup (favicon circle + fake title/URL/description). Save to `Desktop/Daily Brief/NurseRob_PeptideEmpire/favicon-*.html`.

## Iterative Design Process (learned May 17, 2026)

The user went through 6 rounds of favicon iteration. Key lessons:

1. **User rejects flat/ladder designs.** DNA helix must have overlapping sine-wave curves with depth illusion. Flat horizontal rungs look like "construction ladders" — rejected immediately.
2. **User wants diagonal flow.** Bottom-left to top-right. Use `transform="rotate(45 50 50)"` on existing paths rather than rewriting the curve math — preserves the exact look the user already approved.
3. **User wants visible rungs.** White connecting lines or dots between strands, at 55-80% opacity. The word "rungs" resonated — use it.
4. **User iteration pattern:** Show 5 → get feedback → show 5 improved → get feedback → show 10 variations → narrow → pick. Budget 4-6 rounds for visual design tasks.
5. **Pitfall: don't change the path structure when rotating.** When the user says "I like B1 and B5 but make them diagonal", use SVG transform rotate, don't recompute the bezier curves. Recomputed paths lose the character the user approved.

## WINNER: E8 — B5 Dual-Color, 3 Twist Cycles, Diagonal (Deployed May 17, 2026)

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="16" fill="#0A1F3F"/>
  <g transform="rotate(45 50 50)">
    <path d="M25 5 Q55 15 30 30 Q5 45 30 55 Q55 65 30 80 Q5 95 30 100" fill="none" stroke="#00C4B4" stroke-width="4" stroke-linecap="round"/>
    <path d="M75 95 Q45 85 70 70 Q95 55 70 45 Q45 35 70 20 Q95 5 70 0" fill="none" stroke="#C9A84C" stroke-width="4" stroke-linecap="round"/>
    <line x1="34" y1="18" x2="66" y2="22" stroke="#FFFFFF" stroke-width="1.5" opacity="0.55" stroke-linecap="round"/>
    <line x1="28" y1="38" x2="68" y2="42" stroke="#FFFFFF" stroke-width="1.5" opacity="0.55" stroke-linecap="round"/>
    <line x1="34" y1="58" x2="66" y2="62" stroke="#FFFFFF" stroke-width="1.5" opacity="0.55" stroke-linecap="round"/>
  </g>
</svg>
```

Characteristics: navy #0A1F3F rounded rect (rx=16), teal #00C4B4 front strand, gold #C9A84C back strand, both equal 4px weight, 3 full sine-wave cycles, 3 white rung lines at 55% opacity, rotated 45° clockwise. Deployed to all 10 site pages as `/favicon.svg`.

## Deployment

Save final design as `favicon.svg` in website root. Bulk-update all HTML pages:
```bash
cd /mnt/c/Users/Robert/Desktop/nurserobhealth-website
for f in *.html; do
  sed -i 's|<link rel="icon".*type="image/svg+xml".*>|<link rel="icon" type="image/svg+xml" href="/favicon.svg">|g' "$f"
done
git add . && git commit -m "🧬 New favicon" && git push
```
Vercel auto-deploys. Google takes days to weeks to update favicon in search results.
