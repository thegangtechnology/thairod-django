from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

from . import views
from .views import PrintLabelView

router = DefaultRouter()
router.register(r'shipments', views.ShipmentModelViewSet, basename="shipment")
router.register(r'tracking_status', views.TrackingStatusModelViewSet, basename="tracking")

urlpatterns = [
    path('', include(router.urls)),
    path('printlabel/', csrf_exempt(PrintLabelView.as_view()))
]
