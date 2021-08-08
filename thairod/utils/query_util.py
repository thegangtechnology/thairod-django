import datetime
from typing import Optional, Any, List, Tuple

from django.db.models import Q


def smart_equal(col, value: Optional[Any]) -> Q:
    if value is None:
        return Q()
    else:
        return Q(**{col: value})


def smart_range(col, begin, end) -> Q:
    if begin is None and end is None:
        return Q()
    elif begin is None and end is not None:
        return Q(**{f"{col}__lt": end})
    elif begin is not None and end is None:
        return Q(**{f"{col}__ge": begin})
    else:
        return Q(**{f"{col}__range": (begin, end)})


def to_intervals(dates: List[datetime.datetime]) -> List[Tuple[datetime.datetime, datetime.datetime]]:
    """ Convert dates to intervals (sorted from latest to oldest)

    Args:
        dates (List[datetime.datetime]):

    Returns:
        List[Tuple[begin, end]]
    """
    sorted_dates = sorted(dates, reverse=True)
    ret = []
    for begin, end in zip(sorted_dates[1:], sorted_dates[:-1]):
        ret.append((begin, end))
    return ret


def date_range(anchor: datetime.datetime, max_day_diff: int) -> List[datetime.datetime]:
    """List of dates including date_range
    until the date where date-anchor == max_day_diff inclusive

    Args:
        anchor ():
        max_day_diff ():

    Returns:
        List[datetime.datetime]
    """
    step = 1 if max_day_diff > 0 else -1
    return [anchor + datetime.timedelta(days=i) for i in range(0, max_day_diff + step, step)]


def replace_hour(date: datetime.datetime, hour: int) -> datetime.datetime:
    """Replace hour but preserve timezone etc.

    Args:
        date (datetime.datetime):
        hour (int):

    Returns:
        new date at specify hour. minute, second and microseconds are set to 0

    """
    return date.replace(hour=hour, minute=0, second=0, microsecond=0)


def round_to_next_nearest_hour(date: datetime.datetime,
                               hour: int) -> datetime.datetime:
    """Round the date to next nearest hour. That is tomorrow if the date already pass that hour.

    Args:
        date ():
        hour ():

    Returns:
        datetime.datetime
    """
    cutoff_dt = replace_hour(date, hour=hour)
    if date > cutoff_dt:
        return replace_hour(date + datetime.timedelta(days=1), hour=hour)
    else:
        return cutoff_dt
