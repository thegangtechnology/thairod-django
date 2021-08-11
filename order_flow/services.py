from order.dataclasses.cart_item import CartItem
from order.services.order_service import CreateOrderParameter, OrderService, CreateOrderResponse
from order_flow.dataclasses import CreateOrderFlowRequest, OrderFlowResponse, \
    CheckoutDoctorOrderRequest, PatientConfirmationRequest, DoctorOrder
from order_flow.models import OrderFlow
from thairod.utils import tzaware
from order_flow.exceptions import OrderAlreadyConfirmedException, PatientAlreadyConfirmedException
from thairod.services.line import line


class OrderFlowService:

    def create_order_flow(self, create_order_flow_request: CreateOrderFlowRequest) -> OrderFlowResponse:
        doctor_hash = OrderFlow.generate_hash_secret()
        order_flow = OrderFlow.objects.create(doctor_link_hash=doctor_hash,
                                              doctor_link_hash_timestamp=tzaware.now(),
                                              doctor_info=create_order_flow_request.to_data(),
                                              auto_doctor_confirm=create_order_flow_request.auto_doctor_confirm)

        if create_order_flow_request.items:
            doctor_order = DoctorOrder(items=create_order_flow_request.items)
            order_flow.doctor_order = doctor_order.to_data()
            order_flow.save()
            # doesn't make sense if no items and auto_doctor_confirm True..
            if create_order_flow_request.auto_doctor_confirm:
                checkout_doctor_order_request = CheckoutDoctorOrderRequest(doctor_link_hash=doctor_hash,
                                                                           doctor_order=doctor_order)
                return self.write_doctor_order_and_send_line_msg(checkout_doctor_order_request=checkout_doctor_order_request)
        return OrderFlowResponse.from_order_flow_model(order_flow=order_flow)

    def get_order_flow_from_doctor_hash(self, doctor_hash: str) -> OrderFlowResponse:
        return OrderFlowResponse.from_order_flow_model(OrderFlow.objects.get(doctor_link_hash=doctor_hash))

    def get_order_flow_from_patient_hash(self, patient_hash: str) -> OrderFlowResponse:
        return OrderFlowResponse.from_order_flow_model(OrderFlow.objects.get(patient_link_hash=patient_hash))

    def write_doctor_order_to_order_flow(self, checkout_doctor_order_request: CheckoutDoctorOrderRequest) \
            -> OrderFlowResponse:
        patient_hash = OrderFlow.generate_hash_secret()
        order_flow = OrderFlow.objects.get(doctor_link_hash=checkout_doctor_order_request.doctor_link_hash)
        # Order is confirmed. Wait for patient confirmation
        if order_flow.patient_link_hash_timestamp:
            raise OrderAlreadyConfirmedException()
        order_flow.doctor_order = checkout_doctor_order_request.doctor_order.to_data()
        order_flow.patient_link_hash = patient_hash
        order_flow.patient_link_hash_timestamp = tzaware.now()
        order_flow.save()
        return OrderFlowResponse.from_order_flow_model(order_flow=order_flow)

    def write_doctor_order_and_send_line_msg(self, checkout_doctor_order_request: CheckoutDoctorOrderRequest):
        order_response = self.write_doctor_order_to_order_flow(checkout_doctor_order_request=checkout_doctor_order_request)
        order_flow = OrderFlow.objects.get(doctor_link_hash=checkout_doctor_order_request.doctor_link_hash)
        self.send_line_confirmation_message(order_flow=order_flow)
        return order_response

    def write_patient_confirmation_to_order_flow(self, patient_confirmation_request: PatientConfirmationRequest) \
            -> OrderFlowResponse:
        order_flow = OrderFlow.objects.get(patient_link_hash=patient_confirmation_request.patient_link_hash)
        # patient has confirm and order is already created
        if order_flow.order_created and order_flow.patient_confirmation:
            raise PatientAlreadyConfirmedException()
        order_flow.patient_confirmation = patient_confirmation_request.address.to_data()
        order_flow.save()
        return OrderFlowResponse.from_order_flow_model(order_flow=order_flow)

    def construct_create_order_parameter_from_order_flow(self, order_flow: OrderFlow) -> CreateOrderParameter:
        order_flow_response = OrderFlowResponse.from_order_flow_model(order_flow=order_flow)
        return self.construct_create_order_parameter_from_order_flow_response(order_flow_response=order_flow_response)

    def construct_create_order_parameter_from_order_flow_response(self, order_flow_response: OrderFlowResponse) \
            -> CreateOrderParameter:
        create_order_parameter = CreateOrderParameter(account=order_flow_response.doctor_info.account,
                                                      doctor=order_flow_response.doctor_info.doctor,
                                                      patient=order_flow_response.doctor_info.patient,
                                                      shipping_address=order_flow_response.patient_confirmation,
                                                      line_id=order_flow_response.doctor_info.line_id,
                                                      session_id=order_flow_response.doctor_info.session_id,
                                                      items=CartItem.from_doctor_order_response(
                                                          order_flow_response.doctor_order))
        return create_order_parameter

    def save_patient_confirmation_and_make_order(self, patient_confirmation_request: PatientConfirmationRequest) \
            -> CreateOrderResponse:
        self.write_patient_confirmation_to_order_flow(patient_confirmation_request=patient_confirmation_request)
        order_flow = OrderFlow.objects.get(patient_link_hash=patient_confirmation_request.patient_link_hash)
        create_order_param = self.construct_create_order_parameter_from_order_flow(order_flow=order_flow)
        create_order_response = OrderService().create_order(param=create_order_param)
        # successfully create order
        if create_order_response.success:
            order_flow.order_created = True
            order_flow.save()
        return create_order_response

    def send_line_confirmation_message(self, order_flow: OrderFlow) -> None:
        line_uid = order_flow.doctor_order.get('line_id')
        patient_name = order_flow.doctor_info.get('patient').get('name')
        patient_hash = order_flow.patient_link_hash
        line.send_line_patient_address_confirmation_message(line_uid=line_uid,
                                                            patient_name=patient_name,
                                                            patient_hash=patient_hash)
