from django.urls import reverse
from rest_framework.test import APITestCase


from core.tests import BaseTestSimpleApi
from thairod.utils.load_seed import load_seed
from user.models import User


class UserAPITestCase(BaseTestSimpleApi, APITestCase):
    @classmethod
    def setUpTestData(cls):
        load_seed()

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
