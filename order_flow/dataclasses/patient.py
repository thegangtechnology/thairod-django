from dataclasses import dataclass
from thairod.utils.auto_serialize import AutoSerialize
from order.dataclasses.shipping_address import ShippingAddress


@dataclass
class PatientConfirmationRequest(AutoSerialize):
    patient_link_hash: str
    address: ShippingAddress

    @classmethod
    def example(cls):
        return cls(
            patient_link_hash='vKgejBAIPFfd8vgvG45J0nO1Zx6B79c02wa9a8cD5c',
            address=ShippingAddress.example())
