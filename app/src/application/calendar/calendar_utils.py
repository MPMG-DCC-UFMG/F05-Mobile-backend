from datetime import datetime


def get_first_day_of_month() -> float:
    date_today = datetime.now()
    month_first_day = date_today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return month_first_day.timestamp() * 1000


def get_today() -> int:
    date_today = datetime.now()
    return int(date_today.timestamp() * 1000)
