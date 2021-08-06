import logging
from typing import Iterable, DefaultDict

from order.exceptions import ShippopConfirmationError, ShippopCreateOrderError
from order.models import Order
from order.models.order_item import FulfilmentStatus, OrderItem
from shipment.models import Shipment, TrackingStatus
from shipment.models.box_size import BoxSize
from shipment.models.shipment import ShipmentStatus
from thairod.services.line.line import send_line_tracking_message
from thairod.services.shippop.api import ShippopAPI
from thairod.services.shippop.data import ParcelData, AddressData, OrderLineData, OrderData, OrderResponse
from thairod.services.stock.stock import StockService, StockInfo
from thairod.settings import SHIPPOP_EMAIL

ItemVariationID = int
StockCount = int

logger = logging.getLogger(__name__)


class FulFilmentService:

    def attempt_fulfill_shipment(self, shipment: Shipment):
        # temporary this thing has a race condition on stock checking
        for oi in shipment.orderitem_set.all():
            stock = StockService().get_single_stock(oi.product_variation_id)
            if stock.current_total > 0:
                oi.fulfill()
        self.book_and_confirm_shipment(shipment)

    def fulfill_pending_order_items(self):
        order_items = OrderItem.sorted_pending_order_items()
        stock_map = StockService().get_all_stock_map()

        for oi in order_items:
            self._attempt_fulfill_orderitem(oi, stock_map)

    def book_and_confirm_all_pending_shipments(self):
        shipments = Shipment.ready_to_book_shipments()

        for shipment in shipments:
            self.book_and_confirm_shipment(shipment)

    def get_pending_order_items(self) -> Iterable[Order]:
        ret = Order.objects.filter(
            shipment__orderitem__fulfilment_status=FulfilmentStatus.PENDING,
        ).order_by('order_time').all()
        return ret

    def book_and_confirm_shipment(self, shipment):
        if not shipment.is_ready_to_book:
            logger.info(f'Attempt to book and confirm non fulfilled shipment {shipment.id}')
            return

        res = self.add_shipment_to_shippop(shipment)
        self.update_shipment_with_shippop_booking(res, shipment)

        self.confirm_shipment_with_shippop(shipment)
        self.update_shipment_with_confirmation(shipment)

        self.order_confirmed_call_back(shipment)
        logger.info(f'Book and Confirm Shipment id: f{shipment.id}')

    def order_confirmed_call_back(self, shipment: Shipment):
        self.notify_user_with_tracking(shipment)

    def _attempt_fulfill_orderitem(self, oi: OrderItem, stock_map: DefaultDict[int, StockInfo]) -> bool:
        pv_id: int = oi.product_variation_id
        if stock_map[pv_id].current_total > 0:
            oi.fulfill()
            stock_map[pv_id].fulfilled += 1
            return True
        else:
            return False

    def add_shipment_to_shippop(self, shipment: Shipment) -> OrderResponse:
        shippop_api = ShippopAPI()
        response = shippop_api.create_order(self.create_order_data(shipment))

        if not response.status:
            raise ShippopCreateOrderError()
        return response

    def confirm_shipment_with_shippop(self, shipment: Shipment):
        shippop_api = ShippopAPI()

        confirm_success = shippop_api.confirm_order(shipment.shippop_purchase_id)
        if not confirm_success:
            raise ShippopConfirmationError()

    def notify_user_with_tracking(self, shipment: Shipment):
        line_id = shipment.order.line_id
        if line_id:
            send_line_tracking_message(line_uid=line_id,
                                       name=shipment.order.receiver_address.name,
                                       shippop_tracking_code=shipment.tracking_code)

    def update_shipment_with_confirmation(self, shipment: Shipment):
        shipment.status = ShipmentStatus.CONFIRMED
        shipment.save()

    def update_shipment_with_shippop_booking(self, response: OrderResponse,
                                             shipment: Shipment):
        self.create_tracking_status(response, shipment)
        shipment.tracking_code = response.lines[0].tracking_code
        shipment.shippop_purchase_id = response.purchase_id
        shipment.courier_tracking_id = response.lines[0].courier_tracking_code
        shipment.status = ShipmentStatus.BOOKED
        shipment.save()

    def create_tracking_status(self, response: OrderResponse,
                               shipment: Shipment) -> TrackingStatus:
        return TrackingStatus.objects.create(
            status=response.status,
            price=response.lines[0].price,
            discount=response.lines[0].discount,
            courier_code=response.lines[0].courier_code,
            shipment=shipment,
            courier_tracking_code=response.lines[0].tracking_code
        )

    def create_order_data(self, shipment: Shipment) -> OrderData:
        return OrderData(
            email=SHIPPOP_EMAIL,
            success_url='',
            fail_url='',
            data=[
                OrderLineData(
                    from_address=AddressData.from_address_model(
                        shipment.warehouse.address
                    ),
                    to_address=AddressData.from_address_model(shipment.order.receiver_address),
                    parcel=self.parcel_adapter(box_size=shipment.box_size)
                )
            ],
        )

    def parcel_adapter(self, box_size: BoxSize, name="ไทยรอด") -> ParcelData:
        return ParcelData(
            name=name,
            weight=1,
            width=box_size.width,
            length=box_size.length,
            height=box_size.height
        )
