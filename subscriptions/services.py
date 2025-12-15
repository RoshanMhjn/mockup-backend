
from django.utils import timezone
from .models import UserMockupUsage
from .models import UserSubscription

def get_current_usage(user):
    now = timezone.now()
    usage, _ = UserMockupUsage.objects.get_or_create(
        user=user,
        year=now.year,
        month=now.month,
    )
    return usage

def can_generate_mockup(user):
    subscription = UserSubscription.objects.filter(
        user=user,
        is_active=True
    ).select_related("plan").first()

    if not subscription:
        return False, "No active subscription"

    usage = get_current_usage(user)

    if usage.used_count >= subscription.plan.max_mockups_per_month:
        return False, "Monthly mockup limit reached"

    return True, None

def increment_mockup_usage(user):
    usage = get_current_usage(user)
    usage.used_count += 1
    usage.save()
