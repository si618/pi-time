import json
import os
import unittest

from pi_time import settings
from pi_time.config import update


class UpdateTestCase(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        config = \
        '{' \
        '   "laptimer": {' \
        '       "url": "ws://127.0.0.1:8080/ws",' \
        '       "hardware": "RPI_REV2"' \
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
        config_file = os.path.join(os.getcwd(), 'test_update.json')
        cls.config = json.loads(config)
        cls.config_file = config_file
        if os.path.isfile(config_file):
            os.remove(config_file)
        with open(config_file, 'w') as cfg:
            cfg.write(config)

    @classmethod
    def tearDownClass(cls):        
        if os.path.isfile(cls.config_file):
            os.remove(cls.config_file)

    def test_update_laptimer_raises_exception_when_config_is_invalid(self):
        # Arrange
        config = json.loads('{"laptimer": {"bogus": "bogus"}}')
        laptimer = self.config['laptimer']
        # Act
        with self.assertRaises(Exception) as context:
            update.update_laptimer(self.config_file, config, laptimer)
        # Assert
        expected = "Encountered unknown attribute 'bogus' in laptimer " \
            "configuration"
        self.assertEqual(context.exception.message, expected)


    def test_update_laptimer_raises_exception_when_laptimer_is_invalid(self):
        # Arrange
        laptimer = json.loads('{"bogus": "bogus"}')
        # Act
        with self.assertRaises(Exception) as context:
            update.update_laptimer(self.config_file, self.config, laptimer)
        # Assert
        expected = "Encountered unknown attribute 'bogus' in laptimer " \
            "configuration"
        self.assertEqual(context.exception.message, expected)

    def test_update_sensor_raises_exception_when_sensor_is_invalid(self):
        # Arrange
        sensor = json.loads('{"bogus": "bogus"}')
        # Act
        with self.assertRaises(Exception) as context:
            update.update_sensor(self.config_file, self.config, sensor)
        # Assert
        expected = 'Missing sensor name'
        self.assertEqual(context.exception.message, expected)

    def test_update_laptimer_merges_existing_configuration(self):
        # Arrange
        laptimer = json.loads('{"name": "bogus"}')
        # Act
        config = update.update_laptimer(self.config_file, self.config,
            laptimer)
        # Assert
        self.assertEqual(config['laptimer']['name'], 'bogus')

    def test_update_sensor_merges_existing_section(self):
        # Arrange
        sensor = json.loads('{"name": "Start & finish", "hardware": ' \
            '"RPI_REV1"}')
        # Act
        config = update.update_sensor(self.config_file, self.config, sensor)
        # Assert
        self.assertEqual(config['sensors'][0]['hardware'], 'RPI_REV1')

    def test_add_sensor_fails_when_sensor_name_already_exists(self):
        # Arrange
        sensor = json.loads('{"name": "Start & finish"}')
        # Act
        with self.assertRaises(Exception) as context:
            config = update.add_sensor(self.config_file, self.config, sensor)
        # Assert
        self.assertEqual(context.exception.message,
            "Sensor 'Start & finish' already found in configuration")

    def test_add_sensor_adds_new_sensor_section(self):
        # Arrange
        config_json = \
            '{' \
            '   "laptimer": {' \
            '       "url": "ws://127.0.0.1:8080/ws",' \
            '       "hardware": "RPI_REV2"' \
            '   },' \
            '   "sensors": []' \
            '}'
        config_file = os.path.join(os.getcwd(), 'test_update_add_sensor.json')
        if os.path.isfile(config_file):
            os.remove(config_file)
        with open(config_file, 'w') as cfg:
            cfg.write(config_json)
        config = json.loads(config_json)
        sensor = json.loads( \
            '{' \
            '    "name": "Bogus",' \
            '    "url": "ws://127.0.0.1:88/ws",' \
            '    "hardware": "RPI_REV1",' \
            '    "location": "START_FINISH",' \
            '    "pinLedApp": 13' \
            '}')
        # Act
        config = update.add_sensor(config_file, config, sensor)
        # Assert
        self.assertEqual(config['sensors'][0], sensor)
        # Cleanup
        if os.path.isfile(config_file):
            os.remove(config_file)

    def test_rename_sensor_fails_when_sensor_name_doesnt_exist(self):
        # Arrange
        sensor_name = 'Bogus'
        new_sensor_name = 'Bogus 2'
        # Act
        with self.assertRaises(Exception) as context:
            config = update.rename_sensor(self.config_file, self.config, 
                sensor_name, new_sensor_name)
        # Assert
        self.assertEqual(context.exception.message,
            "Can't rename as existing sensor 'Bogus' not found in configuration")

    def test_rename_sensor_fails_when_new_sensor_name_already_exists(self):
        # Arrange
        sensor_name = 'Bogus'
        new_sensor_name = 'Bogus2'
        config_json = \
        '{' \
        '   "laptimer": {' \
        '       "url": "ws://127.0.0.1:8080/ws",' \
        '       "hardware": "RPI_REV1"' \
        '   },' \
        '   "sensors": [{' \
        '       "name": "Bogus",' \
        '       "url": "ws://127.0.0.1:8888/ws",' \
        '       "hardware": "RPI_REV2",' \
        '       "location": "START",' \
        '       "pinLedApp": 13' \
        '    },{' \
        '       "name": "Bogus2",' \
        '       "url": "ws://127.0.0.1:8889/ws",' \
        '       "hardware": "RPI_REV2",' \
        '       "location": "FINISH",' \
        '       "pinLedApp": 13' \
        '    }]' \
        '}'
        config_file = os.path.join(os.getcwd(), 'test_update_rename_sensor.json')
        if os.path.isfile(config_file):
            os.remove(config_file)
        with open(config_file, 'w') as cfg:
            cfg.write(config_json)
        config = json.loads(config_json)
        # Act
        with self.assertRaises(Exception) as context:
            config = update.rename_sensor(config_file, config, sensor_name, 
                new_sensor_name)
        # Assert
        self.assertEqual(context.exception.message, 
            "Can't rename sensor '%s' as '%s' already found in " \
                "configuration" % (sensor_name, new_sensor_name))
        # Cleanup
        if os.path.isfile(config_file):
            os.remove(config_file)

    def test_rename_sensor_passes_when_new_sensor_name_matches_sensor_name(self):
        # Arrange
        sensor_name = 'Start & finish'
        new_sensor_name = 'Start & finish'
        # Act
        config = update.rename_sensor(self.config_file, self.config, 
            sensor_name, new_sensor_name)
        # Assert
        self.assertEqual(self.config, config)

    def test_rename_sensor_passes(self):
        # Arrange
        sensor_name = 'Start & finish'
        new_sensor_name = 'Bogus'
        # Act
        config = update.rename_sensor(self.config_file, self.config, 
            sensor_name, new_sensor_name)
        # Assert
        self.assertEqual(self.config, config)
        # Cleanup
        update.rename_sensor(self.config_file, self.config, 
            new_sensor_name, sensor_name)
