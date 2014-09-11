import unittest

import pytz

from datetime import datetime, timedelta

from pi_time import compute, settings


class ComputeTestCase(unittest.TestCase):

    def testaverage_kilometres_per_hour_returns_none_when_no_start(self):
        # Arrange
        finish = datetime.now(pytz.utc)
        # Act
        avg_kph = compute.average_kilometres_per_hour(None, finish, 10)
        # Assert
        self.assertEqual(None, avg_kph)

    def testaverage_miles_per_hour_returns_none_when_no_start(self):
        # Arrange
        finish = datetime.now(pytz.utc)
        # Act
        avg_mph = compute.average_miles_per_hour(None, finish, 10)
        # Assert
        self.assertEqual(None, avg_mph)

    def test_average_speed_per_hour_returns_none_when_no_start(self):
        # Arrange
        finish = datetime.now(pytz.utc)
        # Act
        avg_sph = compute.average_speed_per_hour(None, finish, 10)
        # Assert
        self.assertEqual(None, avg_sph)

    def test_average_speed_per_second_returns_none_when_no_start(self):
        # Arrange
        finish = datetime.now(pytz.utc)
        # Act
        avg_sps = compute.average_speed_per_second(None, finish, 10)
        # Assert
        self.assertEqual(None, avg_sps)

    def testaverage_kilometres_per_hour_returns_none_when_no_finish(self):
        # Arrange
        start = datetime.now(pytz.utc)
        # Act
        avg_kph = compute.average_kilometres_per_hour(start, None, 10)
        # Assert
        self.assertEqual(None, avg_kph)

    def testaverage_miles_per_hour_returns_none_when_no_finish(self):
        # Arrange
        start = datetime.now(pytz.utc)
        # Act
        avg_mph = compute.average_miles_per_hour(start, None, 10)
        # Assert
        self.assertEqual(None, avg_mph)

    def test_average_speed_per_hour_returns_none_when_no_finish(self):
        # Arrange
        start = datetime.now(pytz.utc)
        # Act
        avg_sph = compute.average_speed_per_hour(start, None, 10)
        # Assert
        self.assertEqual(None, avg_sph)

    def test_average_speed_per_second_returns_none_when_no_finish(self):
        # Arrange
        start = datetime.now(pytz.utc)
        # Act
        avg_sps = compute.average_speed_per_second(start, None, 10)
        # Assert
        self.assertEqual(None, avg_sps)

    def test_average_speed_per_second_raises_exception_when_finish_equals_start(self):
        # Arrange
        start = datetime.now(pytz.utc)
        finish = start
        # Act
        with self.assertRaises(ValueError) as context:
            compute.average_speed_per_second(start, finish, 10)
        # Assert
        self.assertEqual(context.exception.message,
            'Start time must be before finish time!')

    def test_average_speed_per_second_raises_exception_when_finish_less_than_start(self):
        # Arrange
        finish = datetime.now(pytz.utc)
        start = finish + timedelta(seconds=1)
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            compute.average_speed_per_second(start, finish, 10)
        # Assert
        self.assertEqual(context.exception.message,
            'Start time must be before finish time!')

    def test_average_speed_per_second_raises_exception_when_distance_equals_zero(self):
        # Arrange
        start = datetime.now(pytz.utc)
        finish = start + timedelta(seconds=1)
        # Act
        with self.assertRaises(ValueError) as context:
            compute.average_speed_per_second(start, finish, 0)
        # Assert
        self.assertEqual(context.exception.message,
            'Track distance must be greater than zero!')

    def test_average_speed_per_second_raises_exception_when_distance_less_than_zero(self):
        # Arrange
        start = datetime.now(pytz.utc)
        finish = start + timedelta(seconds=1)
        # Act
        with self.assertRaises(ValueError) as context:
            compute.average_speed_per_second(start, finish, -0.1)
        # Assert
        self.assertEqual(context.exception.message,
            'Track distance must be greater than zero!')

    def test_average_speed_per_second_returns_5mps_50m_in_10s(self):
        # Arrange
        start = datetime.now(pytz.utc)
        finish = start + timedelta(seconds=10)
        # Act
        avg_sps = compute.average_speed_per_second(start, finish, 50)
        # Assert
        self.assertEqual(5, avg_sps)

    def testaverage_kilometres_per_hour_returns_12kph_50m_in_15s(self):
        # Arrange
        start = datetime.now(pytz.utc)
        finish = start + timedelta(seconds=15)
        # Act
        avg_kph = compute.average_kilometres_per_hour(start, finish, 50)
        # Assert
        self.assertEqual(12, avg_kph)

    def testaverage_miles_per_hour_returns_expected_6_8182mph_50y_in_15s(self):
        # Arrange
        start = datetime.now(pytz.utc)
        finish = start + timedelta(seconds=15)
        # Act
        avg_mph = compute.average_miles_per_hour(start, finish, 50)
        # Assert
        self.assertEqual(6.8182, avg_mph)

    def test_average_speed_per_hour_returns_metric_result(self):
        # Arrange
        unit_of_measurement = settings.METRIC
        start = datetime.now(pytz.utc)
        finish = start + timedelta(seconds=15)
        # Act
        avg_sph = compute.average_speed_per_hour(start, finish, 50,
            unit_of_measurement)
        # Assert
        self.assertEqual(12, avg_sph)

    def test_average_speed_per_hour_returns_imperial_result(self):
        # Arrange
        unit_of_measurement = settings.IMPERIAL
        start = datetime.now(pytz.utc)
        finish = start + timedelta(seconds=15)
        # Act
        avg_sph = compute.average_speed_per_hour(start, finish, 50,
            unit_of_measurement)
        # Assert
        self.assertEqual(6.8182, avg_sph)

    def test_average_speed_per_hour_returns_imperial_result(self):
        # Arrange
        unit_of_measurement = 'Bogus'
        start = datetime.now(pytz.utc)
        finish = start + timedelta(seconds=15)
        # Act
        with self.assertRaises(ValueError) as context:
            compute.average_speed_per_hour(start, finish, 50,
                unit_of_measurement)
        # Assert
        self.assertEqual(context.exception.message,
            "Unknown unit of measurement 'Bogus'")


if __name__ == '__main__':
    unittest.main()