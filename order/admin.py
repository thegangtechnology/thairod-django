from django.contrib import admin
from core.admin import CustomModelAdmin
from order.models import Order, OrderItem

admin.site.register(Order, CustomModelAdmin)
admin.site.register(OrderItem, CustomModelAdmin)
