import datetime
from dataclasses import dataclass
from typing import List, Optional

from django.db.models import Func
from django.db.models import QuerySet
from django.utils.timezone import now
from future.backports.datetime import timedelta

from product.models import ProductVariation
from shipment.models import Shipment
from shipment.models.shipment import ShipmentStatus
from thairod import settings
from thairod.services.stock.stock import StockInfo, StockService
from thairod.utils.auto_serialize import AutoSerialize
from thairod.utils.query_util import date_range, to_intervals, round_to_next_nearest_hour


class DiffDays(Func):
    function = 'EXTRACT'
    template = "FLOOR(%(function)s(epoch FROM %(expressions)s)/3600)"


@dataclass
class ProductVariationSummary(AutoSerialize):
    pv_id: int
    product_name: str
    pv_name: str
    stock: StockInfo

    @classmethod
    def example(cls, pv_id: int = 1):
        return cls(
            pv_id=pv_id,
            product_name='product name',
            pv_name='pv_name',
            stock=StockInfo.example()
        )


@dataclass
class DailySummary(AutoSerialize):
    begin: Optional[datetime.datetime]
    end: Optional[datetime.datetime]
    total_shipment_created: int  # total shipment created during the time
    total_shipment_confirmed: int  # total confirmed during the time
    product_summaries: List[ProductVariationSummary]

    @classmethod
    def example(cls, end: Optional[datetime.datetime] = None, begin_is_none: bool = False):
        end = now() if end is None else end
        return cls(
            begin=None if begin_is_none else end - timedelta(days=1),
            end=end,
            total_shipment_created=10,
            total_shipment_confirmed=5,
            product_summaries=[ProductVariationSummary.example(pv_id=i) for i in range(3)]
        )


@dataclass
class DashboardSummary(AutoSerialize):
    latest_summary: DailySummary
    interval_summaries: List[DailySummary]

    @classmethod
    def example(cls):
        dates = date_range(now(), -7)
        return cls(
            interval_summaries=[DailySummary.example(end=date) for date in dates],
            latest_summary=DailySummary.example(end=None, begin_is_none=True)
        )


class DashboardService:
    def shipment_between_date(self, begin: datetime.datetime, end: datetime.datetime) -> QuerySet:
        Shipment.objects.filter(status=ShipmentStatus.CONFIRMED,
                                shippop_confirm_date_time__range=(begin, end))

    def shipment_of_the_day(self, should_print_date: datetime.date) -> QuerySet:
        d = should_print_date - datetime.timedelta(days=1)

        begin = datetime.datetime(d.year, d.month, d.day,
                                  hour=settings.SHIPPOP_LOT_CUTTING_TIME,
                                  tzinfo=settings.TIME_ZONE_PY)
        end = begin + datetime.timedelta(days=1)
        return self.shipment_between_date(begin, end)

    def get_dashboard_summary(self,
                              date: datetime.datetime,  # last date
                              n_days=7):
        date = round_to_next_nearest_hour(date, hour=settings.SHIPPOP_LOT_CUTTING_TIME)
        dates = date_range(date, -n_days)
        pv_ids = list(x.id for x in ProductVariation.objects.all())
        interval_summaries = [
            self.get_daily_summary(begin=begin, end=end, pv_ids=pv_ids)
            for begin, end in to_intervals(dates)
        ]
        latest_summary = self.get_daily_summary(begin=None, end=None, pv_ids=pv_ids)

        return DashboardSummary(
            latest_summary=latest_summary,
            interval_summaries=interval_summaries
        )

        # TODO: optimize this
    def get_daily_summary(self,
                          begin: Optional[datetime.datetime],
                          end: Optional[datetime.datetime],
                          pv_ids: List[int]) -> DailySummary:
        return DailySummary(
            begin=begin,
            end=end,
            total_shipment_created=Shipment.total_shipment_created(begin, end),
            total_shipment_confirmed=Shipment.total_shipment_confirmed(begin, end),
            product_summaries=[self.get_product_variation_summary(pv_id, begin=begin, end=end)
                               for pv_id in pv_ids]
        )

    def get_product_variation_summary(self,
                                      pv_id: int,
                                      begin: datetime.datetime,
                                      end: datetime.datetime) -> ProductVariationSummary:
        pv = ProductVariation.objects.get(pk=pv_id)
        stock = StockService().get_single_stock(pv, begin=begin, end=end)
        return ProductVariationSummary(
            pv_id=pv_id,
            product_name=pv.product.name,
            pv_name=pv.name,
            stock=stock
        )
