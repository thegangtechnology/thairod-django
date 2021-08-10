from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg import openapi
from shipment.dataclasses.batch_shipment import BatchNameResponse, AssignBatchToShipmentRequest
from shipment.models import BatchShipment
from shipment.serializers.batch_shipment_serializer import BatchShipmentSerializer, \
    BatchShipmentNameSerializer
from shipment.services.batch_shipment_service import BatchShipmentService


class BatchShipmentModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BatchShipmentSerializer
    queryset = BatchShipment.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]

    @swagger_auto_schema(
        operation_description='Get a next batch name generated by the system',
        responses={200: BatchNameResponse.serializer()}
    )
    @action(detail=False, methods=['GET'], url_path='next-generated-name')
    def get_next_generated_batch_name(self, request):
        return BatchNameResponse(name=BatchShipment.generate_batch_name()).to_response()

    @swagger_auto_schema(
        operation_description='Assign batch name to the given shipments. This will create a new batch'
                              'name if not yet existed',
        request_body=AssignBatchToShipmentRequest.serializer(),
        responses={200: ''}
    )
    @action(detail=False, methods=['POST'], url_path='assign')
    def assign_batch(self, request):
        assign_batch_to_shipment_request = AssignBatchToShipmentRequest.from_post_request(request=request)
        BatchShipmentService().assign_batch_to_shipments(
            assign_batch_to_shipment_request=assign_batch_to_shipment_request)
        return Response()

    @swagger_auto_schema(
        operation_description='Get all batch names',
        responses={200: openapi.Response(
            description='List of batch shipments',
            schema=BatchShipmentSerializer(many=True))}
    )
    @action(detail=False, methods=['GET'], url_path='all')
    def all(self, request):
        all_batch_names = BatchShipment.objects.all()
        serialized_batches = BatchShipmentNameSerializer(all_batch_names, many=True)
        return Response(serialized_batches.data)

    @swagger_auto_schema(
        operation_description='Get all batch names that shipments are yet to deliver',
        responses={200: openapi.Response(
            description='List of batch shipments',
            schema=BatchShipmentSerializer(many=True))}
    )
    @action(detail=False, methods=['GET'], url_path='pending-deliver')
    def pending_deliver(self, request):
        pending_deliver_batch_names = BatchShipment.get_pending_deliver_batch()
        serialized_batches = BatchShipmentNameSerializer(pending_deliver_batch_names, many=True)
        return Response(serialized_batches.data)
