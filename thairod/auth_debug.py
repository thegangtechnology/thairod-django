from django.conf import settings
from django.http import HttpRequest
from rest_framework import authentication

from user.models import User


class DebugAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request: HttpRequest):
        god_mode = request.headers.get('GOD_MODE', default=None) is not None

        if not settings.DEBUG or not god_mode:
            return None
        user = User.objects.last()
        if user is None:
            password = User.objects.make_random_password()
            user = User.objects.create(username='forceauth',
                                       email='testpassuser@thegang.tech',
                                       password=password,
                                       is_staff=True, is_superuser=True
                                       )
        return (user, None)
