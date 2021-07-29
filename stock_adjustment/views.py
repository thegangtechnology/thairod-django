from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from stock_adjustment.models import StockAdjustment
from stock_adjustment.serializers import StockAdjustmentSerializer


class StockAdjustmentModelViewSet(viewsets.ModelViewSet):
    serializer_class = StockAdjustmentSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = StockAdjustment.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['reason', 'warehouse__name', 'warehouse__tel']
