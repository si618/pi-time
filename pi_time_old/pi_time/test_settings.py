from django.conf import settings
from django.test import TestCase
import django_settings


class DjangoSettingsTestCase(TestCase):

    def test_unit_of_measurement_defaults_to_metric(self):
        self.assertTrue(django_settings.exists('unit_of_measurement'))
        self.assertEqual(settings.METRIC,
            django_settings.get('unit_of_measurement'))

    def test_gpio_app_defaults_to_11(self):
        self.assertTrue(django_settings.exists('gpio_app'))
        self.assertEqual(15, django_settings.get('gpio_app'))

    def test_gpio_lap_defaults_to_13(self):
        self.assertTrue(django_settings.exists('gpio_lap'))
        self.assertEqual(16, django_settings.get('gpio_lap'))

    def test_gpio_sensor_defaults_to_18(self):
        self.assertTrue(django_settings.exists('gpio_sensor'))
        self.assertEqual(18, django_settings.get('gpio_sensor'))
