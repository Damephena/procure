import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _

# from phonenumber_field.modelfields import PhoneNumberField
from accounts.managers import CustomManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=500)
    first_name = models.CharField(max_length=250, null=False, blank=False)
    last_name = models.CharField(max_length=250, null=False, blank=False)
    is_admin = models.BooleanField(default=False)
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
        return self.get_full_name() + '-' + self.get_email()

    def get_full_name(self):
        return self.first_name +' '+ self.last_name

    def get_short_name(self):
        return self.first_name

    def get_email(self):
        return self.email

# class Role(models.Model):
#     id
#     name
#     created_at
#     updated_at

# class UserRole(models.Model):
#     user
#     role
#     created_at
#     updated_at

# class Address(models.Model):
#     customer = models.ForeignKey('User', on_delete=models.CASCADE, to_field='id')
#     phone_number = PhoneNumberField(blank=True, null=True)