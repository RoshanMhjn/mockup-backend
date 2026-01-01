from django.utils import timezone
from subscriptions.models import UserMockupUsage, UserSubscription


class MockupPermissionError(Exception):
    def __init__(self, reason, remaining=None):
        self.reason = reason
        self.remaining = remaining
        super().__init__(reason)


def assert_can_generate_mockup(user):
    now = timezone.now()

    try:
        subscription = user.subscription
    except UserSubscription.DoesNotExist:
        raise MockupPermissionError("NO_SUBSCRIPTION")

    if not subscription.is_active():
        raise MockupPermissionError("SUBSCRIPTION_EXPIRED")

    plan = subscription.plan

    usage, _ = UserMockupUsage.objects.get_or_create(
        user=user,
        year=now.year,
        month=now.month,
        defaults={"used_count": 0},
    )

    remaining = plan.max_mockups_per_month - usage.used_count

    if remaining <= 0:
        raise MockupPermissionError(
            "LIMIT_EXCEEDED",
            remaining=0,
        )

    return {
        "plan": plan.code,
        "remaining": remaining,
        "allow_hd": plan.allow_hd_export,
        "remove_watermark": plan.remove_watermark,
    }
