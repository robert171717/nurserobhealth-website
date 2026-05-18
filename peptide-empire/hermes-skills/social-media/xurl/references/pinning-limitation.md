# Pinning Tweets via X API

## Limitation

X API v2 does **not** expose a pin/unpin endpoint. The v1.1 endpoint `POST /1.1/account/settings.json` with `pinned_tweet_id` works but requires **OAuth 1.0a** credentials — OAuth 2.0 tokens receive 403 "You are not permitted to use OAuth2 on this endpoint."

## Pragmatic Solution

After posting the tweet via xurl, direct the user to pin it manually:
1. Open the X app
2. Go to profile
3. Find the tweet
4. Tap `···` → **Pin to profile**

This takes ~10 seconds and is the most reliable method when only OAuth 2.0 is configured.
