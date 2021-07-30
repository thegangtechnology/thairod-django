from typing import List
from django.db import transaction
from address.models import Address
from order.models.order import Order, OrderStatus
from order.models.order_item import OrderItem
from product.models import ProductVariation
from shipment.models import Shipment, TrackingStatus
from shipment.models.shipment import ShipmentStatus
from thairod.services.line.line import send_line_tracking_message
from thairod.services.shippop.api import ShippopAPI
from thairod.services.shippop.data import OrderData, OrderLineData, AddressData, OrderResponse, ParcelData
from thairod.settings import SHIPPOP_EMAIL
from warehouse.models import Warehouse
from order.dataclasses.order import CreateOrderParameter, CreateOrderResponse
from order.exceptions import ShippopConfirmationError, ShippopCreateOrderError


class OrderService:
    def create_order(self, param: CreateOrderParameter) -> CreateOrderResponse:
        try:
            with transaction.atomic():
                address = self.create_address(param)
                order = self.create_order_from_param(param, address)
                shipment = self.create_shipment(param, order)
                self.create_order_items(param, shipment)
                shippop_api = ShippopAPI()
                response = shippop_api.create_order(self.create_order_data(shipment))

                if not response.status:
                    raise ShippopCreateOrderError()

                self.update_shipment_with_shippop_booking(response, shipment)

                confirm_success = shippop_api.confirm_order(shipment.shippop_purchase_id)
                if not confirm_success:
                    raise ShippopConfirmationError()
                self.update_shipment_with_confirmation(shipment)
                if param.line_id:
                    send_line_tracking_message(line_uid=param.line_id,
                                               name=param.patient.name,
                                               shippop_tracking_code=shipment.tracking_code)
                return CreateOrderResponse(success=True,
                                           order_id=order.id,
                                           shippop_tracking_code=shipment.tracking_code,
                                           courier_tracking_code=shipment.courier_tracking_code)

        except (ShippopConfirmationError, ShippopCreateOrderError):
            return CreateOrderResponse(success=False)

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
                    parcel=ParcelData()
                )
            ],

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
            receiver_name=param.patient.name,
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
            status=ShipmentStatus.CREATED
        )

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
