from django.urls import path
from .views import MyMockupListView, MyMockupDetailView, CanGenerateMockupView, RecordMockupView

urlpatterns = [
    path("", MyMockupListView.as_view(), name="my-mockups"),
    path("<int:pk>/", MyMockupDetailView.as_view(), name="mockup-detail"),
    path("can-generate/", CanGenerateMockupView.as_view()),
    path("record/", RecordMockupView.as_view()),

]
