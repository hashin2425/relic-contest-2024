""" https://qiita.com/hashin2425/items/a2287f77d417faa5b2bc
"""

from datetime import datetime
from zoneinfo import ZoneInfo


def get_utc_now():
    return datetime.now(ZoneInfo("UTC"))


def get_jst_now():
    return datetime.now(ZoneInfo("Asia/Tokyo"))


def parse_str_as_jst(dt_str, dt_format, dt_timezone="Asia/Tokyo"):
    return datetime.strptime(dt_str, dt_format).astimezone(ZoneInfo(dt_timezone))
