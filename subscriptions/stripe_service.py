
import stripe
from django.conf import settings
from django.utils import timezone
from datetime import timezone

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(user, plan):
  
  if not plan.stripe_price_id:
    raise ValueError("Stripe price not configured")
  
  session = stripe.checkout.Session.create(
    payment_method_types=["card"],
    mode="subscription",
    customer_email=user.email,
    line_items=[{
      "price": plan.stripe_price_id,
      "quantity": 1,
    }],
    success_url="http://localhost:5173/billing/success?session_id={CHECKOUT_SESSION_ID}",
    cancel_url="http://localhost:5173/pricing?canceled=true",

    metadata={
            "user_id": str(user.id),
            "plan_code": plan.code,
        }
  )
  
  return session

def create_customer_portal_session(user):
    subscription = user.subscription

    if not subscription.stripe_subscription_id:
        raise ValueError("No Stripe subscription found")

    stripe_subscription = stripe.Subscription.retrieve(
        subscription.stripe_subscription_id
    )

    session = stripe.billing_portal.Session.create(
        customer=stripe_subscription.customer,
        return_url=settings.STRIPE_PORTAL_RETURN_URL,
    )

    return session