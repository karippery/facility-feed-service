"""
URL configuration for facility_feed_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.shortcuts import redirect
from decouple import config

APP_NAME_API = config("APP_NAME_API", default="default_app_name")
API_VERSION = config("API_VERSION", default="v1")


def trigger_error(request):
    pass


def redirect_to_swagger(request):
    return redirect("schema-swagger-ui")


urlpatterns = [
    path('admin/', admin.site.urls),
    path("feed_service/", include("feed_service.urls")),
    path("users/", include("users.urls")),
    path(f"{APP_NAME_API}/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="schema-swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("", redirect_to_swagger),
    path('sentry-debug/', trigger_error),
]
