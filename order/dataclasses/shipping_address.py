from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict

from rest_framework.exceptions import ValidationError

from thairod.utils.auto_serialize import AutoSerialize


@dataclass
class ShippingAddress(AutoSerialize):
    street: str
    sub_district: str
    district: str
    province: str
    zipcode: str
    phone_number: str
    note: str

    @classmethod
    def validate_data(cls, data: ShippingAddress):
        if len(data.zipcode) != 5 or not data.zipcode.isnumeric():
            raise ValidationError(detail='Incorrect Postal Code', code='zipcode_error')
        return data

    @classmethod
    def example(cls):
        return cls(
            phone_number="08123435678",
            street='99 ถ.ราชดำเนิน',
            sub_district='ราชดำเนิน',
            district='พระนคร',
            province='กรุงเทพมหานคร',
            zipcode='10200',
            note="บ้านอยู่ชั้นสอง"
        )
