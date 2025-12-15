from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import SubscriptionPlan, UserSubscription

User = get_user_model()

@receiver(post_save, sender=User)
def create_free_subscription(sender, instance, created, **kwargs):
    if not created:
        return

    free_plan = SubscriptionPlan.objects.filter(code='free').first()
    if not free_plan:
        return

    UserSubscription.objects.create(
        user=instance,
        plan=free_plan,
        status='active',
        started_at=timezone.now()
    )
