from datetime import datetime

import pytz

timezone_kst = pytz.timezone('Asia/Seoul')
timezone_utc = pytz.utc


def now() -> datetime:
    return datetime.now(tz=timezone_kst)


def utc_now() -> datetime:
    return datetime.now(tz=timezone_utc)
