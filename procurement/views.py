from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from procurement.serializers import ProcurementSerializer
from procurement.models import Procurement
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import status
from warehouse.models import Warehouse


class ProcurementViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = ProcurementSerializer
    queryset = Procurement.objects.all()
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        # Check warehouse
        default_warehouse = Warehouse.default_warehouse()
        if not default_warehouse:
            return Response({'error': 'No default Warehouse.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            return super(ProcurementViewSet, self).create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
