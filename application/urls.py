"""
URL configuration for application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from decouple import config
from django.conf import settings
from django.contrib import admin
from allauth.account.views import ConfirmEmailView
from django.urls import re_path,path,reverse,include
from django.http import HttpResponsePermanentRedirect
from profiles.views import CurrentUser
from appauth.views import LoginView,LogoutView,LogoutAllView
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView

def home(request):
    return HttpResponsePermanentRedirect(reverse("swagger-ui"))

ADMIN_SITE_URL="{}/".format(config('ADMIN_SITE_URL'))
VERSION=settings.VERSION.split(".")[0]
URL_HEADER=f"application-api/v{VERSION}"

urlpatterns = [
    path("",home,name="home"),
    path(ADMIN_SITE_URL,admin.site.urls),
    path(f"{URL_HEADER}/schema/",SpectacularAPIView.as_view(),name="schema"),
    path(f"{URL_HEADER}/schema/swagger-ui/",SpectacularSwaggerView.as_view(url_name="schema"),name="swagger-ui"),
    # user endpoints
    path(f"{URL_HEADER}/user/",CurrentUser.as_view(),name="current-user"),
    path(f"{URL_HEADER}/login/",LoginView.as_view(),name="knox_login"),
    path(f"{URL_HEADER}/logout/",LogoutView.as_view(),name="knox_logout"),
    path(f"{URL_HEADER}/logout/all/",LogoutAllView.as_view(),name="knox_logout_all"),
    # password/reset/, password/reset/confirm/, password/reset/validate_token/
    path(f"{URL_HEADER}/password/reset/",include('django_rest_passwordreset.urls',namespace='password_reset')),
    # password/change/
    path(f"{URL_HEADER}/", include("dj_rest_auth.urls")),
    # account-confirm-email/
    re_path(f"{URL_HEADER}/registration/account-confirm-email/(?P<key>[-:\w]+)/$",ConfirmEmailView.as_view(),name='account_confirm_email'),
    # registration/ verify-email/ resend-email/ account-email-verification-sent/
    path(f"{URL_HEADER}/registration/",include("dj_rest_auth.registration.urls")),
    # apps endpoints
    path(f"{URL_HEADER}/users/",include("profiles.urls")),
    path(f"{URL_HEADER}/books/",include("books.urls")),
    path(f"{URL_HEADER}/borrowing_records/",include("borrowing_records.urls")),
]
