import datetime
import pytz

def to_start_on_date(d: datetime.date) -> datetime.datetime:
    return datetime.datetime.combine(d, datetime.datetime.min.time())


def to_end_on_date(d: datetime.date) -> datetime.datetime:
    return to_start_on_date(d) + datetime.timedelta(seconds=86400 - 1)

def convert_datetime_to_tz(d: datetime.datetime, tzinfo) -> datetime.datetime:
    return d.astimezone(tzinfo)

def attach_tzinfo_to_datetime(d: datetime.datetime, tzinfo) -> datetime.datetime:
    return tzinfo.localize(d)
