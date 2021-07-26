from django.contrib import admin
from core.admin import CustomModelAdmin
from stock_adjustment.models import StockAdjustment

admin.site.register(StockAdjustment, CustomModelAdmin)
