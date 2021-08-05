from django.contrib import admin
from core.admin import CustomModelAdmin
from shipment.models import Shipment, TrackingStatus, BatchShipment
from shipment.models.box_size import BoxSize
from shipment.models.default_box_size import DefaultBoxSize

admin.site.register(Shipment, CustomModelAdmin)
admin.site.register(TrackingStatus, CustomModelAdmin)
admin.site.register(BatchShipment, CustomModelAdmin)
admin.site.register(BoxSize, CustomModelAdmin)
admin.site.register(DefaultBoxSize, CustomModelAdmin)
