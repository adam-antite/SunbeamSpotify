from django.contrib.auth.backends import BaseBackend
from Sunbeam.apps.users.models import CustomUser


class UsersBackend(BaseBackend):
    def authenticate(self, request, **kwargs):
        spotify_user_id = kwargs['spotify_user_id']
        spotify_username = kwargs['spotify_username']
        try:
            user = CustomUser.objects.get(spotify_username=spotify_username,
                                          spotify_user_id=spotify_user_id)
            return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
