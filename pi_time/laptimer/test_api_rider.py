from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from laptimer import api_rider
from laptimer.models import Rider
import logging


logger = logging.getLogger('laptimer')

class ApiRiderTestCase(TestCase):
    '''Unit tests for rider related API functions.'''

    def test_add_rider_fails_when_rider_found(self):
        # Arrange
        rider = Rider.objects.create(name='bogus')
        # Act
        result = api_rider.add_rider(rider.name)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_rider', result.call)
        error = 'Rider already exists' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_add_rider_fails_when_name_invalid(self):
        # Arrange & Act
        result = api_rider.add_rider(rider_name=None)
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('add_rider', result.call)
        self.assertEqual('IntegrityError', result.data)

    def test_add_rider_passes(self):
        # Arrange
        name = 'bogus rider'
        # Act
        result = api_rider.add_rider(name)
        # Assert
        self.assertTrue(Rider.objects.filter(name=name).exists())
        self.assertTrue(result.ok)
        self.assertEqual('add_rider', result.call)
        rider = Rider.objects.get(name=name)
        self.assertEqual(rider, result.data)

    def test_change_rider_fails_when_rider_not_found(self):
        # Arrange & Act
        result = api_rider.change_rider('bogus rider', 'none')
        # Assert
        self.assertFalse(result.ok)
        self.assertEqual('change_rider', result.call)
        error = 'Rider not found' # TODO: i18n
        self.assertEqual(error, result.data)

    def test_change_rider_fails_when_new_rider_found(self):
        # Arrange
        rider = Rider.objects.create(name='bogus rider')
        # Act
        result = api_rider.change_rider('none', rider.name)
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
        result = api_rider.change_rider(first_name, changed_name)
        # Assert
        self.assertTrue(Rider.objects.filter(name=changed_name).exists())
        self.assertTrue(result.ok)
        self.assertEqual('change_rider', result.call)
        rider = Rider.objects.get(name=changed_name)
        self.assertEqual(rider, result.data)

    def test_remove_rider_fails_when_rider_not_found(self):
        # Arrange & Act
        result = api_rider.remove_rider('bogus rider')
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
        result = api_rider.remove_rider(name)
        # Assert
        self.assertFalse(Rider.objects.filter(name=name).exists())
        self.assertTrue(result.ok)
        self.assertEqual('remove_rider', result.call)
        self.assertEqual(name, result.data)

    def test_get_rider_passes(self):
        # Arrange
        rider = Rider.objects.create(name='bogus')
        # Act
        result = api_rider.get_rider(rider.name)
        # Assert
        self.assertTrue(result.ok)
        self.assertEqual('get_rider', result.call)
        self.assertEqual(rider, result.data)

    def test_get_rider_fails_when_rider_not_found(self):
        # Arrange
        rider = Rider.objects.create(name='bogus rider')
        # Act
        result = api_rider.get_rider('nope')
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
        result = api_rider.get_riders()
        # Assert
        self.assertTrue(result.ok)
        self.assertEqual('get_riders', result.call)
        self.assertEqual(2, result.data.count())
        self.assertEqual(rider1, result.data[0])
        self.assertEqual(rider2, result.data[1])
