from django.urls import path, re_path
from rest_framework.routers import SimpleRouter
from rest_auth.registration.views import (
    SocialAccountListView, SocialAccountDisconnectView
)

from accounts.views import (
    UserProfile, 
    AllUsersView, 
    AllAdminsView,
    RegisterAdminView,
    UserDetailView,
    AdminDetailView
)

# router = SimpleRouter()
# router.register('admins', AdminViewSet, basename='admins')

urlpatterns = [
    path('profile/', UserProfile.as_view(), name='profile'),
    path('admin/users/', AllUsersView.as_view(), name='user-list'),
    path('admin/user/<pk>/', UserDetailView.as_view(), name='user-detail'),
    path('admin/admins/', AllAdminsView.as_view(), name='admin-list'),
    path('admin/admins/<pk>/', AdminDetailView.as_view(), name='admin-detail'),
    path('admin/register/', RegisterAdminView.as_view(), name='admin-create'),
    # path('google/', GoogleLogin.as_view(), name='google_login'),
    # path('socialaccounts/', SocialAccountListView.as_view(), name='social_account_list'
    # ),
    # re_path(r'^socialaccounts/(?P<pk>\d+)/disconnect/$', SocialAccountDisconnectView.as_view(), 
    #     name='social_account_disconnect'
    # ),
    # router.urls
]
# urlpatterns += router.urls
