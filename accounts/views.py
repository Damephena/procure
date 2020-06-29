from django.http import Http404
from django.contrib.auth import get_user_model
from django.shortcuts import render, reverse, redirect

from rest_framework import viewsets, generics, status
from rest_framework.response import Response
# from rest_auth.registration.views import RegisterView
from allauth.account.views import ConfirmEmailView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView
from rest_auth.social_serializers import TwitterLoginSerializer
from rest_auth.registration.serializers import SocialLoginSerializer

import accounts.serializers as serializers
from accounts.models import User

class UserProfile(generics.ListAPIView):
    '''Returns the requesting user's profile'''
    serializer_class = serializers.UserSerializer

    def get(self, request):
        queryset = get_user_model().objects.get(id=request.user.id)
        
        serializer = serializers.UserSerializer(queryset, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            self.object = None
        user = get_user_model().objects.get(email=self.object.email_address.email)
        # redirect_url = reverse('rest_login', args=(user.id,))
        redirect_url = reverse('rest_login')
        return redirect(redirect_url)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://localhost:8000/social-accounts/google/login/callback/"
    serializer_class = SocialLoginSerializer


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class TwitterLogin(SocialLoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter