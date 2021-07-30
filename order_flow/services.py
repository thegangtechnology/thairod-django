from order_flow.dataclasses import CreateOrderFlowRequest, OrderFlowResponse, \
    CheckoutDoctorOrderRequest, PatientConfirmationRequest
from order_flow.models import OrderFlow
from order.services.order_service import CreateOrderParameter, OrderService, CreateOrderResponse
from django.utils import timezone


class OrderFlowService:

    def create_order_flow(self, create_order_flow_request: CreateOrderFlowRequest) -> OrderFlowResponse:
        doctor_hash = OrderFlow.generate_hash_secret()
        order_flow = OrderFlow.objects.create(doctor_link_hash=doctor_hash,
                                              doctor_link_hash_timestamp=timezone.now(),
                                              doctor_info=create_order_flow_request.to_data())
        return OrderFlowResponse.from_order_flow_model(order_flow=order_flow)

    def get_order_flow_from_doctor_hash(self, doctor_hash: str) -> OrderFlowResponse:
        return OrderFlow.objects.get(doctor_link_hash=doctor_hash)

    def get_order_flow_from_patient_hash(self, patient_hash: str) -> OrderFlowResponse:
        return OrderFlow.objects.get(patient_link_hash=patient_hash)

    def write_doctor_order_to_order_flow(self, checkout_doctor_order_request: CheckoutDoctorOrderRequest) \
            -> OrderFlowResponse:
        patient_hash = OrderFlow.generate_hash_secret()
        order_flow = OrderFlow.objects.get(doctor_link_hash=checkout_doctor_order_request.doctor_link_hash)
        order_flow.doctor_order = checkout_doctor_order_request.doctor_order.to_data()
        order_flow.patient_link_hash = patient_hash
        order_flow.patient_link_hash_timestamp = timezone.now()
        order_flow.save()
        return OrderFlowResponse.from_order_flow_model(order_flow=order_flow)

    def write_patient_confirmation_to_order_flow(self, patient_confirmation_request: PatientConfirmationRequest) \
            -> OrderFlowResponse:
        order_flow = OrderFlow.objects.get(patient_link_hash=patient_confirmation_request.patient_link_hash)
        order_flow.patient_confirmation = patient_confirmation_request.address.to_data()
        order_flow.save()
        return OrderFlowResponse.from_order_flow_model(order_flow=order_flow)

    def construct_create_order_parameter_from_order_flow(self, order_flow: OrderFlow) -> CreateOrderParameter:
        order_flow_response = OrderFlowResponse.from_order_flow_model(order_flow=order_flow)
        create_order_parameter = CreateOrderParameter(account=order_flow_response.doctor_info.account,
                                                      doctor=order_flow_response.doctor_info.doctor,
                                                      patient=order_flow_response.doctor_info.patient,
                                                      shipping_address=order_flow_response.patient_confirmation,
                                                      line_id=order_flow_response.doctor_info.line_id,
                                                      session_id=order_flow_response.doctor_info.session_id,
                                                      items=order_flow_response.doctor_order)
        return create_order_parameter

    def save_patient_confirmation_and_make_order(self, patient_confirmation_request: PatientConfirmationRequest)\
            -> CreateOrderResponse:
        self.write_patient_confirmation_to_order_flow(patient_confirmation_request=patient_confirmation_request)
        order_flow = OrderFlow.objects.get(patient_link_hash=patient_confirmation_request.patient_link_hash)
        create_order_param = self.construct_create_order_parameter_from_order_flow(order_flow=order_flow)
        return OrderService().create_order(param=create_order_param)
