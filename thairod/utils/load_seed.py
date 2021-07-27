from django_seed import Seed
from address.models import Address
from order.models import Order, OrderItem
from procurement.models import Procurement
from product.models import ProductVariation, Product, ProductImage
from shipment.models import Shipment, TrackingStatus
from stock_adjustment.models import StockAdjustment
from user.models import User
from warehouse.models import Warehouse
from shopping_link.models import ShoppingLink


def load_seed():
    seeder = Seed.seeder()
    seeder.add_entity(Address, 1)
    seeder.add_entity(Order, 1)
    seeder.add_entity(Product, 1)
    seeder.add_entity(ProductImage, 1)
    seeder.add_entity(ProductVariation, 1)
    seeder.add_entity(TrackingStatus, 1)
    seeder.add_entity(Warehouse, 4)
    seeder.add_entity(Shipment, 1)
    seeder.add_entity(OrderItem, 1)
    seeder.add_entity(Procurement, 1)
    seeder.add_entity(StockAdjustment, 1)
    seeder.add_entity(User, 1)
    seeder.add_entity(ShoppingLink, 1)
    seeder.execute(turn_off_auto_now=False)
