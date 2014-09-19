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

        api = Api(session=self, config_file=config_file)

        def sensor_connected(msg):
            yield self.publish(settings.URI_PREFIX + 'sensor_connected', msg)
        sub_sensor_connected = yield self.subscribe(sensor_connected,
            settings.URI_PREFIX + 'sensor_connected')
        def sensor_disconnected(msg):
            yield self.publish(settings.URI_PREFIX + 'sensor_disconnected',
                msg)
        sub_sensor_disconnected = yield self.subscribe(sensor_disconnected,
            settings.URI_PREFIX + 'sensor_disconnected')

        """
        reg_options = yield self.register(api.get_laptimer_options,
            settings.URI_PREFIX + 'get_laptimer_options')
        reg_config = yield self.register(api.get_laptimer_config,
            settings.URI_PREFIX + 'get_laptimer_config')
        """

        log.msg('Pi-time laptimer v{} ready'.format(pi_time.VERSION))
        yield self.publish(settings.URI_PREFIX + 'start_laptimer')


        """
        ## SUBSCRIBE to a topic and receive events
        ##
        def onhello(msg):
            print("event for 'onhello' received: {}".format(msg))

        sub = yield self.subscribe(onhello, 'io.github.si618.pi-time.onhello')
        print("subscribed to topic 'onhello'")


        ## REGISTER a procedure for remote calling
        ##
        def add2(x, y):
            print("add2() called with {} and {}".format(x, y))
            return x + y

        reg = yield self.register(add2, 'io.github.si618.pi-time.add2')
        print("procedure add2() registered")


        ## PUBLISH and CALL every second .. forever
        ##
        counter = 0
        while True:

            ## PUBLISH an event
            ##
            yield self.publish('io.github.si618.pi-time.oncounter', counter)
            print("published to 'oncounter' with counter {}".format(counter))
            counter += 1


            ## CALL a remote procedure
            ##
            try:
                res = yield self.call('io.github.si618.pi-time.mul2', counter, 3)
                print("mul2() called with result: {}".format(res))
            except ApplicationError as e:
                ## ignore errors due to the frontend not yet having
                ## registered the procedure we would like to call
                if e.error != 'wamp.error.no_such_procedure':
                    raise e


            yield sleep(1)
        """