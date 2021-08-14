from datetime import timedelta

import freezegun

from django.conf import settings
from thairod.services.dashboard import dashboard_service as ds
from thairod.services.dashboard.dashboard_service import DashboardService
from thairod.services.stock.stock import StockInfo
from thairod.utils import tzaware
from thairod.utils.load_seed import RealisticSeed
from thairod.utils.query_util import round_to_next_nearest_hour
from thairod.utils.test_util import TestCase


class TestDashboard(TestCase):
    with_seed = False

    def setUp(self):
        self.seed = RealisticSeed.load_realistic_seed()
        self.seed.full_production()

    def test_get_dash_board_summary(self):
        date = tzaware.now().replace(hour=8)
        anchor = round_to_next_nearest_hour(date, settings.SHIPPOP_LOT_CUTTING_TIME)
        got = ds.DashboardService().get_dashboard_summary(anchor)

        self.assertEqual(got.latest_summary.begin, None)
        self.assertEqual(got.latest_summary.end, None)
        self.assertEqual(len(got.interval_summaries), 7)

    def test_get_daily_summary(self):
        end = tzaware.now()
        begin = end - timedelta(days=1)
        pv_ids = [self.seed.product_variations[0].id, self.seed.product_variations[1].id]
        got = ds.DashboardService().get_daily_summary(begin, end, pv_ids=pv_ids)
        self.assertEqual(got.total_shipment_confirmed, 6)
        self.assertEqual(got.total_shipment_created, 10)
        self.assertEqual(got.begin, begin)
        self.assertEqual(got.end, end)
        self.assertEqual(len(got.product_summaries), 2)

    def test_get_product_summary(self):
        end = tzaware.now()
        begin = end - timedelta(days=1)
        pv_id = self.seed.product_variations[0].id
        got = ds.DashboardService().get_product_variation_summary(
            pv_id=pv_id,
            begin=begin,
            end=end
        )
        self.assertEqual(got.pv_id, pv_id)
        self.assertEqual(got.pv_name, self.seed.product_variations[0].name)
        self.assertEqual(got.product_name, self.seed.product_variations[0].product.name)
        self.assertEqual(got.stock, StockInfo(
            fulfilled=4,
            procured=30,
            adjustment=35,
            to_be_shipped=4,
            ordered=7,
            pending=3
        ))
        self.assertTrue(got.unit != '')


class TestDashBoardNumber(TestCase):
    with_seed = False

    @freezegun.freeze_time(tzaware.datetime(2021, 8, 23, 8))
    def test_dashboard_no_order(self):
        seed = RealisticSeed.load_realistic_seed()
        pv = seed.product_variations[0]
        seed.procure_item(pv_id=pv.id, quantity=10)
        ds = DashboardService().get_dashboard_summary(tzaware.datetime(2021, 8, 23, 8),
                                                      n_days=1)
        latest_summary = ds.latest_summary
        self.assertEqual(latest_summary.total_shipment_created, 0)
        self.assertEqual(latest_summary.total_shipment_confirmed, 0)
        ps = ds.latest_summary.product_summaries[0]
        self.assertEqual(ps.pv_id, pv.id)
        self.assertEqual(ps.stock.procured, 10)
        self.assertEqual(ps.stock.ordered, 0)
        self.assertEqual(ps.stock.fulfilled, 0)

    @freezegun.freeze_time(tzaware.datetime(2021, 8, 23, 8))
    def test_dashboard_some_order(self):
        seed = RealisticSeed.load_realistic_seed()
        pv = seed.product_variations[0]
        # no stock so no fulfill
        seed.procure_item(pv_id=pv.id, quantity=100)
        seed.order_item(pv_id=pv.id, cid='111')
        seed.order_item(pv_id=pv.id, cid='222')
        seed.order_item_no_fulfill(pv_id=pv.id, cid='333')
        ds = DashboardService().get_dashboard_summary(tzaware.datetime(2021, 8, 23, 8),
                                                      n_days=1)
        latest_summary = ds.latest_summary
        self.assertEqual(latest_summary.total_shipment_created, 3)
        self.assertEqual(latest_summary.total_shipment_confirmed, 2)
        ps = ds.latest_summary.product_summaries[0]
        self.assertEqual(ps.pv_id, pv.id)
        self.assertEqual(ps.stock.procured, 100)
        self.assertEqual(ps.stock.ordered, 3)
        self.assertEqual(ps.stock.fulfilled, 2)
