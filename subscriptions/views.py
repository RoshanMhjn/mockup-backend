from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import SubscriptionPlan, UserSubscription
from .serializers import (
  SubscriptionLimitsSerializer, SubscriptionPlanSerializer, UserSubscriptionSerializer, MySubscriptionSerializer 
)
from .services import get_current_usage, can_generate_mockup

from subscriptions.permissions import (
  require_hd_export,
  should_apply_watermark
)

# Create your views here.

class SubscriptionPlanListView(generics.ListAPIView):
  """list all subscription plans"""

  permission_classes = [permissions.AllowAny]
  serializer_class = SubscriptionPlanSerializer
  
  def get_queryset(self):
    return SubscriptionPlan.objects.filter(is_active=True).order_by('price')

class SubscriptionLimitsView(generics.GenericAPIView):
    """
    Auth: return feature limits for current user
    """
    serializer_class = SubscriptionLimitsSerializer

    def get(self, request):
        subscription = request.user.subscription
        plan = subscription.plan

        data = {
            'plan_code': plan.code,
            'max_mockups_per_month': plan.max_mockups_per_month,
            'allow_hd_export': plan.allow_hd_export,
            'remove_watermark': plan.remove_watermark,
        }

        serializer = self.get_serializer(data)
        return Response(serializer.data)

class MySubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            subscription = UserSubscription.objects.select_related('plan').get(
                user=request.user,
                status='active'
            )
        except UserSubscription.DoesNotExist:
            return Response(
                {"detail": "No active subscription"},
                status=404
            )

        serializer = MySubscriptionSerializer(subscription)
        return Response(serializer.data)

class MockupUsageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usage = get_current_usage(request.user)
        subscription = request.user.subscription

        return Response({
            "used": usage.used_count,
            "limit": subscription.plan.max_mockups_per_month,
            "remaining": max(
                subscription.plan.max_mockups_per_month - usage.used_count, 0
            )
        })

class ExportMockupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        export_type = request.data.get("type", "sd")

        if export_type == "hd":
            require_hd_export(request.user)

        apply_watermark = should_apply_watermark(request.user)

        return Response({
            "export_type": export_type,
            "watermark_applied": apply_watermark
        })