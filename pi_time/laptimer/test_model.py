from django.conf import settings
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone
from laptimer.models import Lap, \
                            Rider, \
                            Session, \
                            Sensor, \
                            SensorEvent, \
                            Track


class TrackTestCase(TestCase):

    def test_timeout_defaults_to_twice_distance_when_none(self):
        # Arrange
        Track.objects.create(name='Test Track', distance=10)
        track = Track.objects.get(id=1)
        # Act
        timeout = track.timeout
        # Assert
        self.assertEqual(20, timeout)


class SessionTestCase(TestCase):

    def test_start_defaults_to_now_when_none(self):
        # Arrange
        now = timezone.now()
        Track.objects.create(name='Test Track', distance=10)
        track = Track.objects.get(id=1)
        Session.objects.create(name='Test Session', track=track)
        session = Session.objects.get(id=1)
        # Act & Assert
        self.assertTrue(session.start >= now)

    def test_session_create_fails_when_session_not_unique_for_track(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session_name = 'bogus session'
        Session.objects.create(name=session_name, track=track)
        # Act & assert
        with self.assertRaises(IntegrityError):
            Session.objects.create(name=session_name, track=track)

    def test_session_create_passes_when_session_not_unique_for_different_tracks(self):
        # Arrange
        track1 = Track.objects.create(name='bogus track 1', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        track2 = Track.objects.create(name='bogus track 2', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session_name = 'bogus session'
        Session.objects.create(name=session_name, track=track1)
        # Act & assert
        Session.objects.create(name=session_name, track=track2)


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
        # TODO: SensorEvent + tests
