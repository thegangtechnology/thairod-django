from dataclasses import dataclass
from thairod.utils.auto_serialize import AutoSerialize


@dataclass
class Doctor(AutoSerialize):
    name: str
    license: str

    @classmethod
    def example(cls):
        return cls(name='สมชาย แซ่งตั้ง', license="A123932378")
