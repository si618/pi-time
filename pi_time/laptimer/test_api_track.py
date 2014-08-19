from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from laptimer import api_track
from laptimer.models import Lap, \
                            Rider, \
                            Session, \
                            Sensor, \
                            SensorEvent, \
                            Track
import logging


logger = logging.getLogger('laptimer')

class ApiTrackTestCase(TestCase):
    '''Unit tests for track related API functions.'''

    def test_add_track_fails_when_track_found(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        # Act
        result = api_track.add_track(track.name, track.distance, track.timeout,
            track.unit_of_measurement)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_track', result.call)
        error = 'Track already exists' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_add_track_fails_when_distance_invalid(self):
        # Arrange & Act
        result = api_track.add_track('bogus track', 'FUBAR', 100, settings.METRIC)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_track', result.call)
        self.assertEqual('ValueError', result.data)

    def test_add_track_fails_when_timeout_invalid(self):
        # Arrange & Act
        result = api_track.add_track('bogus track', 50, 'FUBAR', settings.METRIC)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_track', result.call)
        self.assertEqual('ValueError', result.data)

    def test_add_track_fails_when_unit_of_measurement_invalid(self):
        # Arrange & Act
        result = api_track.add_track('bogus track', 50, 100, 'FUBAR')
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_track', result.call)
        self.assertEqual('Invalid unit of measurement', result.data)

    def test_add_track_passes(self):
        # Arrange
        name = 'bogus track'
        # Act
        result = api_track.add_track(name, 50, 100, settings.METRIC)
        # Assert
        self.assertTrue(Track.objects.filter(name=name).exists())
        self.assertTrue(result.ok)
        self.assertEqual('add_track', result.call)
        track = Track.objects.get(name=name)
        self.assertEqual(track, result.data)

    def test_change_track_fails_when_track_not_found(self):
        # Arrange & Act
        result = api_track.change_track('bogus track')
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
        result = api_track.change_track('bogus track 1', 'bogus track 2')
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
        result = api_track.change_track('bogus track')
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
        result = api_track.change_track(track_name='bogus track',
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
        result = api_track.change_track(track_name='bogus track',
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
        result = api_track.change_track(track_name='bogus track',
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
        result = api_track.change_track(track_name='bogus track',
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
        result = api_track.remove_track('bogus track')
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
        result = api_track.remove_track(name)
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
        result = api_track.get_track(track.name)
        # Assert
        self.assertTrue(result.ok)
        self.assertEqual('get_track', result.call)
        self.assertEqual(track, result.data)

    def test_get_track_fails_when_rider_not_found(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        # Act
        result = api_track.get_track('nope')
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
        result = api_track.get_tracks()
        # Assert
        self.assertTrue(result.ok)
        self.assertEqual('get_tracks', result.call)
        self.assertEqual(2, result.data.count())
        self.assertEqual(track1, result.data[0])
        self.assertEqual(track2, result.data[1])
