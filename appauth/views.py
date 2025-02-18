from django.urls import reverse
from django.conf import settings
from django.contrib.auth import login
from rest_framework import permissions
from .serializers import LoginSerializer
from allauth.account.adapter import DefaultAccountAdapter
from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import (
    LoginView as KnoxLoginView,
    LogoutView as KnoxLogoutView,
    LogoutAllView as KnoxLogoutAllView,
)

class CustomAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        """
        Use dj_rest_auth email verification endpoint

        Updates the send_mail context variable to include it
        """

        confirm_email_url=reverse("account_confirm_email",kwargs={"key":context.get("key")})
        base_url=context.get("activate_url").split(confirm_email_url)[0]
        verification_url=f'{base_url}{reverse("rest_verify_email")}'
        ctx={
            "verification_url":verification_url,
            "expires_after":settings.ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS,
        }
        ctx.update(context)
        return super().send_mail(template_prefix, email, ctx)

class LoginView(KnoxLoginView):
    permission_classes=[permissions.AllowAny,]
    
    @extend_schema(
        responses=None,
        request=LoginSerializer,
    )
    def post(self, request, format=None):
        """
        Authenticates user and returns a token. 
        The token is valid for 24 hours
        """
        serializer=AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)

class LogoutView(KnoxLogoutView):
    @extend_schema(
        request=None,
        responses=None,
    )
    def post(self, request, format=None):
        """
        Logs out user from current client session and  
        invalidates the token supplied during authentication
        """
        return super().post(request,format)

class LogoutAllView(KnoxLogoutAllView):
    @extend_schema(
        request=None,
        responses=None,
    )
    def post(self, request, format=None):
        return super().post(request,format)
