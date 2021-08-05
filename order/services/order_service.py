from dataclasses import dataclass
from typing import List

from django.db import transaction

from address.models import Address
from order.dataclasses.order import CreateOrderParameter, CreateOrderResponse
from order.exceptions import ShippopConfirmationError, ShippopCreateOrderError
from order.models.order import Order, OrderStatus
from order.models.order_item import OrderItem
from product.models import ProductVariation
from shipment.models import Shipment, TrackingStatus
from shipment.models.box_size import BoxSize
from shipment.models.shipment import ShipmentStatus
from thairod.services.line.line import send_line_tracking_message
from thairod.services.shippop.api import ShippopAPI
from thairod.services.shippop.data import OrderData, OrderLineData, AddressData, OrderResponse, ParcelData
from thairod.settings import SHIPPOP_EMAIL
from warehouse.models import Warehouse


@dataclass
class RawOrder:
    order: Order
    shipment: Shipment


class OrderService:

    def create_order(self, param: CreateOrderParameter) -> CreateOrderResponse:
        try:
            with transaction.atomic():
                ro = self.create_order_no_callback(param)
                return CreateOrderResponse(success=True,
                                           order_id=ro.order.id,
                                           shippop_tracking_code=ro.shipment.tracking_code,
                                           courier_tracking_code=ro.shipment.courier_tracking_code)

        except (ShippopConfirmationError, ShippopCreateOrderError):
            return CreateOrderResponse(success=False)

    def create_order_no_callback(self, param) -> RawOrder:
        ro = self.create_raw_order(param)
        shippop_order_response = self.add_order_to_shippop(ro)
        for oi in ro.shipment.orderitem_set.all():
            oi.fulfill()
        ro.shipment.status = ShipmentStatus.FULFILLED
        ro.shipment.save()
        self.update_shipment_with_shippop_booking(shippop_order_response, ro.shipment)
        self.confirm_order_with_shippop(ro)
        self.update_shipment_with_confirmation(ro.shipment)
        return ro

    def create_raw_order(self, param: CreateOrderParameter) -> RawOrder:
        address = self.create_address(param)
        order = self.create_order_from_param(param, address)
        shipment = self.create_shipment(param, order)
        self.create_order_items(param, shipment)
        return RawOrder(order=order, shipment=shipment)

    def add_order_to_shippop(self, ro: RawOrder) -> OrderResponse:
        shippop_api = ShippopAPI()
        response = shippop_api.create_order(self.create_order_data(ro.shipment))

        if not response.status:
            raise ShippopCreateOrderError()
        return response

    def confirm_order_with_shippop(self, ro: RawOrder):
        shippop_api = ShippopAPI()

        confirm_success = shippop_api.confirm_order(ro.shipment.shippop_purchase_id)
        if not confirm_success:
            raise ShippopConfirmationError()

    def notify_user_with_tracking(self, ro: RawOrder, param: CreateOrderParameter):
        if param.line_id:
            send_line_tracking_message(line_uid=param.line_id,
                                       name=param.patient.name,
                                       shippop_tracking_code=ro.shipment.tracking_code)

    # TODO: Decouple these
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

    def crate_shippop_address_data(self, param: CreateOrderParameter) -> AddressData:
        return AddressData(
            name=param.patient.name,
            address=param.shipping_address.street,
            state=param.shipping_address.district,
            district=param.shipping_address.sub_district,
            postcode=param.shipping_address.zipcode,
            tel=param.shipping_address.phone_number
        )

    def create_address(self, param: CreateOrderParameter) -> Address:
        return Address.objects.create(
            name=param.patient.name,
            house_number=param.shipping_address.street,
            subdistrict=param.shipping_address.sub_district,
            district=param.shipping_address.district,
            province=param.shipping_address.province,
            postal_code=param.shipping_address.zipcode,
            country='Thailand',
            telno=param.shipping_address.phone_number,
            note=param.shipping_address.note
        )

    def create_order_from_param(self, param: CreateOrderParameter, address: Address) -> Order:
        return Order.objects.create(
            status=OrderStatus.STARTED,
            receiver_address=address,
            cid=param.patient.cid,
            orderer_name=param.doctor.name,
            orderer_license=param.doctor.license
        )

    def create_shipment(self, param: CreateOrderParameter, order: Order) -> Shipment:
        return Shipment.objects.create(
            warehouse=Warehouse.default_warehouse(),
            shipping_method='SHIPPOP',
            label_printed=False,
            order=order,
            shippop_purchase_id=None,
            status=ShipmentStatus.CREATED,
            box_size=self.determine_box_size(param)
        )

    def determine_box_size(self, param: CreateOrderParameter) -> BoxSize:
        # Fix this in the future to do something meaningful
        return BoxSize.get_default_box()

    def create_order_items(self, param: CreateOrderParameter,
                           shipment: Shipment) -> List[OrderItem]:
        ret = []

        for item in param.items:
            product = ProductVariation.objects.get(pk=item.item_id)
            order_item = OrderItem.objects.create(
                shipment=shipment,
                product_variation=product,
                quantity=item.quantity,
                total_price=product.price * item.quantity
            )
            ret.append(order_item)
        return ret
