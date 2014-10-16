import os
import unittest

from pi_time.api import Api


class ApiTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
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
            '       "pinLedLap": 16,' \
            '       "pinLedEvent": 18,' \
            '       "pinEvent": 22' \
            '    }]' \
            '}'
        config_file = os.path.join(os.getcwd(), 'test_api.json')
        if os.path.isfile(config_file):
            os.remove(config_file)
        with open(config_file, 'w') as cfg:
            cfg.write(config_json)
        cls.config_file = config_file

    @classmethod
    def tearDownClass(cls):
        file_name = cls.config_file
        if os.path.isfile(file_name):
            os.remove(file_name)

    def test_init_passes_when_session_is_none(self):
        # Arrange
        session = None
        # Act
        api = Api(session, config_file=self.config_file)
        # Assert
        self.assertIsNotNone(api)

if __name__ == '__main__':
    unittest.main()