from drf_yasg.openapi import Parameter
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from order.dataclasses.order import CreateOrderResponse
from order_flow.dataclasses import CreateOrderFlowParam, CheckoutDoctorOrderRequest, \
    PatientConfirmationRequest, OrderFlowResponse, CreateOrderFlowResponse
from order_flow.services import OrderFlowService
from order_flow.models import OrderFlow
from django.conf import settings
from thairod.utils.auto_serialize import swagger_auto_serialize_post_schema
from thairod.utils.decorators import ip_whitelist
from order_flow.exceptions import OrderAlreadyConfirmedException, PatientAlreadyConfirmedException, HashExpired
from rest_framework.permissions import AllowAny
HASH_DOES_NOT_EXIST = "Hash not found"


class CreateOrderFlowsAPI(GenericAPIView):
    permission_classes = [AllowAny]

    @ip_whitelist(settings.TELEMED_WHITELIST, allow_all_if_debug=True)
    @swagger_auto_serialize_post_schema(CreateOrderFlowParam, CreateOrderFlowResponse)
    def post(self, request: Request) -> Response:
        param = CreateOrderFlowParam.from_post_request(request)
        service = OrderFlowService()
        order_flow = service.create_order_flow(param)
        return CreateOrderFlowResponse.from_doctor_link_hash(doctor_link_hash=order_flow.doctor_link_hash)\
            .to_response()


class OrderFlowsHashAPI(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        manual_parameters=[
            Parameter('doctor', in_='query', type='str', description='doctor hash', example='dfadfsa'),
            Parameter('patient', in_='query', type='str', description='patient hash', example='dfadfsa')
        ]
    )
    def get(self, request: Request) -> Response:
        doctor_hash = request.query_params.get('doctor', None)
        patient_hash = request.query_params.get('patient', None)
        if doctor_hash and patient_hash:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            if doctor_hash:
                return OrderFlowService().get_order_flow_from_doctor_hash(doctor_hash=doctor_hash).to_response()
            if patient_hash:
                return OrderFlowService().get_order_flow_from_patient_hash(patient_hash=patient_hash).to_response()
        except OrderFlow.DoesNotExist:
            return Response(data=HASH_DOES_NOT_EXIST, status=status.HTTP_400_BAD_REQUEST)
        except HashExpired as e:
            return Response(data=e.message, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CheckoutDoctorOrderAPI(GenericAPIView):
    permission_classes = [AllowAny]

    @swagger_auto_serialize_post_schema(CheckoutDoctorOrderRequest, OrderFlowResponse)
    def post(self, request: Request) -> Response:
        param = CheckoutDoctorOrderRequest.from_post_request(request)
        service = OrderFlowService()
        try:
            return service.write_doctor_order_and_send_line_msg(param).to_response()
        except (OrderAlreadyConfirmedException, HashExpired) as e:
            return Response(data=e.message, status=status.HTTP_400_BAD_REQUEST)
        except OrderFlow.DoesNotExist:
            return Response(data=HASH_DOES_NOT_EXIST, status=status.HTTP_400_BAD_REQUEST)


class PatientConfirmationAPI(GenericAPIView):
    permission_classes = [AllowAny]

    @swagger_auto_serialize_post_schema(PatientConfirmationRequest, CreateOrderResponse)
    def post(self, request: Request) -> Response:
        param = PatientConfirmationRequest.from_post_request(request)
        service = OrderFlowService()
        try:
            return service.save_patient_confirmation_and_make_order(param).to_response()
        except (PatientAlreadyConfirmedException, HashExpired) as e:
            return Response(data=e.message, status=status.HTTP_400_BAD_REQUEST)
        except OrderFlow.DoesNotExist:
            return Response(data=HASH_DOES_NOT_EXIST, status=status.HTTP_400_BAD_REQUEST)
