# xAI Image Generation Setup for Hermes Agent

**As of v0.14.0+**, the `image_gen/xai` plugin is bundled but **not enabled by default**. The default backend tries FAL.ai first — fails with "FAL_KEY not set" even when xAI is configured.

## One-Time Setup

### 1. Get xAI API Key
Sign up at [console.x.ai](https://console.x.ai) → create key. Separate from X Premium — pay-per-use with no monthly subscription.

### 2. Add to Hermes
```bash
echo 'XAI_API_KEY=xai-...' >> ~/.hermes/.env
hermes plugins enable image_gen/xai          # CRITICAL — bundled but off by default
systemctl --user restart hermes-gateway
```

### 3. Verify (fresh session required)
Plugin changes need session restart. Use direct API as immediate fallback.

## Direct API Fallback (No Plugin Needed)
The xAI Imagine API is OpenAI-compatible. Works even before plugin takes effect:

```python
resp = requests.post("https://api.x.ai/v1/images/generations",
    headers={"Authorization": f"Bearer {api_key}"},
    json={"model": "grok-imagine-image", "prompt": "...", "n": 1})
url = resp.json()["data"][0]["url"]
cost_usd = resp.json()["usage"]["cost_in_usd_ticks"] / 10_000_000_000  # ~$0.02/img
```

## One Key, All APIs
Same `XAI_API_KEY` works for chat, image gen, video gen, TTS — no separate keys needed.

## Pitfalls
- **"FAL_KEY not set" error**: `image_generate` defaults to FAL. Must `hermes plugins enable image_gen/xai` + session restart.
- **X Premium ≠ xAI API**: X Premium blue check ($8/mo) does not include API access. Console.x.ai is separate.
- **Temp URLs expire ~24hrs**: Download and save images for permanent use.
- **Plugin changes need session restart**: Use direct API fallback to work immediately.
