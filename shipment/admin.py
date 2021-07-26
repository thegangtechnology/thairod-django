from django.contrib import admin
from core.admin import CustomModelAdmin
from shipment.models import Shipment, TrackingStatus

admin.site.register(Shipment, CustomModelAdmin)
admin.site.register(TrackingStatus, CustomModelAdmin)
