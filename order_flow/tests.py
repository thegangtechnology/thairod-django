from thairod.utils.load_seed import load_seed
from thairod.utils.test_util import TestCase
from order_flow.services import OrderFlowService
from order_flow.dataclasses import CreateOrderFlowRequest
from order_flow.models import OrderFlow


class TestOrderFlowService(TestCase):
    reset_sequences = True

    def setUp(self):
        load_seed()

    # TODO: More test after this week
    def test_create_order_flow(self):
        # minimal test because this is supposedly to be for next week
        old_count = OrderFlow.objects.count()
        OrderFlowService().create_order_flow(create_order_flow_request=CreateOrderFlowRequest.example())
        new_count = OrderFlow.objects.count()
        self.assertEqual(old_count + 1, new_count)
