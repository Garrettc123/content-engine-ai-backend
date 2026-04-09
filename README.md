# Content Engine AI — Backend

FastAPI backend for the Content Engine AI platform. Provides AI-powered content generation, SEO optimization, and Stripe billing.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/plans` | List subscription plans |
| POST | `/generate-content` | Generate SEO content |
| POST | `/create-checkout-session` | Create Stripe checkout |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Recommended | Powers real AI content generation |
| `STRIPE_SECRET_KEY` | For billing | Enables live Stripe checkout sessions |

## Local Development

```bash
pip install -r requirements.txt
uvicorn api.index:app --reload
```

## Deployment

Deployed on Vercel via `vercel --prod`.
