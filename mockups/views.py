from django.shortcuts import render
from rest_framework.generics import ListAPIView , RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from mockups.models import Mockup
from .serializers import MockupSerializer

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
