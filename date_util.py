from datetime import datetime, date
import calendar

def roll_year(dt: date, year: int) -> date:
    if (calendar.isleap(dt.year) and dt.month == 2 and dt.day == 29
        and not calendar.isleap(dt.year + year)):
        return datetime(dt.year + year, dt.month, 28).date()

    return datetime(dt.year + year, dt.month, dt.day).date()

def date_from_str(date_string: str) -> date:
    return datetime.strptime(date_string, "%Y-%m-%d").date()
