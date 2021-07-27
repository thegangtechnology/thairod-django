from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'stock_adjustments', views.StockAdjustmentModelViewSet, basename="stock-adjustments")

urlpatterns = [
    path('', include(router.urls)),
]
