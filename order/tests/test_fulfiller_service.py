from order.services.fulfiller_service import FulFilmentService
from shipment.models.box_size import BoxSize
from thairod.services.shippop.data import ParcelData
from thairod.utils.test_util import TestCase


class TestFulFillerService(TestCase):

    def test_get_pending_orders(self):
        FulFilmentService().get_pending_order_items()

    def test_parcel_adapter(self):
        box = BoxSize(name="G2", width=1, height=2, length=3)
        parcel = FulFilmentService().parcel_adapter(box, name="test")
        expect = ParcelData(name="test", width=1, height=2, length=3)
        self.assertEqual(
            parcel, expect
        )
