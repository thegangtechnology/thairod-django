from rest_framework import viewsets, mixins
from procurement.serializers import ProcurementSerializers
from procurement.models import Procurement


class ProcurementViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = ProcurementSerializers
    queryset = Procurement.objects.all()
