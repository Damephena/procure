from django.urls import path, re_path

from rest_framework.routers import SimpleRouter

from accounts.views import UserProfile

urlpatterns = [
    path('profile/', UserProfile.as_view(), name='profile'),
]

