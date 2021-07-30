from django.urls import reverse
from django.utils import timezone

from core.tests import BaseTestSimpleApiMixin
from shipment.models import BatchShipment, Shipment
from thairod.utils.test_util import APITestCase


class BatchShipmentAPITestCase(APITestCase, BaseTestSimpleApiMixin):

    def setUp(self):
        self.model = BatchShipment
        self.set_up_user()
        self.obj = BatchShipment.objects.first()
        self.list_url = reverse('batch-shipment-list')
        self.detail_url = reverse('batch-shipment-detail', kwargs={'pk': self.obj.pk})
        self.valid_field = {
            "name": "test BATCH"
        }

    def test_generated_batch_name(self):
        today = timezone.now().today()
        no_batch_create_today = BatchShipment.objects.filter(created_date__year=today.year,
                                                             created_date__month=today.month,
                                                             created_date__day=today.day).count()
        expected_name = f"{timezone.now().strftime('%Y-%m-%d')}_{no_batch_create_today + 1}"
        self.assertEqual(expected_name, BatchShipment.generate_batch_name())
        url = reverse("batch-shipment-get-next-generated-batch-name")
        response = self.client.get(url, format='json')
        self.assertEqual(expected_name, response.data.get('name'))

    def test_count_batch_today(self):
        today = timezone.now().today()
        no_batch_create_today = BatchShipment.objects.filter(created_date__year=today.year,
                                                             created_date__month=today.month,
                                                             created_date__day=today.day).count()
        self.assertEqual(no_batch_create_today, BatchShipment.count_create_today())

    def test_assign_batch(self):
        batch_name = "batch_name"
        shipments = [Shipment.objects.first().id]
        request = {"batch_name": batch_name, "shipments": shipments}
        url = reverse("batch-shipment-assign-batch")
        response = self.client.post(url, request, format='json')
        self.assertTrue(response.status_code, 200)
        shipment = Shipment.objects.first()
        self.assertEqual(batch_name, shipment.batch.name)
