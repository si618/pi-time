from django.conf import settings
from django.utils import timezone
import django_settings
import logging
import RPi.GPIO as GPIO
import time


logger = logging.getLogger('gpio')

class PiTimeGPIO:
    gpio_app = django_settings.get('gpio_app')
    gpio_lap = django_settings.get('gpio_lap')
    gpio_sensor = django_settings.get('gpio_sensor')

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpio_app, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.gpio_lap, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.gpio_sensor, GPIO.IN, initial=GPIO.LOW,
            pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.gpio_sensor, GPIO.RISING,
            callback=_sensor_event, bouncetime=1000)
        logging.debug('GPIO channels configured as app: %i lap: %i sensor: %i'
            % (self.gpio_app, self.gpio_lap, self.gpio_sensor))

    def appOpen(self):
        logging.debug('App open')
        _strobe_led(self.gpio_app, GPIO.HIGH)

    def appClose(self):
        logging.debug('App close')
        _strobe_led(self.gpio_app, GPIO.LOW)

    def cleanup(self):
        logging.debug('Cleaning up')
        GPIO.output(self.gpio_app, GPIO.LOW)
        GPIO.output(self.gpio_lap, GPIO.LOW)
        GPIO.remove_event_detect(self.gpio_sensor)
        GPIO.cleanup()

    def _sensor_event(self, channel):
        time = timezone.now()
        logging.debug('Sensor event')
        _strobe_led(self.gpio_lap, GPIO.LOW)
        # TODO: trigger event to call api.end_lap

    def _strobe_led(self, channel, final_state):
        on = not GPIO.input(channel)
        strobe_count = 10 # TODO: settings?
        strobe_sleep = 0.1 #
        for index in xrange(1, strobe_count):
            GPIO.output(channel, on)
            time.sleep(strobe_sleep)
            on = not on
        GPIO.output(channel, final_state)
