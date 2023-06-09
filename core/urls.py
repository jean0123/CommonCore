"""
URL configuration for core project.

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
from django.urls import path, reverse_lazy, include, re_path
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.conf import settings
from .routers import drf_url
from users.views import Login, Logout

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Core API",
        default_version='v1',
        description="Core API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="tescolsas@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('admin:index'))),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/login/', Login.as_view(), name='login'),
    path('api/logout/', Logout.as_view(), name='logout'),
    path('api/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(drf_url)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
