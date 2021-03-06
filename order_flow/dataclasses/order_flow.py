from dataclasses import dataclass
from thairod.utils.auto_serialize import AutoSerialize
from order.dataclasses.doctor import Doctor
from order.dataclasses.patient import Patient
from order.dataclasses.shipping_address import ShippingAddress
from order_flow.models import OrderFlow
from typing import Optional
from order_flow.dataclasses.doctor_order import DoctorOrderResponse


@dataclass
class CreateOrderFlowRequest(AutoSerialize):
    account: str
    doctor: Doctor
    patient: Patient
    shipping_address: ShippingAddress
    line_id: str
    session_id: str

    @classmethod
    def example(cls):
        return cls(
            account='frappet',
            doctor=Doctor.example(),
            patient=Patient.example(),
            shipping_address=ShippingAddress.example(),
            line_id="",
            session_id="AAABB2134")


@dataclass
class OrderFlowResponse(AutoSerialize):
    doctor_link_hash: str
    doctor_link_hash_timestamp: str
    doctor_info: CreateOrderFlowRequest
    doctor_order: Optional[DoctorOrderResponse]
    patient_link_hash: Optional[str]
    patient_link_hash_timestamp: Optional[str]
    patient_confirmation: Optional[ShippingAddress]

    @classmethod
    def example(cls):
        return cls(
            doctor_link_hash='vKgejBAIPFfd8vgvG45J0nO1Zx6B79c02wa9a8cD5c',
            doctor_link_hash_timestamp="",
            doctor_info=CreateOrderFlowRequest.example(),
            doctor_order=DoctorOrderResponse.example(),
            patient_link_hash='vsdasadadafrqwJ0nO1Zryeyre9a8cD5c',
            patient_link_hash_timestamp="",
            patient_confirmation=ShippingAddress.example())

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
            doctor_info=CreateOrderFlowRequest(**order_flow.doctor_info),
            doctor_order=doctor_order_data,
            patient_link_hash=order_flow.patient_link_hash,
            patient_link_hash_timestamp=patient_link_hash_timestamp_data,
            patient_confirmation=patient_confirmation_data
        )
