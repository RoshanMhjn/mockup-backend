from django.urls import path
from .views import MyMockupListView, MyMockupDetailView, GenerateMockupView, RecordMockupView, AdminCreateMockupTemplateView, MockupTemplateDetailView

urlpatterns = [
    path("", MyMockupListView.as_view(), name="my-mockups"),
    path("<int:pk>/", MyMockupDetailView.as_view(), name="mockup-detail"),
    path("generate/", GenerateMockupView.as_view()),
    path("record/", RecordMockupView.as_view()),
    path("admin/templates/", AdminCreateMockupTemplateView.as_view()),
    path("templates/<uuid:id>/", MockupTemplateDetailView.as_view()),
]
