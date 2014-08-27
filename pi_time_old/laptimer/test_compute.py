from django.conf import settings
from django.test import TestCase
from django.utils import timezone
import compute
import datetime
import django_settings


class ComputeTestCase(TestCase):

    def test_average_kilometres_per_hour_returns_none_when_no_start(self):
        # Arrange
        finish = timezone.now()
        # Act
        avg_kph = compute.average_kilometres_per_hour(None, finish, 10)
        # Assert
        self.assertEqual(None, avg_kph)

    def test_average_miles_per_hour_returns_none_when_no_start(self):
        # Arrange
        finish = timezone.now()
        # Act
        avg_mph = compute.average_miles_per_hour(None, finish, 10)
        # Assert
        self.assertEqual(None, avg_mph)

    def test_average_speed_per_hour_returns_none_when_no_start(self):
        # Arrange
        finish = timezone.now()
        # Act
        avg_sph = compute.average_speed_per_hour(None, finish, 10)
        # Assert
        self.assertEqual(None, avg_sph)

    def test_average_speed_per_second_returns_none_when_no_start(self):
        # Arrange
        finish = timezone.now()
        # Act
        avg_sps = compute.average_speed_per_second(None, finish, 10)
        # Assert
        self.assertEqual(None, avg_sps)

    def test_average_kilometres_per_hour_returns_none_when_no_finish(self):
        # Arrange
        start = timezone.now()
        # Act
        avg_kph = compute.average_kilometres_per_hour(start, None, 10)
        # Assert
        self.assertEqual(None, avg_kph)

    def test_average_miles_per_hour_returns_none_when_no_finish(self):
        # Arrange
        start = timezone.now()
        # Act
        avg_mph = compute.average_miles_per_hour(start, None, 10)
        # Assert
        self.assertEqual(None, avg_mph)

    def test_average_speed_per_hour_returns_none_when_no_finish(self):
        # Arrange
        start = timezone.now()
        # Act
        avg_sph = compute.average_speed_per_hour(start, None, 10)
        # Assert
        self.assertEqual(None, avg_sph)

    def test_average_speed_per_second_returns_none_when_no_finish(self):
        # Arrange
        start = timezone.now()
        # Act
        avg_sps = compute.average_speed_per_second(start, None, 10)
        # Assert
        self.assertEqual(None, avg_sps)

    def test_average_speed_per_second_raises_exception_when_finish_equals_start(self):
        # Arrange
        start = timezone.now()
        finish = start
        # Act & Assert
        with self.assertRaises(ValueError):
            compute.average_speed_per_second(start, finish, 10)

    def test_average_speed_per_second_raises_exception_when_finish_less_than_start(self):
        # Arrange
        finish = timezone.now()
        start = finish + datetime.timedelta(seconds=1)
        # Act & Assert
        with self.assertRaises(ValueError):
            compute.average_speed_per_second(start, finish, 10)

    def test_average_speed_per_second_raises_exception_when_distance_equals_zero(self):
        # Arrange
        start = timezone.now()
        finish = start + datetime.timedelta(seconds=1)
        # Act & assert
        with self.assertRaises(ValueError):
            compute.average_speed_per_second(start, finish, 0)

    def test_average_speed_per_second_raises_exception_when_distance_less_than_zero(self):
        # Arrange
        start = timezone.now()
        finish = start + datetime.timedelta(seconds=1)
        # Act & Assert
        with self.assertRaises(ValueError):
            compute.average_speed_per_second(start, finish, -0.1)

    def test_average_speed_per_second_returns_5mps_50m_in_10s(self):
        # Arrange
        start = timezone.now()
        finish = start + datetime.timedelta(seconds=10)
        # Act
        avg_sps = compute.average_speed_per_second(start, finish, 50)
        # Assert
        self.assertEqual(5, avg_sps)

    def test_average_kilometres_per_hour_returns_12kph_50m_in_15s(self):
        # Arrange
        start = timezone.now()
        finish = start + datetime.timedelta(seconds=15)
        # Act
        avg_kph = compute.average_kilometres_per_hour(start, finish, 50)
        # Assert
        self.assertEqual(12, avg_kph)

    def test_average_miles_per_hour_returns_expected_6_8182mph_50y_in_15s(self):
        # Arrange
        start = timezone.now()
        finish = start + datetime.timedelta(seconds=15)
        # Act
        avg_mph = compute.average_miles_per_hour(start, finish, 50)
        # Assert
        self.assertEqual(6.8182, avg_mph)

    def test_average_speed_per_hour_returns_metric_result(self):
        # Arrange
        django_settings.set('String', 'unit_of_measurement', settings.METRIC)
        start = timezone.now()
        finish = start + datetime.timedelta(seconds=15)
        # Act
        avg_sph = compute.average_speed_per_hour(start, finish, 50)
        # Assert
        self.assertEqual(12, avg_sph)

    def test_average_speed_per_hour_returns_imperial_result(self):
        # Arrange
        django_settings.set('String', 'unit_of_measurement', settings.IMPERIAL)
        start = timezone.now()
        finish = start + datetime.timedelta(seconds=15)
        # Act
        avg_sph = compute.average_speed_per_hour(start, finish, 50)
        # Assert
        self.assertEqual(6.8182, avg_sph)
        django_settings.set('String', 'unit_of_measurement', settings.METRIC)
