import serial
from micropyGPS import MicropyGPS


INTERVAL = 1


def main():
    uart = serial.Serial('/dev/serial0', 9600, timeout=10)
    my_gps = MicropyGPS(9, 'dd')

    tm_last = 0
    while True:
        sentence = uart.readline()
        if len(sentence) == 0:
            continue

        for x in sentence:
            if x < 10 or 126 < x:
                continue

            stat = my_gps.update(chr(x))
            if not stat:
                continue

            tm = my_gps.timestamp
            tm_now = (tm[0] * 3600) + (tm[1] * 60) + int(tm[2])
            if (tm_now - tm_last) < INTERVAL:
                continue
            tm_last = tm_now

            date_str = f"{my_gps.date_string()} {tm[0]} {tm[1]} {int(tm[2])}"
            latitude = my_gps.latitude[0]
            longitude = my_gps.longitude[0]
            print("="*20)
            print(f"date: {date_str}")
            print(f"latitude: {latitude}")
            print(f"longitude: {longitude}")

            with open("/var/log/device/gps.log", "a") as f:
                f.write(f"{date_str},{latitude},{longitude}\n")


if __name__ == "__main__":
    main()
