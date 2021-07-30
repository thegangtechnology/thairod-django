from django.contrib import admin
from core.admin import CustomModelAdmin
from order_flow.models import OrderFlow

admin.site.register(OrderFlow, CustomModelAdmin)
