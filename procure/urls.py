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
from accounts.views import CustomConfirmEmailView, GoogleLogin
# from procure.other_urls import urlpatterns as others

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
    # patterns = others,
    permission_classes = (permissions.AllowAny,),
)

urlpatterns = [
    # path('', TemplateView.as_view(template_name="social_app/index.html")), # <--
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('accounts.urls')),

    # path('/social-accounts/google/login/callback/', ),
    # path('api-auth/', include('rest_framework.urls')), # allows login and out for browser API
    # path('api/v1/social-accounts/', include('allauth.urls')),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/v1/rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    re_path('api/v1/rest-auth/registration/account-confirm-email/(?P<key>.+)/', CustomConfirmEmailView.as_view(), name='account_confirm_email'),
    # re_path('api/v1/rest-auth/registration/account-confirm-email/(?P<key>.+)/', confirm_email, name='account_confirm_email'),
    
    # path('api/v1/rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api/v1/rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api/v1/rest-auth/login/', TokenObtainPairView.as_view(), name='rest_login'),
    # re_path('api/v1/rest-auth/login/', TokenObtainPairView.as_view(), name='rest_login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/v1/rest-auth/', include('rest_auth.urls')),
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
]

# urlpatterns = [
#     # path('', TemplateView.as_view(template_name="social_app/index.html")), # <--
#     # path('admin/', admin.site.urls),
#     # path('api/v1/accounts/', include('accounts.urls')),

#     # # path('/social-accounts/google/login/callback/', ),
#     # path('api-auth/', include('rest_framework.urls')), # allows login and out for browser API
#     # path('api/v1/social-accounts/', include('allauth.urls')),
#     # # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     # path('api/v1/rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
#     # re_path('api/v1/rest-auth/registration/account-confirm-email/(?P<key>.+)/', CustomConfirmEmailView.as_view(), name='account_confirm_email'),
#     # # re_path('api/v1/rest-auth/registration/account-confirm-email/(?P<key>.+)/', confirm_email, name='account_confirm_email'),
#     # path('api/v1/rest-auth/registration/', include('rest_auth.registration.urls')),

#     # re_path('api/v1/rest-auth/login/', TokenObtainPairView.as_view(), name='rest_login'),
#     # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     # path('api/v1/rest-auth/', include('rest_auth.urls')),
#     # re_path(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', PasswordResetConfirmView.as_view(),
#     #             name='password_reset_confirm'),
#     # path('api/v1/password/reset/', PasswordResetView.as_view(),
#     #     name='rest_password_reset'),
#     # path('api/v1/password/change/', PasswordChangeView.as_view(),
#     #     name='rest_password_change'),
#     # path('api/v1/logout/', LogoutView.as_view(), name='rest_logout'),
    
#     url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#     url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
# ]
