from __future__ import annotations

from dataclasses import dataclass

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from order.models import Order
from thairod.utils.auto_serialize import swagger_auto_serialize_get_schema, AutoSerialize


@dataclass
class DidOrderNonRepeatableParam(AutoSerialize):
    cid: str

    @classmethod
    def example(cls) -> DidOrderNonRepeatableParam:
        return cls(cid='0987654532217')


@dataclass
class DidOrderNonRepeatableResponse(AutoSerialize):
    did_order_non_repeatable: bool


class DidOrderNonRepeatableAPI(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_serialize_get_schema(
        query_type=DidOrderNonRepeatableParam,
        response_type=DidOrderNonRepeatableResponse
    )
    def get(self, request: Request) -> Response:
        param = DidOrderNonRepeatableParam.from_get_request(request)
        return self.do(param).to_response()

    def do(self, param: DidOrderNonRepeatableParam) -> DidOrderNonRepeatableResponse:
        return DidOrderNonRepeatableResponse(
            did_order_non_repeatable=Order.used_to_order_non_repeatable(param.cid)
        )
