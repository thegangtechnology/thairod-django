from dataclasses import dataclass
from typing import List

from django.db import transaction
from rest_framework.exceptions import ValidationError

from address.models import Address
from order.dataclasses.order import CreateOrderParam, CreateOrderResponse
from order.exceptions import ShippopConfirmationError, ShippopCreateOrderError
from order.models.order import Order, OrderStatus
from order.models.order_item import OrderItem
from order.services.fulfiller_service import FulfilmentService
from product.models import ProductVariation
from shipment.models import Shipment
from shipment.models.box_size import BoxSize
from shipment.models.shipment import ShipmentStatus
from thairod.services.line.line import send_line_order_created_message
from thairod.services.shippop.data import AddressData
from warehouse.models import Warehouse


@dataclass
class RawOrder:
    order: Order
    shipment: Shipment


class OrderService:

    def create_order(self, param: CreateOrderParam, auto_fulfill=True) -> CreateOrderResponse:
        try:
            with transaction.atomic():
                ro = self.create_order_no_fulfill(param)
            self.on_order_created_callback(ro.order)
            if auto_fulfill:
                FulfilmentService().attempt_fulfill_shipment(ro.shipment)
            return CreateOrderResponse(success=True,
                                       order_id=ro.order.id,
                                       shippop_tracking_code=ro.shipment.tracking_code,
                                       courier_tracking_code=ro.shipment.courier_tracking_code)

        except (ShippopConfirmationError, ShippopCreateOrderError):
            return CreateOrderResponse(success=False)

    def create_order_no_fulfill(self, param: CreateOrderParam) -> RawOrder:
        if not param.is_valid_order():
            raise ValidationError(detail={'cid': 'this cid has already ordered restricted item'})
        ro = self.create_raw_order(param)
        return ro

    def on_order_created_callback(self, order: Order):
        send_line_order_created_message(line_uid=order.line_id,
                                        name=order.receiver_address.name,
                                        order_id=order.id)

    def create_raw_order(self, param: CreateOrderParam) -> RawOrder:
        address = self.create_address(param)
        order = self.create_order_from_param(param, address)
        shipment = self.create_shipment(param, order)
        self.create_order_items(param, shipment)
        return RawOrder(order=order, shipment=shipment)

    def crate_shippop_address_data(self, param: CreateOrderParam) -> AddressData:
        return AddressData(
            name=param.patient.name,
            address=param.shipping_address.street,
            state=param.shipping_address.district,
            district=param.shipping_address.sub_district,
            postcode=param.shipping_address.zipcode,
            tel=param.shipping_address.phone_number
        )

    def create_address(self, param: CreateOrderParam) -> Address:
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

    def create_order_from_param(self, param: CreateOrderParam, address: Address) -> Order:
        return Order.objects.create(
            status=OrderStatus.STARTED,
            receiver_address=address,
            cid=param.patient.cid,
            orderer_name=param.doctor.name,
            orderer_license=param.doctor.license,
            line_id=param.line_id,
            telemed_session_id=param.session_id
        )

    def create_shipment(self, param: CreateOrderParam, order: Order) -> Shipment:
        return Shipment.objects.create(
            warehouse=Warehouse.default_warehouse(),
            shipping_method='SHIPPOP',
            label_printed=False,
            order=order,
            shippop_purchase_id=None,
            status=ShipmentStatus.CREATED,
            box_size=self.determine_box_size(param)
        )

    def determine_box_size(self, param: CreateOrderParam) -> BoxSize:
        pv_ids = [it.item_id for it in param.items]
        return BoxSize.determine_box_size_by_pv_ids(pv_ids)

    def create_order_items(self, param: CreateOrderParam,
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
