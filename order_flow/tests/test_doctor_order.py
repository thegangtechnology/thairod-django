from order_flow.dataclasses import DoctorOrderResponse
from thairod.utils.load_seed import load_realistic_seed
from thairod.utils.test_util import TestCase


class TestDoctorOrder(TestCase):

    def setUp(self):
        seed = load_realistic_seed()
        self.seed = seed

    def test_doctor_order_response(self):
        items = {'items': []}
        doctor_order_response = DoctorOrderResponse.from_doctor_order_dict(items, is_confirmed=False)
        assert len(doctor_order_response.items) == 0
        items = {'items': [{'item_id': self.seed.product_variations[0].id,
                            'quantity': 10}]}
        doctor_order_response = DoctorOrderResponse.from_doctor_order_dict(items, is_confirmed=False)
        assert len(doctor_order_response.items) == 1
        assert doctor_order_response.items[0].id == self.seed.product_variations[0].id
        assert doctor_order_response.items[0].quantity == 10
        assert doctor_order_response.items[0].description == self.seed.product_variations[0].description
