import pi_time

from os import path

from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.util import sleep
from autobahn.wamp.exception import ApplicationError

from twisted.internet.defer import inlineCallbacks
from twisted.python import log

from pi_time import settings
from pi_time.api import Api


class LaptimerAppSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        config_dir = path.dirname(path.dirname(path.realpath(__file__)))
        config_file = path.join(config_dir, 'config.json')

        self.api = Api(session=self, config_file=config_file)

        # Methods to publish events from laptimer node to laptimer clients
        #def player_changed(msg):
        #    yield self.publish(settings.URI_PREFIX + 'player_changed', msg)

        # Subscribe to events from laptimer node
        #yield self.subscribe(player_changed,
        #    settings.URI_PREFIX + 'player_changed')

        # Register procedures available from laptimer clients
        yield self.register(self.api)

        log.msg('Pi-time laptimer v{} ready'.format(pi_time.VERSION))

        # Broadcast to all sensor sessions that laptimer session started
        yield self.publish(settings.URI_PREFIX + 'laptimer_started',
            str(details))

    @inlineCallbacks
    def onLeave(self, details):

        # Broadcast to all sensor sessions that laptimer session stopped
        yield self.publish(settings.URI_PREFIX + 'laptimer_stopped', 
            str(details))
