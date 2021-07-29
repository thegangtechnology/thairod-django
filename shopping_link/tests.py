from django.urls import reverse, exceptions
from rest_framework.test import APITestCase
from shopping_link.models import ShoppingLink
from thairod.utils.load_seed import load_seed
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
import json

json_content_type = "application/json"


class ShoppingLinkAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        load_seed()

    def setUp(self):
        self.obj = ShoppingLink.objects.first()
        self.list_url = reverse('shopping-link-list')
        raw_data = '{\r\n    \"raw_json_data\": {\r\n  \"username\": \"frappet\",\r\n  \"doctor\": {\r\n    \"name\": ' \
                   '\"Kazuya Sojo\",\r\n    \"license\": \"12345678\"\r\n  },\r\n  \"patient\": {\r\n    \"name\": ' \
                   '\"Green Covid\",\r\n    \"cid\": \"1234567890123\",\r\n    \"phoneno\": \"0811234567\",' \
                   '\r\n    \"hn\": \"123477889\",\r\n    \"address\": {\r\n      \"street\": \"123 ' \
                   '\u0E16\u0E19\u0E19abcd\",\r\n      \"subdistrict\": \"chimplee\",\r\n      \"disctrict\": ' \
                   '\"talingchan\",\r\n      \"zipcode\": \"12345\",\r\n      \"note\": \"next to 7\/11\"\r\n    ' \
                   '}\r\n  },\r\n  \"session_id\": \"abcd_for_callback\",\r\n  \"line_oa_id\": \"or something for ' \
                   'lineoa callback\"\r\n}\r\n} '
        self.valid_field = {
            "callback_secret": "-vKgejBAIPFfd8vgvG45J0nO1Zx6B79c02wa9a8cD5c",
            "raw_json_data": json.loads(raw_data),
            "is_expired": False
        }
        self.create_field = {
            "raw_json_data": json.loads(raw_data)
        }

    def test_list(self) -> None:
        response = self.client.get(self.list_url, content_type=json_content_type)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get(self) -> None:
        with self.assertRaises(exceptions.NoReverseMatch):
            self.client.get(reverse('shopping-link-detail', kwargs={'pk': self.obj.pk}),
                            content_type=json_content_type)
        response = self.client.get('api/shopping-link/', kwargs={'pk': self.obj.pk}, content_type=json_content_type)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create(self) -> None:
        response = self.client.post(self.list_url, self.create_field, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self) -> None:
        with self.assertRaises(exceptions.NoReverseMatch):
            self.client.put(reverse('shopping-link-detail', kwargs={'pk': self.obj.pk}),
                            self.valid_field, format="json")
        response = self.client.put('api/shopping-link/', kwargs={'pk': self.obj.pk}, content_type=json_content_type)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_with_querystring(self) -> None:
        created_secret = self.client.post(self.list_url, self.create_field, format='json')
        callback = created_secret.data.get('callback_secret')
        response = self.client.get(self.list_url, {'callback': callback},
                                   content_type=json_content_type)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_expired_secret(self) -> None:
        shopping_link = ShoppingLink.objects.create(**self.valid_field)
        # check after two house
        expired_time = timezone.now() + timedelta(hours=2, minutes=0)
        expired_time = expired_time.astimezone(tz=timezone.utc)
        self.assertFalse(shopping_link.is_expired)
        shopping_link.update_is_expired(timezone_object=expired_time)
        self.assertTrue(shopping_link.is_expired)
