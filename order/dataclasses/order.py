from dataclasses import dataclass, field
from thairod.utils.auto_serialize import AutoSerialize
from order.dataclasses.doctor import Doctor
from order.dataclasses.shipping_address import ShippingAddress
from order.dataclasses.patient import Patient
from order.dataclasses.cart_item import CartItem
from typing import List


@dataclass
class CreateOrderParameter(AutoSerialize):
    account: str
    doctor: Doctor
    patient: Patient
    shipping_address: ShippingAddress
    line_id: str
    session_id: str
    items: List[CartItem]

    @classmethod
    def example(cls):
        return cls(
            account='frappet',
            doctor=Doctor.example(),
            patient=Patient.example(),
            shipping_address=ShippingAddress.example(),
            line_id="",
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