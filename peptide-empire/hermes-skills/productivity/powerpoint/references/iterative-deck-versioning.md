# Iterative Deck Versioning Pattern

## When This Matters

When a presentation goes through 3+ revisions with a user who:
- Manually tweaks slides in PowerPoint between versions
- Adds personal media (photos) that must be preserved
- Requests precise content corrections (numbers, rates, timeline)
- Needs each version saved separately for comparison/showing

## Versioning Convention

```
Cybercab_Family_Deck_v1.pptx    # Initial draft
Cybercab_Family_Deck_v2.pptx    # After text/rate corrections
Cybercab_Family_Deck_v3.pptx    # After layout fixes (overlaps)
Cybercab_Family_Deck_v4_HERO.pptx  # After adding hero GIF
Cybercab_Family_Deck_v5_EXIT.pptx  # After adding exit strategy
Cybercab_Family_Deck_v6_ROBOTAXI.pptx  # After adding external graphic
Cybercab_Family_Deck_v7_FINAL.pptx  # After final number corrections
```

Rule: `{Project}_{DeckName}_v{N}_{CHANGE_SUMMARY}.pptx`

## Change Tracking Per Version

After each version, summarize to the user exactly what changed and what was preserved:

```
### v6 → v7
- Slide 4: Loan amount updated ($35k→$40k), payment ($420→$515)
- Slide 7: Added two-phase electricity subtitle (E-28 home / commercial lot)
- Preserved: family photo, hero GIF, robotaxi graphic, all 18 slides
```

This prevents the user from having to re-check the entire deck after each change.

## When to Rebuild vs. Edit

| Change Type | Approach | Why |
|-------------|----------|-----|
| Text content only | XML surgery or JS edit + regen | Either works; JS edit is cleaner |
| Number updates | JS edit + regen | Safer, no risk of partial updates |
| Coordinate fixes (overlaps) | JS edit + regen | MUST rebuild — too many dependent xfrms |
| Adding slides | JS edit + regen | Must shift all slide numbers |
| User-added media preserved | Rebuild from JS with photo extracted from previous PPTX | Only way to keep their custom additions |
| Minor PowerPoint tweaks | User does them manually, then we extract for next rebuild | Don't fight PowerPoint, work with it |

## The Extraction → Rebuild Loop

When the user makes manual tweaks in PowerPoint (photo position, text edits):

1. Extract their modified media from the PPTX (images, GIFs)
2. Read their slide content to identify what they changed
3. Update the JS source accordingly
4. Regenerate with their media embedded
5. Tell them what was preserved and what changed

This keeps the JS source as the canonical version while respecting their manual edits.
