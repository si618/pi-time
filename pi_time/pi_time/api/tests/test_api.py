import os
import unittest

from pi_time.api import api
from pi_time.models import rpc


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
        method = 'bogusMethod'
        context = 'bogusContext'
        request = rpc.RpcRequest(method, context)
        # Act
        response = self.api.process(request)
        # Assert
        # TODO:

if __name__ == '__main__':
    unittest.main()