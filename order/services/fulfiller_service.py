import logging
from typing import Iterable, DefaultDict, List

from django.db import transaction

from order.exceptions import ShippopConfirmationError
from order.models import Order
from order.models.order_item import FulfilmentStatus, OrderItem
from shipment.dataclasses.batch_shipment import AssignBatchToShipmentRequest
from shipment.models import Shipment, TrackingStatus, BatchShipment
from shipment.models.box_size import BoxSize
from shipment.models.shipment import ShipmentStatus
from shipment.services.batch_shipment_service import BatchShipmentService
from thairod.services.line.line import send_line_tracking_message
from thairod.services.shippop.api import ShippopAPI
from thairod.services.shippop.data import ParcelData, AddressData, OrderLineData, OrderData, OrderResponse, \
    spe_postal_codes
from thairod.services.stock.stock import StockService, StockInfo
from thairod.settings import SHIPPOP_EMAIL
from thairod.utils import tzaware
from thairod.utils.exceptions import ShippopAPIException

ItemVariationID = int
StockCount = int

logger = logging.getLogger(__name__)


class FulFilmentException(Exception):
    pass


class UnsupportedZipCode(FulFilmentException):
    pass


class FulfilmentService:

    def attempt_fulfill_shipment(self, shipment: Shipment) -> bool:
        # temporary this thing has a race condition on stock checking
        for oi in shipment.orderitem_set.all():
            self.attempt_to_fulfill_orderitem(oi)
        if shipment.is_ready_to_book:
            return self.book_and_confirm_shipment(shipment)
        else:
            return False

    def fulfill_pending_order_items(self):
        order_items: Iterable[OrderItem] = OrderItem.sorted_pending_order_items()
        stock_map = StockService().get_all_stock_map()

        for oi in order_items:
            success = self.attempt_to_fulfill_orderitem(oi, stock_map)
            if success:
                self.attempt_to_mark_shipment_fulfilled(oi.shipment)

    def process_all_orders(self):
        self.fulfill_pending_order_items()
        self.mark_all_ready_fulfill_shipment()
        self.book_and_confirm_all_pending_shipments()

    def mark_all_ready_fulfill_shipment(self):
        shipments = Shipment.ready_to_fulfill_shipments()
        for shipment in shipments:
            self.attempt_to_mark_shipment_fulfilled(shipment)

    def attempt_to_mark_shipment_fulfilled(self, shipment: Shipment) -> bool:
        if shipment.is_ready_to_fulfill:
            shipment.mark_fulfilled()
            return True
        else:
            return False

    def book_and_confirm_all_pending_shipments(self):
        shipments = Shipment.ready_to_book_shipments()
        for shipment in shipments:
            try:
                self.book_and_confirm_shipment(shipment)
            except ShippopAPIException as e:
                logger.error(f'Book and Confirm Fail for {shipment.id}')
                logger.error(e.detail)

    def get_pending_order_items(self) -> Iterable[Order]:
        ret = Order.objects.filter(
            shipment__orderitem__fulfilment_status=FulfilmentStatus.PENDING,
        ).order_by('order_time').all()
        return ret

    def book_and_confirm_shipment(self, shipment) -> bool:
        if not shipment.is_ready_to_book:
            logger.info(f'Attempt to book and confirm non fulfilled shipment {shipment.id}')
            return False
        with transaction.atomic():
            res = self.book_shipment_with_shippop([shipment])
            self.update_shipment_with_shippop_booking(res, shipment)

        with transaction.atomic():
            self.confirm_shipment_with_shippop(shipment)
            self.update_shipment_with_confirmation(shipment)

        with transaction.atomic():
            self.put_shipment_in_auto_batch(shipment)
            self.order_confirmed_call_back(shipment)

        logger.info(f'Book and Confirm Shipment id: {shipment.id}')
        return True

    def put_shipment_in_auto_batch(self, shipment: Shipment):
        BatchShipmentService.assign_batch_to_shipments(AssignBatchToShipmentRequest(
            batch_name=BatchShipment.generate_auto_batch_name(),
            shipments=[shipment.id]
        ))

    def order_confirmed_call_back(self, shipment: Shipment):
        self.notify_user_with_tracking(shipment)

    def attempt_to_fulfill_orderitem(self, oi: OrderItem, stock_map: DefaultDict[int, StockInfo] = None) -> bool:
        if oi.fulfilment_status != FulfilmentStatus.PENDING:
            return False
        pv_id: int = oi.product_variation_id
        stock = stock_map[pv_id] if stock_map is not None else StockService().get_single_stock(pv_id)
        if stock.current_total() >= oi.quantity:
            oi.fulfill()
            stock.fulfilled += oi.quantity
            return True
        else:
            return False

    def book_shipment_with_shippop(self, shipments: List[Shipment]):
        shippop_api = ShippopAPI()
        response = shippop_api.create_order(self.create_order_data(shipments))
        # some of them bound to fail
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
        shipment.shippop_confirm_date_time = tzaware.now()
        shipment.save()

    def update_shipment_with_shippop_booking(self, response: OrderResponse,
                                             shipment: Shipment):
        self.create_tracking_status(response, shipment)
        shipment.tracking_code = response.lines[0].tracking_code
        shipment.courier_code = response.lines[0].courier_code
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

    def create_order_data(self, shipments: List[Shipment]) -> OrderData:
        return OrderData(
            email=SHIPPOP_EMAIL,
            success_url='',
            fail_url='',
            data=[
                OrderLineData(
                    courier_code=self.determine_courier_code(shipment),
                    from_address=AddressData.from_address_model(
                        shipment.warehouse.address
                    ),
                    to_address=AddressData.from_address_model(shipment.order.receiver_address),
                    parcel=self.parcel_adapter(box_size=shipment.box_size)
                )
                for shipment in shipments
            ],
        )

    def determine_courier_code(self, shipment: Shipment):
        zip_code = shipment.order.receiver_address.postal_code
        if zip_code in spe_postal_codes:
            return 'SPE'
        else:
            raise UnsupportedZipCode(zip_code)

    def parcel_adapter(self, box_size: BoxSize, name="ไทยรอด") -> ParcelData:
        return ParcelData(
            name=name,
            weight=1,
            width=box_size.width,
            length=box_size.length,
            height=box_size.height
        )
