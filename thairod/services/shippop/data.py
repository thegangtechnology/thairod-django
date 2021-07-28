from dataclasses import dataclass, asdict
from decimal import Decimal
from typing import List, Optional
from datetime import datetime

from address.models import Address
from thairod.settings import SHIPPOP_DEFAULT_COURIER_CODE

# flake8: noqa

@dataclass
class AddressData:
    name: str
    address: str
    district: str
    state: str
    province: str
    postcode: str
    tel: str
    country: Optional[str] = None
    lat: Optional[str] = None
    lng: Optional[str] = None
    origin_id: Optional[str] = None
    mem_id: Optional[int] = None
    dest_id: Optional[int] = None
    email: Optional[str] = None

    @classmethod
    def from_address_model(cls, address: 'Address'):
        # address: Address = address
        return cls(
            name = address.name,
            address = address.house_number,
            state = address.district,
            district=address.subdistrict,
            province=address.province,
            postcode=address.postal_code,
            tel = address.telno
        )

    def to_request_dict(self) -> dict:
        return {
            "name": self.name,
            "address": self.address,
            "district": self.district,
            "state": self.state,
            "province": self.province,
            "postcode": self.postcode,
            "tel": self.tel
        }


@dataclass
class ParcelData:
    weight: Optional[int] = None
    width: Optional[int] = None
    length: Optional[int] = None
    height: Optional[int] = None
    name: Optional[str] = ""


@dataclass
class OrderLineData:
    from_address: AddressData
    to_address: AddressData
    parcel: ParcelData
    courier_code: str = "THP"

    def to_request_dict(self) -> dict:
        return {
            "from": self.from_address.to_request_dict(),
            "to": self.to_address.to_request_dict(),
            "parcel": asdict(self.parcel),
            "courier_code": self.courier_code
        }


@dataclass
class OrderData:
    email: str
    success_url: str
    fail_url: str
    data: List[OrderLineData]

    def to_request_dict(self) -> dict:
        return {
            'email': self.email,
            'success': self.success_url,
            'fail': self.fail_url,
            'data': [d.to_request_dict() for d in self.data]
        }


@dataclass
class OrderLineResponse:
    status: bool
    tracking_code: str
    price: Decimal
    discount: Decimal
    from_address: AddressData
    to_address: AddressData
    courier_tracking_code: str
    courier_code: str = SHIPPOP_DEFAULT_COURIER_CODE
    parcel: Optional[ParcelData] = None
    weight: Optional[int] = None
    datetime_shipping: Optional[datetime] = None

    def __post_init__(self):
        if self.datetime_shipping is None:
            return
        self.datetime_shipping = datetime.fromisoformat(self.datetime_shipping)

    @classmethod
    def from_create_api(cls, response: dict) -> 'OrderLineResponse':
        from_address = AddressData(**response.pop('from'))
        to_address = AddressData(**response.pop('to'))
        return cls(**response, from_address=from_address, to_address=to_address)

    @classmethod
    def from_detail_api(cls, response: dict) -> 'OrderLineResponse':
        parcel = response.pop('parcel', None)
        if parcel is not None:
            parcel = ParcelData(**parcel)

        from_address = response.pop('from')
        from_address['state'] = from_address.pop('city')
        from_address['tel'] = from_address.pop('phone')
        from_address = AddressData(**from_address)

        to_address = response.pop('to')
        to_address['state'] = to_address.pop('city')
        to_address['tel'] = to_address.pop('phone')
        to_address = AddressData(**to_address)
        return cls(**response, from_address=from_address, to_address=to_address, parcel=parcel)


@dataclass
class OrderResponse:
    status: bool
    purchase_id: int
    total_price: Decimal
    lines: List[OrderLineResponse]
    purchase_status: Optional[str] = None
    total_discount: Optional[Decimal] = Decimal(0.0)


@dataclass
class TrackingState:
    datetime: datetime
    location: str
    description: str

    def __post_init__(self):
        self.datetime = datetime.fromisoformat(self.datetime)


@dataclass
class TrackingData:
    status: bool
    order_status: str
    order_cancel_detail: str
    courier_code: str
    tracking_code: str
    courier_tracking_code: str
    origin_postcode: str
    destination_postcode: str
    datetime_shipping: datetime
    states: List[TrackingState]
    parcel: ParcelData

    def __post_init__(self):
        if self.datetime_shipping is None or len(self.datetime_shipping) == 0:
            return
        self.datetime_shipping = datetime.fromisoformat(self.datetime_shipping)


@dataclass
class Pricing:
    estimate_time: str
    courier_code: str
    price: Decimal
    available: str
    remark: str
    err_code: str
    courier_name: str
    pick_up_fee: Optional[Decimal] = None
    notice: Optional[str] = None
