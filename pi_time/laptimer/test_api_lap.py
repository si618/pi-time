from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from laptimer import api_lap
from laptimer.models import Lap, \
                            Rider, \
                            Session, \
                            Sensor, \
                            SensorEvent, \
                            Track
import logging


logger = logging.getLogger('laptimer')

class ApiLapTestCase(TestCase):
    '''Unit tests for lap related API functions.'''

    def test_change_rider_for_lap_passes(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session = Session.objects.create(name='bogus session',
            track=track)
        rider1 = Rider.objects.create(name='bogus rider 1')
        rider2 = Rider.objects.create(name='bogus rider 2')
        sensor = Sensor.objects.create(name='bogus sensor', track=track,
            sensor_pos=settings.SENSOR_POS_START_FINISH)
        lap = Lap.objects.create(session=session, rider=rider1)
        time = timezone.now()
        sensor_event = SensorEvent.objects.create(lap=lap, sensor=sensor,
            time=time)
        lap.start = sensor_event
        lap.save()
        # Act
        result = api_lap.change_rider_for_lap(track.name, session.name,
            rider1.name, time, rider2.name)
        # Assert
        self.assertTrue(result.ok)
        self.assertEqual('change_rider_for_lap', result.call)
        lap = Lap.objects.get(id=1)
        self.assertEqual(lap, result.data)
        self.assertEqual(time, lap.start.time)
        self.assertEqual(rider2, lap.rider)

    def test_remove_lap_passes(self):
        # Arrange
        # Act
        # Assert
        pass

    def test_remove_incomplete_laps_passes(self):
        # Arrange
        # Act
        # Assert
        pass

    def test_get_incomplete_laps_passes(self):
        # Arrange
        # Act
        # Assert
        pass
