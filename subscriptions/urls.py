from django.urls import path
from .views import (
    SubscriptionPlanListView,
    MySubscriptionView,
    SubscriptionLimitsView,
    MockupUsageView,CreateCheckoutSessionView, CreateCustomerPortalView,
    VerifyCheckoutSessionView
)
from .webhooks import stripe_webhook

urlpatterns = [
    path('plans/', SubscriptionPlanListView.as_view(), name='subscription-plans'),
    path('me/', MySubscriptionView.as_view(), name='my-subscription'),
    path('limits/', SubscriptionLimitsView.as_view(), name='subscription-limits'),
    path("usage/", MockupUsageView.as_view(), name="mockup-usage"),
    path("checkout/", CreateCheckoutSessionView.as_view(), name="checkout"),
    path("webhook/stripe/", stripe_webhook),
    path("portal/", CreateCustomerPortalView.as_view(), name="customer-portal"),
    path("verify-session/", VerifyCheckoutSessionView.as_view()),

]
