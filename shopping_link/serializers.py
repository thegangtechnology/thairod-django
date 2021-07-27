from rest_framework import serializers
from shopping_link.models import ShoppingLink


class ShoppingLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingLink
        fields = '__all__'


class CreateShoppingLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingLink
        fields = ['raw_json_data']

    def create(self, validated_data):
        secret = ShoppingLink.generate_callback_secret()
        return ShoppingLink.objects.create(callback_secret=secret, **validated_data)
