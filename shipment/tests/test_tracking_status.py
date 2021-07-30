from django.urls import reverse
from thairod.utils.test_util import APITestCase

from core.tests import BaseTestSimpleApiMixin
from order.models import Order
from shipment.models import TrackingStatus, Shipment
from thairod.utils.load_seed import load_seed
from user.models import User


class TrackingStatusAPITestCase(BaseTestSimpleApiMixin, APITestCase):
    @classmethod
    def setUpTestData(cls):
        load_seed()

    def setUp(self):
        self.model = TrackingStatus
        self.set_up_user()
        self.obj = TrackingStatus.objects.first()
        self.order = Order.objects.first()
        self.shipment = Shipment.objects.first()
        self.list_url = reverse('tracking-list')
        self.detail_url = reverse('tracking-detail', kwargs={'pk': self.obj.pk})
        self.valid_field = {
            "status": "PENDING",
            "price": 2345.124,
            "discount": 123.124,
            "shipment": self.shipment.pk,
            "courier_code": "123456789",
            "courier_tracking_code": "987654321"
        }

    def set_up_user(self):
        password = User.objects.make_random_password()
        self.user = User.objects.create(username='forceauth',
                                        email='testpassuser@thegang.tech',
                                        password=password,
                                        is_staff=True, is_superuser=True
                                        )
        self.client.force_authenticate(self.user)
