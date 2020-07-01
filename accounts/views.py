from django.http import Http404
from django.contrib.auth import get_user_model
from django.shortcuts import render, reverse, redirect

from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
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


# class UserViewSet(viewsets.ModelViewSet):
#     '''
#     Exposes API endpoint for Admin access only for `User` model.
#     '''
#     queryset = User.objects.all()
#     serializer_class = serializers.UserCompleteInfo
#     permission_classes = (IsAdminUser, )


class AllUsersView(generics.ListAPIView):
    '''Returns's all users. Only avaliable to `admin` usertype.'''
    serializer_class = serializers.UserCompleteInfo
    permission_classes = (IsAdminUser, )

    def get(self, request):
        queryset = User.objects.filter(is_staff=False)
        serializer = serializers.UserCompleteInfo(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AllAdminsView(generics.ListAPIView):
    '''
    API endpoint for Listing all Admins. Only available to other `admin` usertypes.
    '''
    serializer_class = serializers.UserCompleteInfo
    permission_classes = (IsAdminUser,)

    def get(self, request):
        queryset = User.objects.filter(is_staff=True)
        serializer = serializers.UserCompleteInfo(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class RegisterAdminView(generics.CreateAPIView):
    '''
    API endpoint for admin registration.
    '''
    queryset = User.objects.all()
    serializer_class = serializers.AdminRegisterSerializer

    def post(self, request):
        serializer = serializers.AdminRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer._errors)   


class UserView(generics.RetrieveUpdateDestroyAPIView):
    pass


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