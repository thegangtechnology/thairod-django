from django.template import loader
from typing import List
from shipment.models import Shipment


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
