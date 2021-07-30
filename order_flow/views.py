from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from order_flow.dataclasses import CreateOrderFlowRequest, CheckoutDoctorOrderRequest, PatientConfirmationRequest
from order_flow.services import OrderFlowService
from rest_framework import status


class CreateOrderFlowsAPI(GenericAPIView):

    def post(self, request: Request) -> Response:
        param = CreateOrderFlowRequest.from_post_request(request)
        service = OrderFlowService()
        return service.create_order_flow(param).to_response()


class OrderFlowsHashAPI(GenericAPIView):

    def get(self, request: Request) -> Response:
        doctor_hash = request.query_params.get('doctor', None)
        if doctor_hash:
            return OrderFlowService().get_order_flow_from_doctor_hash(doctor_hash=doctor_hash).to_response()
        patient_hash = request.query_params.get('patient', None)
        if patient_hash:
            return OrderFlowService().get_order_flow_from_patient_hash(patient_hash=patient_hash).to_response()
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CheckoutDoctorOrderAPI(GenericAPIView):

    def post(self, request: Request) -> Response:
        param = CheckoutDoctorOrderRequest.from_post_request(request)
        service = OrderFlowService()
        return service.write_doctor_order_to_order_flow(param).to_response()


class PatientConfirmationAPI(GenericAPIView):

    def post(self, request: Request) -> Response:
        param = PatientConfirmationRequest.from_post_request(request)
        service = OrderFlowService()
        return service.save_patient_confirmation_and_make_order(param).to_response()
