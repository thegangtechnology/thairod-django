from order.dataclasses.shipping_address import ShippingAddress
from thairod.utils.test_util import TestCase


class TestShippingAddress(TestCase):
    with_seed = False

    def test_shipping_address_bad_zipcode(self):
        s = ShippingAddress.example()
        serializer = ShippingAddress.serializer()
        data = serializer(s).data
        data['zipcode'] = 'aaaaa'
        self.assertFalse(serializer(data=data).is_valid())
