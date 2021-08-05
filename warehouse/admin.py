from django.contrib import admin
from core.admin import CustomModelAdmin
from warehouse.models import Warehouse
from warehouse.models.default_warehouse import DefaultWarehouse

admin.site.register(Warehouse, CustomModelAdmin)
admin.site.register(DefaultWarehouse, CustomModelAdmin)
