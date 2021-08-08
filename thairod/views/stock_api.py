from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from django.http import HttpResponseBadRequest
from rest_framework.request import Request
from rest_framework.views import APIView

from thairod.services.stock.stock import StockInfo, StockService
from thairod.utils.auto_serialize import AutoSerialize, swagger_auto_serialize_get_schema


@dataclass
class StockResponse(AutoSerialize):
    stocks: Dict[int, StockInfo]

    @classmethod
    def example(cls) -> StockResponse:
        return cls(
            stocks={
                1: StockInfo.example(),
                2: StockInfo.example()
            }
        )


@dataclass
class StockAPIGet(AutoSerialize):
    pv_id: List[int]

    @classmethod
    def example(cls):
        return StockAPIGet(
            pv_id=[1, 2, 3]
        )


class StockAPI(APIView):
    @swagger_auto_serialize_get_schema(
        StockAPIGet, StockResponse,
        operation_description='request for stock information',
    )
    def get(self, request: Request):  # TODO: Optimize this for multiple stock
        pv_ids = request.query_params.getlist('pv_id')
        print(StockAPIGet.request.query_params)
        if not pv_ids:
            return HttpResponseBadRequest('Empty Product Variation ID.')

        return self.do_it(pv_ids).to_response()

    def do_it(self, pv_ids: List[int]) -> StockResponse:
        def get_stock(pv_id: int) -> StockInfo:
            return StockService().get_single_stock(pv_id)

        data = {pv_id: get_stock(pv_id) for pv_id in pv_ids}
        return StockResponse(stocks=data)
