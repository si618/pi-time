import json
import os
import unittest

from pi_time import settings
from pi_time.api import api
from pi_time.models.rpc import RpcRequest


class ApiTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        file_name = os.path.join(os.getcwd(), 'test_api.json')
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
        with open(file_name, 'w') as config_file:
            config_file.write(config_json)
        cls.api_test_config_file = file_name
        cls.api = api.Api(file_name)

    @classmethod
    def tearDownClass(cls):
        file_name = cls.api_test_config_file
        if os.path.isfile(file_name):
            os.remove(file_name)

    def test_process_returns_expected_response_invalid_request(self):
        # Arrange
        request = 'bogus'
        # Act
        response = self.api.process(request)
        # Assert
        self.assertEqual(response.error, "Expected RpcRequest but got str")

    def test_process_returns_expected_response_invalid_method(self):
        # Arrange
        method = 'bogusMethod'
        context = 'bogusContext'
        request = RpcRequest('get_sensor_options', context=context)
        request.method = method;
        # Act
        response = self.api.process(request)
        # Assert
        self.assertEqual(response.error, "Unknown API method 'bogusMethod'")

    def test_process_returns_expected_response_valid_method(self):
        # Arrange
        method = 'get_sensor_options'
        context = 'testing'
        request = RpcRequest(method=method, context=context)
        sensor_options = (
            ('locations', settings.OPTIONS_SENSOR_LOCATION),
            ('hardwares', settings.OPTIONS_HARDWARE)
        )        
        # Act
        response = self.api.process(request)
        # Assert
        self.assertEqual(response.error, None)
        self.assertEqual(response.data, sensor_options)


if __name__ == '__main__':
    unittest.main()