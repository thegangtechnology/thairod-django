from rest_framework import viewsets, filters

from address.models import Address
from address.serializers import AddressSerializer


class AddressModelViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['house_number', 'subdistrict', 'district', 'province', 'postal_code', 'country', 'note']
