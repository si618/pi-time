import pi_time

from os import path

from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.util import sleep
from autobahn.wamp.exception import ApplicationError

from twisted.internet.defer import inlineCallbacks
from twisted.python import log

from pi_time.api import api
from pi_time.models.rpc import RpcRequest


class SensorAppSession(ApplicationSession):
    """
    Sensor application session.
    """

    @inlineCallbacks
    def onJoin(self, details):
        config_dir = path.dirname(path.dirname(path.realpath(__file__)))
        config_file = path.join(config_dir, 'config.json')
        self.api = api.Api(config_file=config_file)
        self.context = 'Sensor session {}'.format(details.session)

        def get_sensor_config():
            result = self.call_api('get_sensor_config')
            return result

        def get_sensor_options():
            result = self.call_api('get_sensor_options')
            return result

        reg_get_sensor_config = yield self.register(get_sensor_config,
            'io.github.si618.pi-time.get_sensor_config')
        reg_get_sensor_options = yield self.register(get_sensor_options,
            'io.github.si618.pi-time.get_sensor_options')

        log.msg("Sensor v{} ready".format(pi_time.VERSION))


    def call_api(self, method, params=None):
        request = RpcRequest(method, self.context, params)
        response = self.api.process(request)
        return response.encode()