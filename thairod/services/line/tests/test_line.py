from thairod.services.line.line import send_line_message, send_line_tracking_message
from thairod.utils.test_util import TestCase


class TestLine(TestCase):
    patch_external = True
    with_seed = False

    def setUp(self) -> None:
        self.uid = 'U5f7f3fc4414c147a0c029e93071d8700'

    def test_send_line_message(self):
        ret = send_line_message(self.uid, 'hello')
        self.assertTrue(ret)

    def test_send_tracking_message(self):
        ret = send_line_tracking_message(self.uid, name='ปิติ องค์มงคลกุล', shippop_tracking_code='SP025181932')
        self.assertTrue(ret)
