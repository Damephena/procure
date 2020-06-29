from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_field
# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

class CustomUserAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        '''
        Saves a new `User` instance using information provided in the signup form.
        '''
        user = super().save_user(request, user, form, False)
        # user_field(user, 'first_name', request.data.get('first_name', ''))
        # user_field(user, 'last_name', request.data.get('last_name'))
        user.save()
        return user

