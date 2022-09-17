import datetime

from dateutil import tz


def read_last_line(path: str) -> str:
    line = ""
    with open(path) as f:
        for l in f:
            pass
        line = l
    return line


def parse_line(line: str):
    split = line.split(",")
    id = split[0]
    dt = parse_datetime(split[1])
    lat, lng = float(split[2]), float(split[3])
    return id, dt, lat, lng


TZ = tz.gettz("Asia/Tokyo")


def parse_datetime(datetime_str: str) -> datetime.datetime:
    year, month, day, hour, minute, second = [int(s) for s in datetime_str.split()]
    return datetime.datetime(year, month, day, hour, minute, second, tzinfo=TZ)
