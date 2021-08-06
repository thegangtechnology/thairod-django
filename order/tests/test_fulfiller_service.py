from order.models.order_item import FulfilmentStatus
from order.services.fulfiller_service import FulFilmentService
from shipment.models import Shipment
from shipment.models.box_size import BoxSize
from thairod.services.shippop.data import ParcelData
from thairod.utils.load_seed import RealisticSeed
from thairod.utils.test_util import TestCase


class TestFulFillerService(TestCase):
    with_seed = False

    def setUp(self):
        self.seed = RealisticSeed.load_realistic_seed()
        self.seed.full_production()

    def test_get_pending_orders(self):
        FulFilmentService().get_pending_order_items()

    def test_parcel_adapter(self):
        box = BoxSize(name="G2", width=1, height=2, length=3)
        parcel = FulFilmentService().parcel_adapter(box, name="test")
        expect = ParcelData(name="test", width=1, height=2, length=3)
        self.assertEqual(
            parcel, expect
        )

    def test_attempt_fulfill_shipment_on_has_stock(self):
        shipment: Shipment = Shipment.pending_shipments().first()
        FulFilmentService().attempt_fulfill_shipment(shipment)
        for oi in shipment.orderitem_set.all():
            self.assertEqual(oi.fulfilment_status, FulfilmentStatus.FULFILLED)
