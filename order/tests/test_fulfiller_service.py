from order.services.fulfiller_service import FulFillerService
from thairod.utils.test_util import TestCase


class TestFulFillerService(TestCase):
    def test_fulfill_orders(self):
        FulFillerService().fulfill_orders()
