from django.http import Http404
from django.contrib.auth import get_user_model
from django.shortcuts import reverse, redirect

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from allauth.account.views import ConfirmEmailView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView
from rest_auth.social_serializers import TwitterLoginSerializer
from rest_auth.registration.serializers import SocialLoginSerializer

import accounts.serializers as serializers


class UserProfile(generics.ListAPIView):
    '''Returns the requesting user's profile'''
    serializer_class = serializers.UserSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AllUsersView(generics.ListAPIView):
    '''Returns's all users. Only avaliable to `admin` usertype.'''
    serializer_class = serializers.UserCompleteInfo
    permission_classes = (IsAdminUser, )

    def get(self, request):
        queryset = get_user_model().objects.filter(is_staff=False)
        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''Retrieve, Update or Delete a regular `user`. Only available to `admin` usertype.'''
    look_up = 'pk'
    serializer_class = serializers.UserCompleteInfo
    queryset = get_user_model().objects.filter(is_staff=False)
    permission_classes = (IsAdminUser,)


class DeactivateUser(generics.UpdateAPIView):
    '''
    API endpoint to deactivate either a regular `user` or `admin` user. Only available to `admin` usertype.
    '''


class AllAdminsView(generics.ListAPIView):
    '''
    API endpoint for Listing all Admins. Only available to other `admin` usertypes.
    '''
    serializer_class = serializers.UserCompleteInfo
    permission_classes = (IsAdminUser,)

    def get(self, request):
        queryset = get_user_model().objects.filter(is_staff=True)
        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrieve, Update or Delete an `admin` usertype. Only available to other `admin` usertypes.
    '''
    look_up = 'pk'
    serializer_class = serializers.UserCompleteInfo
    queryset = get_user_model().objects.filter(is_staff=True)
    permission_classes = (IsAdminUser,)


class RegisterAdminView(generics.CreateAPIView):
    '''
    API endpoint for admin registration.
    '''
    queryset = get_user_model().objects.all()
    serializer_class = serializers.AdminRegisterSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors)


class CustomConfirmEmailView(ConfirmEmailView):
    '''View for creating custom email verification'''
    def get(self, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            self.object = None
        # user = get_user_model().objects.get(email=self.object.email_address.email)
        # redirect_url = reverse('rest_login', args=(user.id,))
        redirect_url = reverse('rest_login')
        return redirect(redirect_url)


class GoogleLogin(SocialLoginView):
    '''API endpoint for Authenticating using Google.'''
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://localhost:8000/social-accounts/google/login/callback/"
    serializer_class = SocialLoginSerializer


class FacebookLogin(SocialLoginView):
    '''API endpoint for Authenticating using Facebook.'''
    adapter_class = FacebookOAuth2Adapter
    client_class = OAuth2Client
    # serializer_class = SocialSerializer
    # renderer_classes = (UserJSONRenderer,)

    # def serializer_social_details(self, data):
    #     loginserializer = LoginSerializer(data=data)
    #     loginserializer.is_valid(raise_exception=True)
    #     return Response(loginserializer.data, status=status.HTTP_201_CREATED)

    # def post(self, request):
    #     data = json.loads(request.body.decode('utf-8'))
    #     access_token = data.get('access_token')
    #     # password = User.objects.make_random_password()
    #     password = "123456789"
    #     try:
    #         fb_graph_api_data = facebook.GraphAPI(access_token=access_token)
    #         user_info = fb_graph_api_data.get_object(
    #             id='me',
    #             fields='first_name, last_name, email, name')
    #     except facebook.GraphAPIError:
    #         return JsonResponse({'error': 'Invalid data'}, safe=False)
    #     try:
    #         user = User.objects.get(email=user_info.get('email'))

    #         if user:
    #             data = {
    #                 "email": user_info.get('email'),
    #                 "password": password,
    #             }
    #             # loginserializer = LoginSerializer(data=data)
    #             # loginserializer.is_valid(raise_exception=True)
    #             # return Response(loginserializer.data, status=status.HTTP_201_CREATED)
    #             self.serializer_social_details(data)
    #     except User.DoesNotExist:
    #         data = {
    #             "password": password,
    #             "first_name": user_info.get('first_name'),
    #             "last_name": user_info.get('last_name'),
    #             "email": user_info.get('email')
    #         }
    #         serializer = self.serializer_class(data=data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     return self.serializer_social_details(data)


class TwitterLogin(SocialLoginView):
    '''API endpoint for Authenticating using Twitter.'''
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter
