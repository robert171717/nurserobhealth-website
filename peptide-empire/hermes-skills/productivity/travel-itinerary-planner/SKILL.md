---
description: "Plan complete solo trips with budget constraints, flight search, hotels, dining, and activities"
name: "travel-itinerary-planner"
---

# Travel Itinerary Planner

## Purpose
Plan complete solo trips with budget constraints, including flight search, hotel booking, daily schedules, and dietary-specific restaurant recommendations.

## Prerequisites
- `curl` available (no Playwright required)
- Python with regex module
- web_search tool access

## Workflow

### 1. Flight Search Strategy

**Primary Method: curl + KAYAK scraping + web_search verification**
```python
import subprocess
import re
import time

# Search format: kayak.com/flights/ORIG/DEST/DEPART_DATE/RETURN_DATE
url = "https://www.kayak.com/flights/MOA/PDX/2026-05-28/2026-05-31"

result = subprocess.run(
    ['curl', '-s', '-A', 'Mozilla/5.0', '-L', '--max-time', '10', url],
    capture_output=True, timeout=15
)

# CRITICAL: Decode bytes to string (handles encoding errors)
content = result.stdout.decode('utf-8', errors='ignore')

# Extract prices
prices = re.findall(r'\$([\d,]+)', content)
prices = [int(p.replace(',', '')) for p in prices if p.replace(',', '').isdigit()]

# Filter realistic round-trip prices (avoid noise)
flight_prices = [p for p in prices if 150 <= p <= 800]
```

**⚠️ CRITICAL: Verify actual flight times, not just prices!**
- Scraped prices don't include departure/arrival times
- Use web_search to verify: "Alaska Airlines PHX PDX flight schedule June 2026"
- Check specific requirements: "depart before 9 AM", "arrive 8-10 PM"
- Verify on flightaware.com or airline schedules
- Example: AS 746 departs PDX 6:21 PM, arrives PHX 9:00 PM (perfect for 8-10 PM window)
- WRONG: 11:25 PM arrival doesn't meet 8-10 PM constraint

**⚠️ CRITICAL: Search for specific airline schedules for return windows!**
- If user requires arrival between 8-10 PM, search: "PDX to PHX evening flight schedule 6pm 7pm 8pm arrival 8pm 9pm 10pm"
- Southwest often has better evening departures (6:30-7:00 PM PDX → 9:00-9:45 PM PHX)
- Alaska Airlines: Search "AS flight PDX PHX schedule departure times arrival times"
- Flight duration: ~2.5 hours non-stop for PHX-PDX
- **CRITICAL: Calculate arrival time properly!**
  - Example: 6:45 PM PDX departure + 2.5h flight = 9:15 PM PHX arrival ✅ (within 8-10 PM window)
  - Example: 9:00 PM PDX departure + 2.5h = 11:30 PM PHX ❌ (outside 8-10 PM window)
  - Account for time zone changes if applicable (Pacific vs Mountain time)
- Verify on flightaware.com or airline schedules
- Example: AS 746 departs PDX 6:21 PM, arrives PHX 9:00 PM (perfect for 8-10 PM window)
- WRONG: 11:25 PM arrival doesn't meet 8-10 PM constraint

**Key Insights:**
- KAYAK works better than Skyscanner (less JS, faster)
- Average fetch time: 1.5s per route
- PHX vs AZA: PHX has more options, same price
- Alaska Airlines dominates PHX-PDX routes
- **Always cross-reference times with web_search**

### 2. Hotel Search

**Method: web_search + cross-reference multiple sources**
```python
from hermes_tools import web_search
result = web_search("Portland Oregon hotel Pearl District June 2026 prices per night", limit=5)
```

