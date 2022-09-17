import time
import RPi.GPIO as GPIO

AUDIO_PIN = 21
BUTTON_PIN = 5


def main():
    pwm = GPIO.PWM(AUDIO_PIN, 1)

    while True:
        if GPIO.input(BUTTON_PIN) == 0:
            print("Button pressed")

            send_gps_log()
            while GPIO.input(BUTTON_PIN) == 0:
                buzzer(pwm)
                time.sleep(0.01)

            print("Button released")

        time.sleep(0.03)


def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(AUDIO_PIN, GPIO.OUT, initial=GPIO.LOW)


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


def send_gps_log():
    print("Send GPS log")


if __name__ == "__main__":
    init()
    main()
