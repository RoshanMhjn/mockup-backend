from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class SubscriptionPlan(models.Model):
    PLAN_CHOICES = (
    ('free', 'Free'),
    ('pro', 'Pro'),
    ('team', 'Team'),
    )

    code = models.CharField(
    max_length=20,
    choices=PLAN_CHOICES,
    unique=True
    )
    
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default='USD')
    stripe_price_id = models.CharField(max_length=100, blank=True, null=True)
    
    #feature
    
    max_mockups_per_month = models.IntegerField(default=5)
    allow_hd_export = models.BooleanField(default=False)
    remove_watermark = models.BooleanField(default=False)
    allow_premium_templates = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'subscription_plans'
    
    def __str__(self):
        return self.name

class UserSubscription(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscription'
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,
        related_name='subscriptions'
    )
    
    stripe_subscription_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    started_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(null=True, blank=True)

    def is_active(self):
        if self.status!= "active":
            return False
        if self.expires_at:
            return self.expires_at > timezone.now()
        return True

    def __str__(self):
        return f"{self.user.email} → {self.plan.code}"

class UserMockupUsage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mockup_usages"
    )

    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()

    used_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "year", "month")
        ordering = ["-year", "-month"]

    def __str__(self):
        return f"{self.user.email} - {self.year}/{self.month} ({self.used_count})"