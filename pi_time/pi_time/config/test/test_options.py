import unittest

from pytz import common_timezones

from pi_time import settings
from pi_time.config import options


class OptionsTestCase(unittest.TestCase):
    def test_get_laptimer_options_returns_expected_options(self):
        # Arrange
        units = settings.OPTIONS_UNIT_OF_MEASUREMENT
        timezones = common_timezones
        # Act
        laptimer_options = options.get_laptimer_options()
        # Assert
        self.assertSequenceEqual(units, laptimer_options['unitsOfMeasurement'])
        self.assertSequenceEqual(timezones, laptimer_options['timezones'])

    def test_get_sensor_options_returns_expected_options(self):
        # Arrange
        locations = settings.OPTIONS_SENSOR_LOCATION
        hardwares = settings.OPTIONS_HARDWARE
        # Act
        sensor_options = options.get_sensor_options()
        # Assert
        self.assertEqual(locations, sensor_options['locations'])
        self.assertEqual(hardwares, sensor_options['hardwares'])
