from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from laptimer import api
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
        self.assertEqual(15, django_settings.get('gpio_app'))

    def test_gpio_lap_defaults_to_13(self):
        self.assertTrue(django_settings.exists('gpio_lap'))
        self.assertEqual(16, django_settings.get('gpio_lap'))

    def test_gpio_sensor_defaults_to_18(self):
        self.assertTrue(django_settings.exists('gpio_sensor'))
        self.assertEqual(18, django_settings.get('gpio_sensor'))


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


class ApiTestCase(TestCase):

    # TODO:

    # Rider tests

    def test_add_rider_fails_when_rider_exists(self):
        rider = Rider.objects.create(name='bogus')
        result = api.add_rider(rider.name)
        self.assertFalse(result.result)
        self.assertEqual('add_rider', result.call)
        error = 'Rider already exists' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_add_rider_fails_when_name_invalid(self):
        result = api.add_rider(rider_name=None)
        self.assertFalse(result.result)
        self.assertEqual('add_rider', result.call)
        self.assertEqual('IntegrityError', result.data)

    def test_add_rider_passes(self):
        name = 'bogus'
        result = api.add_rider(name)
        self.assertTrue(Rider.objects.filter(name=name).exists())
        self.assertTrue(result.result)
        self.assertEqual('add_rider', result.call)
        rider = Rider.objects.get(name=name)
        self.assertEqual(rider, result.data)

    def test_change_rider_fails_when_rider_not_found(self):
        result = api.change_rider('bogus', 'none')
        self.assertFalse(result.result)
        self.assertEqual('change_rider', result.call)
        error = 'Rider not found' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_change_rider_fails_when_new_rider_exists(self):
        rider = Rider.objects.create(name='bogus')
        result = api.change_rider('none', rider.name)
        self.assertFalse(result.result)
        self.assertEqual('change_rider', result.call)
        error = 'Rider already exists' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_change_rider_passes(self):
        first_name = 'bogus'
        changed_name = 'betty'
        Rider.objects.create(name=first_name)
        result = api.change_rider(first_name, changed_name)
        self.assertTrue(Rider.objects.filter(name=changed_name).exists())
        self.assertTrue(result.result)
        self.assertEqual('change_rider', result.call)
        rider = Rider.objects.get(name=changed_name)
        self.assertEqual(rider, result.data)

    def test_remove_rider_fails_when_rider_not_found(self):
        result = api.remove_rider('bogus')
        self.assertFalse(result.result)
        self.assertEqual('remove_rider', result.call)
        error = 'Rider not found' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_remove_rider_passes(self):
        name = 'bogus'
        rider = Rider.objects.create(name=name)
        result = api.remove_rider(name)
        self.assertFalse(Rider.objects.filter(name=name).exists())
        self.assertTrue(result.result)
        self.assertEqual('remove_rider', result.call)
        self.assertEqual(name, result.data)

    # Track tests

    def test_add_track_fails_when_track_exists(self):
        track = Track.objects.create(name='bogus', distance=50, timeout=100,
            unit_of_measurement=settings.METRIC)
        result = api.add_track(track.name, track.distance, track.timeout,
            track.unit_of_measurement)
        self.assertFalse(result.result)
        self.assertEqual('add_track', result.call)
        error = 'Track already exists' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_add_track_fails_when_distance_invalid(self):
        result = api.add_track('bogus', 'FUBAR', 100, settings.METRIC)
        self.assertFalse(result.result)
        self.assertEqual('add_track', result.call)
        self.assertEqual('ValueError', result.data)

    def test_add_track_fails_when_timeout_invalid(self):
        result = api.add_track('bogus', 50, 'FUBAR', settings.METRIC)
        self.assertFalse(result.result)
        self.assertEqual('add_track', result.call)
        self.assertEqual('ValueError', result.data)

    def test_add_track_fails_when_unit_of_measurement_invalid(self):
        result = api.add_track('bogus', 50, 100, 'FUBAR')
        self.assertFalse(result.result)
        self.assertEqual('add_track', result.call)
        self.assertEqual('Invalid unit of measurement', result.data)

    def test_add_track_passes(self):
        name = 'bogus'
        result = api.add_track(name, 50, 100, settings.METRIC)
        self.assertTrue(Track.objects.filter(name=name).exists())
        self.assertTrue(result.result)
        self.assertEqual('add_track', result.call)
        track = Track.objects.get(name=name)
        self.assertEqual(track, result.data)

    # Session tests

    # Lap tests
