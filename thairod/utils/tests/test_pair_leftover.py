from thairod.utils.collection_util import pair_leftover
from thairod.utils.test_util import TestCase


class TestPairLeftOver(TestCase):
    with_seed = False

    def test_pair_leftover_more_right(self):
        p, la, lb = pair_leftover([1, 2, 3], [9, 8, 7, 6])
        self.assertEqual(p, [(1, 9), (2, 8), (3, 7)])
        self.assertEqual(la, [])
        self.assertEqual(lb, [6])

    def test_pair_leftover_more_left(self):
        p, la, lb = pair_leftover([1, 2, 3, 4], [9, 8, 7])
        self.assertEqual(p, [(1, 9), (2, 8), (3, 7)])
        self.assertEqual(la, [4])
        self.assertEqual(lb, [])
