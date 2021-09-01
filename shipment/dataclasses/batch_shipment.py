from thairod.utils.auto_serialize import AutoSerialize
from dataclasses import dataclass
from typing import List


@dataclass
class BatchNameResponse(AutoSerialize):
    name: str

    @classmethod
    def example(cls):
        return cls(name="2021-07-29_1")


@dataclass
class AssignBatchToShipmentParam(AutoSerialize):
    batch_name: str
    shipments: List[int]

    @classmethod
    def example(cls):
        return cls(batch_name="2021-07-29_1",
                   shipments=[1, 2, 3, 4])


@dataclass
class UnassignBatchToShipmentParam(AutoSerialize):
    shipments: List[int]

    @classmethod
    def example(cls):
        return cls(shipments=[1, 2, 3, 4])
