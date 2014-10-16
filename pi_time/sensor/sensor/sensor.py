import pi_time

from os import path

from autobahn.twisted.wamp import ApplicationSession

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

        # Methods to publish events from sensor node to sensor clients
        # def sensor_triggered(msg):
        # # Let sensor clients know a sensor event was triggered
        #    yield self.publish(settings.URI_PREFIX + 'sensor_triggered', msg)

        # Subscribe to events from laptimer or sensor clients
        #yield self.subscribe(sensor_triggered,
        #    settings.URI_PREFIX + 'sensor_triggered')

        # Register procedures available from sensor clients
        yield self.register(api)

        log.msg('Pi-time sensor v{} ready'.format(pi_time.VERSION))

        yield self.publish(settings.URI_PREFIX + 'sensor_started',
                           str(details))

    @inlineCallbacks
    def onLeave(self, details):
        yield self.publish(settings.URI_PREFIX + 'sensor_stopped',
                           str(details))
