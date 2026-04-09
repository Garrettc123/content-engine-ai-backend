from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI(
    title="Content Engine AI",
    description="AI-powered content generation and SEO optimization backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Models ---
class ContentRequest(BaseModel):
    topic: str
    keywords: Optional[List[str]] = []
    tone: Optional[str] = "professional"
    word_count: Optional[int] = 500


class ContentResponse(BaseModel):
    title: str
    meta_description: str
    content: str
    keywords_used: List[str]
    seo_score: int


class CheckoutRequest(BaseModel):
    plan: str  # "starter" | "pro" | "enterprise"
    email: Optional[str] = None
    success_url: Optional[str] = "https://contentengine.ai/success"
    cancel_url: Optional[str] = "https://contentengine.ai/cancel"


# --- Plan pricing ---
PLANS = {
    "starter": {"price_id": "price_starter_monthly", "amount": 2900, "name": "Starter"},
    "pro": {"price_id": "price_pro_monthly", "amount": 7900, "name": "Pro"},
    "enterprise": {"price_id": "price_enterprise_monthly", "amount": 19900, "name": "Enterprise"},
}


# --- Routes ---
@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "content-engine-ai", "version": "1.0.0"}


@app.get("/")
async def root():
    return {
        "message": "Content Engine AI API",
        "docs": "/docs",
        "health": "/health"
    }


@app.post("/generate-content", response_model=ContentResponse)
async def generate_content(request: ContentRequest):
    """
    Generate SEO-optimized content based on topic and keywords.
    In production, this connects to an LLM (e.g., OpenAI GPT-4).
    """
    keywords = request.keywords or []
    keyword_str = ", ".join(keywords) if keywords else request.topic

    # Stub response — replace with real LLM call using OPENAI_API_KEY
    title = f"The Complete Guide to {request.topic.title()}"
    meta_description = (
        f"Discover everything you need to know about {request.topic}. "
        f"Expert insights covering {keyword_str}. Start optimizing today."
    )

    paragraphs = [
        f"## Introduction\n\n"
        f"{request.topic.capitalize()} is one of the most important topics in today's digital landscape. "
        f"Understanding {request.topic} gives your business a competitive edge and drives measurable results.\n\n",

        f"## Why {request.topic.title()} Matters\n\n"
        f"Businesses that leverage {request.topic} see significant improvements in engagement, "
        f"conversion rates, and organic search visibility. "
        f"Key areas to focus on include: {keyword_str}.\n\n",

        f"## Best Practices\n\n"
        f"When implementing {request.topic}, follow these proven strategies:\n"
        f"1. Start with thorough keyword research\n"
        f"2. Create high-quality, user-focused content\n"
        f"3. Optimize meta tags and structured data\n"
        f"4. Build authoritative backlinks\n"
        f"5. Monitor performance and iterate\n\n",

        f"## Conclusion\n\n"
        f"Success with {request.topic} requires consistent effort and data-driven decision making. "
        f"Use the Content Engine AI platform to automate and scale your content strategy.",
    ]

    content = "".join(paragraphs)

    return ContentResponse(
        title=title,
        meta_description=meta_description,
        content=content,
        keywords_used=keywords,
        seo_score=82,
    )


@app.post("/create-checkout-session")
async def create_checkout_session(request: CheckoutRequest):
    """
    Create a Stripe checkout session for Content Engine plans.
    Requires STRIPE_SECRET_KEY environment variable in production.
    """
    plan = request.plan.lower()

    if plan not in PLANS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid plan '{plan}'. Choose from: {', '.join(PLANS.keys())}"
        )

    stripe_key = os.environ.get("STRIPE_SECRET_KEY")

    if stripe_key:
        try:
            import stripe
            stripe.api_key = stripe_key
            plan_info = PLANS[plan]

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price": plan_info["price_id"],
                    "quantity": 1,
                }],
                mode="subscription",
                customer_email=request.email,
                success_url=request.success_url,
                cancel_url=request.cancel_url,
            )

            return {
                "checkout_url": session.url,
                "session_id": session.id,
                "plan": plan,
                "amount": plan_info["amount"],
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Stripe error: {str(e)}")
    else:
        # Stub response when Stripe key not configured
        plan_info = PLANS[plan]
        return {
            "checkout_url": f"https://checkout.stripe.com/pay/stub_{plan}",
            "session_id": f"cs_stub_{plan}_session",
            "plan": plan,
            "amount": plan_info["amount"],
            "note": "Stub response — set STRIPE_SECRET_KEY to enable live Stripe checkout",
        }


@app.get("/plans")
async def list_plans():
    """List available subscription plans and pricing."""
    return {
        "plans": [
            {
                "id": "starter",
                "name": "Starter",
                "price_monthly": 29,
                "features": ["50 AI content pieces/month", "Basic SEO analysis", "Email support"]
            },
            {
                "id": "pro",
                "name": "Pro",
                "price_monthly": 79,
                "features": ["200 AI content pieces/month", "Advanced SEO + competitor analysis", "Priority support", "API access"]
            },
            {
                "id": "enterprise",
                "name": "Enterprise",
                "price_monthly": 199,
                "features": ["Unlimited content", "Custom AI fine-tuning", "Dedicated account manager", "SLA guarantee"]
            },
        ]
    }
