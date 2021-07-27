from rest_framework import viewsets, filters
from user.models import User
from user.serializers import UserSerializers


class UserModelViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializers
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
