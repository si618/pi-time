from django.test import TestCase
from django.utils import timezone
from laptimer import utils
import datetime


class UtilsTestCase(TestCase):

    def test_time_to_string_returns_none_when_start_is_none(self):
        # Arrange
        start = None
        finish = timezone.now()
        # Act
        result = utils.time_to_string(start, finish)
        # Assert
        self.assertEqual(None, result)

    def test_time_to_string_returns_none_when_finish_is_none(self):
        # Arrange
        start = timezone.now()
        finish = None
        # Act
        result = utils.time_to_string(start, finish)
        # Assert
        self.assertEqual(None, result)

    def test_time_to_string_raises_error_when_start_and_finish_are_equal(self):
        # Arrange
        start = timezone.now()
        finish = start
        # Act
        with self.assertRaises(ValueError) as cm:
            utils.time_to_string(start, finish)
        # Assert
        error = 'Start time must be before finish time!'
        self.assertEqual(error, cm.exception.args[0])

    def test_time_to_string_raises_error_when_finish_less_than_start(self):
        # Arrange
        start = timezone.now()
        finish = timezone.now() + datetime.timedelta(seconds=-1)
        # Act
        with self.assertRaises(ValueError) as cm:
            utils.time_to_string(start, finish)
        # Assert
        error = 'Start time must be before finish time!'
        self.assertEqual(error, cm.exception.args[0])
