from django.urls import reverse
from rest_framework.test import APITestCase

from address.models import Address
from core.tests import BaseTestSimpleApi
from thairod.utils.load_seed import load_seed


class AddressAPITestCase(BaseTestSimpleApi, APITestCase):
    @classmethod
    def setUpTestData(cls):
        load_seed()

    def setUp(self):
        self.model = Address
        self.obj = Address.objects.first()
        self.list_url = reverse('address-list')
        self.detail_url = reverse('address-detail', kwargs={'pk': self.obj.pk})
        self.valid_field = {
            "name": 'the gang tech',
            "lat": 67856.1234567,
            "lon": 567778.1234567,
            "house_number": "23456",
            "subdistrict": "qwerty",
            "district": "rtyuu",
            "province": "bangkok",
            "postal_code": "10123",
            "telno": "1234678",
            "country": "Thailand",
        }

    def test_search_house_number(self):
        self.set_up_user()
        search_url = self.list_url + f'?search={self.obj.house_number}'
        response = self.client.get(search_url)
        self.assertNotEqual(response.data['results'], [])

    def test_search_subdistrict(self):
        self.set_up_user()
        search_url = self.list_url + f'?search={self.obj.subdistrict}'
        response = self.client.get(search_url)
        self.assertNotEqual(response.data['results'], [])

    def test_search_district(self):
        self.set_up_user()
        search_url = self.list_url + f'?search={self.obj.district}'
        response = self.client.get(search_url)
        self.assertNotEqual(response.data['results'], [])

    def test_search_province(self):
        self.set_up_user()
        search_url = self.list_url + f'?search={self.obj.province}'
        response = self.client.get(search_url)
        self.assertNotEqual(response.data['results'], [])

    def test_search_postal_code(self):
        self.set_up_user()
        search_url = self.list_url + f'?search={self.obj.postal_code}'
        response = self.client.get(search_url)
        self.assertNotEqual(response.data['results'], [])

    def test_search_country(self):
        self.set_up_user()
        search_url = self.list_url + f'?search={self.obj.country}'
        response = self.client.get(search_url)
        self.assertNotEqual(response.data['results'], [])

    def test_search_note(self):
        self.set_up_user()
        search_url = self.list_url + f'?search={self.obj.note}'
        response = self.client.get(search_url)
        self.assertNotEqual(response.data['results'], [])
