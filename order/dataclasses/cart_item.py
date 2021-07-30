from dataclasses import dataclass
from thairod.utils.auto_serialize import AutoSerialize
from typing import List


@dataclass
class CartItem(AutoSerialize):
    item_id: int
    quantity: int

    @classmethod
    def example(cls):
        return cls(item_id=1, quantity=1)

    @classmethod
    def from_doctor_order(cls, order) -> 'List[CartItem]':
        items = order.get('items', None)
        lst = []
        if items:
            for item in order.get('items'):
                lst.append(CartItem(**item))
        return lst
