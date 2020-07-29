import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

from accounts.managers import CustomManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=500)
    first_name = models.CharField(max_length=250, null=False, blank=False)
    last_name = models.CharField(max_length=250, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name +' '+ self.last_name

    def get_short_name(self):
        return self.first_name


class Address(models.Model):
    GENDER_CHOICES = [
        ('F', 'Female'),
        ('M', 'Male'),
        ('N', 'Unspecified'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(blank=True, null=True, help_text='Eg +234, +233')
    # gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='N')
    address_line_1 = models.TextField()
    address_line_2 = models.TextField(blank=True, null=True)
    address_line_3 = models.TextField(blank=True, null=True)
    address_line_4 = models.TextField(blank=True, null=True)
    town_city = models.TextField(help_text='Enter residing city or town')
    state = models.CharField(max_length=50)
    country = CountryField(blank_label='(select country)', multiple=False)


    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return self.user.first_name
