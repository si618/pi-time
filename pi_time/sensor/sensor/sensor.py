import pi_time

from os import path

from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.util import sleep
from autobahn.wamp.exception import ApplicationError

from twisted.internet.defer import inlineCallbacks
from twisted.python import log

from pi_time.api import api
from pi_time.models.api import ApiRequest


class SensorAppSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        config_dir = path.dirname(path.dirname(path.realpath(__file__)))
        config_file = path.join(config_dir, 'config.json')
        self.api = api.Api(config_file=config_file, applicationSession=self)
        # TODO: Handle multiple sensors
        self.sensor_name = self.api.config['sensors'][0]['name']
        self.context = 'sensor {}'.format(self.sensor_name)

        def get_sensor_config():
            response = self.api.call('get_sensor_config', self.context)
            return response.encode()

        def get_sensor_options():
            response = self.api.call('get_sensor_options', self.context)
            return response.encode()

        reg_get_sensor_config = yield self.register(get_sensor_config,
            'io.github.si618.pi-time.get_sensor_config')
        reg_get_sensor_options = yield self.register(get_sensor_options,
            'io.github.si618.pi-time.get_sensor_options')

        log.msg("Sensor v{} ready".format(pi_time.VERSION))
