from django.shortcuts import render
from rest_framework.generics import ListAPIView , RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from mockups.models import Mockup, MockupTemplate, GeneratedMockup
from .serializers import MockupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response



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

class CanGenerateMockupView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "allowed": True,
            "remaining": 999,
            "user_id": str(user.id)
        })

class RecordMockupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        template_id = request.data.get("template_id")
        image_url = request.data.get("image_url")

        template = MockupTemplate.objects.get(id=template_id)

        GeneratedMockup.objects.create(
            user=request.user,
            template=template,
            image_url=image_url
        )

        return Response({"success": True})
