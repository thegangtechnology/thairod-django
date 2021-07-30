from thairod.utils.auto_serialize import AutoSerialize
from dataclasses import dataclass
from typing import List


@dataclass
class PrintLabelParam(AutoSerialize):
    shipments: List[int]

    @classmethod
    def example(cls):
        return ['1', '2', '3']