**⚠️ CRITICAL: Verify hotel names, cities, and ratings!**
- Search specific hotel names: "Cambria Hotel Portland Pearl District rates June 2026"
- Cross-reference: KAYAK, Expedia, Booking.com, TripAdvisor
- **DON'T trust single source lowball prices** (e.g., $67/night Pearl District is unrealistic)
- Real Pearl District mid-range: $82-115/night in 2026
- **CRITICAL: Verify hotel CITY!** Hotel 1000 is in SEATTLE, not Portland - search "Hotel Name [City]" to confirm location
- Search: "Hotel Name Portland Oregon address" to verify city
- Common mistake: Hotel names can exist in multiple cities (Hotel 1000 = Seattle, NOT Portland!)
- **NEVER assume** - always verify with web_search before including in itinerary
- **Users may want higher-rated hotels:** Research boutique/4-star options proactively
  - Search: "Portland Oregon best boutique hotels 2026 highly rated 4 star"
  - Search: "best rated hotels Pearl District Portland 2026 reviews"
  - Cross-reference ratings: TripAdvisor, Yelp, Google Reviews
  - Example upscale options: Canopy by Hilton (9.0★, $160-175/night), The Hoxton (boutique, $160-190/night), The Benson (4★, $170-200/night)

**Target Areas:**
- Pearl District (walkable, safe, central) - $80-120/night realistic
- Downtown (near MAX light rail) - $70-100/night
- Old Town (historic, budget-friendly) - $60-90/night

**Budget Targets (REALISTIC 2026):**
- Budget: $70-90/night
- Mid-range: $90-130/night
- Luxury: $150+/night

### 3. Budget Allocation Template

**⚠️ PROVIDE MULTIPLE BUDGET OPTIONS WHEN APPROPRIATE**
- If user requests multiple budgets (e.g., $1000, $1200, $1400), provide COMPLETE separate itineraries for each
- Each budget should have different hotel tiers, food options, and activity levels
- Show clear trade-offs between budget levels
- Example structure:
  - **$1000 Budget**: Budget hotel, self-catered breakfasts, limited activities
  - **$1200 Budget**: Mid-range hotel, mix of restaurants, some paid attractions
  - **$1400+ Budget**: Boutique/4-star hotel, all restaurants, premium activities
- Always be transparent about tight budgets and what compromises are needed

**Budget Allocation Template:**
```
FLIGHTS         XX% (25-30% of budget)
HOTEL           XX% (30-40% of budget)
FOOD            XX% (20-25% of budget)
TRANSPORT       XX% (10% of budget)
ACTIVITIES      XX% (5-10% of budget)
BUFFER          XX% (5-10% contingency)
```

**Example $1000 Budget:**
- Flights: $235 (24%)
- Hotel 4 nights: $268 (27%)
- Food 4 days: $240 (24%)
- Transport: $85 (9%)
- Activities: $38 (4%)
- Buffer: $142 (14%)

**⚠️ BUDGET TRANSPARENCY: Always be honest about tight budgets!**
- If budget is tight (within $200 of realistic cost), say so upfront
- Provide TWO budgets:
  1. **Ideal Budget** - realistic costs with good options
  2. **Budget Mode** - specific trade-offs to meet target
- Show exact savings from each adjustment
- Example: "Cambria Hotel vs Motel 6: -$120 savings"
- Don't hide that $1000 is tight for 4 nights + flights + food
- User can always add budget, but hiding reality wastes their time

### 4. Dietary Restrictions (GF + Soy-Free)

**Search Strategy: Search for BOTH restrictions explicitly**
```python
from hermes_tools import web_search
# WRONG: "gluten free restaurants Portland"
# RIGHT: "Portland Oregon gluten free soy free restaurants 2026"
result = web_search("Portland Oregon gluten free soy free restaurants best rated 2026", limit=5)
```

**⚠️ CRITICAL: Specificity matters!**
- "Gluten-free" ≠ "Gluten-free AND soy-free"
- Soy is common in Asian cuisine, sauces, marinades
- Search for dedicated GF kitchens (safest)
- Verify menu items explicitly mention soy-free options

