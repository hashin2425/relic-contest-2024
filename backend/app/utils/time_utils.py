""" https://qiita.com/hashin2425/items/a2287f77d417faa5b2bc
"""

from datetime import datetime
from typing import Union
from zoneinfo import ZoneInfo

TIMEZONE_JST = ZoneInfo("Asia/Tokyo")
TIMEZONE_UTC = ZoneInfo("UTC")


def get_utc_now():
    return datetime.now(TIMEZONE_UTC)


def get_jst_now():
    return datetime.now(TIMEZONE_JST)


def parse_str_as_jst(dt_str, dt_format, dt_timezone: Union[str, None] = None):
    if dt_timezone is None:
        dt_timezone_obj = TIMEZONE_JST
    else:
        dt_timezone_obj = ZoneInfo(dt_timezone)

    return datetime.strptime(dt_str, dt_format).replace(tzinfo=dt_timezone_obj)
