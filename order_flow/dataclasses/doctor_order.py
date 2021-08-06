from dataclasses import dataclass
from thairod.utils.auto_serialize import AutoSerialize
from product.models.product_variation import ProductVariationUnit, ProductVariation
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
class OrderedProductInfo(AutoSerialize):
    id: int
    name: str
    price: int
    description: str  # product variation description
    product_description: str  # product description
    unit: str
    quantity: int

    @classmethod
    def from_cart_item(cls, cart_item: CartItem):
        product_variation = ProductVariation.objects.get(pk=cart_item.item_id)
        return cls(id=product_variation.id,
                   name=product_variation.name,
                   price=product_variation.price,
                   description=product_variation.description,
                   product_description=product_variation.product.description,
                   unit=product_variation.unit,
                   quantity=cart_item.quantity
                   )

    @classmethod
    def example(cls):
        return cls(id=1,
                   name='product variation 1',
                   price=10,
                   description='product variation 1 description',
                   product_description='product description',
                   unit=ProductVariationUnit.PIECES.value,
                   quantity=5)


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
