from django.urls import path, re_path
from rest_framework.routers import SimpleRouter
from rest_auth.registration.views import (
    SocialAccountListView, SocialAccountDisconnectView
)

from accounts.views import UserProfile, UserViewSet, FacebookLogin, TwitterLogin, GoogleLogin

# router = SimpleRouter()
# router.register('', UserViewSet, basename='users')

urlpatterns = [
    path('profile/', UserProfile.as_view(), name='profile'),
    # path('google/', GoogleLogin.as_view(), name='google_login'),
    # path('socialaccounts/', SocialAccountListView.as_view(), name='social_account_list'
    # ),
    # re_path(r'^socialaccounts/(?P<pk>\d+)/disconnect/$', SocialAccountDisconnectView.as_view(), 
    #     name='social_account_disconnect'
    # ),
    # router.urls
]
# urlpatterns = router.urls
