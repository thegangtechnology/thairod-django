from order.models import Order
from order.models.order_item import FulfilmentStatus, OrderItem
from order.services.fulfiller_service import FulfilmentService, UnsupportedZipCode
from shipment.models import Shipment
from shipment.models.box_size import BoxSize
from shipment.models.shipment import ShipmentStatus
from thairod.services.shippop.data import ParcelData
from thairod.utils import tzaware
from thairod.utils.load_seed import RealisticSeed
from thairod.utils.test_util import TestCase


class TestFulfilmentService(TestCase):
    with_seed = False

    def setUp(self):
        self.seed = RealisticSeed.load_realistic_seed()
        self.seed.full_production()

    def test_get_pending_orders(self):
        FulfilmentService().get_pending_order_items()

    def test_parcel_adapter(self):
        box = BoxSize(name="G2", width=1, height=2, length=3)
        parcel = FulfilmentService().parcel_adapter(box, name="test")
        expect = ParcelData(name="test", width=1, height=2, length=3)
        self.assertEqual(
            parcel, expect
        )

    def test_attempt_fulfill_shipment_on_has_stock(self):
        shipment: Shipment = Shipment.pending_shipments().first()
        self.line_mock.reset_mock()
        FulfilmentService().attempt_fulfill_shipment(shipment)
        for oi in shipment.orderitem_set.all():
            self.assertEqual(oi.fulfilment_status, FulfilmentStatus.FULFILLED)
        diff = tzaware.now() - shipment.fulfilled_date
        shipment.refresh_from_db()
        self.assertLess(diff.total_seconds(), 10)
        self.assertEqual(shipment.status, ShipmentStatus.CONFIRMED)
        self.assertIn('auto', shipment.batch.name)
        self.assertEqual(shipment.courier_code, 'SPE')
        self.line_mock.assert_called_once()  # line message sent

    def test_attempt_fulfill_shipment_on_no_stock(self):
        pv = self.seed.make_product()
        ro = self.seed.order_item_no_fulfill(pv.id, '111')
        order = Order.objects.get(pk=ro.order.id)
        success = FulfilmentService().attempt_fulfill_shipment(order.shipment_set.first())
        self.assertFalse(success)

    def test_attempt_fulfill_shipment_funny_zipcode(self):
        pv = self.seed.make_product()
        self.seed.procure_item(pv.id, 10)
        ro = self.seed.order_item_no_fulfill(pv.id, '111')
        order = Order.objects.get(pk=ro.order.id)

        order.receiver_address.postal_code = '50100'
        order.receiver_address.province = 'เชียงใหม่'
        order.receiver_address.save()
        # for some reason they dont' reject SPE to อ่างทอง
        FulfilmentService().attempt_fulfill_shipment(order.shipment_set.first())

    def test_fulfill_pending_order_items(self):
        begin = len(OrderItem.sorted_pending_order_items())
        FulfilmentService().fulfill_pending_order_items()
        end = len(OrderItem.sorted_pending_order_items())
        self.assertLess(end, begin)

    def test_fulfill_shipments_auto_fulfilled(self):
        begin = Shipment.objects.filter(status=ShipmentStatus.FULFILLED).count()
        FulfilmentService().fulfill_pending_order_items()
        end = Shipment.objects.filter(status=ShipmentStatus.FULFILLED).count()
        self.assertLess(begin, end)

    def test_process_all_orders(self):
        fulfilled_oi_before = OrderItem.objects.exclude(fulfilment_status=FulfilmentStatus.PENDING).count()
        fulfilled_shipment_before = Shipment.objects.exclude(status=ShipmentStatus.CREATED).count()
        FulfilmentService().process_all_orders()
        fulfilled_oi_after = OrderItem.objects.exclude(fulfilment_status=FulfilmentStatus.PENDING).count()
        fulfilled_shipment_after = Shipment.objects.exclude(status=ShipmentStatus.CREATED).count()
        self.assertGreater(fulfilled_oi_after, fulfilled_oi_before)
        self.assertGreater(fulfilled_shipment_after, fulfilled_shipment_before)
