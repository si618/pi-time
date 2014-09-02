from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.util import sleep
from autobahn.wamp.exception import ApplicationError
from twisted.internet.defer import inlineCallbacks
from twisted.python import log
from pi_time.api import Api

class AppSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        api = Api()

        counter = 0
        while True:
            counter += 1
            yield sleep(1)


        ## SUBSCRIBE to a topic and receive events
        #def onhello(msg):
        #    print("event for 'onhello' received: {}".format(msg))

        #sub = yield self.subscribe(onhello, 'io.github.si618.pi-time.onhello')
        #print("subscribed to topic 'onhello'")


        ## REGISTER a procedure for remote calling
        #def add2(x, y):
        #    print("add2() called with {} and {}".format(x, y))
        #    return x + y

        #reg = yield self.register(add2, 'io.github.si618.pi-time.add2')
        #print("procedure add2() registered")


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
