from __future__ import annotations

from django.db import models

from core.models import AbstractModel


class Address(AbstractModel):
    name = models.CharField(max_length=255)
    lat = models.DecimalField(decimal_places=7, max_digits=15, null=True)
    lon = models.DecimalField(decimal_places=7, max_digits=15, null=True)
    house_number = models.CharField(max_length=255)
    subdistrict = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=5)
    country = models.CharField(max_length=255)
    telno = models.CharField(max_length=255)
    note = models.CharField(max_length=255, blank=True, default="")

    def full_address(self) -> str:
        s = self
        return f'{s.house_number} แขวง/ตำบล {s.subdistrict} เขต/อำเภอ {s.district} จังหวัด {s.province} {s.postal_code}'

    @classmethod
    def example(cls) -> Address:
        return Address(
            name='คนไทย ใจดี',
            house_number='เลขที่ 599 สามแยกกล้วยน้ำไท',
            subdistrict='คลองเตย',
            district='คลองเตย',
            province='กรุงเทพมหานคร',
            postal_code='10110',
            country='Thailand',
            telno='0928908989',
            note='เลยร้านตามสั่งมา 2 หลัง'
        )
