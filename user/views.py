from rest_framework import viewsets, filters, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.models import User
from user.serializers import UserSerializers, CurrentUserSerializer


class UserModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserSerializers
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']


class CurrentUserAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            return Response({"error": "user is anonymous."})
        return Response(CurrentUserSerializer(user).data)
