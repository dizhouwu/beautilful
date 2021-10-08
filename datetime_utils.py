import datetime
import pytz

def to_utc(datetime1: datetime.datetime):
    utc_datetime1 = datetime1.astimezone(datetime.timezone.utc).replace(tzinfo=None)
    return utc_datetime1

def to_eastern(datetime1: datetime.datetime):
    eastern_datetime1 = datetime1.astimezone(pytz.timezone("America/New_York")).replace(tzinfo=None)
    return eastern_datetime1
