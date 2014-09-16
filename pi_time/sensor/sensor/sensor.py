import pi_time

from os import path

from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.util import sleep
from autobahn.wamp.exception import ApplicationError

from twisted.internet.defer import inlineCallbacks
from twisted.python import log

from pi_time.api.processor import ApiProcessor
from pi_time.models.api import ApiRequest


class SensorAppSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        config_dir = path.dirname(path.dirname(path.realpath(__file__)))
        config_file = path.join(config_dir, 'config.json')
        self.api = ApiProcessor(config_file=config_file, app_session=self)
        # TODO: Handle multiple sensors
        self.sensor_name = self.api.config['sensors'][0]['name']
        self.context = 'sensor {}'.format(self.sensor_name)

        config = yield self.api.register('get_sensor_config', self.context)
        options = yield self.api.register('get_sensor_options', self.context)

        log.msg("Sensor v{} ready".format(pi_time.VERSION))

        yield