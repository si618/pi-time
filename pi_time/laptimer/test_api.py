from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from laptimer import api
from laptimer.models import Lap, \
                            Rider, \
                            Session, \
                            Sensor, \
                            SensorEvent, \
                            Track
import logging


logger = logging.getLogger('laptimer')


class RiderTestCase(TestCase):

    def test_add_rider_fails_when_rider_found(self):
        # Arrange
        rider = Rider.objects.create(name='bogus')
        # Act
        result = api.add_rider(rider.name)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_rider', result.call)
        error = 'Rider already exists' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_add_rider_fails_when_name_invalid(self):
        # Arrange & Act
        result = api.add_rider(rider_name=None)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_rider', result.call)
        self.assertEqual('IntegrityError', result.data)

    def test_add_rider_passes(self):
        # Arrange
        name = 'bogus rider'
        # Act
        result = api.add_rider(name)
        # Assert
        self.assertTrue(Rider.objects.filter(name=name).exists())
        self.assertTrue(result.ok)
        self.assertEqual('add_rider', result.call)
        rider = Rider.objects.get(name=name)
        self.assertEqual(rider, result.data)

    def test_change_rider_fails_when_rider_not_found(self):
        # Arrange & Act
        result = api.change_rider('bogus rider', 'none')
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('change_rider', result.call)
        error = 'Rider not found' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_change_rider_fails_when_new_rider_found(self):
        # Arrange
        rider = Rider.objects.create(name='bogus rider')
        # Act
        result = api.change_rider('none', rider.name)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('change_rider', result.call)
        error = 'Rider already exists' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_change_rider_passes(self):
        # Arrange
        first_name = 'bogus rider'
        changed_name = 'betty boo'
        Rider.objects.create(name=first_name)
        # Act
        result = api.change_rider(first_name, changed_name)
        # Assert
        self.assertTrue(Rider.objects.filter(name=changed_name).exists())
        self.assertTrue(result.ok)
        self.assertEqual('change_rider', result.call)
        rider = Rider.objects.get(name=changed_name)
        self.assertEqual(rider, result.data)

    def test_remove_rider_fails_when_rider_not_found(self):
        # Arrange & Act
        result = api.remove_rider('bogus rider')
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('remove_rider', result.call)
        error = 'Rider not found' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_remove_rider_passes(self):
        # Arrange
        name = 'bogus rider'
        rider = Rider.objects.create(name=name)
        # Act
        result = api.remove_rider(name)
        # Assert
        self.assertFalse(Rider.objects.filter(name=name).exists())
        self.assertTrue(result.ok)
        self.assertEqual('remove_rider', result.call)
        self.assertEqual(name, result.data)

    def test_get_rider_passes(self):
        # Arrange
        rider = Rider.objects.create(name='bogus')
        # Act
        result = api.get_rider(rider.name)
        # Assert
        self.assertTrue(result.ok)
        self.assertEqual('get_rider', result.call)
        self.assertEqual(rider, result.data)

    def test_get_rider_fails_when_rider_not_found(self):
        # Arrange
        rider = Rider.objects.create(name='bogus rider')
        # Act
        result = api.get_rider('nope')
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('get_rider', result.call)
        error = 'Rider not found' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_get_riders_passes(self):
        # Arrange
        rider1 = Rider.objects.create(name='bogus rider 1')
        rider2 = Rider.objects.create(name='bogus rider 2')
        # Act
        result = api.get_riders()
        # Assert
        self.assertTrue(result.ok)
        self.assertEqual('get_riders', result.call)
        self.assertEqual(2, result.data.count())
        self.assertEqual(rider1, result.data[0])
        self.assertEqual(rider2, result.data[1])


