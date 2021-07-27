from unittest import TestCase

from thairod.services.shippop.api import ShippopAPI
from thairod.services.shippop.data import OrderResponse, TrackingData, Pricing
from thairod.services.shippop.tests import load_test_data


class ShippopAPITest(TestCase):
    def setUp(self) -> None:
        obj = load_test_data()
        self.order_data = obj["order_data"]
        self.order_lines = obj["order_lines"]
        self.to_address = obj["to_address"]
        self.from_address = obj["from_address"]
        self.parcel = obj["parcel"]
        self.shippop_api = ShippopAPI()
        self.shippop_order = self.shippop_api.create_order(order_data=self.order_data)

    def test_create_order(self):
        response = self.shippop_api.create_order(order_data=self.order_data)
        self.assertEqual(type(response), OrderResponse)
        self.assertEqual(len(response.lines), 1)

    def test_confirm_order(self):
        self.assertEqual(self.shippop_api.confirm_order(purchase_id=self.shippop_order.purchase_id), True)

    def test_get_order_detail(self):
        response = self.shippop_api.get_order_detail(purchase_id=self.shippop_order.purchase_id)
        self.assertEqual(type(response), OrderResponse)
        self.assertEqual(len(response.lines), 1)

    def test_get_tracking_data(self):
        tracking_code = self.shippop_order.lines[0].tracking_code
        self.assertEqual(type(self.shippop_api.get_tracking_data(tracking_code=tracking_code)), TrackingData)

    def test_get_pricing(self):
        response = self.shippop_api.get_pricing(order_data=self.order_data)
        self.assertEqual(len(response) > 0, True)
        self.assertEqual(type(response[0]), Pricing)

    def test_get_label(self):
        self.shippop_api.confirm_order(purchase_id=self.shippop_order.purchase_id)
        response = self.shippop_api.get_label(purchase_id=self.shippop_order.purchase_id)
        self.assertEqual(type(response), str)

