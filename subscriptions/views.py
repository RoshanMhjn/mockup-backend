from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import SubscriptionPlan, UserSubscription
from .serializers import (
    SubscriptionLimitsSerializer, SubscriptionPlanSerializer, UserSubscriptionSerializer, MySubscriptionSerializer, UpgradeSubscriptionSerializer 
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
            'allow_premium_templates': plan.allow_premium_templates,
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
        
class UpgradeSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UpgradeSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plan_code = serializer.validated_data["plan_code"]

        try:
            new_plan = SubscriptionPlan.objects.get(
                code=plan_code,
                is_active=True
            )
        except SubscriptionPlan.DoesNotExist:
            return Response(
                {"detail": "Invalid plan"},
                status=status.HTTP_400_BAD_REQUEST
            )

        subscription = request.user.subscription

        if subscription.plan.code == new_plan.code:
            return Response(
                {"detail": "You are already on this plan"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if new_plan.price < subscription.plan.price:
            return Response(
                {"detail": "Downgrades are not allowed"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        subscription.plan = new_plan
        subscription.status = "active"
        subscription.expires_at = None
        subscription.save()

        return Response(
            MySubscriptionSerializer(subscription).data,
            status=status.HTTP_200_OK
        )
