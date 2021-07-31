from drf_yasg.openapi import Parameter
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from order.dataclasses.order import CreateOrderResponse
from order_flow.dataclasses import CreateOrderFlowRequest, CheckoutDoctorOrderRequest, \
    PatientConfirmationRequest, OrderFlowResponse
from order_flow.services import OrderFlowService
from thairod.utils.auto_serialize import swagger_auto_serialize_schema


class CreateOrderFlowsAPI(GenericAPIView):

    @swagger_auto_serialize_schema(CreateOrderFlowRequest, OrderFlowResponse)
    def post(self, request: Request) -> Response:
        param = CreateOrderFlowRequest.from_post_request(request)
        service = OrderFlowService()
        return service.create_order_flow(param).to_response()


class OrderFlowsHashAPI(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            Parameter('doctor', in_='query', type='str', description='doctor hash', example='dfadfsa'),
            Parameter('patient', in_='query', type='str', description='patient hash', example='dfadfsa')
        ]
    )
    def get(self, request: Request) -> Response:
        doctor_hash = request.query_params.get('doctor', None)
        if doctor_hash:
            return OrderFlowService().get_order_flow_from_doctor_hash(doctor_hash=doctor_hash).to_response()
        patient_hash = request.query_params.get('patient', None)
        if patient_hash:
            return OrderFlowService().get_order_flow_from_patient_hash(patient_hash=patient_hash).to_response()
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CheckoutDoctorOrderAPI(GenericAPIView):

    @swagger_auto_serialize_schema(CheckoutDoctorOrderRequest, OrderFlowResponse)
    def post(self, request: Request) -> Response:
        param = CheckoutDoctorOrderRequest.from_post_request(request)
        service = OrderFlowService()
        return service.write_doctor_order_to_order_flow(param).to_response()


class PatientConfirmationAPI(GenericAPIView):

    @swagger_auto_serialize_schema(PatientConfirmationRequest, CreateOrderResponse)
    def post(self, request: Request) -> Response:
        param = PatientConfirmationRequest.from_post_request(request)
        service = OrderFlowService()
        return service.save_patient_confirmation_and_make_order(param).to_response()
