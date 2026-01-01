
import requests
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.shortcuts import render
from rest_framework.generics import ListAPIView , RetrieveAPIView
from mockups.models import Mockup, MockupTemplate, GeneratedMockup
from .serializers import MockupSerializer, AdminMockupTemplateCreateSerializer, MockupTemplateDetailSerializer
from rest_framework.response import Response
from subscriptions.models import UserMockupUsage, UserSubscription
from .services.node_mockup import generate_mockup_via_node
from django.utils import timezone
from .services.permissions import (
    assert_can_generate_mockup, MockupPermissionError,
)


# Create your views here.

class MyMockupListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MockupSerializer

    def get_queryset(self):
        return Mockup.objects.filter(user=self.request.user)

class MyMockupDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MockupSerializer

    def get_queryset(self):
        return Mockup.objects.filter(user=self.request.user)

class GenerateMockupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        template_id = request.data.get("template_id")
        design_file = request.FILES.get("design")
        export_type = request.data.get("export_type", "sd")

        if not template_id or not design_file:
            return Response(
                {"error": "template_id and design file are required"},
                status=400,
            )

        # Permission check
        try:
            permission = assert_can_generate_mockup(request.user)
        except MockupPermissionError as e:
            return Response(
                {
                    "allowed": False,
                    "reason": e.reason,
                    "remaining": e.remaining,
                },
                status=403,
            )

        # Enforce HD rule
        if export_type == "hd" and not permission["allow_hd"]:
            return Response(
                {"error": "HD export not allowed for your plan"},
                status=403,
            )

        template = MockupTemplate.objects.get(id=template_id)

        # Rendering options
        options = {
            "export_quality": export_type,
            "watermark": not permission["remove_watermark"],
        }

        # Call Node
        output_url = generate_mockup_via_node(
            template=template,
            design_file=design_file,
            options=options,
        )

        # Save result
        GeneratedMockup.objects.create(
            user=request.user,
            template=template,
            image_url=output_url,
        )

        # Increment usage
        now = timezone.now()
        usage = UserMockupUsage.objects.get(
            user=request.user,
            year=now.year,
            month=now.month,
        )
        usage.used_count += 1
        usage.save()

        return Response(
            {
                "success": True,
                "image_url": output_url,
                "remaining": permission["remaining"] - 1,
            }
        )

class RecordMockupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        now = timezone.now()

        template_id = request.data.get("template_id")
        image_url = request.data.get("image_url")

        template = MockupTemplate.objects.get(id=template_id)
        
        GeneratedMockup.objects.create(
            user=user,
            template=template,
            image_url=image_url
        )

        usage, _ = UserMockupUsage.objects.get_or_create(
            user=user,
            year=now.year,
            month=now.month,
            defaults={"used_count": 0}
        )

        usage.used_count += 1
        usage.save()

        return Response({"success": True})

class AdminCreateMockupTemplateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = AdminMockupTemplateCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        template = serializer.save()
        return Response(serializer.data, status=201)

class MockupTemplateDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MockupTemplateDetailSerializer
    lookup_field = "id"

    def get_queryset(self):
        return MockupTemplate.objects.filter(is_active=True)
