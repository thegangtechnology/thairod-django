from django.urls import include, path
from rest_framework.routers import DefaultRouter

import shipment.views.model_views
from .views import views
from .views.print_label_views import PrintSampleLabelView, PrintLabelView, PrintOfTheDayView
from .views.simple_shipment_list import SimpleShipmentListView

router = DefaultRouter()
router.register(r'shipments', shipment.views.model_views.ShipmentModelViewSet, basename="shipment")
router.register(r'tracking-status', shipment.views.model_views.TrackingStatusModelViewSet, basename="tracking")
router.register(r'batch-shipments', views.BatchShipmentModelViewSet, basename="batch-shipment")

urlpatterns = [
    path('', include(router.urls)),
    path('printlabel/', PrintLabelView.as_view(), name='print-label'),
    path('samplelabel/', PrintSampleLabelView.as_view(), name='sample-label'),
    path('simple-shipment/', SimpleShipmentListView.as_view(), name='simple-shipment-list'),
    path('print-of-the-day/', PrintOfTheDayView.as_view(), name='print-of-the-day')
]
