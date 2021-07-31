from django.urls import reverse

from order.dataclasses.order import CreateOrderParameter
from order.services.order_service import OrderService
from thairod.utils.test_util import APITestCase


class TestPrintLabelAPI(APITestCase):
    patch_shippop = False

    def test_sample_label(self):
        # note no login
        url = reverse('sample-label')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_print_label(self):
        self.set_up_user()
        param = CreateOrderParameter.example_with_valid_item()
        ros = [OrderService().create_order_no_callback(param) for _ in range(2)]
        res = self.client.get(reverse('print-label'), {"shipments": [ro.shipment.id for ro in ros]})
        self.assertEqual(res.status_code, 200)

    def test_simple_shipment_list(self):
        self.set_up_user()
        res = self.client.get(reverse('simple-shipment-list'))
        self.assertEqual(res.status_code, 200)