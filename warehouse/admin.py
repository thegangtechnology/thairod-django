from django.contrib import admin
from core.admin import CustomModelAdmin
from warehouse.models import Warehouse

admin.site.register(Warehouse, CustomModelAdmin)
