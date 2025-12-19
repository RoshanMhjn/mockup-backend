from django.urls import path
from .views import (
    SubscriptionPlanListView,
    MySubscriptionView,
    SubscriptionLimitsView,
    MockupUsageView, UpgradeSubscriptionView
)

urlpatterns = [
    path('plans/', SubscriptionPlanListView.as_view(), name='subscription-plans'),
    path('me/', MySubscriptionView.as_view(), name='my-subscription'),
    path('limits/', SubscriptionLimitsView.as_view(), name='subscription-limits'),
    path("usage/", MockupUsageView.as_view(), name="mockup-usage"),
    path("upgrade/", UpgradeSubscriptionView.as_view(), name="upgrade-plan"),
]