**Restaurant Verification Checklist:**
- [ ] Dedicated GF kitchen (best - no cross-contamination)
- [ ] 100% GF menu (like Mestizo Portland, Bastion PDX)
- [ ] GF menu items clearly marked
- [ ] Soy-free explicitly mentioned or confirmed
- [ ] Multiple reviews mentioning GF + soy-free success
- [ ] Rating 4.5+ on Yelp/FindMeGlutenFree

**Example Verified Restaurants (Portland 2026):**
- **Bastion PDX**: 100% GF, dairy-free, soy-free, refined sugar-free
- **Mestizo**: 100% GF AND soy-free Mexican (2910 SE Division)
- **Kirari West**: Dedicated GF cafe (Japanese-inspired)
- **Honey Butter Country Fare**: Dedicated GF food cart (carnival food)

### 5. Activity Planning

**Nature Hikes:**
- Search: "[Destination] easy beginner hikes day trip 2026"
- Target: <2 miles, <500 ft elevation gain
- Parking fees: $10-20 (note Northwest Pass for Columbia Gorge)
- **⚠️ CRITICAL: Check for timed-entry permits!**
  - Multnomah Falls: $2 timed entry permit REQUIRED (May 22 - Sept 7, 2026)
  - Reserve EXACTLY 30 days in advance at recreation.gov (permits sell out)
  - Permit time slots: 9:00 AM - 6:00 PM daily
  - Permit is for PARKING only, not hiking (hiking itself is free)
  - Set calendar reminder for permit booking date
  - Popular hikes often require advance reservations
  - Search: "[Trail name] timed entry permit 2026"

**Free Attractions:**
- Public parks
- Walking tours
- Free museums (check schedules)
- Streetcar/metro (often free in Portland)

### 6. Common Pitfalls

**❌ DON'T:**
- Use web_extract on JS-heavy sites (Skyscanner times out)
- Trust all scraped prices (filter for realistic ranges)
- Forget to decode bytes to string in curl output
- Book flights last minute (prices rise)
- Assume hotel breakfast is included (check!)
- Forget timed-entry permits (Multnomah Falls $2 parking permit required May-Sept, book exactly 30 days ahead at recreation.gov - permit is for PARKING only, hiking is free)
- Assume hotel city without verifying (Hotel 1000 is in Seattle, NOT Portland!)
- Skip browser tool if Playwright fails - use web_search as primary, browser as backup

**✅ DO:**
- Use curl for direct HTML scraping
- Search multiple airports (PHX vs AZA)
- Include transport costs (airport shuttles, Uber, parking)
- Build 10-15% buffer into budget
- Verify dietary options with restaurants directly
- **Browser fallback:** If browser_navigate fails (Playwright not installed), rely on multiple web_search queries with specific terms
- Cross-reference 3+ sources for any critical info (hotels, flight times)

### 7. Output Format

Use visual formatting for readability:
```
══════════════════════════════════════════════
╔═══════════════════════════════════════════╗
║       ✈️  TRIP NAME - COMPLETE PLAN      ║
╚═══════════════════════════════════════════╝
══════════════════════════════════════════════

**📊 BUDGET SUMMARY**
┌─────────────────────────────────────────────┐
│  Flights          $XXX                      │
│  Hotel (N nights) $XXX                      │
└─────────────────────────────────────────────┘
```

### 8. Tools Checklist

- [ ] curl (system command)
- [ ] Python subprocess + re modules
- [ ] web_search tool
- [ ] web_extract (for simple pages)
- [ ] Browser tool (backup for complex sites)

### 9. Performance Notes

- Average flight search: 1.5s per route
- 5-10 route comparisons: 10-15 seconds total
- Hotel search: 2-3 seconds
- Restaurant search: 2-3 seconds
- Total planning time: 2-5 minutes for complete itinerary

## Example Use Cases
- Weekend getaways ($500-1500 budget)
- Multi-city tours (compare 3-5 destinations)
- Dietary-restricted travel (GF, vegan, allergies)
- Nature-focused trips (hiking, parks)
- Foodie tours (restaurant hopping)
