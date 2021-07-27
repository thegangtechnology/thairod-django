from django.contrib import admin
from core.admin import CustomModelAdmin
from shopping_link.models import ShoppingLink

admin.site.register(ShoppingLink, CustomModelAdmin)
