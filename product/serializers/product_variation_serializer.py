from rest_framework import serializers
from product.models import ProductVariation


class ProductVariationSerializer(serializers.ModelSerializer):
    product_description = serializers.CharField(source='product.description', read_only=True)

    class Meta:
        model = ProductVariation
        fields = '__all__'


class ProductVariationNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariation
        fields = ('name', 'id', )
