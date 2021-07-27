from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views


router = DefaultRouter()
router.register(r'products', views.ProductModelViewSet, basename="product")
router.register(r'product_images', views.ProductImageModelViewSet, basename="product-image")
router.register(r'product_variations', views.ProductVariationModelViewSet, basename="product-variation")

urlpatterns = [
    path('', include(router.urls))
]
