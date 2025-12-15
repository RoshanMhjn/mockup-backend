from django.utils import timezone
from .models import UserSubscription

def get_active_subscription(user):
    try:
        return UserSubscription.objects.select_related('plan').get(
            user=user,
            status='active'
        )
    except UserSubscription.DoesNotExist:
        return None

def can_export_hd(user):
    sub = get_active_subscription(user)
    return bool(sub and sub.plan.allow_hd_export)

def can_remove_watermark(user):
    sub = get_active_subscription(user)
    return bool(sub and sub.plan.remove_watermark)

def max_mockups_per_month(user):
    sub = get_active_subscription(user)
    return sub.plan.max_mockups_per_month if sub else 0
