from datetime import datetime as dt

from django.utils import timezone


def datetime(year: int, month: int = 1, day: int = 1, hour: int = 0, minute: int = 0, *args, **kwds) -> dt:
    """Gives Timezone Aware Localtime"""
    return timezone.make_aware(dt(year=year, month=month, day=day, hour=hour, minute=minute))


def now() -> dt:
    """Gives Timezone Aware Now"""
    return dt.now(tz=timezone.get_current_timezone())
