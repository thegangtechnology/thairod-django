from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import PrintLabelView, PrintSampleLabelView

router = DefaultRouter()
router.register(r'shipments', views.ShipmentModelViewSet, basename="shipment")
router.register(r'tracking-status', views.TrackingStatusModelViewSet, basename="tracking")
router.register(r'batch-shipments', views.BatchShipmentModelViewSet, basename="batch-shipment")

urlpatterns = [
    path('', include(router.urls)),
    path('printlabel/', PrintLabelView.as_view(), name='print-label'),
    path('samplelabel/', PrintSampleLabelView.as_view(), name='sample-label')
]
