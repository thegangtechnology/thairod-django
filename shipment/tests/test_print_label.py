from os.path import dirname, join

from bs4 import BeautifulSoup
from django.test import TransactionTestCase

from order.views import OrderService, CreateOrderParameter
from shipment.models import Shipment
from shipment.utils.print_label_util import split_print_label
from shipment.views import PrintLabelView, PrintLabelParam, PrintLabelService
from thairod.services.shippop.tests import load_test_data
from thairod.utils.load_seed import load_seed


class TestPrintLabel(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        load_seed()
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
        first_order = OrderService().crate_order(
            CreateOrderParameter.example()
        )
        second_order = OrderService().crate_order(
            CreateOrderParameter.example()
        )
        shipments = Shipment.objects.filter(order_id__in=[first_order.order_id, second_order.order_id])
        html = PrintLabelView().generate_label(PrintLabelParam(
            shipments=shipments
        ))
        soup = BeautifulSoup(html, features="html.parser")
        pages = soup.find_all("div", {"class": "page"})
        assert len(pages) == 4
