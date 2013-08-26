from autobahn.websocket import WebSocketServerProtocol, WebSocketServerFactory
from laptimer import api
from laptimer.models import APIResult, APIBroadcast
from twisted.python import log
import django_settings
import json
import logging
import sys


logger = logging.getLogger('laptimer')

class APIMessageHandler:
    '''Handles processing of API calls.'''
    # Events broadcasted before they are invoked
    _broadcast_pre = ['server_poweroff']
    # Events broadcasted after they are invoked TODO: Use django signals?
    _broadcast_post = [
        'add_rider', 'change_rider', 'remove_rider',
        'add_track', 'change_track', 'remove_track',
        'add_session', 'change_session', 'remove_session', 'start_session', 'end_session',
        'remove_lap', 'start_lap', 'end_lap', 'cancel_lap'
    ]

    # TODO: User authentication and API authorization using WAMP RPC instead of WebSocket,
    # which replaces this manual message handling with autobahn code, see:
    # http://autobahn.ws/static/reference/python/wampserver.html#autobahn.wamp.WampCraServerProtocol
    # Authorization groups:
    #   admin     - full access
    #   rider     - modify own rider details, modify some session details
    #   sensor    - trigger sensor related events
    #   spectator - view all data (get_...)

    def process(self, server, msg):
        '''Processes an API call.'''
        data = self._load_data(server, msg)
        if not data:
            return
        call = data['call']
        kwargs = data['args']
        method = self._get_api_method(server, call)
        if not method:
            return
        self._broadcast(server, call, self._broadcast_pre, kwargs)
        logger.debug('Invoking method: %s(%s)' % (call, ', '.join(['%s=%s' % (key, value)
            for key, value in kwargs.iteritems()])))
        result = method(**kwargs)
        if not self._verify_type(server, result, APIResult, call):
            return
        server.sendMessage(result.toJSON())
        if result.successful:
            self._broadcast(server, call, self._broadcast_post, result.data)

    def _load_data(self, server, msg):
        if 'call' not in msg:
            error = "Message missing 'call': %s" % msg
            logger.error(error)
            result = APIResult(call=None, successful=False, data=error)
            server.sendMessage(result.toJSON())
            return
        data = json.loads(msg)
        if 'args' not in data:
            data['args'] = {}
        return data

    def _get_api_method(self, server, call):
        method = getattr(api, call)
        if not method:
            error = "Method not implemented in API: %s" % call
            logger.error(error)
            result = APIResult(call, successful=False, data=error)
            server.sendMessage(result.toJSON())
            return
        return method

    def _broadcast(self, server, call, broadcast_events, data):
        if call not in broadcast_events:
            return
        broadcast = APIBroadcast(call, data)
        server.factory.broadcast(broadcast.toJSON())

    def _verify_type(self, server, actual, expected, call):
        match = isinstance(actual, expected)
        if not match:
            error = "Method must return %s, error in: %s" % (expected.__name__, call)
            logger.error(error)
            result = APIResult(call, successful=False, data=error)
            server.sendMessage(result.toJSON())
        return match

class APIServerProtocol(WebSocketServerProtocol):
    _handler = APIMessageHandler()

    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, msg, binary):
        if binary:
            return
        try:
            self._handler.process(self, msg)
        except Exception as e:
            logger.error('Unhandled exception: %s' % e)
            error = type(e).__name__ + ' from message: ' + msg
            result = APIResult('Unknown', successful=False, data=error)
            self.sendMessage(result.toJSON())

    def connectionLost(self, reason):
        logger.debug('Connection lost: %s' % reason)
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


observer = log.PythonLoggingObserver()
observer.start()
log.startLogging(sys.stdout)

class APIServerFactory(WebSocketServerFactory):
    protocol = APIServerProtocol

    def __init__(self, url, debug):
        WebSocketServerFactory.__init__(self, url, debug)
        self.clients = []

    def register(self, client):
        if not client in self.clients:
            log.msg('Registered client: ' + client.peerstr,
                logLevel=logging.DEBUG)
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            log.msg('Unregistered client: ' + client.peerstr,
                logLevel=logging.DEBUG)
            self.clients.remove(client)

    def broadcast(self, msg):
        log.msg('Broadcasting message: %s' % msg, logLevel=logging.DEBUG)
        for client in self.clients:
            logging.debug('Sending to: ' + client.peerstr)
            client.sendMessage(msg)
