from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.admin import CustomModelAdmin
from .models import User, APIKey

admin.site.register(User, UserAdmin)
admin.site.register(APIKey, CustomModelAdmin)
