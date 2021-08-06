from order_flow.dataclasses import CreateOrderFlowRequest
from order_flow.models import OrderFlow
from order_flow.services import OrderFlowService
from thairod.utils.test_util import TestCase


class TestOrderFlowService(TestCase):

    # TODO: More test
    def test_create_order_flow(self):
        # minimal test because this is supposedly to be for next week
        old_count = OrderFlow.objects.count()
        OrderFlowService().create_order_flow(create_order_flow_request=CreateOrderFlowRequest.example())
        new_count = OrderFlow.objects.count()
        self.assertEqual(old_count + 1, new_count)
