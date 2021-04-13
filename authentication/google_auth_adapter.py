from allauth.account.utils import perform_login
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from projects.models.users import User


class GoogleAuthAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        google_user = sociallogin.user
        if google_user.id:
            return
        try:
            existing_user = User.objects.get(email=google_user.email)
            sociallogin.state['process'] = 'connect'
            perform_login(request, existing_user, 'none')
        except User.DoesNotExist:
            raise ValueError
