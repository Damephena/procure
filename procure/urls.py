"""procure URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from django.views.generic import TemplateView # <--

import rest_framework.permissions as permissions
from allauth.account.views import confirm_email
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_auth.views import (
    PasswordResetConfirmView,
    PasswordChangeView,
    PasswordResetView,
    LogoutView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts.views import CustomConfirmEmailView

schema_view = get_schema_view(
    openapi.Info(
        title = 'Procure API',
        default_version = 'v1',
        description = 'Procure application: An E-commerce site',
        terms_of_service = 'https://www.google.com/policies/terms/',
      contact=openapi.Contact(email='contact@snippets.local'),
      license=openapi.License(name='BSD License'),
    ),
    public = True,
    permission_classes = (permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/orders/', include('orders.urls')),

    path('api-auth/', include('rest_framework.urls')),

    path('api/v1/rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api/v1/rest-auth/login/', TokenObtainPairView.as_view(), name='rest_login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    re_path('api/v1/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', PasswordResetConfirmView.as_view(),
                name='password_reset_confirm'),
    path('api/v1/password/reset/', PasswordResetView.as_view(),
        name='rest_password_reset'),
    path('api/v1/password/change/', PasswordChangeView.as_view(),
        name='rest_password_change'),
    path('api/v1/logout/', LogoutView.as_view(), name='rest_logout'),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
