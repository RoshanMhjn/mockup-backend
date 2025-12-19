import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SubscriptionPlan, UserSubscription

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        return JsonResponse({"error": "Invalid signature"}, status=400)

    data = event["data"]["object"]

    if event["type"] == "checkout.session.completed":
        user_id = data["metadata"]["user_id"]
        plan_code = data["metadata"]["plan_code"]
        stripe_subscription_id = data["subscription"]

        plan = SubscriptionPlan.objects.get(code=plan_code)

        UserSubscription.objects.update_or_create(
            user_id=user_id,
            defaults={
                "plan": plan,
                "status": "active",
                "stripe_subscription_id": stripe_subscription_id,
            }
        )

    elif event["type"] == "customer.subscription.deleted":
        stripe_subscription_id = data["id"]

        UserSubscription.objects.filter(
            stripe_subscription_id=stripe_subscription_id
        ).update(status="cancelled")

    return JsonResponse({"status": "ok"})
