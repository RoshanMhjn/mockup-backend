

from rest_framework import serializers
from .models import SubscriptionPlan, UserSubscription

class SubscriptionPlanSerializer(serializers.ModelSerializer):
  class Meta:
    model = SubscriptionPlan
    fields = [
      'id',
      'code',
      'name',
      'price',
      'currency',
      'max_mockups_per_month',
      'allow_hd_export',
      'remove_watermark',
    ]
  
class UserSubscriptionSerializer(serializers.ModelSerializer):
  plan = SubscriptionPlanSerializer(read_only=True)
  
  class Meta:
    model = UserSubscription
    fields = [
      'status',
      'started_at',
      'expires_at',
      'plan',
    ]

class SubscriptionLimitsSerializer(serializers.Serializer):
  plan_code = serializers.CharField()
  max_mockups_per_month = serializers.IntegerField()
  allow_hd_export = serializers.BooleanField()
  remove_watermark = serializers.BooleanField()