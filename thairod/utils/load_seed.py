from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from django_seed import Seed

from address.models import Address
from order.dataclasses.cart_item import CartItem
from order.models import Order, OrderItem
from order.services.order_service import RawOrder
from order.views import OrderService, CreateOrderParameter
from procurement.models import Procurement
from product.models import ProductVariation, Product, ProductImage
from shipment.models import Shipment, TrackingStatus, BatchShipment
from shipment.models.box_size import BoxSize
from stock_adjustment.models import StockAdjustment
from user.models import User
from warehouse.models import Warehouse


def load_seed():
    seeder = Seed.seeder()

    seeder.add_entity(Address, 3, {
        'postal_code': lambda x: 10110
    })
    seeder.execute(turn_off_auto_now=False)

    seeder.add_entity(Warehouse, 4, {
        'address': Address.objects.first()
    })

    seeder.add_entity(Product, 1)
    seeder.execute(turn_off_auto_now=False)
    seeder.add_entity(ProductImage, 1, {
        'product': Product.objects.first()
    })
    seeder.execute(turn_off_auto_now=False)
    seeder.add_entity(ProductVariation, 3, {
        'product': Product.objects.first()
    })
    seeder.execute(turn_off_auto_now=False)
    seeder.add_entity(OrderItem, 5)
    seeder.add_entity(Order, 5)
    seeder.execute(turn_off_auto_now=False)
    seeder.add_entity(Shipment, 5, {
        'warehouse': Warehouse.objects.first(),
        'box_size': BoxSize.objects.first()
    })
    seeder.execute(turn_off_auto_now=False)
    seeder.add_entity(TrackingStatus, 1, {
        'shipment': Shipment.objects.first()
    })
    seeder.add_entity(Procurement, 1, {
        'product_variation': ProductVariation.objects.first(),
        'warehouse': Warehouse.objects.first()
    })
    seeder.add_entity(StockAdjustment, 1, {
        'warehouse': Warehouse.objects.first(),
        'product_variation': ProductVariation.objects.first()
    })
    seeder.add_entity(User, 1)
    seeder.add_entity(BatchShipment, 1)
    seeder.execute(turn_off_auto_now=False)


@dataclass
class RealisticSeed:
    warehouses: List[Warehouse] = field(default_factory=list)
    products: List[Product] = field(default_factory=list)
    product_variations: List[ProductVariation] = field(default_factory=list)

    @classmethod
    def load_realistic_seed(cls) -> RealisticSeed:
        """A Warehouse and two products

        Returns:

        """
        seed = RealisticSeed()
        warehouse = Warehouse.example()
        warehouse.address.save()
        warehouse.save()
        seed.warehouses.append(warehouse)

        product = Product.example()
        product.save()
        seed.products.append(product)

        product_variation = ProductVariation.example()
        product_variation.product = product
        product_variation.save()

        product_variation2 = ProductVariation.example()
        product_variation2.product = product
        product_variation2.save()

        seed.product_variations.append(product_variation)
        seed.product_variations.append(product_variation2)
        return seed

    def full_production(self):
        self.procure_items()
        self.some_adjustment()
        self.some_order()

    def procure_items(self) -> List[Procurement]:
        p_map = {
            self.product_variations[0].id: [10, 20],
            self.product_variations[1].id: [10, 30],
        }
        ret = []
        for pv_id, quantities in p_map.items():
            for quantity in quantities:
                proc = Procurement.objects.create(
                    product_variation_id=pv_id,
                    warehouse=self.warehouses[0],
                    quantity=quantity,
                    unit_price=0
                )
                ret.append(proc)
        return ret

    def some_adjustment(self) -> List[StockAdjustment]:
        adjustments = {
            self.product_variations[0].id: [40, -5],
            self.product_variations[1].id: [10],
        }
        ret = []
        for pv_id, quantities in adjustments.items():
            for quantity in quantities:
                sa = StockAdjustment.objects.create(
                    product_variation_id=pv_id,
                    warehouse=self.warehouses[0],
                    quantity=quantity,
                    reason='feel like it'
                )
                ret.append(sa)
        return ret

    def some_order(self):
        order_map = {
            self.product_variations[0].id: [1] * 7,
            self.product_variations[1].id: [1] * 3
        }
        for pv_id, quantities in order_map.items():
            for i, quantity in enumerate(quantities):
                order = self.create_one_order(pv_id, quantity=quantity)
                if i % 2 == 0:
                    for oi in order.shipment.orderitem_set.all():
                        oi.fulfill()

    def create_one_order(self, product_variation_id: int, quantity: int) -> RawOrder:
        cart = CartItem(item_id=product_variation_id, quantity=quantity)
        param = CreateOrderParameter.example(items=[cart])
        order = OrderService().create_raw_order(param)
        return order


def load_realistic_seed() -> RealisticSeed:
    """A Warehouse and two products

    Returns:

    """
    return RealisticSeed.load_realistic_seed()


def load_meaningful_seed():
    seeder = Seed.seeder()
    seeder.add_entity(Product, 1)
    seeder.add_entity(ProductImage, 1)
    seeder.add_entity(ProductVariation, 3)
    seeder.execute(turn_off_auto_now=False)

    warehouse = Warehouse.example()
    warehouse.address.save()
    warehouse.save()
    orders = [OrderService().create_order(CreateOrderParameter.example_with_valid_item()) for _ in range(5)]
    return orders
