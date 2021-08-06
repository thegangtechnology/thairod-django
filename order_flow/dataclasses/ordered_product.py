from dataclasses import dataclass
from thairod.utils.auto_serialize import AutoSerialize
from product.models.product_variation import ProductVariationUnit, ProductVariation
from order.dataclasses.cart_item import CartItem


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
