# GSC OAuth Consent Screen — Navigation Dead-End

## Problem
When the user navigates to **APIs & Services → OAuth consent screen**, Google Cloud sometimes redirects to the **Overview/metrics tab** instead of the consent configuration screen. This happens when the consent screen was already configured and Google defaults to showing metrics.

## What the User Sees
- "OAuth overview" page with empty metrics
- Tabs: Overview, Branding, Audience, Clients, Data Access, Verification Center, Settings
- No obvious "Test users" section visible

## Solution
Click the **Audience** tab — this is where the Test users section lives. It's not on the Overview tab.

## Navigation Path (from memory)
1. ☰ menu → APIs & Services → OAuth consent screen
2. If you land on Overview/metrics, click **Audience** tab
3. Scroll down past "Publishing status" and "User type" → **Test users** section
4. **+ ADD USERS** → type email → **SAVE** (may need to click SAVE twice — Google UI quirk)

## Alternative Path (if OAuth consent screen link is dead)
If clicking "OAuth consent screen" in the nav does nothing:
1. Go to **APIs & Services → Credentials** first
2. Click **+ CREATE CREDENTIALS → OAuth client ID**
3. Google will prompt "You must first configure your consent screen" with a link
4. Click that link — it takes you directly to the consent configuration (not the metrics overview)
