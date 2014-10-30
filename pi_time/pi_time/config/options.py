from pytz import common_timezones

from pi_time import settings


def get_laptimer_options():
    """
    Gets available options for all laptimer configuration items.

    :returns: Available laptimer options.
    :rtype: dictionary.
    """
    laptimer_options = dict()
    laptimer_options['unitsOfMeasurement'] = settings.OPTIONS_UNIT_OF_MEASUREMENT
    laptimer_options['timezones'] = common_timezones
    laptimer_options['pins'] = settings.OPTIONS_PIN_LAPTIMER
    return laptimer_options


def get_sensor_options():
    """
    Gets available options for all sensor configuration items.

    :returns: Available sensor options.
    :rtype: dictionary.
    """
    sensor_options = dict()
    sensor_options['locations'] = settings.OPTIONS_SENSOR_LOCATION
    sensor_options['hardwares'] = settings.OPTIONS_HARDWARE
    sensor_options['pins'] = settings.OPTIONS_PIN_SENSOR
    return sensor_options

