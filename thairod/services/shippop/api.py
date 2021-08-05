from typing import List

import requests

from thairod.services.shippop.data import OrderData, OrderResponse, TrackingData, OrderLineResponse, TrackingState, \
    ParcelData, Pricing
from thairod.settings import SHIPPOP_API_KEY, SHIPPOP_URL
# flake8: noqa
from thairod.utils.exceptions import ShippopAPIException


class ShippopAPI:
    api_key: str = SHIPPOP_API_KEY
    url: str = SHIPPOP_URL

    def shippop_request(self, path: str, payload: dict, no_key: bool = False) -> dict:
        if not no_key:
            payload = {"api_key": self.api_key, **payload}
        r = requests.request("POST", f"{self.url}/{path}", json=payload)
        r_json = r.json()
        if not r_json['status']:
            raise ShippopAPIException(r_json['notice'])
        return r_json

    def create_order(self, order_data: OrderData) -> OrderResponse:
        request_dict = order_data.to_request_dict()
        resp = self.shippop_request(path="booking/", payload=request_dict)
        data = resp.pop('data').values()
        return OrderResponse(**resp, lines=[OrderLineResponse.from_create_api(response=d) for d in data])

    def confirm_order(self, purchase_id: int) -> bool:
        resp = self.shippop_request(path="confirm/", payload={"purchase_id": purchase_id})
        return resp.get('status', False)

    def get_order_detail(self, purchase_id: int) -> OrderResponse:
        resp = self.shippop_request(path="tracking_purchase/", payload={"purchase_id": purchase_id})
        data = resp.pop('data').values()
        return OrderResponse(**resp, lines=[OrderLineResponse.from_detail_api(response=d) for d in data])

    def get_tracking_data(self, tracking_code: str) -> TrackingData:
        resp = self.shippop_request(path="tracking/", payload={"tracking_code": tracking_code}, no_key=True)
        resp.pop('state', None)
        states = resp.pop('states')
        parcel = resp.pop('parcel', None)
        parcel = ParcelData(**parcel)
        return TrackingData(**resp, states=[TrackingState(**s) for s in states], parcel=parcel)

    def get_pricing(self, order_data: OrderData) -> List[Pricing]:
        resp = self.shippop_request(path="pricelist/", payload=order_data.to_request_dict())
        data = resp.pop('data').get("0", {}).values()
        return [Pricing(**d) for d in data]

    def print_label(self, purchase_id: int, size: str = 'A4', label_type: str = 'html') -> str:
        """
            Return string of HTML. Beware of injection
            Type: html, pdf
        """
        resp = self.shippop_request(path="label/",
                                    payload={"purchase_id": purchase_id, "size": size, "type": label_type})
        return resp[label_type]

    def print_multiple_labels(self, tracking_codes: List[str], size: str = 'A4', label_type: str = 'html') -> str:
        """
            Return string of HTML. Beware of injection
            Type: html, pdf
        """
        resp = self.shippop_request(path="label_tracking_code/",
                                    payload={"tracking_code": ",".join(tracking_codes), "size": size,
                                             "type": label_type})
        return resp[label_type]

    def tracking_link(self, shippop_tracking_code: str) -> str:
        return f'https://www.shippop.com/tracking?typeid=domestic&tracking_code={shippop_tracking_code}'
