import django_settings
from django.test import TestCase
from django.conf import settings

class DjangoSettingsTestCase(TestCase):
	
	def test_unit_of_measurement_defaults_to_metric(self):
		self.assertEqual(settings.METRIC, django_settings.get('unit_of_measurement'))
