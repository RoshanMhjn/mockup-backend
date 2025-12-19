
from rest_framework import serializers
from .models import SubscriptionPlan, UserSubscription
from subscriptions.permissions import require_hd_export

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
      'allow_premium_templates',
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
  allow_premium_templates = serializers.BooleanField()

class MySubscriptionSerializer(serializers.ModelSerializer):
    plan = serializers.CharField(source='plan.code')
    plan_name = serializers.CharField(source='plan.name')
    price = serializers.DecimalField(
        source='plan.price',
        max_digits=10,
        decimal_places=2
    )
    currency = serializers.CharField(source='plan.currency')
    max_mockups_per_month = serializers.IntegerField(
        source='plan.max_mockups_per_month'
    )
    allow_hd_export = serializers.BooleanField(
        source='plan.allow_hd_export'
    )
    remove_watermark = serializers.BooleanField(
        source='plan.remove_watermark'
    )

    class Meta:
        model = UserSubscription
        fields = [
            'plan',
            'plan_name',
            'price',
            'currency',
            'status',
            'max_mockups_per_month',
            'allow_hd_export',
            'remove_watermark',
            'started_at',
            'expires_at',
        ]

class MockupExportSerializer(serializers.Serializer):
    export_type = serializers.ChoiceField(choices=["sd", "hd"])

    def validate_export_type(self, value):
        request = self.context["request"]

        if value == "hd":
            require_hd_export(request.user)

        return value