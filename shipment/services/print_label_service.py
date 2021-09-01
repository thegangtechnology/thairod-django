from typing import List, Optional

from django.template import loader

from shipment.dataclasses.print_label import PrintLabelParam
from shipment.models import Shipment
from shipment.utils.print_label_util import split_print_label
from thairod.services.shippop.api import ShippopAPI


class PrintLabelService:

    def generate_label_interleave(self, labels: List[str], shipments: List[Shipment]) -> str:
        pairs = list(zip(labels, shipments))
        template = loader.get_template('shipping_label.html')
        context = {
            'pairs': pairs,
            'left_over': []
        }
        s = template.render(context)
        return s

    def generate_label(self, param: PrintLabelParam) -> Optional[str]:
        shipments = (Shipment.objects
                     .filter(id__in=param.shipments)
                     .exclude(tracking_code__isnull=True)
                     .order_by('courier_code')
                     .all())
        if len(shipments) == 0:
            return None
        shippop = ShippopAPI()
        label_html = shippop.print_multiple_labels(tracking_codes=[s.tracking_code for s in shipments])
        labels = split_print_label(label_html)
        return PrintLabelService().generate_label_interleave(labels, shipments)
