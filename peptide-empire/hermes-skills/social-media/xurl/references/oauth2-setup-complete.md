# xurl OAuth2 — Complete Setup Flow (Portal → First Post)

Step-by-step from zero to posting. Every pitfall we hit on 2026-05-10 is encoded.

## Portal Setup (developer.x.com)

1. **Create Project + App** at https://developer.x.com/en/portal/dashboard
2. **User Authentication Settings:**
   - App Type: **"Web App, Automated App or Bot"** — NOT "Native App" (Native App causes `unauthorized_client` OAuth errors)
   - Permissions: **Read and Write**
   - Redirect URI: `http://localhost:8080/callback` (http, not https)
3. **Save** → Keys & Tokens → Copy Client ID and Client Secret
4. **Move to Production:** Dashboard → Manage → "Pay-per-use" package → Production environment. This fixes `client-forbidden` errors. API keys/tokens stay the same — no regeneration needed.

## Terminal Setup (xurl CLI)

### Register the app
```bash
xurl auth apps add nurse-rob \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_CLIENT_SECRET
```

### Authenticate (CRITICAL: --app is NOT optional)
```bash
xurl auth oauth2 --app nurse-rob NurseRobHealth
```
**Without `--app nurse-rob`**, the OAuth token lands on the empty `default` profile (no client-id/secret), and every command returns 401. This is the #1 setup mistake.

Browser opens → authorize → tokens saved. If `UsernameNotFound` or 403 on `/2/users/me` right after OAuth, pass your handle explicitly (xurl v1.1.0+ handles this automatically with the third argument above).

### Set default + verify
```bash
xurl auth default nurse-rob
xurl whoami
```
Expected: JSON with `"username":"NurseRobHealth"` and your profile data.

## Traps We Hit (2026-05-10 Session)

| Trap | Symptom | Fix |
|---|---|---|
| `--app` omitted from `auth oauth2` | 401 on everything despite successful OAuth flow | Re-run with `--app nurse-rob` |
| App type = "Native App" | `unauthorized_client` during OAuth browser flow | Change to "Web App, Automated App or Bot" |
| Wrong Client ID used in `auth apps add` | OAuth flow succeeds but tokens don't match | Use the ID from Keys & Tokens tab (ends in `MTpjaQ`) |
| `xurl auth app --access-token ...` | `unknown flag: --access-token` — this flag does not exist | Only OAuth2 browser flow or `--bearer-token` for app-only auth |
| App stuck in Development | 401 on `whoami` even with valid OAuth | Move to Production (Pay-per-use) in portal |
| Two "Client Secret" values in portal | UI shows two — first is actually Client ID | Confirm on Keys and Tokens page |
| `xurl auth oauth2 NurseRobHealth` (no `--app`) | Token on wrong profile, 401s | Re-run with `--app nurse-rob` |

## First Post Test
```bash
xurl post "Test post from Nurse Rob Peptide Empire 🧬"
```

## Thread Posting Pattern
```bash
xurl post "🧵 Opener tweet"
xurl reply TWEET_ID "1/ First thread tweet"
xurl reply TWEET_ID "2/ Second thread tweet"
# ... chain each reply to the previous tweet ID
```
