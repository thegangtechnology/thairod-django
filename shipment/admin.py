from django.contrib import admin
from core.admin import CustomModelAdmin
from shipment.models import Shipment, TrackingStatus, BatchShipment

admin.site.register(Shipment, CustomModelAdmin)
admin.site.register(TrackingStatus, CustomModelAdmin)
admin.site.register(BatchShipment, CustomModelAdmin)
