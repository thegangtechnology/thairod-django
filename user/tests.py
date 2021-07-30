from django.urls import reverse

from core.tests import BaseTestSimpleApiMixin
from thairod.utils.test_util import APITestCase
from user.models import User


class UserAPITestCase(APITestCase, BaseTestSimpleApiMixin):

    def setUp(self):
        self.model = User
        self.set_up_user()
        self.obj = User.objects.first()
        self.list_url = reverse('user-list')
        self.detail_url = reverse('user-detail', kwargs={'pk': self.obj.pk})
        self.valid_field = {
            "username": "joedon",
            "password": User.objects.make_random_password(),
            "email": "joedon@example.com",
            "first_name": "joe",
            "last_name": "don"
        }
