from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from warehouse.models import Warehouse
from warehouse.serializers import WarehouseSerializer


class WarehouseModelViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = WarehouseSerializer
    queryset = Warehouse.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'tel', 'address']
