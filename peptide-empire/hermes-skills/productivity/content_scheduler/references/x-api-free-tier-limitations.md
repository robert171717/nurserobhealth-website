# X API Free Tier Limitations & Cost Optimization

**Verified May 17, 2026.**

## Media Attachment (Blocked)

| Operation | Free Tier | Basic ($100/mo) |
|---|---|---|
| Upload media | ✅ Works | ✅ |
| Attach media to tweet | ❌ "Your media IDs are invalid" | ✅ |
| Post text-only | ✅ | ✅ |
| Reply in threads | ✅ | ✅ |

**Flag correction:** xurl uses `--media-id` (not `--media`). Even with the correct flag, free tier rejects media_ids.

**Workflow:** Images auto-generate to `Desktop\Daily Brief\NurseRob_PeptideEmpire\images\`. The content_scheduler posts text-only. User manually attaches images from Desktop via X app. Thread images go on the opener tweet; single-post images go on the post itself. To replace: delete the text-only reply, re-post with image attached.

## Verification Cost Optimization

**Before (expensive):**
- `xurl search "from:NurseRobHealth [text]"` for every post verification
- 3 retries with escalating specificity for search index propagation
- ~10-15 Read requests/day

**After (cheap):**
- Trust `xurl post` response (returns post_id on success — that IS verification)
- `xurl get [post_id]` as cheap fallback (1 request)
- Thread verification via single conversation_id lookup
- ~2-4 requests/day

**Savings: ~$0.10-0.15/day on Read requests.**

## Lead Sniper Optimization

Cut from 4x/day to 2x/day (6AM + 12PM). Evening and overnight paused.
- Savings: ~$0.15-0.20/day
- Can scale back up when traffic/leads increase

## Daily Cost Projection

| Before | After |
|---|---|
| ~$1.17/day | ~$0.80-0.90/day |
| ~$35/month | ~$24-27/month |
| 35% of $100 free tier | 24-27% of $100 free tier |

## GSC Indexing API Limitation

The Indexing API requires a service account with Owner access in GSC. The service account `hermes-gsc@nurserob-gsc.iam.gserviceaccount.com` exists but GSC rejects it with "email address not found." OAuth works for read access only.

**Workaround:** Use GSC UI URL Inspection tool (manual, 30 sec per URL) or sitemap resubmission. Pages will be discovered naturally via sitemap over days/weeks.
