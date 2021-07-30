from django.db import models
from core.models import AbstractModel
from django.utils import timezone


class BatchShipment(AbstractModel):
    name = models.CharField(max_length=255, unique=True)

    @classmethod
    def generate_batch_name(cls) -> str:
        no_batch_create_today = cls.count_create_today()
        return f"{timezone.now().strftime('%Y-%m-%d')}_{no_batch_create_today+1}"

    @classmethod
    def count_create_today(cls) -> int:
        today = timezone.now().today()
        return BatchShipment.objects.filter(created_date__year=today.year,
                                            created_date__month=today.month,
                                            created_date__day=today.day).count()
