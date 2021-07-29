from core.views import MultiSerializersGenericViewSet
from rest_framework import mixins
from shopping_link.models import ShoppingLink
from shopping_link.serializers import ShoppingLinkSerializer, CreateShoppingLinkSerializer
from rest_framework.response import Response
from rest_framework.views import status
from django.utils import timezone
from thairod.utils.auto_serialize import swagger_auto_serialize_schema


class ShoppingLinkViewSet(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          MultiSerializersGenericViewSet):
    serializer_class = ShoppingLinkSerializer
    queryset = ShoppingLink.objects.all()
    serializers = {
        'create': CreateShoppingLinkSerializer,
    }

    def perform_create(self, serializer):
        return serializer.save()

    # @swagger_auto_serialize_schema(CreateShoppingLinkSerializer, ShoppingLinkSerializer)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        instance_serializer = ShoppingLinkSerializer(instance)
        return Response(instance_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        callback_req = self.request.query_params.get('callback', None)
        if callback_req:
            try:
                shopping_link = ShoppingLink.objects.get(callback_secret=callback_req)
                now = timezone.now()
                shopping_link.update_is_expired(timezone_object=now)
                if shopping_link.is_expired:
                    return Response({'error': 'The callback is already expired'},
                                    status=status.HTTP_400_BAD_REQUEST)
                return Response(ShoppingLinkSerializer(shopping_link).data)
            except ShoppingLink.DoesNotExist as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)