class TrackTestCase(TestCase):

    def test_add_track_fails_when_track_found(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        # Act
        result = api.add_track(track.name, track.distance, track.timeout,
            track.unit_of_measurement)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_track', result.call)
        error = 'Track already exists' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_add_track_fails_when_distance_invalid(self):
        # Arrange & Act
        result = api.add_track('bogus track', 'FUBAR', 100, settings.METRIC)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_track', result.call)
        self.assertEqual('ValueError', result.data)

    def test_add_track_fails_when_timeout_invalid(self):
        # Arrange & Act
        result = api.add_track('bogus track', 50, 'FUBAR', settings.METRIC)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_track', result.call)
        self.assertEqual('ValueError', result.data)

    def test_add_track_fails_when_unit_of_measurement_invalid(self):
        # Arrange & Act
        result = api.add_track('bogus track', 50, 100, 'FUBAR')
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_track', result.call)
        self.assertEqual('Invalid unit of measurement', result.data)

    def test_add_track_passes(self):
        # Arrange
        name = 'bogus track'
        # Act
        result = api.add_track(name, 50, 100, settings.METRIC)
        # Assert
        self.assertTrue(Track.objects.filter(name=name).exists())
        self.assertTrue(result.ok)
        self.assertEqual('add_track', result.call)
        track = Track.objects.get(name=name)
        self.assertEqual(track, result.data)

    def test_change_track_fails_when_track_not_found(self):
        # Arrange & Act
        result = api.change_track('bogus track')
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('change_track', result.call)
        error = 'Track not found' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_change_track_fails_when_new_track_found(self):
        # Arrange
        track = Track.objects.create(name='bogus track 1', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        track = Track.objects.create(name='bogus track 2', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        # Act
        result = api.change_track('bogus track 1', 'bogus track 2')
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('change_track', result.call)
        error = 'Track already exists' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_change_track_fails_when_no_new_data_entered(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        # Act
        result = api.change_track('bogus track')
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('change_track', result.call)
        error = 'At least one new track detail is required' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_change_track_fails_when_new_distance_is_invalid(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        # Act
        result = api.change_track(track_name='bogus track',
            new_track_distance='bogus')
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('change_track', result.call)
        self.assertEqual('ValueError', result.data)

    def test_change_track_fails_when_new_timeout_is_invalid(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        # Act
        result = api.change_track(track_name='bogus track',
            new_lap_timeout='bogus')
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('change_track', result.call)
        self.assertEqual('ValueError', result.data)

    def test_change_track_fails_when_new_unit_of_measurement_is_invalid(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        # Act
        result = api.change_track(track_name='bogus track',
            new_unit_of_measurement='bogus')
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('change_track', result.call)
        error = 'Invalid unit of measurement' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_change_track_passes(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        # Act
        result = api.change_track(track_name='bogus track',
            new_track_name='bogus track 2', new_track_distance=51,
            new_lap_timeout=101, new_unit_of_measurement=settings.IMPERIAL)
        # Assert
        self.assertTrue(result.ok)
        self.assertEqual('change_track', result.call)
        track = Track.objects.get(name='bogus track 2')
        self.assertEqual(track, result.data)
        self.assertEqual(51, track.distance)
        self.assertEqual(101, track.timeout)
        self.assertEqual(settings.IMPERIAL, track.unit_of_measurement)

    def test_remove_track_fails_when_track_not_found(self):
        # Arrange & Act
        result = api.remove_track('bogus track')
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('remove_track', result.call)
        error = 'Track not found' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_remove_track_passes(self):
        # Arrange
        name = 'bogus track'
        track = Track.objects.create(name=name, distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        # Act
        result = api.remove_track(name)
        # Assert
        self.assertFalse(Track.objects.filter(name=name).exists())
        self.assertTrue(result.ok)
        self.assertEqual('remove_track', result.call)
        self.assertEqual(name, result.data)

    def test_get_track_passes(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        # Act
        result = api.get_track(track.name)
        # Assert
        self.assertTrue(result.ok)
        self.assertEqual('get_track', result.call)
        self.assertEqual(track, result.data)

    def test_get_track_fails_when_rider_not_found(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        # Act
        result = api.get_track('nope')
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('get_track', result.call)
        error = 'Track not found' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_get_tracks_passes(self):
        # Arrange
        track1 = Track.objects.create(name='bogus track 1', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        track2 = Track.objects.create(name='bogus track 2', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        # Act
        result = api.get_tracks()
        # Assert
        self.assertTrue(result.ok)
        self.assertEqual('get_tracks', result.call)
        self.assertEqual(2, result.data.count())
        self.assertEqual(track1, result.data[0])
        self.assertEqual(track2, result.data[1])


class SessionTestCase(TestCase):

    def test_add_session_fails_when_session_found(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session = Session.objects.create(name='bogus session', track_id=track.id)
        # Act
        result = api.add_session(track.name, session.name)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_session', result.call)
        error = 'Session already exists' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_add_session_fails_when_name_invalid(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        # Act
        result = api.add_session(track_name=track.name, session_name=None)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_session', result.call)
        self.assertEqual('IntegrityError', result.data)

    def test_add_session_fails_when_track_not_found(self):
        # Arrange & Act
        result = api.add_session('bogus track', 'bogus session')
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_session', result.call)
        error = 'Track not found' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_add_session_passes(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        name = 'bogus session'
        # Act
        result = api.add_session(track.name, name)
        # Assert
        self.assertTrue(Session.objects.filter(name=name).exists())
        self.assertTrue(result.ok)
        self.assertEqual('add_session', result.call)
        session = Session.objects.get(name=name)
        self.assertEqual(session, result.data)

    def test_change_session_fails_when_session_not_found(self):
        # Arrange & Act
        result = api.change_session('bogus session')
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('change_session', result.call)
        error = 'Session not found' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_change_session_fails_when_new_session_found(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session = Session.objects.create(name='bogus session', track_id=track.id)
        session2 = Session.objects.create(name='bogus session 2', track_id=track.id)
        # Act
        result = api.change_session(session.name, session2.name, track.name)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('change_session', result.call)
        error = 'Session already exists' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_change_session_fails_when_new_track_not_found(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session = Session.objects.create(name='bogus session', track_id=track.id)
        # Act
        result = api.change_session(session.name, 'bogus session 2', 'bogus track 2')
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('change_session', result.call)
        error = 'Track not found' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_change_session_fails_when_new_session_and_track_both_none(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session = Session.objects.create(name='bogus session', track_id=track.id)
        # Act
        result = api.change_session(session.name)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('change_session', result.call)
        error = 'New session or track name is required' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_change_session_passes(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        track2 = Track.objects.create(name='bogus track 2', distance=51,
            timeout=101, unit_of_measurement=settings.IMPERIAL)
        session = Session.objects.create(name='bogus session', track_id=track.id)
        # Act
        result = api.change_session(session.name, 'bogus session 2', track2.name)
        # Assert
        self.assertTrue(result.ok)
        self.assertEqual('change_session', result.call)
        session = Session.objects.get(name='bogus session 2')
        self.assertEqual(session, result.data)

    def test_remove_session_fails_when_session_not_found(self):
        # Arrange & Act
        result = api.remove_session('bogus session')
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('remove_session', result.call)
        error = 'Session not found' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_remove_session_passes(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        name = 'bogus session'
        session = Session.objects.create(name=name, track=track)
        # Act
        result = api.remove_session(name)
        # Assert
        self.assertFalse(Session.objects.filter(name=name).exists())
        self.assertTrue(result.ok)
        self.assertEqual('remove_session', result.call)
        self.assertEqual(name, result.data)

    def test_get_session_passes(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        name = 'bogus session'
        session = Session.objects.create(name=name, track=track)
        # Act
        result = api.get_session(name)
        # Assert
        self.assertTrue(result.ok)
        self.assertEqual('get_session', result.call)
        self.assertEqual(session, result.data)

    def test_get_session_fails_when_session_not_found(self):
        # Arrange
        # Act
        result = api.get_session('nope')
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('get_session', result.call)
        error = 'Session not found' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_get_sessions_for_track_passes(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session1 = Session.objects.create(name='bogus session 1', track=track)
        session2 = Session.objects.create(name='bogus session 2', track=track)
        # Act
        result = api.get_sessions_for_track(track.name)
        # Assert
        self.assertTrue(result.ok)
        self.assertEqual('get_sessions_for_track', result.call)
        self.assertEqual(2, result.data.count())
        self.assertEqual(session1, result.data[0])
        self.assertEqual(session2, result.data[1])

    def test_get_sessions_for_track_fails_when_track_not_found(self):
        # Arrange
        # Act
        result = api.get_sessions_for_track('nope')
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('get_sessions_for_track', result.call)
        error = 'Track not found' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_get_sessions_passes(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session1 = Session.objects.create(name='bogus session 1', track=track)
        session2 = Session.objects.create(name='bogus session 2', track=track)
        # Act
        result = api.get_sessions()
        # Assert
        self.assertTrue(result.ok)
        self.assertEqual('get_sessions', result.call)
        self.assertEqual(2, result.data.count())
        self.assertEqual(session1, result.data[0])
        self.assertEqual(session2, result.data[1])


class LapTestCase(TestCase):

    def test_add_lap_time_fails_when_session_not_found(self):
        # Arrange
        session_name = 'bogus session'
        rider_name = 'bogus rider'
        sensor_name = 'bogus sensor'
        time = None
        # Act
        result = api.add_lap_time(session_name, rider_name, sensor_name, time)
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
        result = api.add_lap_time(session_name, rider_name, sensor_name, time)
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
        result = api.add_lap_time(session_name, rider_name, sensor_name, time)
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
        result = api.add_lap_time(session_name, rider_name, sensor_name, time)
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
        result = api.add_lap_time(session_name, rider_name, sensor_name, time)
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
        result = api.add_lap_time(session_name, rider_name, sensor_name, time)
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
        result = api.add_lap_time(session_name, rider_name, sensor_name, time)
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
        sensor_start = Sensor.objects.create(name=sensor_start_name, track_id=track.id,
            sensor_type=settings.SENSOR_START)
        sensor_finish = Sensor.objects.create(name=sensor_finish_name, track_id=track.id,
            sensor_type=settings.SENSOR_FINISH)
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
        result = api.add_lap_time(session_name, rider_name,
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
        sensor_start = Sensor.objects.create(name=sensor_start_name, track_id=track.id,
            sensor_type=settings.SENSOR_START)
        sensor_finish = Sensor.objects.create(name=sensor_finish_name, track_id=track.id,
            sensor_type=settings.SENSOR_FINISH)
        time_finish = timezone.now()
        # Act
        result = api.add_lap_time(session_name, rider_name,
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
        sensor_start = Sensor.objects.create(name=sensor_start_name, track_id=track.id,
            sensor_type=settings.SENSOR_START)
        sensor_finish = Sensor.objects.create(name=sensor_finish_name, track_id=track.id,
            sensor_type=settings.SENSOR_FINISH)
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
        result = api.add_lap_time(session_name, rider_name,
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
        result = api.add_lap_time(session_name, rider_name, sensor_name, time)
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
        lapTime_start = SensorEvent.objects.create(lap=lap_start, sensor=sensor,
            time=time_start)
        lapTime_start.save()
        lap_start.start = lapTime_start
        lap_start.save()
        time_finish = timezone.now()
        # Act
        result = api.add_lap_time(session_name, rider_name,
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
        result = api.add_lap_time(session_name, rider_name, sensor_name, time)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_lap_time', result.call)
        error = 'Sector based sensors not currently supported'
        self.assertEqual(error, result.data)
