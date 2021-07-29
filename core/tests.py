from rest_framework import status

from user.models import User


class BaseTestSimpleApi:
    def set_up_user(self):
        password = User.objects.make_random_password()
        self.user = User.objects.create(username='forceauth',
                                        email='testpassuser@thegang.tech',
                                        password=password,
                                        is_staff=True, is_superuser=True
                                        )
        self.client.force_authenticate(self.user)

    def test_list(self) -> None:
        self.set_up_user()
        response = self.client.get(self.list_url, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get(self) -> None:
        self.set_up_user()
        response = self.client.get(self.detail_url, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self) -> None:
        self.set_up_user()
        response = self.client.post(self.list_url, self.valid_field, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self) -> None:
        self.set_up_user()
        response = self.client.put(self.detail_url, self.valid_field, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
