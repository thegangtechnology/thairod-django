from dataclasses import dataclass

from thairod.utils.auto_serialize import AutoSerialize
from thairod.utils.test_util import TestCase


@dataclass
class Sample(AutoSerialize):
    a: int

    def b(self) -> int:
        return self.a + 1

    @classmethod
    def fields(cls):
        return ['__all__', 'b']


class TestAutoSerialize(TestCase):
    with_seed = False

    def test_auto_serialize_has_property(self):
        serializer = Sample.serializer()
        d = serializer(Sample(a=1)).data
        self.assertDictEqual(d, {'a': 1, 'b': 2})
