import json
import os
import unittest

from pi_time import config, settings


class ConfigTestCase(unittest.TestCase):

    def test_check_name_raises_exception_when_name_is_not_str(self):
        # Arrange
        laptimer = json.loads('{"name": 123}')
        # Act
        with self.assertRaises(Exception) as context:
            config.check_name(laptimer, 'laptimer')
        # Assert
        self.assertEqual(context.exception.message,
            "'name' in laptimer configuration must be str (<type 'int'> " \
            "encountered)")

    def test_check_name_passes_when_name_is_str(self):
        # Arrange
        laptimer = json.loads('{"name": "bogus"}')
        # Act & Assert
        config.check_name(laptimer, 'laptimer')

    def test_check_url_raises_exception_when_url_is_not_missing(self):
        # Arrange
        laptimer = json.loads('{"urlbogus": "bogus"}')
        # Act
        with self.assertRaises(Exception) as context:
            config.check_url(laptimer, 'laptimer')
        # Assert
        self.assertEqual(context.exception.message,
            "'url' required in laptimer configuration")

    def test_check_url_raises_exception_when_url_is_not_str(self):
        # Arrange
        laptimer = json.loads('{"url": 123}')
        # Act
        with self.assertRaises(Exception) as context:
            config.check_url(laptimer, 'laptimer')
        # Assert
        self.assertEqual(context.exception.message,
            "'url' in laptimer configuration must be str (<type 'int'> " \
            "encountered)")

    def test_check_url_raises_exception_when_url_is_invalid(self):
        # Arrange
        laptimer = json.loads('{"url": "bogus"}')
        # Act
        with self.assertRaises(Exception) as context:
            config.check_url(laptimer, 'laptimer')
        # Assert
        self.assertEqual(context.exception.message,
            "Invalid 'url' in laptimer configuration : invalid WebSocket " \
            "URL: missing hostname")

    def test_check_url_passes_when_url_is_valid(self):
        # Arrange
        laptimer = json.loads('{"url": "ws://127.0.0.1:8080/ws"}')
        # Act & Assert
        config.check_url(laptimer, 'laptimer')

    def test_check_unit_of_measurement_raises_exception_when_unit_is_invalid(self):
        # Arrange
        laptimer = json.loads('{"unitOfMeasurement": "bogus"}')
        # Act
        with self.assertRaises(Exception) as context:
            config.check_unit_of_measurement(laptimer)
        # Assert
        self.assertEqual(context.exception.message,
            "'unitOfMeasurement' in laptimer configuration must be " \
            "('METRIC', 'IMPERIAL') (bogus encountered)")

    def test_check_unit_of_measurement_passes_when_unit_is_valid(self):
        # Arrange
        laptimer = json.loads('{"unitOfMeasurement": "%s"}' %
            (settings.METRIC))
        # Act & Assert
        config.check_unit_of_measurement(laptimer)

    def test_check_timezone_raises_exception_when_timezone_is_invalid(self):
        # Arrange
        laptimer = json.loads('{"timezone": "bogus"}')
        # Act
        with self.assertRaises(Exception) as context:
            config.check_timezone(laptimer)
        # Assert
        self.assertEqual(context.exception.message,
            "'timezone' in laptimer configuration must be valid entry in " \
            "pytz.common_timezones (bogus encountered)")

    def test_check_timezone_passes_when_timezone_is_valid(self):
        # Arrange
        laptimer = json.loads('{"timezone": "Australia/Adelaide"}')
        # Act & Assert
        config.check_timezone(laptimer)

    def test_check_sensor_location_raises_exception_when_location_is_invalid(self):
        # Arrange
        sensor = json.loads('{"location": "bogus"}')
        # Act
        with self.assertRaises(Exception) as context:
            config.check_sensor_location(sensor)
        # Assert
        self.assertEqual(context.exception.message,
            "'location' in sensor configuration must be ('START', 'FINISH', " \
            "'START_FINISH', 'SECTOR') (bogus encountered)")

    def test_check_sensor_location_passes_when_location_is_valid(self):
        # Arrange
        sensor = json.loads('{"location": "%s"}' %
            (settings.SENSOR_LOCATION_START))
        # Act & Assert
        config.check_sensor_location(sensor)

    def test_check_sensor_position_raises_exception_when_position_is_not_integer(self):
        # Arrange
        sensor = json.loads('{"position": "bogus"}')
        # Act
        with self.assertRaises(Exception) as context:
            config.check_sensor_position(sensor)
        # Assert
        self.assertEqual(context.exception.message,
            "'position' in sensor configuration must be integer (<type " \
            "'unicode'> encountered)")

    def test_check_sensor_position_raises_exception_when_position_is_zero(self):
        # Arrange
        sensor = json.loads('{"position": 0}')
        # Act
        with self.assertRaises(Exception) as context:
            config.check_sensor_position(sensor)
        # Assert
        self.assertEqual(context.exception.message,
            "'position' in sensor configuration must be greater than zero")

    def test_check_sensor_position_passes_when_position_is_valid(self):
        # Arrange
        sensor = json.loads('{"position": 1}')
        # Act & Assert
        config.check_sensor_position(sensor)

    def test_check_sensor_hardware_raises_exception_when_hardware_is_invalid(self):
        # Arrange
        sensor = json.loads('{"hardware": "bogus"}')
        # Act
        with self.assertRaises(Exception) as context:
            config.check_sensor_hardware(sensor)
        # Assert
        self.assertEqual(context.exception.message,
            "'hardware' in sensor configuration must be ('TEST', 'RPI_REV1', " \
            "'RPI_REV2', 'RPI_B+') (bogus encountered)")

    def test_check_sensor_hardware_passes_when_hardware_is_valid(self):
        # Arrange
        sensor = json.loads('{"hardware": "%s"}' %
            (settings.SENSOR_HW_RPI_BPLUS))
        # Act & Assert
        config.check_sensor_hardware(sensor)

    def test_check_sensor_pin_raises_exception_when_pin_is_invalid_type(self):
        # Arrange
        pin = settings.SENSOR_PIN_LED_HEARTBEAT[0]
        sensor = json.loads('{"%s": "bogus"}' % (pin))
        # Act
        with self.assertRaises(Exception) as context:
            config.check_sensor_pin(sensor, pin)
        # Assert
        self.assertEqual(context.exception.message,
            "'bogus' in sensor configuration must be integer (<type " \
            "'unicode'> encountered)")

    def test_check_sensor_pin_raises_exception_when_hardware_is_missing(self):
        # Arrange
        pin = settings.SENSOR_PIN_LED_HEARTBEAT[0]
        sensor = json.loads('{"%s": 22}' % (pin))
        # Act
        with self.assertRaises(Exception) as context:
            config.check_sensor_pin(sensor, pin)
        # Assert
        self.assertEqual(context.exception.message,
            "'hardware' in sensor configuration must be specified if setting " \
            "pin")

    def test_check_sensor_pin_raises_exception_when_pin_is_invalid(self):
        # Arrange
        hardware = settings.SENSOR_HW_RPI_REV1
        pin = settings.SENSOR_PIN_LED_HEARTBEAT[0]
        sensor = json.loads('{"hardware": "%s", "%s": 40}' % (hardware, pin))
        # Act
        with self.assertRaises(Exception) as context:
            config.check_sensor_pin(sensor, pin)
        # Assert
        self.assertEqual(context.exception.message,
            "'pinLedHeartbeat' in sensor configuration invalid for RPI_REV1 " \
            "hardware, must be (3, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, " \
            "21, 22, 23, 24, 26) (40 encountered)")

    def test_check_sensor_pin_passes_with_test_hardware(self):
        # Arrange
        hardware = settings.SENSOR_HW_TEST
        pin = settings.SENSOR_PIN_LED_HEARTBEAT[0]
        sensor = json.loads('{"hardware": "%s","%s": 40}' % (hardware, pin))
        # Act & Assert
        config.check_sensor_pin(sensor, pin)

    def test_check_sensor_pin_passes_when_hardware_and_pin_are_valid(self):
        # Arrange
        hardware = settings.SENSOR_HW_RPI_BPLUS
        pin = settings.SENSOR_PIN_LED_HEARTBEAT[0]
        sensor = json.loads('{"hardware": "%s","%s": 40}' % (hardware, pin))
        # Act & Assert
        config.check_sensor_pin(sensor, pin)

    def test_check_sensor_raises_exception_when_not_dictionary(self):
        # Arrange
        sensor = json.loads('{"bogus": "data"}')
        # Act
        with self.assertRaises(Exception) as context:
            config.check_sensor(sensor)
        # Assert
        self.assertEqual(context.exception.message,
            "Encountered unknown attribute 'bogus' in sensor configuration")

    def test_check_sensor_raises_exception_when_attribute_is_invalid(self):
        # Arrange
        sensors = json.loads('{"sensors": {"bogus": "data"}}')
        sensor = sensors['sensors']
        # Act
        with self.assertRaises(Exception) as context:
            config.check_sensor(sensor)
        # Assert
        self.assertEqual(context.exception.message,
            "Encountered unknown attribute 'bogus' in sensor configuration")

    def test_check_sensor_passes_when_attributes_are_valid(self):
        # Arrange
        sensors = json.loads('{"sensors": [{"url": "ws://127.0.0.1:80/ws"}]}')
        sensor = sensors['sensors'][0]
        # Act & Assert
        config.check_sensor(sensor)

    def test_check_laptimer_raises_exception_when_not_dictionary(self):
        # Arrange
        laptimer = json.loads('{"bogus": "data"}')
        # Act
        with self.assertRaises(Exception) as context:
            config.check_laptimer(laptimer)
        # Assert
        self.assertEqual(context.exception.message,
            "Encountered unknown attribute 'bogus' in laptimer configuration")

    def test_check_laptimer_raises_exception_when_attribute_is_invalid(self):
        # Arrange
        laptimerItem = json.loads('{"laptimer": [{"bogus": "data"}]}')
        laptimer = laptimerItem['laptimer']
        # Act
        with self.assertRaises(Exception) as context:
            config.check_laptimer(laptimer)
        # Assert
        self.assertEqual(context.exception.message,
            "Encountered unknown attribute '{u'bogus': u'data'}' in laptimer "\
            "configuration")

    def test_check_laptimer_passes_when_attributes_are_valid(self):
        # Arrange
        laptimer = json.loads('{"url": "ws://127.0.0.1:8080/ws"}')
        # Act & Assert
        config.check_laptimer(laptimer)

    def test_check_config_file_raises_exception_when_file_is_invalid_json(self):
        # Arrange
        file_name = os.path.join(os.getcwd(), 'bogus.json')
        if os.path.isfile(file_name):
            os.remove(file_name)
        config_file = open(file_name, 'w')
        config_file.write('bogus')
        config_file.close()
        # Act
        with self.assertRaises(Exception) as context:
            config.check_config_file(file_name)
        # Assert
        msg = "Configuration file '{}' does not seem to be proper JSON ('No " \
            "JSON object could be decoded')".format(file_name)
        self.assertEqual(context.exception.message, msg)
        # Cleanup
        os.remove(file_name)

    def test_check_config_file_passes(self):
        # Arrange
        file_name = os.path.join(os.getcwd(), 'valid.json')
        config_json = \
        '{' \
        '   "laptimer": {' \
        '       "url": "ws://127.0.0.1:8080/ws"' \
        '   },' \
        '   "sensors": [{' \
        '       "name": "Start & finish",' \
        '       "url": "ws://127.0.0.1:8888/ws",' \
        '       "location": "START_FINISH",' \
        '       "hardware": "RPI_REV2",' \
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
        config_file = open(file_name, 'w')
        config_file.write(config_json)
        config_file.close()
        # Act
        cfg = config.check_config_file(file_name)
        # Assert
        laptimer = cfg['laptimer']
        url = laptimer['url']
        self.assertEqual('ws://127.0.0.1:8080/ws', url)
        # Cleanup
        os.remove(file_name)
