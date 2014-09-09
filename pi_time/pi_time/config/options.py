import pytz

from pi_time import settings


def get_laptimer_options():
    """
    Gets available options for all laptimer configuration items.

    :returns: Available laptimer options.
    :rtype: tuple.
    """
    laptimer_options = (
        ('unitsOfMeasurement', settings.OPTIONS_UNIT_OF_MEASUREMENT),
        ('timezones', pytz.common_timezones)
    )
    return laptimer_options
    

def get_sensor_options():
    """
    Gets available options for all sensor configuration items.

    :returns: Available sensor options.
    :rtype: tuple.
    """
    sensor_options = (
        ('locations', settings.OPTIONS_SENSOR_LOCATION),
        ('hardwares', settings.OPTIONS_HARDWARE)

    )
    return sensor_options

