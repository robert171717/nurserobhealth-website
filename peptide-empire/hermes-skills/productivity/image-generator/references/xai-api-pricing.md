# xAI API Pricing Reference

Source: docs.x.ai/developers/pricing (scraped 2026-05-17)

## Chat API (per 1M tokens)

| Model | Context | Input | Cached Input | Output |
|-------|---------|-------|-------------|--------|
| grok-4.3 | 1M | $1.25 | $0.20 | $2.50 |
| grok-4.20-multi-agent | 2M | $1.25 | $0.20 | $2.50 |
| grok-4.20-reasoning | 1M | $1.25 | $0.20 | $2.50 |
| grok-4.20-non-reasoning | 1M | $1.25 | $0.20 | $2.50 |

## Imagine API (Image & Video Generation)

### Text/Image → Image

| Model | Media Input | Resolution | Output Cost |
|-------|------------|------------|-------------|
| grok-imagine-image-quality | $0.01/img | 1K | $0.05/img |
| grok-imagine-image-quality | $0.01/img | 2K | $0.07/img |
| grok-imagine-image | $0.002/img | 1K | $0.02/img |
| grok-imagine-image | $0.002/img | 2K | $0.02/img |

### Text/Image/Video → Video

| Model | Input | Resolution | Output Cost |
|-------|-------|------------|-------------|
| grok-imagine-video | $0.01/sec + $0.002/img | 480p | $0.05/sec |
| grok-imagine-video | $0.01/sec + $0.002/img | 720p | $0.07/sec |

## Voice API

| Mode | Cost |
|------|------|
| Realtime | $0.05/min ($3.00/hr) |
| Text to Speech | $15.00/1M characters |
| Speech to Text (REST) | $0.10/hr |
| Speech to Text (Streaming) | $0.20/hr |

## Nurse Rob Monthly Cost Estimate

Volume: 60 images/month (2 posts/day × 30 days)

| Quality | Cost/image | Monthly | Annual |
|---------|-----------|---------|--------|
| Standard (grok-imagine-image, 1K) | $0.02 | $1.20 | $14.40 |
| HQ (grok-imagine-image-quality, 1K) | $0.05 | $3.00 | $36.00 |
| HQ 2K | $0.07 | $4.20 | $50.40 |

All within the $25/month free credit tier. Zero additional cost at current volume.

## Access

- **Signup:** console.x.ai (free account)
- **API key:** From console → Team → API Keys
- **Free tier:** $25/month in credits (no credit card required initially)
- **Beyond free:** Pay-as-you-go, add payment method
- **NOT required:** X Premium, X Premium+, Supergrok subscription
