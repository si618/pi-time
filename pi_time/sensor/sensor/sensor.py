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

        self.api = Api(session=self, config_file=config_file)

        # Methods to publish events from sensor node to sensor clients
        #def sensor_event(msg):
        #    # Let sensor clients know a sensor event was triggered
        #    yield self.publish(settings.URI_PREFIX + 'sensor_event', msg)

        # Subscribe to events from laptimer or sensor clients
        #yield self.subscribe(sensor_event,
        #    settings.URI_PREFIX + 'sensor_event')

        # Register procedures available from sensor clients
        def _register(method, uri):
            self.register(method, settings.URI_PREFIX + uri);
        # TODO: How to avoid ApplicationError.PROCEDURE_ALREADY_EXISTS?
        _register(self.api.get_laptimer_config, 'get_laptimer_config')
        _register(self.api.get_sensor_options, 'get_sensor_options')
        _register(self.api.get_sensor_config, 'get_sensor_config')

        log.msg('Pi-time sensor v{} ready'.format(pi_time.VERSION))

        yield self.publish(settings.URI_PREFIX + 'sensor_started',
            str(details))
        yield self.publish(settings.URI_PREFIX + 'sensor_triggered',
            'TODO: Testing')

    @inlineCallbacks
    def onLeave(self, details):

        self.publish(settings.URI_PREFIX + 'sensor_stopped', str(details))
