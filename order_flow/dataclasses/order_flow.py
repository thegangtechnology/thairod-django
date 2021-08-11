from dataclasses import dataclass
from thairod.utils.auto_serialize import AutoSerialize
from order.dataclasses.doctor import Doctor
from order.dataclasses.patient import Patient
from order.dataclasses.shipping_address import ShippingAddress
from order.dataclasses.order import CreateOrderParameter
from order_flow.models import OrderFlow
from typing import Optional
from order_flow.dataclasses.doctor_order import DoctorOrderResponse
from typing import List
from order.dataclasses.cart_item import CartItem


@dataclass
class CreateOrderFlowRequest(CreateOrderParameter):
    auto_doctor_confirm: bool

    @classmethod
    def example(cls,
                items: Optional[List[CartItem]] = None,
                auto_doctor_confirm: bool = False) \
            -> 'CreateOrderFlowRequest':
        return cls(
            account='frappet',
            doctor=Doctor.example(),
            patient=Patient.example(),
            shipping_address=ShippingAddress.example(),
            line_id="",
            session_id="AAABB2134",
            items=[CartItem.example()] if items is None else items,
            auto_doctor_confirm=auto_doctor_confirm
        )

    @classmethod
    def from_doctor_info(cls, doctor_info_dict):
        doctor = Doctor(**doctor_info_dict.get('doctor', None))
        patient = Patient(**doctor_info_dict.get('patient', None))
        shipping_address = ShippingAddress(**doctor_info_dict.get('shipping_address', None))
        items = [CartItem(item_id=item.get('item_id', None), quantity=item.get('quantity', 0)) for item in
                 doctor_info_dict.get('items', [])]
        return cls(
            account=doctor_info_dict.get('account', None),
            doctor=doctor,
            patient=patient,
            shipping_address=shipping_address,
            line_id=doctor_info_dict.get('line_id', None),
            session_id=doctor_info_dict.get('session_id', None),
            items=items,
            auto_doctor_confirm=doctor_info_dict.get('auto_doctor_confirm', None)
        )


@dataclass
class OrderFlowResponse(AutoSerialize):
    doctor_link_hash: str
    doctor_link_hash_timestamp: str
    doctor_info: CreateOrderFlowRequest
    doctor_order: Optional[DoctorOrderResponse]
    patient_link_hash: Optional[str]
    patient_link_hash_timestamp: Optional[str]
    patient_confirmation: Optional[ShippingAddress]
    auto_doctor_confirm: bool
    order_created: bool

    @classmethod
    def example(cls):
        return cls(
            doctor_link_hash='vKgejBAIPFfd8vgvG45J0nO1Zx6B79c02wa9a8cD5c',
            doctor_link_hash_timestamp="2021-08-10T11:14:48",
            doctor_info=CreateOrderFlowRequest.example(),
            doctor_order=DoctorOrderResponse.example(),
            patient_link_hash='vsdasadadafrqwJ0nO1Zryeyre9a8cD5c',
            patient_link_hash_timestamp="2021-08-10T11:14:48",
            patient_confirmation=ShippingAddress.example(),
            auto_doctor_confirm=False,
            order_created=False
        )

    @classmethod
    def from_order_flow_model(cls, order_flow: OrderFlow):
        datetime_format = '%Y-%m-%dT%H:%M:%S'
        doctor_order_data = None
        patient_confirmation_data = None
        patient_link_hash_timestamp_data = None
        if order_flow.doctor_order:
            is_confirmed = order_flow.patient_link_hash is not None
            doctor_order_data = DoctorOrderResponse.from_doctor_order_dict(doctor_order=dict(**order_flow.doctor_order),
                                                                           is_confirmed=is_confirmed)
        if order_flow.patient_confirmation:
            patient_confirmation_data = ShippingAddress(**order_flow.patient_confirmation)
        if order_flow.patient_link_hash_timestamp:
            patient_link_hash_timestamp_data = order_flow.patient_link_hash_timestamp.strftime(datetime_format)
        return cls(
            doctor_link_hash=order_flow.doctor_link_hash,
            doctor_link_hash_timestamp=order_flow.doctor_link_hash_timestamp.strftime(datetime_format),
            doctor_info=CreateOrderFlowRequest.from_doctor_info(order_flow.doctor_info),
            doctor_order=doctor_order_data,
            patient_link_hash=order_flow.patient_link_hash,
            patient_link_hash_timestamp=patient_link_hash_timestamp_data,
            patient_confirmation=patient_confirmation_data,
            auto_doctor_confirm=order_flow.auto_doctor_confirm,
            order_created=order_flow.order_created
        )
