from django.test import TestCase
from laptimer import api
import logging


logger = logging.getLogger('laptimer')

class ApiTestCase(TestCase):
	'''Unit tests for general API functions.'''

	def test_get_all_data_returns_expected_result(self):
		# Arrange
		# TODO: Setup test data for each object model
		# Act
		result = api.get_all_data()
		# Assert
		self.assertTrue(result.ok)
		self.assertEqual('get_all_data', result.call)
		# TODO: Verify test data matches returned data
