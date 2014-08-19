from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from laptimer import api_session
from laptimer.models import Lap, \
                            Rider, \
                            Session, \
                            Sensor, \
                            SensorEvent, \
                            Track
import logging


logger = logging.getLogger('laptimer')

class ApiSessionTestCase(TestCase):
    '''Unit tests for session related API functions.'''

    def test_add_session_fails_when_session_found(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session = Session.objects.create(name='bogus session', 
            track_id=track.id)
        # Act
        result = api_session.add_session(track.name, session.name)
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
        result = api_session.add_session(track_name=track.name, 
            session_name=None)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_session', result.call)
        self.assertEqual('IntegrityError', result.data)

    def test_add_session_fails_when_track_not_found(self):
        # Arrange & Act
        result = api_session.add_session('bogus track', 'bogus session')
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
        result = api_session.add_session(track.name, name)
        # Assert
        self.assertTrue(Session.objects.filter(name=name).exists())
        self.assertTrue(result.ok)
        self.assertEqual('add_session', result.call)
        session = Session.objects.get(name=name)
        self.assertEqual(session, result.data)

    def test_change_session_fails_when_session_not_found(self):
        # Arrange & Act
        result = api_session.change_session('bogus session')
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('change_session', result.call)
        error = 'Session not found' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_change_session_fails_when_new_session_found(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session = Session.objects.create(name='bogus session', 
            track_id=track.id)
        session2 = Session.objects.create(name='bogus session 2', 
            track_id=track.id)
        # Act
        result = api_session.change_session(session.name, session2.name, 
            track.name)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('change_session', result.call)
        error = 'Session already exists' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_change_session_fails_when_new_track_not_found(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session = Session.objects.create(name='bogus session', 
            track_id=track.id)
        # Act
        result = api_session.change_session(session.name, 'bogus session 2', 
            'bogus track 2')
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('change_session', result.call)
        error = 'Track not found' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_change_session_fails_when_new_session_and_track_both_none(self):
        # Arrange
        track = Track.objects.create(name='bogus track', distance=50,
            timeout=100, unit_of_measurement=settings.METRIC)
        session = Session.objects.create(name='bogus session', 
            track_id=track.id)
        # Act
        result = api_session.change_session(session.name)
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
        session = Session.objects.create(name='bogus session', 
            track_id=track.id)
        # Act
        result = api_session.change_session(session.name, 'bogus session 2', 
            track2.name)
        # Assert
        self.assertTrue(result.ok)
        self.assertEqual('change_session', result.call)
        session = Session.objects.get(name='bogus session 2')
        self.assertEqual(session, result.data)

    def test_remove_session_fails_when_session_not_found(self):
        # Arrange & Act
        result = api_session.remove_session('bogus session')
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
        result = api_session.remove_session(name)
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
        result = api_session.get_session(name)
        # Assert
        self.assertTrue(result.ok)
        self.assertEqual('get_session', result.call)
        self.assertEqual(session, result.data)

    def test_get_session_fails_when_session_not_found(self):
        # Arrange
        # Act
        result = api_session.get_session('nope')
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
        result = api_session.get_sessions_for_track(track.name)
        # Assert
        self.assertTrue(result.ok)
        self.assertEqual('get_sessions_for_track', result.call)
        self.assertEqual(2, result.data.count())
        self.assertEqual(session1, result.data[0])
        self.assertEqual(session2, result.data[1])

    def test_get_sessions_for_track_fails_when_track_not_found(self):
        # Arrange
        # Act
        result = api_session.get_sessions_for_track('nope')
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
        result = api_session.get_sessions()
        # Assert
        self.assertTrue(result.ok)
        self.assertEqual('get_sessions', result.call)
        self.assertEqual(2, result.data.count())
        self.assertEqual(session1, result.data[0])
        self.assertEqual(session2, result.data[1])
