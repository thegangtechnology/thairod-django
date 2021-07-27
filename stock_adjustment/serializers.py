from rest_framework import serializers

from stock_adjustment.models import StockAdjustment


class StockAdjustmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockAdjustment
        fields = '__all__'
