from rest_framework import viewsets, filters
from rest_framework.decorators import action
from product.models import Product, ProductVariation, ProductImage
from product.serializers.product_image_serializer import ProductImageSerializer
from product.serializers.product_serializer import ProductSerializer
from product.serializers.product_variation_serializer import ProductVariationSerializer, \
    ProductVariationNameSerializer
from rest_framework.response import Response


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

    @action(detail=False, methods=['GET'], url_path='all')
    def all(self, request):
        all_product_variations = ProductVariation.objects.all()
        serialized_batches = ProductVariationNameSerializer(all_product_variations, many=True)
        return Response(serialized_batches.data)
