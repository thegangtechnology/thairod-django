from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from address.models import Address
from address.serializers import AddressSerializer


class AddressModelViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['house_number', 'subdistrict', 'district', 'province', 'postal_code', 'country', 'note']
