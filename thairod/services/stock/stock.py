from __future__ import annotations

import datetime
import itertools
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from typing import DefaultDict, Optional

from order.models import OrderItem
from procurement.models import Procurement
from stock_adjustment.models import StockAdjustment


@dataclass
class StockInfo:
    fulfilled: int
    procured: int
    adjustment: int
    ordered: int
    pending: int

    @classmethod
    def empty(cls) -> StockInfo:
        return StockInfo(
            fulfilled=0,
            procured=0,
            adjustment=0,
            ordered=0,
            pending=0
        )

    @property
    def current_total(self):
        return self.procured - self.fulfilled + self.adjustment

    @classmethod
    def for_id(cls, product_variation_id: int,
               begin: Optional[date] = None,
               end: Optional[date] = None) -> StockInfo:
        return StockInfo(
            fulfilled=OrderItem.total_fulfilled_for_id(product_variation_id, begin, end),
            procured=Procurement.total_procurement_for_id(product_variation_id, begin, end),
            ordered=OrderItem.total_ordered_for_id(product_variation_id, begin, end),
            adjustment=StockAdjustment.total_adjustment_for_id(product_variation_id, begin, end),
            pending=OrderItem.total_pending_for_id(product_variation_id, begin, end)
        )


class StockService:
    def get_single_stock(self, product_variation_id: int,
                         begin: Optional[datetime.date] = None,
                         end: Optional[datetime.date] = None) -> StockInfo:
        return StockInfo.for_id(product_variation_id=product_variation_id,
                                begin=begin,
                                end=end)

    def get_all_stock_map(self) -> DefaultDict[int, StockInfo]:
        fulfilled_map = OrderItem.total_fulfilled_map()
        pending_map = OrderItem.total_pending_map()
        procured_map = Procurement.total_procurement_map()
        adjustment_map = StockAdjustment.total_adjustment_map()
        ordered_map = OrderItem.total_ordered_map()
        key_set = set()
        ret = defaultdict(StockInfo.empty)
        for key in itertools.chain(fulfilled_map.keys(), procured_map.keys(),
                                   adjustment_map.keys(), pending_map.keys()):
            if key not in key_set:
                ret[key] = StockInfo(
                    procured=procured_map[key],
                    fulfilled=fulfilled_map[key],
                    ordered=ordered_map[key],
                    adjustment=adjustment_map[key],
                    pending=pending_map[key]
                )
                key_set.add(key)
        return ret
