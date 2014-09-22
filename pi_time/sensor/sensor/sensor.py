import pi_time

from os import path

from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.util import sleep
from autobahn.wamp.exception import ApplicationError

from twisted.internet.defer import inlineCallbacks
from twisted.python import log

from pi_time import settings
from pi_time.api import Api


class SensorAppSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        config_dir = path.dirname(path.dirname(path.realpath(__file__)))
        config_file = path.join(config_dir, 'config.json')

        api = Api(session=self, config_file=config_file)

        def laptimer_connected(msg):
            yield self.publish(settings.URI_PREFIX + 'laptimer_connected',
                msg)
        sub_laptimer_connected = yield self.subscribe(
            laptimer_connected,
            settings.URI_PREFIX + 'laptimer_connected')
        def laptimer_disconnected(msg):
            yield self.publish(settings.URI_PREFIX + 'laptimer_disconnected',
                msg)
        sub_laptimer_disconnected = yield self.subscribe(
            laptimer_disconnected,
            settings.URI_PREFIX + 'laptimer_disconnected')

        self.register(api.sensor_started,
            settings.URI_PREFIX + 'sensor_started');

        log.msg('Pi-time sensor v{} ready'.format(pi_time.VERSION))
