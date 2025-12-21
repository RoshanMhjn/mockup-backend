import logging
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from allauth.socialaccount.models import SocialAccount, SocialApp
from rest_framework.authtoken.models import Token

from .serializers import CustomUserDetailsSerializer

logger = logging.getLogger(__name__)
User = get_user_model()


@api_view(["POST"])
@permission_classes([AllowAny])
def google_login(request):
    """
    POST /api/auth/google/

    Body:
    {
        "access_token": "<google_id_token>"
    }
    """
    token = request.data.get("access_token")

    if not token:
        return Response(
            {"detail": "access_token is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
        
    google_app = (
        SocialApp.objects
        .filter(provider="google")
        .order_by("id")
        .first()
    )

    if not google_app:
        return Response(
            {"detail": "Google OAuth is not configured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            google_app.client_id,
        )

        email = idinfo.get("email")
        google_uid = idinfo.get("sub")

        if not email or not google_uid:
            return Response(
                {"detail": "Invalid Google token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        first_name = idinfo.get("given_name", "")
        last_name = idinfo.get("family_name", "")
        email_verified = idinfo.get("email_verified", False)

        #Find or create user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "is_active": True,
            },
        )

        #Mark email verified (Google emails ARE verified)
        if email_verified and not getattr(user, "email_verified", False):
            user.email_verified = True
            user.save(update_fields=["email_verified"])

        #Link social account (idempotent)
        SocialAccount.objects.get_or_create(
            user=user,
            provider="google",
            uid=google_uid,
            defaults={"extra_data": idinfo},
        )

        #Token auth
        token_obj, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "key": token_obj.key,
                "user": CustomUserDetailsSerializer(user).data,
                "created": created,
            },
            status=status.HTTP_200_OK,
        )

    except ValueError:
        return Response(
            {"detail": "Invalid or expired Google token"},
            status=status.HTTP_400_BAD_REQUEST,
        )
