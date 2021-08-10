import datetime

import freezegun
from django.urls import reverse
from django.utils import timezone

from core.tests import BaseTestSimpleApiMixin
from shipment.models import BatchShipment, Shipment
from shipment.services.batch_shipment_service import BatchShipmentService
from thairod import settings
from thairod.utils.test_util import APITestCase, TestCase


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

    def test_generated_batch_name_after(self):
        date = timezone.datetime(2020, 8, 23, settings.SHIPPOP_LOT_CUTTING_TIME) + datetime.timedelta(hours=1)
        batch_name = BatchShipment.generate_batch_name(date)
        self.assertEqual(batch_name, '2020-08-24_1')

    def test_generated_batch_name_before(self):
        date = timezone.datetime(2020, 8, 23, settings.SHIPPOP_LOT_CUTTING_TIME) - datetime.timedelta(hours=1)
        batch_name = BatchShipment.generate_batch_name(date)
        self.assertEqual(batch_name, '2020-08-23_1')

    @freezegun.freeze_time(timezone.datetime(2020, 8, 23, 8))
    def test_generated_batch_name_no_argument(self):
        batch_name = BatchShipment.generate_batch_name()
        self.assertEqual(batch_name, '2020-08-23_1')

    @freezegun.freeze_time(timezone.datetime(2020, 8, 23, 8))
    def test_generated_batch_name_api(self):
        url = reverse("batch-shipment-get-next-generated-batch-name")
        response = self.client.get(url, format='json')
        self.assertEqual('2020-08-23_1', response.data.get('name'))

    @freezegun.freeze_time(timezone.datetime(2020, 8, 23, 8))
    def test_count_batch_today(self):
        # not to rely on db time
        BatchShipment.objects.create(name='aaaa', created_date=timezone.now())
        BatchShipment.objects.create(name='bbb', created_date=timezone.now())
        got = BatchShipment.count_created_today()
        self.assertEqual(got, 2)

    def test_all(self):
        count = BatchShipment.objects.all().count()
        url = reverse("batch-shipment-all")
        response = self.client.get(url, format='json')
        self.assertEqual(count, len(response.data))

    def test_pending_deliver(self):
        count = BatchShipment.objects.filter(shipment__deliver=False).distinct().count()
        url = reverse("batch-shipment-pending-deliver")
        response = self.client.get(url, format='json')
        self.assertEqual(count, len(response.data))

    def test_assign_batch(self):
        batch_name = "batch_name"
        shipments = [Shipment.objects.first().id]
        request = {"batch_name": batch_name, "shipments": shipments}
        url = reverse("batch-shipment-assign-batch")
        response = self.client.post(url, request, format='json')
        self.assertTrue(response.status_code, 200)
        shipment = Shipment.objects.first()
        self.assertEqual(batch_name, shipment.batch.name)


class TestBatchShipmentService(TestCase):
    with_seed = False

    def test_determine_batch_after_cutoff(self):
        h = settings.SHIPPOP_LOT_CUTTING_TIME + 1
        dt = timezone.datetime(1982, 8, 23, h)
        got = BatchShipmentService.determine_print_date(dt)
        self.assertEqual(got, datetime.date(1982, 8, 24))

    def test_determine_batch_before_cutoff(self):
        h = settings.SHIPPOP_LOT_CUTTING_TIME - 1
        dt = timezone.datetime(1982, 8, 23, h)
        got = BatchShipmentService.determine_print_date(dt)
        self.assertEqual(got, datetime.date(1982, 8, 23))
