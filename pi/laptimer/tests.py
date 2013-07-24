import datetime
import django_settings
from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from models import Track, Rider, Session, Lap

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
		now = timezone.make_aware(datetime.datetime.now(),
			timezone.get_default_timezone())
		Track.objects.create(name='Test Track', distance=10)
		track = Track.objects.get(id=1)
		Session.objects.create(name='Test Session', track=track)
		session = Session.objects.get(id=1)
		self.assertTrue(session.start >= now)

class LapTestCase(TestCase):

	@classmethod
	def setUpClass(cls):
		cls.start = timezone.make_aware(datetime.datetime.now(),
			timezone.get_default_timezone())

	def setUp(self):
		Track.objects.create(name='Test Track', distance=50, timeout=100)
		Rider.objects.create(name='Test Rider')
		Session.objects.create(name='Test Session',
			track=Track.objects.get(name='Test Track'), start=self.start)
		Lap.objects.create(session=Session.objects.get(name='Test Session'),
			rider=Rider.objects.get(name='Test Rider'), start=self.start)

	def test_avg_speed_per_hour_return_none_when_no_finish(self):
		lap = Lap.objects.get(id=1)
		self.assertEqual(None, lap.avg_speed_per_hour())

	def test_avg_speed_per_second_return_none_when_no_finish(self):
		lap = Lap.objects.get(id=1)
		self.assertEqual(None, lap.avg_speed_per_second())

	def test_avg_speed_per_hour_return_12kph_50m_in_15s(self):
		lap = Lap.objects.get(id=1)
		self.assertEqual(50, lap.session.track.distance)
		lap.finish = lap.start + datetime.timedelta(seconds=15)
		self.assertEqual(12, lap.avg_speed_per_hour())

	def test_avg_speed_per_second_return_5mps_50m_in_10s(self):
		lap = Lap.objects.get(id=1)
		self.assertEqual(50, lap.session.track.distance)
		lap.finish = lap.start + datetime.timedelta(seconds=10)
		self.assertEqual(5, lap.avg_speed_per_second())
