# X API Free Tier Reply Restriction

## Symptom

`xurl reply` returns:
```json
{
  "detail": "Reply to this conversation is not allowed because you have not been mentioned or otherwise engaged by the author of the post you are replying to.",
  "type": "about:blank",
  "title": "Forbidden",
  "status": 403
}
```

Exit code: 1

## Cause

X API v2 Free/Basic tier enforces conversation attribution. You can ONLY reply to:

1. **Posts that mention your account** — even if you're not the OP, if the post contains @yourhandle, you're in the conversation.
2. **Your own posts** — any reply in a thread you started.
3. **Posts in conversations you're already part of** — once you've replied in a thread, you can continue replying.

You CANNOT reply to:
- A random user's post that doesn't mention you
- A thread you've never participated in
- A post in a conversation where your account has zero presence

This is NOT a bug — it's working as designed on Free/Basic tier. The X API Pro/Enterprise tiers may have different rules.

## Workaround — Public Mention Posts

Instead of `xurl reply POST_ID "text"`, use:

```bash
xurl post "@username Great question! Here's what the research shows..."
```

This creates a NEW tweet (not a reply) that:
- Contains an @mention of the target user
- Shows up in their notifications tab
- Is visible to your followers as a regular tweet
- Has NO threading connection to the original post

**Limitations:**
- The target user does NOT get a reply notification — just a mention notification
- The tweet does NOT appear under the original conversation
- Lower engagement rate than a direct reply
- The user may not associate the mention with their original question

**When direct reply works:**
- Target user replies to one of your posts → you're now in the conversation
- Target user mentions @NurseRobHealth in their post
- You're replying in your own thread

## Verified: Nurse Rob Setup (May 12, 2026)

- OAuth2 tokens valid (xurl auth shows `(no credentials)` display quirk but API calls work)
- Both apps tested: `default` (NurseRobHealth) and `nurse-rob`
- Both returned identical 403 on `xurl reply`
- Workaround confirmed working: `xurl post` with @mentions succeeded
- Post IDs created via mention workaround: 2054186128794620194, 2054186170813190198, 2054186177704448396
- All three mention posts are visible on @NurseRobHealth's timeline
