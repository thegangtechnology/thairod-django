from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'shipments', views.ShipmentModelViewSet, basename="shipment")
router.register(r'tracking_status', views.TrackingStatusModelViewSet, basename="tracking")

urlpatterns = [
    path('', include(router.urls)),
    path('printlabel', views.print_label)
]
