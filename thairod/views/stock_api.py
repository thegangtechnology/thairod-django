from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List

from django.http import HttpResponseBadRequest
from drf_yasg.openapi import Parameter
from rest_framework.request import Request
from rest_framework.views import APIView

from thairod.services.stock.stock import StockInfo, StockService
from thairod.utils.auto_serialize import AutoSerialize, swagger_auto_serialize_schema


@dataclass
class SingleStockResponse(AutoSerialize):
    fulfilled: int
    procured: int
    adjustment: int
    pending: int
    current_total: int

    @classmethod
    def from_stock_info(cls, stock_info: StockInfo) -> SingleStockResponse:
        return cls(
            current_total=stock_info.current_total,
            **asdict(stock_info)
        )

    @classmethod
    def example(cls) -> SingleStockResponse:
        return cls(
            fulfilled=10,
            procured=20,
            adjustment=-2,
            pending=10,
            current_total=12
        )


@dataclass
class StockResponse(AutoSerialize):
    stocks: Dict[int, SingleStockResponse]

    @classmethod
    def example(cls) -> StockResponse:
        return cls(
            stocks={
                1: SingleStockResponse.example(),
                2: SingleStockResponse.example()
            }
        )


class StockAPI(APIView):
    @swagger_auto_serialize_schema(
        None, StockResponse,
        operation_description='request for stock information',
        manual_parameters=[
            Parameter('pv_id', in_='query', type='integer', description='product variation id. Repeatable.', example='1')]
    )
    def get(self, request: Request):  # TODO: Optimize this for multiple stock
        pv_ids = request.query_params.getlist('pv_id')
        if not pv_ids:
            return HttpResponseBadRequest('Empty Product Variation ID.')

        return self.do_it(pv_ids).to_response()

    def do_it(self, pv_ids: List[int]) -> StockResponse:
        def get_stock(pv_id: int) -> SingleStockResponse:
            stock_info = StockService().get_single_stock(pv_id)
            return SingleStockResponse.from_stock_info(stock_info)

        data = {pv_id: get_stock(pv_id) for pv_id in pv_ids}

        return StockResponse(stocks=data)
