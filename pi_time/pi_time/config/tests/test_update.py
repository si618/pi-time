import json
import os
import unittest

from pi_time import settings
from pi_time.config import update


class UpdateTestCase(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        file_name = os.path.join(os.getcwd(), 'test_update.json')
        config_json = \
        '{' \
        '   "laptimer": {' \
        '       "url": "ws://127.0.0.1:8080/ws"' \
        '       "hardware": "RPI_REV2",' \
        '   },' \
        '   "sensors": [{' \
        '       "name": "Start & finish",' \
        '       "url": "ws://127.0.0.1:8888/ws",' \
        '       "hardware": "RPI_REV2",' \
        '       "location": "START_FINISH",' \
        '       "pinLedApp": 13,' \
        '       "pinLedHeartbeat": 15,' \
        '       "pinLedLap": 16,' \
        '       "pinLedEvent": 18,' \
        '       "pinEvent": 22' \
        '    }]' \
        '}'
        file_name = os.path.join(os.getcwd(), file_name)
        if os.path.isfile(file_name):
            os.remove(file_name)
        with open(file_name, 'w') as config_file:
            config_file.write(config_json)
        cls.test_config_file = file_name

    @classmethod
    def tearDownClass(cls):
        file_name = cls.test_config_file
        if os.path.isfile(file_name):
            os.remove(file_name)

    def test_update_laptimer_raises_exception_when_config_file_is_invalid_json(self):
        # Arrange
        file_name = os.path.join(os.getcwd(), 'test_update_invalid.json')
        config = 'bogus'
        laptimer = config
        with open(file_name, 'w') as config_file:
            config_file.write('config')
        # Act
        with self.assertRaises(Exception) as context:
            update.update_laptimer(file_name, config, laptimer)
        # Assert
        expected = 'Unable to find laptimer in config'
        self.assertEqual(context.exception.message, expected)
        # Cleanup
        if os.path.isfile(file_name):
            os.remove(file_name)

    def test_update_sensor_raises_exception_when_config_file_is_invalid_json(self):
        # Arrange
        # Act
        # Assert
        self.fail('TODO:')

    def test_update_laptimer_raises_exception_when_config_is_invalid(self):
        # Arrange
        # Act
        # Assert
        self.fail('TODO:')

    def test_update_sensor_raises_exception_when_config_is_invalid(self):
        # Arrange
        # Act
        # Assert
        self.fail('TODO:')

    def test_update_laptimer_raises_exception_when_laptimer_is_invalid(self):
        # Arrange
        # Act
        # Assert
        self.fail('TODO:')

    def test_update_sensor_raises_exception_when_laptimer_is_invalid(self):
        # Arrange
        # Act
        # Assert
        self.fail('TODO:')

    def test_update_laptimer_merges_existing_configuration(self):
        # Arrange
        # Act
        # Assert
        self.fail('TODO:')

    def test_update_sensor_merges_existing_section(self):
        # Arrange
        # Act
        # Assert
        self.fail('TODO:')

    def test_update_sensor_adds_new_sensor_section(self):
        # Arrange
        # Act
        # Assert
        self.fail('TODO:')
