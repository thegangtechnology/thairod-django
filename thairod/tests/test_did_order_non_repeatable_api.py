from django.urls import reverse

from thairod.utils.load_seed import RealisticSeed
from thairod.utils.test_util import APITestCase
from thairod.views.ordered_non_repeatable import DidOrderNonRepeatableParam, DidOrderNonRepeatableAPI


class TestDidOrderNonRepeatable(APITestCase):
    with_seed = False

    def setUp(self):
        self.seed = RealisticSeed.load_realistic_seed()
        pv = self.seed.make_product(restricted=True)
        self.seed.order_item(pv_id=pv.id, cid='111')

    def test_do_true(self):
        param = DidOrderNonRepeatableParam(
            cid='111'
        )
        res = DidOrderNonRepeatableAPI.do(param)
        self.assertTrue(res.did_order_non_repeatable)

    def test_do_false(self):
        param = DidOrderNonRepeatableParam(
            cid='222'
        )
        res = DidOrderNonRepeatableAPI.do(param)
        self.assertFalse(res.did_order_non_repeatable)

    def test_api_true(self):
        res = self.client.get(reverse('did-order-non-repeatable'), {'cid': '111'})
        self.assertTrue(res.data['did_order_non_repeatable'])

    def test_api_false(self):
        res = self.client.get(reverse('did-order-non-repeatable'), {'cid': '222'})
        self.assertTrue(res.data['did_order_non_repeatable'])
