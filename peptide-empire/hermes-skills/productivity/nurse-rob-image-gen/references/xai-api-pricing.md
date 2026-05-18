# xAI API Pricing (scraped from docs.x.ai — May 17, 2026)

All prices in USD. xAI API is PAY-AS-YOU-GO, separate from X Premium subscriptions.
API access via console.x.ai with XAI_API_KEY.

## Chat API (per 1M tokens)

| Model | Context | Input | Cached Input | Output |
|-------|---------|-------|-------------|--------|
| grok-4.3 | 1M | $1.25 | $0.20 | $2.50 |
| grok-4.20-multi-agent | 2M | $1.25 | $0.20 | $2.50 |
| grok-4.20-reasoning | 1M | $1.25 | $0.20 | $2.50 |
| grok-4.20-non-reasoning | 1M | $1.25 | $0.20 | $2.50 |

## Imagine API (Image Generation)

| Model | Media Input | Resolution | Output Cost |
|-------|------------|------------|-------------|
| grok-imagine-image-quality | $0.01/img | 1K | $0.05/img |
| grok-imagine-image-quality | $0.01/img | 2K | $0.07/img |
| grok-imagine-image | $0.002/img | 1K | $0.02/img |
| grok-imagine-image | $0.002/img | 2K | $0.02/img |

## Imagine API (Video Generation)

| Model | Media Input | Resolution | Output Cost |
|-------|------------|------------|-------------|
| grok-imagine-video | $0.01/sec + $0.002/img | 480p | $0.05/sec |
| grok-imagine-video | $0.01/sec + $0.002/img | 720p | $0.07/sec |

## Voice API

| Mode | Cost |
|------|------|
| Realtime | $0.05/min ($3.00/hr) |
| Text to Speech | $15.00/1M characters |
| Speech to Text (REST) | $0.10/hr |
| Speech to Text (Streaming) | $0.20/hr |

## Nurse Rob Usage Estimates

- Image gen: grok-imagine-image (~$0.02/img)
- 2 images/day × 30 days = 60 images = ~$1.20/month
- Even with HQ mode: ~$3.00-4.20/month
- Text usage via deepseek-v4-flash (not xAI), so xAI costs limited to images

## Key Facts

- X Premium ($8/mo blue check) does NOT include xAI API access
- xAI API is separate — sign up at console.x.ai
- One API key works for all endpoints (chat, image, video, voice)
- Direct API call: POST https://api.x.ai/v1/images/generations
- OpenAI SDK compatible — set base_url to https://api.x.ai/v1
