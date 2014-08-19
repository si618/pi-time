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
