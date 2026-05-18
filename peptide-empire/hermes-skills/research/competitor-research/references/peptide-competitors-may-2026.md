# Peptide Competitors — May 2026 Research Session

## Competitors Identified (May 14, 2026 via xurl + DuckDuckGo)

### Tier 1 (100K+ followers)
| Account | Handle | Followers | Positioning |
|---|---|---|---|
| Ben Greenfield | @bengreenfield | 160,565 | NYT Bestselling Author, Podcaster, Biohacking Investor |

### Tier 2 (10K-100K followers)
| Account | Handle | Followers | Positioning |
|---|---|---|---|
| Jay Campbell | @JayCampbell333 | 37,697 | Longevity science, 6x bestselling author, co-founder @BioLongevityUSA |
| Maximus | @MaximusTribe | 11,169 | Doctor-prescribed peptide protocols for men |

### Tier 3 (1K-10K followers)
| Account | Handle | Followers | Positioning |
|---|---|---|---|
| Peptide Sciences | @PeptideScience | 7,195 | Research-grade peptide synthesis, purity-focused |
| Marek Health | @marekhealth | 4,954 | 130+ biomarkers, TRT, peptides, GLPs |
| BioLongevity Labs | @BioLongevityUSA | 1,536 | Premium peptides & bioregulators, triple tested |
| Haelo Peptides | @HaeloPeptides | — | Peptide brand |

### Tier 4 (sub-1K)
| Account | Handle | Followers | Notes |
|---|---|---|---|
| DoctorTristan | @DoctorTristan | 473 | Small account, medical angle |
| LongevityMD | @LongevityMD | 259 | Personal mission statement |
| Limitless_Life | @Limitless_Life | 207 | Different niche (not peptide) |
| corepeptides | @corepeptides | 13 | Discount codes, deal-focused |

## Nurse Rob Positioning (as of May 14, 2026)
- @NurseRobHealth: 1,246 followers, 34,215 tweets
- Key differentiator: Only licensed RN in the space doing peptide education
- 34K tweet library is years of content waiting to be repurposed
- Content is text-only on X — zero video

## Search Methodology Used
1. `xurl search "peptide therapy BPC-157" -n 20` — surfaced Ez-Peptides, AxiomLabz
2. `xurl search "BPC-157 TB-500 healing recovery peptide" -n 20` — surfaced HaeloPeptides, WellnessCd
3. `xurl search "peptide health longevity biohacking" -n 15` — surfaced biohacking crossover accounts
4. Individual `xurl user "@<account>"` lookups — verified all metrics above
5. DuckDuckGo HTML search via `curl` for web presence when Firecrawl was unavailable:
   - `curl -s -H "User-Agent: Mozilla/5.0" "https://html.duckduckgo.com/html/?q=peptide+therapy+competitors" | grep -oP "result__snippet[^>]*>\\K[^<]+"`
6. `xurl whoami` for Nurse Rob's own metrics
7. `xurl timeline -n 5` for recent activity snapshot

## Key Insights from This Session
- Nurse Rob's raw timeline was dominated by political/crypto retweets — had to filter via `xurl search "from:NurseRobHealth peptide"` to find actual original content
- `xurl whoami` returned `URL: ?` even though Rob confirmed his cal.com link was set and working — the API field is unreliable
- Firecrawl credits exhausted mid-session — DDG curl fallback still worked
- The `image_generator` skill (with underscore) didn't exist; `image-generator` (hyphen) existed with wrong branding colors
