from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from order.dataclasses.cart_item import CartItem
from order.dataclasses.doctor import Doctor
from order.dataclasses.patient import Patient
from order.dataclasses.shipping_address import ShippingAddress
from product.models import ProductVariation
from thairod.utils.auto_serialize import AutoSerialize


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
    def example(cls, items: Optional[List[CartItem]] = None) -> CreateOrderParameter:
        return cls(
            account='frappet',
            doctor=Doctor.example(),
            patient=Patient.example(),
            shipping_address=ShippingAddress.example(),
            line_id="12321",
            session_id="AAABB2134",
            items=[CartItem.example()] if items is None else items)

    @classmethod
    def example_with_valid_item(cls):
        ret = cls.example()
        for item in ret.items:
            item.item_id = ProductVariation.objects.first().id
        return ret


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
