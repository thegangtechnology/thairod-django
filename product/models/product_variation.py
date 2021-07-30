from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import AbstractModel
from product.models import Product


class ProductVariationUnit(models.TextChoices):
    PIECES = 'PIECES', _('Pieces (เม็ด)')
    PACKS = 'PACKS', _('Packs (แผง)')
    BOXES = 'BOXES', _('Boxes (กล่อง)')


class ProductVariation:
    pass


class ProductVariation(AbstractModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    unit = models.CharField(max_length=6,
                            choices=ProductVariationUnit.choices,
                            default=ProductVariationUnit.PIECES)

    @classmethod
    def example(cls) -> ProductVariation:
        return ProductVariation(
            product=Product.example(),
            price=20,
            name='random product variation',
            description='hello',
            unit=ProductVariationUnit.PIECES
        )
