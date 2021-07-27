from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'warehouses', views.WarehouseModelViewSet, basename="warehouse")

urlpatterns = [
    path('', include(router.urls)),
]
