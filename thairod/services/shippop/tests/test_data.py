from django.test import TestCase
from thairod.services.shippop.tests import load_test_data


class ShippopDataTest(TestCase):
    def setUp(self):
        obj = load_test_data()
        self.order_data = obj["order_data"]
        self.order_lines = obj["order_lines"]
        self.to_address = obj["to_address"]
        self.from_address = obj["from_address"]
        self.parcel = obj["parcel"]

    def test_order_data_request_to_dict(self):
        req = self.order_data.to_request_dict()
        self.assertIn('email', req.keys())
        self.assertIn('success', req.keys())
        self.assertIn('fail', req.keys())
        self.assertIn('data', req.keys())

    def test_order_line_data_request_to_dict(self):
        req = self.order_lines[0].to_request_dict()
        self.assertIn('from', req.keys())
        self.assertIn('to', req.keys())
        self.assertIn('parcel', req.keys())
        self.assertIn('courier_code', req.keys())

    def test_address_data_request_to_dict(self):
        req = self.from_address.to_request_dict()
        self.assertIn("name", req.keys())
        self.assertIn("address", req.keys())
        self.assertIn("district", req.keys())
        self.assertIn("state", req.keys())
        self.assertIn("province", req.keys())
        self.assertIn("postcode", req.keys())
        self.assertIn("tel", req.keys())
