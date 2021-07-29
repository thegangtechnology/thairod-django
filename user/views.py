from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from user.models import User
from user.serializers import UserSerializers


class UserModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializers
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
