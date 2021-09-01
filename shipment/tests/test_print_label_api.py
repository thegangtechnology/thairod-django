from django.urls import reverse

from order.dataclasses.order import CreateOrderParam
from order.services.fulfiller_service import FulfilmentService
from order.services.order_service import OrderService
from thairod.utils.load_seed import RealisticSeed
from thairod.utils.test_util import APITestCase
from unittest import skipIf
from django.conf import settings


class TestPrintLabelAPI(APITestCase):
    patch_shippop = False
    with_seed = False

    def setUp(self):
        self.seed = RealisticSeed.load_realistic_seed()
        self.seed.procure_items()
        self.set_up_user()

    def test_sample_label(self):
        # note no login
        self.client.logout()
        url = reverse('sample-label')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    @skipIf(settings.SHIPPOP_TEST_ERR, reason="Shippop breaks, minimum order 3")
    def test_print_label(self):
        param = CreateOrderParam.example_with_valid_item()
        ros = [OrderService().create_order_no_fulfill(param) for _ in range(2)]
        for ro in ros:
            FulfilmentService().attempt_fulfill_shipment(ro.shipment)
        res = self.client.get(reverse('print-label'), {"shipments": [ro.shipment.id for ro in ros]})
        self.assertEqual(res.status_code, 200)

    def test_simple_shipment_list(self):
        res = self.client.get(reverse('simple-shipment-list'))
        self.assertEqual(res.status_code, 200)

    @skipIf(settings.SHIPPOP_TEST_ERR, reason="Shippop breaks, minimum order 3")
    def test_print_label_api_not_found(self):
        param = CreateOrderParam.example_with_valid_item()
        ros = [OrderService().create_order_no_fulfill(param) for _ in range(2)]
        for ro in ros:
            FulfilmentService().attempt_fulfill_shipment(ro.shipment)
        res = self.client.get(reverse('print-label'), {"shipments": [999888]})
        self.assertEqual(res.status_code, 404)
