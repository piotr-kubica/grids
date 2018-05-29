from datetime import datetime, timedelta


def timedelta_from_hh_mm(activity_duration):
    try:
        dt = datetime.strptime(activity_duration, "%H:%M")
        return timedelta(days=0, hours=dt.hour, minutes=dt.minute)
    except ValueError:
        return timedelta(0)


def timedelta_to_hh_mm(td):
    return ':'.join(str(td).split(':')[:2])
