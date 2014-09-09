import unittest

import pytz

from pi_time import settings
from pi_time.config import options


class OptionsTestCase(unittest.TestCase):

    def test_get_laptimer_options_returns_expected_options(self):
        # Arrange
        units = ('unitsOfMeasurement', settings.OPTIONS_UNIT_OF_MEASUREMENT)
        timezones = ('timezones', pytz.common_timezones)
        # Act
        laptimer_options = options.get_laptimer_options()
        # Assert
        self.assertSequenceEqual(units, laptimer_options[0])
        self.assertSequenceEqual(timezones, laptimer_options[1])


    def test_get_sensor_options_returns_expected_options(self):
        # Arrange
        locations = ('locations', settings.OPTIONS_SENSOR_LOCATION)
        hardwares = ('hardwares', settings.OPTIONS_HARDWARE)
        # Act
        sensor_options = options.get_sensor_options()
        # Assert
        self.assertEqual(locations, sensor_options[0])
        self.assertEqual(hardwares, sensor_options[1])
