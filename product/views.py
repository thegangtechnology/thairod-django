from rest_framework import viewsets, filters

from product.models import Product, ProductVariation, ProductImage
from product.serializers.product_image_serializer import ProductImageSerializer
from product.serializers.product_serializer import ProductSerializer
from product.serializers.product_variation_serializer import ProductVariationSerializer


class ProductModelViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['sku', 'name', 'description']


class ProductImageModelViewSet(viewsets.ModelViewSet):
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['product__sku', 'product__name', 'product__description']


class ProductVariationModelViewSet(viewsets.ModelViewSet):
    serializer_class = ProductVariationSerializer
    queryset = ProductVariation.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['product__sku', 'product__name', 'product__description', 'name', 'description', 'price']

# TODO: Check for stock API
