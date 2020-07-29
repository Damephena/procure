import django.contrib.auth.password_validation as validators
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.core import exceptions

from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    '''Serializer for fetching profile to regular users.'''
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'created_at',
        )


class UserCompleteInfo(serializers.ModelSerializer):
    '''User serializer which is only available to only `Admin` usertype'''
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'is_superuser',
            'is_staff',
            'is_active',
            'created_at',
            'last_login',
        )


class AdminRegisterSerializer(serializers.ModelSerializer):
    '''
    Admin registration serializer.
    '''
    password1 = serializers.CharField(
        max_length=100, 
        required=True, 
        write_only=True,
    )
    password2 = serializers.CharField(
        max_length=100, 
        required=True,
        write_only=True,
    )


    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
        )
    
    def validate(self, data):
        password = data.get('password1')
        confirm_password = data.get('password2')
        errors = dict()

        if password != confirm_password:
            message = "Password mismatch!"
            errors['password'] = ["Password mismatch!"]
        
        try:
            validators.validate_password(password)
        except exceptions.ValidationError as err:
            errors['password'] = list(err.messages)
        
        if errors:
            raise serializers.ValidationError(errors)
        return super(AdminRegisterSerializer, self).validate(data)
    
    def create(self, validated_data):
        admin = User.objects.create_superuser(
            email=validated_data['email'].lower(),
            password=validated_data['password1'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return admin


class RegisterSerializer(serializers.Serializer):
    '''
    Register as a user.
    '''
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.save(update_fields=['first_name', 'last_name'])

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user
