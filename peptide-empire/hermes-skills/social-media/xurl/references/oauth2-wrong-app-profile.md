# xurl OAuth2 Token on Wrong App Profile — Diagnosis & Fix

## Symptom
- `xurl auth oauth2 --app nurse-rob` says "OAuth2 authentication successful!"
- But `xurl whoami` returns 401 Unauthorized
- `xurl auth status` shows token on `default` app (no client_id), not on `nurse-rob`

## Root Cause
xurl's OAuth2 flow stores the token on whatever app is current. If the `default` app
is active (even though it has no client_id/secret), the token lands there instead of
the named app. The `default` app has `(no credentials)` so the token can never
validate — every request gets 401.

This happens when: the user never set a default app before authenticating, OR the
X API's `/2/users/me` call fails during OAuth (common with newer X API enrollments),
causing xurl to fail to resolve the username.

## Diagnosis Commands
```bash
# Shows which app has the token
xurl auth status
```

**Bad output** — token on `default` (no client_id):
```
▸ default  [(no credentials)]
      oauth2: NurseRobHealth       ← token HERE, but no app creds
  nurse-rob  [client_id: aW5iVFJT…]
      oauth2: (none)               ← app has creds, but no token
```

**Good output** — token on `nurse-rob`:
```
  default  [(no credentials)]
      oauth2: NurseRobHealth
▸ nurse-rob  [client_id: aW5iVFJT…]
      oauth2: NurseRobHealth       ← token AND app creds together
```

## Fix Sequence
```bash
# Step 1: Authenticate with explicit username (binds token to app)
xurl auth oauth2 --app nurse-rob NurseRobHealth
# Opens browser → log in to X → "OAuth2 authentication successful!"

# Step 2: Set as default (may already be done, verify with auth status)
xurl auth default nurse-rob

# Step 3: Verify
xurl whoami
# Should return user data JSON with 200, not 401
```

## Why `--app` + Username Matters
Without the username argument, xurl calls `/2/users/me` to resolve it. On newer X API
enrollments (post-2024), this call frequently fails with 403 or UsernameNotFound.
When it fails, the token gets stored but isn't bound to a username, causing 401 on
all subsequent calls. Passing the handle explicitly skips this broken API call.

## The "Wrong Fix" Trap
If you see the token on `default`, do NOT try to move it manually. There is no
CLI flag to import OAuth2 tokens. The ONLY way to get the token onto the correct
app is `xurl auth oauth2 --app <app-name> <username>`. Browser flow is mandatory.
