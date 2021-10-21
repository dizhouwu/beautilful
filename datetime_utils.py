import datetime
import pytz

def to_start_on_date(d: datetime.date) -> datetime.datetime:
    return datetime.datetime.combine(d, datetime.datetime.min.time())


def to_end_on_date(d: datetime.date) -> datetime.datetime:
    return to_start_on_date(d) + datetime.timedelta(seconds=86400 - 1)
