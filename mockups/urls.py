from django.urls import path
from .views import MyMockupListView, MyMockupDetailView

urlpatterns = [
    path("", MyMockupListView.as_view(), name="my-mockups"),
    path("<int:pk>/", MyMockupDetailView.as_view(), name="mockup-detail"),
]
