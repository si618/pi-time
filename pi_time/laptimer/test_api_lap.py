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

    def test_add_lap_time_fails_when_session_not_found(self):
        # Arrange
        session_name = 'bogus session'
        rider_name = 'bogus rider'
        sensor_name = 'bogus sensor'
        time = None
        # Act
        result = api_lap.add_lap_time(session_name, rider_name, sensor_name, 
            time)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_lap_time', result.call)
        error = 'Session not found' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_add_lap_time_fails_when_rider_not_found(self):
        # Arrange
        session_name = 'bogus session'
        rider_name = 'bogus rider'
        sensor_name = 'bogus sensor'
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session = Session.objects.create(name=session_name, track_id=track.id)
        time = None
        # Act
        result = api_lap.add_lap_time(session_name, rider_name, sensor_name, 
            time)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_lap_time', result.call)
        error = 'Rider not found' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_add_lap_time_fails_when_sensor_not_found(self):
        # Arrange
        session_name = 'bogus session'
        rider_name = 'bogus rider'
        sensor_name = 'bogus sensor'
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session = Session.objects.create(name=session_name, track_id=track.id)
        rider = Rider.objects.create(name=rider_name)
        time = None
        # Act
        result = api_lap.add_lap_time(session_name, rider_name, sensor_name, 
            time)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_lap_time', result.call)
        error = 'Sensor not found' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_add_lap_time_fails_when_time_is_null(self):
        # Arrange
        track_name = 'bogus track'
        session_name = 'bogus session'
        rider_name = 'bogus rider'
        sensor_name = 'bogus sensor'
        track = Track.objects.create(name=track_name, distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session = Session.objects.create(name=session_name, track_id=track.id)
        rider = Rider.objects.create(name=rider_name)
        sensor = Sensor.objects.create(name=sensor_name, track_id=track.id,
            sensor_type=settings.SENSOR_START_FINISH)
        time = None
        # Act
        result = api_lap.add_lap_time(session_name, rider_name, sensor_name, 
            time)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_lap_time', result.call)
        error = 'Time must be valid datetime' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_add_lap_time_fails_when_time_is_not_datetime_object(self):
        # Arrange
        track_name = 'bogus track'
        session_name = 'bogus session'
        rider_name = 'bogus rider'
        sensor_name = 'bogus sensor'
        track = Track.objects.create(name=track_name, distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session = Session.objects.create(name=session_name, track_id=track.id)
        rider = Rider.objects.create(name=rider_name)
        sensor = Sensor.objects.create(name=sensor_name, track_id=track.id,
            sensor_type=settings.SENSOR_START_FINISH)
        time = 'bogus time'
        # Act
        result = api_lap.add_lap_time(session_name, rider_name, sensor_name, 
            time)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_lap_time', result.call)
        error = 'Time must be valid datetime' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_add_lap_time_passes_sensor_start(self):
        # Arrange
        track_name = 'bogus track'
        session_name = 'bogus session'
        rider_name = 'bogus rider'
        sensor_name = 'bogus sensor'
        track = Track.objects.create(name=track_name, distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session = Session.objects.create(name=session_name, track_id=track.id)
        rider = Rider.objects.create(name=rider_name)
        sensor = Sensor.objects.create(name=sensor_name, track_id=track.id,
            sensor_type=settings.SENSOR_START)
        time = timezone.now()
        # Act
        result = api_lap.add_lap_time(session_name, rider_name, sensor_name, 
            time)
        # Assert
        self.assertTrue(result.ok)
        self.assertEqual('add_lap_time', result.call)
        lap = Lap.objects.get(id=1)
        self.assertEqual(lap, result.data)
        self.assertEqual(time, lap.start.time)

    def test_add_lap_time_fails_sensor_start_when_existing_incomplete_lap(self):
        # Arrange
        track_name = 'bogus track'
        session_name = 'bogus session'
        rider_name = 'bogus rider'
        sensor_name = 'bogus sensor'
        track = Track.objects.create(name=track_name, distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session = Session.objects.create(name=session_name, track_id=track.id)
        rider = Rider.objects.create(name=rider_name)
        sensor = Sensor.objects.create(name=sensor_name, track_id=track.id,
            sensor_type=settings.SENSOR_START)
        time = timezone.now()
        lap = Lap.objects.create(session=session, rider=rider)
        lap.save()
        lapTime = SensorEvent.objects.create(lap=lap, sensor=sensor, time=time)
        lapTime.save()
        lap.start = lapTime
        lap.save()
        # Act
        result = api_lap.add_lap_time(session_name, rider_name, sensor_name, 
            time)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_lap_time', result.call)
        error = 'Unable to start lap as an incomplete lap for rider %s in ' \
                'session %s already exists' % (rider_name, session_name) # TODO: i18n
        self.assertEqual(error, result.data)

    def test_add_lap_time_passes_sensor_finish(self):
        # Arrange
        track_name = 'bogus track'
        session_name = 'bogus session'
        rider_name = 'bogus rider'
        sensor_start_name = 'bogus start sensor'
        sensor_finish_name = 'bogus finish sensor'
        track = Track.objects.create(name=track_name, distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session = Session.objects.create(name=session_name, track_id=track.id)
        rider = Rider.objects.create(name=rider_name)
        sensor_start = Sensor.objects.create(name=sensor_start_name, 
            track_id=track.id, sensor_type=settings.SENSOR_START)
        sensor_finish = Sensor.objects.create(name=sensor_finish_name, 
            track_id=track.id, sensor_type=settings.SENSOR_FINISH)
        time_start = timezone.now()
        lap_start = Lap.objects.create(session=session, rider=rider)
        lap_start.save()
        lapTime_start = SensorEvent.objects.create(lap=lap_start,
            sensor=sensor_start, time=time_start)
        lapTime_start.save()
        lap_start.start = lapTime_start
        lap_start.save()
        time_finish = timezone.now()
        # Act
        result = api_lap.add_lap_time(session_name, rider_name,
            sensor_finish_name, time_finish)
        # Assert
        self.assertTrue(result.ok)
        self.assertEqual('add_lap_time', result.call)
        lap = Lap.objects.get(id=1)
        self.assertEqual(lap, result.data)
        self.assertEqual(time_start, lap.start.time)
        self.assertEqual(time_finish, lap.finish.time)

    def test_add_lap_time_fails_sensor_finish_when_no_incomplete_lap(self):
        # Arrange
        track_name = 'bogus track'
        session_name = 'bogus session'
        rider_name = 'bogus rider'
        sensor_start_name = 'bogus start sensor'
        sensor_finish_name = 'bogus finish sensor'
        track = Track.objects.create(name=track_name, distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session = Session.objects.create(name=session_name, track_id=track.id)
        rider = Rider.objects.create(name=rider_name)
        sensor_start = Sensor.objects.create(name=sensor_start_name, 
            track_id=track.id, sensor_type=settings.SENSOR_START)
        sensor_finish = Sensor.objects.create(name=sensor_finish_name, 
            track_id=track.id, sensor_type=settings.SENSOR_FINISH)
        time_finish = timezone.now()
        # Act
        result = api_lap.add_lap_time(session_name, rider_name,
            sensor_finish_name, time_finish)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_lap_time', result.call)
        error = 'Unable to finish lap as no incomplete lap was found for ' \
                'rider %s in session %s' % (rider.name, session.name) # TODO: i18n
        self.assertEqual(error, result.data)

    def test_add_lap_time_fails_sensor_finish_when_multiple_incomplete_laps(self):
        # Arrange
        track_name = 'bogus track'
        session_name = 'bogus session'
        rider_name = 'bogus rider'
        sensor_start_name = 'bogus start sensor'
        sensor_finish_name = 'bogus finish sensor'
        track = Track.objects.create(name=track_name, distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session = Session.objects.create(name=session_name, track_id=track.id)
        rider = Rider.objects.create(name=rider_name)
        sensor_start = Sensor.objects.create(name=sensor_start_name, 
            track_id=track.id, sensor_type=settings.SENSOR_START)
        sensor_finish = Sensor.objects.create(name=sensor_finish_name, 
            track_id=track.id, sensor_type=settings.SENSOR_FINISH)
        time_1 = timezone.now()
        lap_1 = Lap.objects.create(session=session, rider=rider)
        lap_1.save()
        lapTime_1 = SensorEvent.objects.create(lap=lap_1, sensor=sensor_start,
            time=time_1)
        lapTime_1.save()
        lap_1.start = lapTime_1
        lap_1.save()
        time_2 = timezone.now()
        lap_2 = Lap.objects.create(session=session, rider=rider)
        lap_2.save()
        lapTime_2 = SensorEvent.objects.create(lap=lap_2, sensor=sensor_start,
            time=time_2)
        lapTime_2.save()
        lap_2.start = lapTime_2
        lap_2.save()
        time_finish = timezone.now()
        # Act
        result = api_lap.add_lap_time(session_name, rider_name,
            sensor_finish_name, time_finish)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_lap_time', result.call)
        error = 'Unable to finish lap as more than one incomplete lap was ' \
                'found for rider %s in session %s' % (rider.name, session.name) # TODO: i18n
        self.assertEqual(error, result.data)

    def test_add_lap_time_passes_sensor_start_finish_starts(self):
        # Arrange
        track_name = 'bogus track'
        session_name = 'bogus session'
        rider_name = 'bogus rider'
        sensor_name = 'bogus sensor'
        track = Track.objects.create(name=track_name, distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session = Session.objects.create(name=session_name, track_id=track.id)
        rider = Rider.objects.create(name=rider_name)
        sensor = Sensor.objects.create(name=sensor_name, track_id=track.id,
            sensor_type=settings.SENSOR_START_FINISH)
        time = timezone.now()
        # Act
        result = api_lap.add_lap_time(session_name, rider_name, sensor_name, 
            time)
        # Assert
        self.assertTrue(result.ok)
        self.assertEqual('add_lap_time', result.call)
        lap = Lap.objects.get(id=1)
        self.assertEqual(lap, result.data)
        self.assertEqual(time, lap.start.time)

    def test_add_lap_time_passes_sensor_start_finish_finishes(self):
        # Arrange
        track_name = 'bogus track'
        session_name = 'bogus session'
        rider_name = 'bogus rider'
        sensor_name = 'bogus sensor'
        track = Track.objects.create(name=track_name, distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session = Session.objects.create(name=session_name, track_id=track.id)
        rider = Rider.objects.create(name=rider_name)
        sensor = Sensor.objects.create(name=sensor_name, track_id=track.id,
            sensor_type=settings.SENSOR_START_FINISH)
        time_start = timezone.now()
        lap_start = Lap.objects.create(session=session, rider=rider)
        lap_start.save()
        lapTime_start = SensorEvent.objects.create(lap=lap_start, 
            sensor=sensor, time=time_start)
        lapTime_start.save()
        lap_start.start = lapTime_start
        lap_start.save()
        time_finish = timezone.now()
        # Act
        result = api_lap.add_lap_time(session_name, rider_name,
            sensor_name, time_finish)
        # Assert
        self.assertTrue(result.ok)
        self.assertEqual('add_lap_time', result.call)
        lap = Lap.objects.get(id=1)
        self.assertEqual(lap, result.data)
        self.assertEqual(time_start, lap.start.time)
        self.assertEqual(time_finish, lap.finish.time)

    def test_add_lap_time_fails_sensor_sector(self):
        # Arrange
        track_name = 'bogus track'
        session_name = 'bogus session'
        rider_name = 'bogus rider'
        sensor_name = 'bogus sensor'
        track = Track.objects.create(name=track_name, distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session = Session.objects.create(name=session_name, track_id=track.id)
        rider = Rider.objects.create(name=rider_name)
        sensor = Sensor.objects.create(name=sensor_name, track_id=track.id,
            sensor_type=settings.SENSOR_SECTOR)
        time = timezone.now()
        # Act
        result = api_lap.add_lap_time(session_name, rider_name, sensor_name, 
            time)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_lap_time', result.call)
        error = 'Sector based sensors not currently supported'
        self.assertEqual(error, result.data)
