from thairod.tasks import add
from thairod.utils.test_util import TestCase


class TestTasks(TestCase):
    with_seed = False

    def test_tasks(self):
        s = add.delay(3, 4)
        self.assertEqual(s.get(timeout=5), 7)
