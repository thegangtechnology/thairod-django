from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

from . import views
from .views import CreateOrderAPI

router = DefaultRouter()
router.register(r'orders', views.OrderModelViewSet, basename="order")
router.register(r'order_items', views.OrderItemModelViewSet, basename="order-item")


urlpatterns = [
    path('', include(router.urls)),
    path('create-order', csrf_exempt(CreateOrderAPI.as_view()))
]
