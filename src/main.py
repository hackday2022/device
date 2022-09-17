import RPi.GPIO as GPIO
import time

from firestore import send_gps_id
from gps import GPS_LOG_PATH
from util import parse_last_line
from sig_handler import SigHandler


AUDIO_PIN = 21
BUTTON_PIN = 5


def main():
    pwm = GPIO.PWM(AUDIO_PIN, 1)

    sig_handler = SigHandler()

    while not sig_handler.killed:
        if GPIO.input(BUTTON_PIN) == 0:
            print("Button pressed")

            send(GPS_LOG_PATH)
            while GPIO.input(BUTTON_PIN) == 0:
                buzzer(pwm)
                time.sleep(0.01)

            print("Button released")

        time.sleep(0.03)


def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(AUDIO_PIN, GPIO.OUT, initial=GPIO.LOW)


def send(gps_log_path: str):
    print("Send gps log")
    id, _, _, _ = parse_last_line(gps_log_path)
    send_gps_id(id)


FREQ_MIN = 599
FREQ_MAX = 1500
FREQ_STEP = 100
INTERVAL = 0.005


def buzzer(pwm):
    pwm.start(50)

    for freq in range(FREQ_MAX, FREQ_MIN, -FREQ_STEP):
        pwm.ChangeFrequency(freq)
        time.sleep(INTERVAL)
    for freq in range(FREQ_MIN, FREQ_MAX, FREQ_STEP):
        pwm.ChangeFrequency(freq)
        time.sleep(INTERVAL)

    pwm.stop()


if __name__ == "__main__":
    init()
    main()
