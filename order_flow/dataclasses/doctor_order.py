from dataclasses import dataclass
from thairod.utils.auto_serialize import AutoSerialize
from order_flow.dataclasses.ordered_product import OrderedProductInfo
from order.dataclasses.cart_item import CartItem
from typing import List


@dataclass
class DoctorOrder(AutoSerialize):
    items: List[CartItem]

    @classmethod
    def example(cls):
        return cls(
            items=[CartItem.example()])


@dataclass
class DoctorOrderResponse(AutoSerialize):
    items: List[OrderedProductInfo]
    is_confirmed: bool

    @classmethod
    def from_doctor_order_dict(cls, doctor_order: dict, is_confirmed: bool = False):
        items = doctor_order.get('items', None)
        lst = []
        if items:
            for cart_item in items:
                lst.append(OrderedProductInfo.from_cart_item(cart_item=CartItem(**cart_item)))
        return cls(is_confirmed=is_confirmed,
                   items=lst)

    @classmethod
    def example(cls):
        return cls(
            is_confirmed=False,
            items=[OrderedProductInfo.example()])


@dataclass
class CheckoutDoctorOrderRequest(AutoSerialize):
    doctor_link_hash: str
    doctor_order: DoctorOrder

    @classmethod
    def example(cls):
        return cls(
            doctor_link_hash='vKgejBAIPFfd8vgvG45J0nO1Zx6B79c02wa9a8cD5c',
            doctor_order=DoctorOrder.example())
