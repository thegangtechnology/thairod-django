from rest_framework import authentication

from thairod import settings


class DebugAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        if not settings.DEBUG:
            return None
        from user.models import User
        user = User.objects.last()

        if user is None:
            password = User.objects.make_random_password()
            user = User.objects.create(username='forceauth',
                                       email='testpassuser@thegang.tech',
                                       password=password,
                                       is_staff=True, is_superuser=True
                                       )
        return (user, None)
