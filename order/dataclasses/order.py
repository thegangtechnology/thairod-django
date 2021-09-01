from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from rest_framework.exceptions import ValidationError

from order.dataclasses.cart_item import CartItem
from order.dataclasses.doctor import Doctor
from order.dataclasses.patient import Patient
from order.dataclasses.shipping_address import ShippingAddress
from order.models import Order
from product.models import ProductVariation
from thairod.services.shippop.data import spe_postal_codes
from thairod.utils.auto_serialize import AutoSerialize


@dataclass
class CreateOrderParam(AutoSerialize):
    account: str
    doctor: Doctor
    patient: Patient
    shipping_address: ShippingAddress
    line_id: str
    session_id: str
    items: List[CartItem]

    @classmethod
    def validate_data(cls, data: CreateOrderParam) -> CreateOrderParam:
        # item
        for item in data.items:
            if not ProductVariation.objects.filter(id=item.item_id).exists():
                raise ValidationError(detail=f'Product with id {item.item_id} does not exists')
            if item.quantity < 0:
                raise ValidationError(detail=f'Quantity cannot be negative. ({item.item_id})')
        return data

    @classmethod
    def example(cls, items: Optional[List[CartItem]] = None) -> CreateOrderParam:
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

    def is_valid_order(self) -> bool:
        cid = self.patient.cid
        pv_ids = [item.item_id for item in self.items]

        def try_to_order_non_repeatable_item():
            return (ProductVariation.objects
                    .filter(id__in=pv_ids, product__non_repeatable=True)
                    .exists())

        def used_to_order_non_repeatable():
            return Order.used_to_order_non_repeatable(cid)

        return not (try_to_order_non_repeatable_item() and used_to_order_non_repeatable())


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
