from django.contrib import admin
from core.admin import CustomModelAdmin
from product.models import Product, ProductImage, ProductVariation


admin.site.register(Product, CustomModelAdmin)
admin.site.register(ProductImage, CustomModelAdmin)
admin.site.register(ProductVariation, CustomModelAdmin)
