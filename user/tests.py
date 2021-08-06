from django.urls import reverse
from rest_framework import status

from thairod.utils.test_util import APITestCase
from user.models import User


class UserAPITestCase(APITestCase):

    def setUp(self):
        self.model = User
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

    def test_get_current_user(self):
        self.user_test = User.objects.create(
            username='forceauth', password=User.objects.make_random_password(), first_name='joe', last_name='don')
        self.client.force_authenticate(self.user_test)
        response = self.client.get(reverse("current-user"))
        self.assertEqual(response.data['username'], 'forceauth')
        self.assertEqual(response.data['first_name'], 'joe')
        self.assertEqual(response.data['last_name'], 'don')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_anonymous(self):
        self.client.force_authenticate()
        response = self.client.get(reverse("current-user"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'user is not authenticated.')
