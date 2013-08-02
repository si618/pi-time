from django.conf import settings
from django.utils import timezone
import django_settings
import logging
import RPi.GPIO as GPIO
import time


logger = logging.getLogger('laptimer')

class LapTimerGPIO:
    gpio_app = django_settings.get('gpio_app')
    gpio_lap = django_settings.get('gpio_lap')
    gpio_sensor = django_settings.get('gpio_sensor')

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpio_app, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.gpio_lap, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.gpio_sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.gpio_sensor, GPIO.RISING,
            callback=_sensor_event_detected, bouncetime=1000)
        logging.debug('GPIO channels configured as app: %i lap: %i sensor: %i'
            % (self.gpio_app, self.gpio_lap, self.gpio_sensor))

    def flashAppReady(self):
        logging.debug('Flashing app ready')
        _strobe_led(self.gpio_app, GPIO.HIGH)

    def cleanup(self):
        logging.debug('Cleaning up')
        GPIO.output(self.gpio_app, GPIO.LOW)
        GPIO.output(self.gpio_lap, GPIO.LOW)
        GPIO.remove_event_detect(self.gpio_sensor)
        GPIO.cleanup()

    def _sensor_event_detected(self, channel):
        time = timezone.now()
        logging.debug('Sensor event detected')
        _strobe_led(self.gpio_lap, GPIO.HIGH)

    def _strobe_led(self, channel, final_state):
        on = not GPIO.input(channel)
        for index in xrange(1, 10):
            GPIO.output(channel, on)
            time.sleep(0.1)
            on = not on
        GPIO.output(channel, final_state)