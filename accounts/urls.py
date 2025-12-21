from django.urls import path
from .social_auth import google_login

urlpatterns = [
    path("google/", google_login, name="google-login"),
]