import os
import serial
import uuid

from firestore import send_gps_log
from micropyGPS import MicropyGPS
from sig_handler import SigHandler


INTERVAL = 60
GPS_LOG_PATH = "/var/log/device/gps.log"
SERIAL_PORT = os.environ.get("SERIAL_PORT", "/dev/serial0")


def main():
    uart = serial.Serial(SERIAL_PORT, 9600, timeout=10)
    my_gps = MicropyGPS(9, 'dd')

    sig_handler = SigHandler()

    tm_last = 0
    while not sig_handler.killed:
        sentence = uart.readline()
        if len(sentence) == 0:
            continue

        for x in sentence:
            if x < 10 or 126 < x:
                continue

            stat = my_gps.update(chr(x))
            if not stat:
                continue

            time = my_gps.timestamp
            hour, minute, second = time[0], time[1], int(time[2])
            tm_now = (hour * 3600) + (minute * 60) + second
            if (tm_now - tm_last) < INTERVAL:
                continue
            tm_last = tm_now

            year, month, day = parse_date(my_gps.date)
            if year == "0" or month == "0" or day == "0":
                continue
            datetime_str = f"{year} {month} {day} {hour} {minute} {second}"

            lat, lng = my_gps.latitude[0], my_gps.longitude[0]
            if lat == 0 or lng == 0:
                continue
            # NOTE: add value to hide real one
            lat += 0.5
            lng += 0.5

            id = str(uuid.uuid4())

            send_gps_log(datetime_str, lat, lng, id)
            with open(GPS_LOG_PATH, "a") as f:
                f.write(f"{id},{datetime_str},{lat},{lng}\n")
            dump_gps(id, datetime_str, lat, lng)

    print("Finish gps")


def parse_date(date: list):
    year = f"20{date[2]}" if date[2] != 0 else "0"
    month = date[1]
    day = date[0]
    return year, month, day


def dump_gps(id: str, date: str, latitude: float, longitude: float):
    print("="*20)
    print(f"id: {id}")
    print(f"date: {date}")
    print(f"latitude: {latitude}")
    print(f"longitude: {longitude}")


if __name__ == "__main__":
    main()
