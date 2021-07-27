from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'orders', views.OrderModelViewSet, basename="order")
router.register(r'order_items', views.OrderItemModelViewSet, basename="order-item")

urlpatterns = [
    path('', include(router.urls)),
]
