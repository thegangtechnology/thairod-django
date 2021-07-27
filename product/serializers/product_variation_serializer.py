from rest_framework import serializers
from product.models import ProductVariation


class ProductVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = '__all__'
