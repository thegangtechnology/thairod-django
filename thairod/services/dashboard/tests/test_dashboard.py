from datetime import timedelta

from django.utils.timezone import now

from shipment.models import Shipment
from thairod import settings
from thairod.services.dashboard import dashboard_service as ds
from thairod.services.stock.stock import StockInfo
from thairod.utils.load_seed import RealisticSeed
from thairod.utils.query_util import round_to_next_nearest_hour
from thairod.utils.test_util import TestCase


class TestDashboard(TestCase):
    with_seed = False

    def setUp(self):
        self.seed = RealisticSeed.load_realistic_seed()
        self.seed.full_production()

    def test_get_dash_board_summary(self):
        date = now().replace(hour=8)
        anchor = round_to_next_nearest_hour(date, settings.SHIPPOP_LOT_CUTTING_TIME)
        got = ds.DashboardService().get_dashboard_summary(date)

        self.assertEqual(got.latest_summary.begin, None)
        self.assertEqual(got.latest_summary.end, None)
        self.assertEqual(len(got.interval_summaries), 7)

    def test_get_daily_summary(self):
        end = now()
        begin = end - timedelta(days=1)
        pv_ids = [self.seed.product_variations[0].id, self.seed.product_variations[1].id]
        got = ds.DashboardService().get_daily_summary(begin, end, pv_ids=pv_ids)
        self.assertEqual(got.total_shipment_confirmed, 6)
        self.assertEqual(got.total_shipment_created, 10)
        self.assertEqual(got.begin, begin)
        self.assertEqual(got.end, end)
        self.assertEqual(len(got.product_summaries), 2)

    def test_get_product_summary(self):
        end = now()
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
            ordered=7,
            pending=3
        ))
