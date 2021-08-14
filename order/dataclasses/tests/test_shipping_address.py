from order.dataclasses.shipping_address import ShippingAddress
from thairod.utils.load_seed import RealisticSeed
from thairod.utils.test_util import TestCase


class TestShippingAddress(TestCase):
    with_seed = False
    def setUp(self):
        self.seed = RealisticSeed.load_realistic_seed()
        self.seed.full_production()

    def test_blank_note_is_valid(self):
        sa = ShippingAddress.example()
        sa.note = ''
        ser = ShippingAddress.serializer()
        data = ser(sa).data
        got = ser(data=data)
        self.assertTrue(got.is_valid(raise_exception=True))
