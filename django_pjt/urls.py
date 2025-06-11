from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.permissions import AllowAny


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path(
    'schema/',
    SpectacularAPIView.as_view(permission_classes=[AllowAny]),
    name='schema'
    ),
    path(
        'swagger/',
        SpectacularSwaggerView.as_view(url_name='schema', permission_classes=[AllowAny]),
        name='swagger-ui'
    ),
]