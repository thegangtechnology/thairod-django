from shipment.models.box_size import BoxSize
from thairod.utils.test_util import TestCase


class TestBoxSize(TestCase):
    with_db = False

    def test_default_box_id(self):
        ret = BoxSize.get_default_box_id()
        self.assertEqual(type(ret), int)
