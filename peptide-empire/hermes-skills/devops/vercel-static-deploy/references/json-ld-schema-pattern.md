# JSON-LD Structured Data Pattern

Reusable JSON-LD blocks for static websites. Paste into `<head>` before `</head>`.

## When to Use
- Any static HTML site deployment
- SEO improvement pass
- User asks about structured data, schema, Google Knowledge Panel, or AI search optimization

## Why It Matters
- **Google Knowledge Panel**: Person + Organization schema enables a rich panel in search results
- **AI Search Engines** (Perplexity, ChatGPT, Claude, Grok): Use structured data as their #1 source of truth
- **Rich Snippets**: Offer schema shows price/description directly in search results

## Pattern 1: Homepage (Organization + Person + WebSite)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "name": "BRAND_NAME",
      "url": "https://DOMAIN.com",
      "description": "ONE_SENTENCE_DESCRIPTION",
      "logo": "https://DOMAIN.com/og-card.jpg",
      "sameAs": ["SOCIAL_PROFILE_URL"],
      "founder": {
        "@type": "Person",
        "name": "PERSON_NAME",
        "honorificSuffix": "CREDENTIAL",
        "jobTitle": "TITLE"
      },
      "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "Consultation Booking",
        "url": "BOOKING_URL",
        "availableLanguage": "English"
      }
    },
    {
      "@type": "WebSite",
      "name": "BRAND_NAME",
      "url": "https://DOMAIN.com",
      "inLanguage": "en",
      "potentialAction": {
        "@type": "SearchAction",
        "target": "https://DOMAIN.com/search?q={search_term_string}",
        "query-input": "required name=search_term_string"
      }
    },
    {
      "@type": "Person",
      "name": "PERSON_NAME",
      "honorificSuffix": "CREDENTIAL",
      "jobTitle": "TITLE",
      "description": "DETAILED_DESCRIPTION_WITH_KEYWORDS",
      "url": "https://DOMAIN.com",
      "sameAs": ["SOCIAL_URL"],
      "knowsAbout": [
        "TOPIC_1", "TOPIC_2", "TOPIC_3"
      ],
      "makesOffer": {
        "@type": "Offer",
        "name": "OFFER_NAME",
        "price": "PRICE",
        "priceCurrency": "USD",
        "url": "BOOKING_URL",
        "description": "OFFER_DESCRIPTION"
      }
    }
  ]
}
</script>
```

## Pattern 2: Article Page (Article + FAQPage)

Used on standalone content pages (guides, calculators, resources):

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Article",
      "headline": "PAGE_TITLE",
      "description": "PAGE_DESCRIPTION",
      "author": {
        "@type": "Person",
        "name": "AUTHOR_NAME",
        "honorificSuffix": "CREDENTIAL",
        "jobTitle": "TITLE",
        "url": "https://DOMAIN.com"
      },
      "publisher": {
        "@type": "Organization",
        "name": "BRAND_NAME",
        "logo": { "@type": "ImageObject", "url": "LOGO_URL" }
      },
      "url": "PAGE_URL",
      "mainEntityOfPage": "PAGE_URL",
      "datePublished": "YYYY-MM-DD",
      "dateModified": "YYYY-MM-DD",
      "image": "OG_IMAGE_URL",
      "about": ["KEYWORD_1", "KEYWORD_2", "KEYWORD_3"],
      "isAccessibleForFree": true
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "QUESTION_TEXT",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "ANSWER_TEXT"
          }
        }
      ]
    }
  ]
}
</script>
```

## Pitfalls
- `knowsAbout` array: include ALL relevant topics — this feeds AI search engines
- `dateModified`: update when content changes — Google uses this for freshness
- `price`: use string format with 2 decimal places ("197.00", not 197)
- Validate at https://validator.schema.org before deploying
- Always include both Organization AND Person schema on the homepage — not one or the other
