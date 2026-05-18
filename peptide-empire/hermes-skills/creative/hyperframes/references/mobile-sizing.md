# Mobile-First Sizing for HyperFrames Compositions

## The Problem

HyperFrames compositions render at 1920×1080 by default. On a 4-5" smartphone screen, every element appears at roughly 1/8 scale — text becomes illegible, icons become specks, and users must "squint to even read the words."

## The Rule

**All text, icons, cards, and visual elements must be 50-75% larger than what looks comfortable on a desktop monitor.**

## Sizing Guidelines

| Element Class | Desktop-Default | Mobile-Safe |
|--------------|-----------------|-------------|
| Hero title (e.g., "BPC-157") | 120-160px | 200-260px |
| Section labels | 40-56px | 72-76px |
| Subtitle / body text | 24-32px | 46-48px |
| Body copy / descriptions | 14-18px | 22-26px |
| Fact/stat numbers | 60-80px | 110-140px |
| Card minimum dimensions | 260×200 | 350×270 |
| Step markers / small icons | 40-48px | 56-64px |
| Mechanism icon rings | 80-120px | 160px |
| SVGs | 48×48 viewBox | 64×64 to 80×110 rendered |
| CTA buttons | 36px text, 14px padding | 48px text, 18px padding |
| Gold line dividers | 120px wide | 180-320px |
| Branding bar | 14-16px | 20px |
| Card gaps | 48px | 60-100px |

## Verification

After rendering, extract a frame at midpoint and check at 25% zoom (simulates phone):
```bash
ffmpeg -i final.mp4 -ss 00:00:30 -vframes 1 preview.png
```

The "squint test": can you read every word without leaning in? If not, keep scaling up.
