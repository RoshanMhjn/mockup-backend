from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings

from subscriptions.models import SubscriptionPlan, UserSubscription

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_free_subscription(sender, instance, created, **kwargs):
    if not created:
        return

    free_plan = SubscriptionPlan.objects.filter(code='free').first()
    if not free_plan:
        return

    UserSubscription.objects.get_or_create(
        user=instance,
        defaults={
        "plan": free_plan
        }
    )
