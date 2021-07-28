from dataclasses import dataclass, field
from typing import List

from django.db import transaction
from rest_framework import viewsets, filters
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from address.models import Address
from order.models.order import Order, OrderStatus
from order.models.order_item import OrderItem
from order.serializers import OrderSerializer, OrderItemSerializer
from product.models import ProductVariation
from shipment.models import Shipment, TrackingStatus
from shipment.models.shipment import ShipmentStatus
from thairod.services.shippop.api import ShippopAPI
from thairod.services.shippop.data import OrderData, OrderLineData, AddressData, OrderResponse, ParcelData
from thairod.utils.auto_serialize import AutoSerialize, swagger_auto_serialize_schema
from thairod.utils.decorators import ip_whitelist
from warehouse.models import Warehouse


class OrderModelViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['receiver_name', 'receiver_address', 'receiver_tel', 'cid', 'order_time']


class OrderItemModelViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['total_price', 'shipment__title', 'product_variation__name']


@dataclass
class Doctor(AutoSerialize):
    name: str
    license: str

    @classmethod
    def example(cls):
        return cls(name='สมชาย แซ่งตั้ง', license="A123932378")


@dataclass
class Patient(AutoSerialize):
    name: str
    cid: str

    @classmethod
    def example(cls):
        return cls(name='คนป่วย รอเตียง', cid='3210987654321')


@dataclass
class ShippingAddress(AutoSerialize):
    street: str
    sub_district: str
    district: str
    province: str
    zipcode: str
    phone_number: str
    note: str

    @classmethod
    def example(cls):
        return cls(
            phone_number="08123435678",
            street='99 ถ.ราชดำเนิน',
            sub_district='ราชดำเนิน',
            district='พระนคร',
            province='กรุงเทพ',
            zipcode='12345',
            note="บ้านอยู่ชั้นสอง"
        )


@dataclass
class CartItem(AutoSerialize):
    item_id: int
    quantity: int

    @classmethod
    def example(cls):
        return cls(item_id=1, quantity=1)


@dataclass
class CreateOrderParameter(AutoSerialize):
    doctor: Doctor
    patient: Patient
    shipping_address: ShippingAddress
    line_id: str
    session_id: str
    items: List[CartItem]

    @classmethod
    def example(cls):
        return cls(doctor=Doctor.example(),
                   patient=Patient.example(),
                   shipping_address=ShippingAddress.example(),
                   line_id="steven_weinberg",
                   session_id="AAABB2134",
                   items=[CartItem.example()])


@dataclass
class CreateOrderResponse(AutoSerialize):
    success: bool
    order_id: int
    shippop_tracking_code: str = field(default='')
    courier_tracking_code: str = field(default='')

    @classmethod
    def example(cls):
        return cls(success=True,
                   order_id=10,
                   shippop_tracking_code='shippop101',
                   courier_tracking_code='c_track')


class ShippopConfirmationError(Exception):
    pass


class ShippopCreateOrderError(Exception):
    pass


class CreateOrderAPI(GenericAPIView):

    @ip_whitelist(['127.0.0.1'])
    @swagger_auto_serialize_schema(CreateOrderParameter, CreateOrderResponse)
    def post(self, request: Request, format=None) -> Response:
        param = CreateOrderParameter.from_request(request)
        service = OrderService()
        return service.crate_order(param).to_response()


class OrderService:
    def crate_order(self, param: CreateOrderParameter) -> CreateOrderResponse:
        try:
            with transaction.atomic():
                address = self.create_address(param)
                order = self.create_order(param, address)
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
            email='',
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

    def create_order(self, param: CreateOrderParameter, address: Address) -> Order:
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
