"""
URL configuration for virtflow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf.urls.static import static
from virtflow import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView, SpectacularJSONAPIView, SpectacularYAMLAPIView, RedirectView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Schema
    path("api/v1/schema/json/", SpectacularJSONAPIView.as_view(), name="json"),
    path("api/v1/schema/yaml/", SpectacularYAMLAPIView.as_view(), name="yaml"),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/swagger-ui', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/docs', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API
    re_path(r'^api/v1/', include(('virtflow.api.v1.urls'), namespace='v1')),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=False)),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
] 
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
