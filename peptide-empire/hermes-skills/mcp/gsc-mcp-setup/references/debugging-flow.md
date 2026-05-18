# GSC MCP Auth Debugging Flow (2026-05-13)

## The Full Error Chain (and what fixed it)

### Attempt 1: Public OAuth (Path B)
```
Error: "Access blocked: Hermes GSC has not completed the Google verification process"
```
- Used `suganthan-gsc-mcp`'s published OAuth credentials
- Google blocked it — no "Advanced" link available
- **Verdict:** Public OAuth path is dead for new users. Don't even try.

### Attempt 2: Service Account (Path A)
1. Created `nurserob-gsc` Cloud project ✓
2. Enabled Search Console API ✓
3. Created `hermes-gsc` service account + downloaded JSON key ✓
4. Verified domain via DNS TXT record at Porkbun ✓
5. Attempted to add service account email to GSC: **FAILED**
   ```
   Failed to add user: email address not found
   ```
6. Tested: service account IS valid (got 200 on OAuth token, listed APIs)
7. But GSC web UI's user directory hadn't indexed it yet
8. Also tested different site URL formats (sc-domain vs https://) — didn't matter
9. **Verdict:** Service account works but propagation delay makes it unusable for same-day setup

### Attempt 3: Own-Project OAuth (Path C) ✅
1. Same Cloud project (`nurserob-gsc`) — API already enabled
2. Configured OAuth consent screen (app name, email, skip scopes)
3. Created Desktop OAuth client ID → downloaded JSON
4. Flipped Hermes config to OAuth with own credentials
5. First attempt: `Access blocked: Hermes GSC has not completed the Google verification process. Error 403, access denied.` — missing test user!
6. Added self as test user (hit SAVE twice — Google UI quirk) → **RESOLVED**
7. **Verdict:** Works. ~4 minutes. The missing test-user step is the trap. Key distinction: the 403 \"access denied\" on Path C means test user not added (fixable). The same-looking block on Path B means Google permablocks the public app (unfixable).

### Bonus: Sitemap Submission OAuth Scope Trap
- Domain properties (`sc-domain:*`) don't support Sitemaps API at all — even with Manage scope
- URL-prefix properties do, but require **both** checkboxes during OAuth consent: "View" AND "Manage"
- If you only checked "View" during initial OAuth → sitemap calls fail with \"Insufficient Permission\"
- Fix: clear OAuth cache and re-auth with both scopes, OR submit sitemap manually in GSC web UI (10 seconds)

## Key Insight

Google has tightened OAuth enforcement. The traps are:
1. Public OAuth apps get fully blocked (no "Advanced" escape hatch anymore)
2. Own-project OAuth requires test-user self-addition (easy to miss)
3. Google OAuth console sometimes ignores first SAVE click on test users — hit SAVE twice
4. IAM notification ("Grant principals access") during setup is a red herring — ignore it
5. Brand new GSC properties return all zeros — use inspect_url to verify, not site_snapshot

Path C + test user (with double-save) = the only reliable fast path as of May 2026.

## DNS: Porkbun TXT Record

```
Type: TXT
Host: @ (or blank)
Value: google-site-verification=<string>
```
Porkbun: Domain Management → domain → DNS → + ADD RECORD → TXT
