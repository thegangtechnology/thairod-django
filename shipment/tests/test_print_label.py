from os.path import dirname, join

from bs4 import BeautifulSoup

from order.views import OrderService, CreateOrderParameter
from product.models import ProductVariation
from shipment.dataclasses.print_label import PrintLabelParam
from shipment.models import Shipment
from shipment.services.print_label_service import PrintLabelService
from shipment.utils.print_label_util import split_print_label
from shipment.views.print_label_views import PrintLabelView
from thairod.services.shippop.tests import load_test_data
from thairod.utils.load_seed import load_seed
from thairod.utils.test_util import TestCase


class TestPrintLabel(TestCase):

    def setUp(self):
        self.label_html_file = join(dirname(__file__), './ttt.html')
        with open(self.label_html_file) as f:
            self.label_html = f.read()
        self.order_data = load_test_data()['order_data']

    def test_split_print_label(self):
        pages = split_print_label(self.label_html)
        assert len(pages) == 2

    def test_generate_label(self):
        shipments = Shipment.objects.all()
        labels = split_print_label(self.label_html)
        s = PrintLabelService().generate_label_interleave(
            labels=labels, shipments=shipments)
        soup = BeautifulSoup(s, features="html.parser")
        pages = soup.find_all("div", {"class": "page"})
        assert len(pages) == 4

    def test_print_label_live(self):
        param = CreateOrderParameter.example()
        param.items[0].item_id = ProductVariation.objects.first().id
        first_order = OrderService().create_order(param)
        second_order = OrderService().create_order(param)
        shipments = Shipment.objects.filter(order_id__in=[first_order.order_id, second_order.order_id])
        html = PrintLabelView().generate_label(PrintLabelParam(
            shipments=shipments
        ))
        soup = BeautifulSoup(html, features="html.parser")
        pages = soup.find_all("div", {"class": "page"})
        assert len(pages) == 4
