from django.db import transaction
from django_seed import Seed

from address.models import Address
from order.models import Order, OrderItem
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


def load_meaningful_seed():
    with transaction.atomic():
        seeder = Seed.seeder()
        seeder.add_entity(Product, 1)
        seeder.add_entity(ProductImage, 1)
        seeder.add_entity(ProductVariation, 3)
        seeder.execute(turn_off_auto_now=False)

        warehouse = Warehouse.example()
        warehouse.address.save()
        warehouse.save()
        orders = [OrderService().create_order(CreateOrderParameter.example()) for _ in range(5)]
        return orders
