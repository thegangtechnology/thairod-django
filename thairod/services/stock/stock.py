from __future__ import annotations

from dataclasses import dataclass

from order.models import OrderItem
from procurement.models import Procurement
from stock_adjustment.models import StockAdjustment


@dataclass
class StockInfo:
    fulfilled: int
    procured: int
    adjustment: int
    pending: int

    @property
    def current_total(self):
        return self.procured - self.fulfilled + self.adjustment

    @classmethod
    def for_id(cls, product_variation_id: int) -> StockInfo:
        return StockInfo(
            fulfilled=OrderItem.total_fulfilled_for_id(product_variation_id),
            procured=Procurement.total_procurement_for_id(product_variation_id),
            adjustment=StockAdjustment.total_adjustment_for_id(product_variation_id),
            pending=OrderItem.total_pending_for_id(product_variation_id)
        )


class StockService:
    def get_single_stock(self, product_variation_id: int) -> StockInfo:
        return StockInfo.for_id(product_variation_id=product_variation_id)

    def get_all_stock_map(self):
        raise NotImplementedError()  # TODO: fill this later
