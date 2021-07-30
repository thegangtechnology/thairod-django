from dataclasses import dataclass
from thairod.utils.auto_serialize import AutoSerialize


@dataclass
class Patient(AutoSerialize):
    name: str
    cid: str

    @classmethod
    def example(cls):
        return cls(name='คนป่วย รอเตียง', cid='3210987654321')
