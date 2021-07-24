from django.contrib import admin
from core.admin import CustomModelAdmin
from address.models import Address

admin.site.register(Address, CustomModelAdmin)
