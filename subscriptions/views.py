from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import SubscriptionPlan
from .serializers import (
  SubscriptionLimitsSerializer, SubscriptionPlanSerializer, UserSubscriptionSerializer 
)

# Create your views here.

class SubscriptionPlanListView(generics.ListAPIView):
  """list all subscription plans"""

  permission_classes = [permissions.AllowAny]
  serializer_class = SubscriptionPlanSerializer
  
  def get_queryset(self):
    return SubscriptionPlan.objects.filter(is_active=True).order_by('price')

class MySubscriptionView(generics.RetrieveAPIView):
    """
    Auth: get current user's subscription
    """
    serializer_class = UserSubscriptionSerializer

    def get_object(self):
        return self.request.user.subscription


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