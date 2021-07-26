from rest_framework.routers import DefaultRouter
from django.urls import path, include
from procurement.views import ProcurementViewSet


router = DefaultRouter()
router.register(r'procurement', ProcurementViewSet, basename="procurement")


urlpatterns = [
    path('', include(router.urls))
]
