from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from models import Track, Rider, Session, Lap
import compute
import datetime
import django_settings
import unittest

class DjangoSettingsTestCase(TestCase):

	def test_unit_of_measurement_defaults_to_metric(self):
		self.assertTrue(django_settings.exists('unit_of_measurement'))
		self.assertEqual(settings.METRIC,
			django_settings.get('unit_of_measurement'))

	def test_gpio_app_defaults_to_11(self):
		self.assertTrue(django_settings.exists('gpio_app'))
		self.assertEqual(11, django_settings.get('gpio_app'))

	def test_gpio_lap_defaults_to_13(self):
		self.assertTrue(django_settings.exists('gpio_lap'))
		self.assertEqual(13, django_settings.get('gpio_lap'))

	def test_gpio_sensor_defaults_to_5(self):
		self.assertTrue(django_settings.exists('gpio_sensor'))
		self.assertEqual(5, django_settings.get('gpio_sensor'))

class TrackTestCase(TestCase):

	def test_timeout_defaults_to_twice_distance_when_none(self):
		Track.objects.create(name='Test Track', distance=10)
		track = Track.objects.get(id=1)
		self.assertEqual(20, track.timeout)

class SessionTestCase(TestCase):

	def test_start_defaults_to_now_when_none(self):
		now = timezone.now()
		Track.objects.create(name='Test Track', distance=10)
		track = Track.objects.get(id=1)
		Session.objects.create(name='Test Session', track=track)
		session = Session.objects.get(id=1)
		self.assertTrue(session.start >= now)

class LapTestCase(TestCase):

	@classmethod
	def setUpClass(cls):
		cls.start = timezone.now()

	def setUp(self):
		Track.objects.create(name='Test Track', distance=50, timeout=100)
		Rider.objects.create(name='Test Rider')
		Session.objects.create(name='Test Session',
			track=Track.objects.get(name='Test Track'), start=self.start)
		Lap.objects.create(session=Session.objects.get(name='Test Session'),
			rider=Rider.objects.get(name='Test Rider'), start=self.start)


class ComputeTestCase(unittest.TestCase):

	def test_average_kilometres_per_hour_returns_none_when_no_start(self):
		finish = timezone.now()
		self.assertEqual(None, 
			compute.average_kilometres_per_hour(None, finish, 10))

	def test_average_miles_per_hour_returns_none_when_no_start(self):
		finish = timezone.now()
		self.assertEqual(None, 
			compute.average_miles_per_hour(None, finish, 10))

	def test_average_speed_per_hour_returns_none_when_no_start(self):
		finish = timezone.now()
		self.assertEqual(None, 
			compute.average_speed_per_hour(None, finish, 10))

	def test_average_speed_per_second_returns_none_when_no_start(self):
		finish = timezone.now()
		self.assertEqual(None, 
			compute.average_speed_per_second(None, finish, 10))

	def test_average_kilometres_per_hour_returns_none_when_no_finish(self):
		start = timezone.now()
		self.assertEqual(None, 
			compute.average_kilometres_per_hour(start, None, 10))

	def test_average_miles_per_hour_returns_none_when_no_finish(self):
		start = timezone.now()
		self.assertEqual(None, 
			compute.average_miles_per_hour(start, None, 10))

	def test_average_speed_per_hour_returns_none_when_no_finish(self):
		start = timezone.now()
		self.assertEqual(None, 
			compute.average_speed_per_hour(start, None, 10))

	def test_average_speed_per_second_returns_none_when_no_finish(self):
		start = timezone.now()
		self.assertEqual(None, 
			compute.average_speed_per_second(start, None, 10))

	def test_average_speed_per_second_raises_exception_when_finish_equals_start(self):
		start = timezone.now()
		finish = start
		with self.assertRaises(ValueError):
			compute.average_speed_per_second(start, finish, 10)

	def test_average_speed_per_second_raises_exception_when_finish_less_than_start(self):
		finish = timezone.now()
		start = finish + datetime.timedelta(seconds=1)
		with self.assertRaises(ValueError):
			compute.average_speed_per_second(start, finish, 10)

	def test_average_speed_per_second_raises_exception_when_distance_equals_zero(self):
		start = timezone.now()
		finish = start + datetime.timedelta(seconds=1)
		with self.assertRaises(ValueError):
			compute.average_speed_per_second(start, finish, 0)

	def test_average_speed_per_second_raises_exception_when_distance_less_than_zero(self):
		start = timezone.now()
		finish = start + datetime.timedelta(seconds=1)
		with self.assertRaises(ValueError):
			compute.average_speed_per_second(start, finish, -0.1)

	def test_average_speed_per_second_returns_5mps_50m_in_10s(self):
		start = timezone.now()
		finish = start + datetime.timedelta(seconds=10)			
		self.assertEqual(5, 
			compute.average_speed_per_second(start, finish, 50))

	def test_average_kilometres_per_hour_returns_12kph_50m_in_15s(self):
		start = timezone.now()
		finish = start + datetime.timedelta(seconds=15)			
		self.assertEqual(12, 
			compute.average_kilometres_per_hour(start, finish, 50))

	def test_average_miles_per_hour_returns_expected_6_8182mph_50y_in_15s(self):
		start = timezone.now()
		finish = start + datetime.timedelta(seconds=15)			
		self.assertEqual(6.8182, 
			compute.average_miles_per_hour(start, finish, 50))

	def test_average_speed_per_hour_returns_metric_result(self):
		django_settings.set('String', 'unit_of_measurement', settings.METRIC)
		start = timezone.now()
		finish = start + datetime.timedelta(seconds=15)			
		self.assertEqual(12, 
			compute.average_speed_per_hour(start, finish, 50))

	def test_average_speed_per_hour_returns_imperial_result(self):
		django_settings.set('String', 'unit_of_measurement', settings.IMPERIAL)
		start = timezone.now()
		finish = start + datetime.timedelta(seconds=15)
		self.assertEqual(6.8182, 
			compute.average_speed_per_hour(start, finish, 50))
		django_settings.set('String', 'unit_of_measurement', settings.METRIC)
