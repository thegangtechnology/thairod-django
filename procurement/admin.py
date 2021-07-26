from django.contrib import admin
from core.admin import CustomModelAdmin
from procurement.models import Procurement

admin.site.register(Procurement, CustomModelAdmin)
