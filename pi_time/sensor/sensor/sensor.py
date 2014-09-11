from os import path

from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.util import sleep
from autobahn.wamp.exception import ApplicationError

from twisted.internet.defer import inlineCallbacks
from twisted.python import log

from pi_time.api import api
from pi_time.models import RpcRequest


class AppSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        config_dir = path.dirname(path.dirname(path.realpath(__file__)))
        config_file = path.join(config_dir, 'config.json')
        self.api = api.Api(config_file=config_file)

        yield

        ## SUBSCRIBE to a topic and receive events
        #def onhello(msg):
        #    print("event for 'onhello' received: {}".format(msg))

        #sub = yield self.subscribe(onhello, 'io.github.si618.pi-time.onhello')
        #print("subscribed to topic 'onhello'")


        ## REGISTER a procedure for remote calling
        def get_sensor_options(self):
            request = RpcRequest('get_sensor_options', 'sensor')
            return api.process(request)

        get_sensor_options = yield self.register(get_sensor_options, 
            'io.github.si618.pi-time.get_sensor_options')
        log.msg("Registered procedure 'get_sensor_options'")


        ## PUBLISH and CALL every second .. forever
        #counter = 0
        #while True:

            ## PUBLISH an event
            #yield self.publish('io.github.si618.pi-time.oncounter', counter)
            #print("published to 'oncounter' with counter {}".format(counter))
            #counter += 1


            ## CALL a remote procedure
            #try:
            #    res = yield self.call('io.github.si618.pi-time.mul2', counter, 3)
            #    print("mul2() called with result: {}".format(res))
            #except ApplicationError as e:
                ## ignore errors due to the frontend not yet having
                ## registered the procedure we would like to call
                #if e.error != 'wamp.error.no_such_procedure':
                #    raise e

            #yield sleep(1)
