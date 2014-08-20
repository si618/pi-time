from autobahn.twisted.websocket import WebSocketClientFactory, \
                                       WebSocketClientProtocol
from autobahn.twisted.websocket import connectWS
from twisted.internet import reactor
import django_settings
import json
import logging


logger = logging.getLogger('laptimer')

class APIClientProtocol(WebSocketClientProtocol):

    def callAPI(self):
        self.sendMessage('{"call":"add_rider","args":{"rider_name":"Test API Rider"}}')
        self.sendMessage('{"call":"change_rider","args":{"rider_name":"Test API Rider","new_rider_name":"API Rider"}}')
        self.sendMessage('{"call":"remove_rider","args":{"rider_name":"API Rider"}}')
        self.sendMessage('{"call":"get_all_data"}')

    def onOpen(self):
        logger.debug('Connection open')
        self.callAPI()

    def onClose(self, wasClean, code, reason):
        logger.debug('Connection closed')

    def onMessage(self, msg, binary):
        jsonMsg = json.loads(msg)
        if 'call' in msg:
            call = jsonMsg['call']
        else:
            call = '<empty>'
        if 'data' in msg:
            data = jsonMsg['data']
        else:
            data = '<empty>'
        if 'ok' in msg:
            if jsonMsg['ok']:
                ok = 'Successful'
            else:
                ok = 'Failed'
            logger.debug('%s call: %s data: %s ' % (ok, call, data))
            return
        if 'event' in msg:
            event = jsonMsg['event']
            logger.debug('Received message: %s data: %s' % (event, data))
            return
        logger.debug('Unknown message')


if __name__ == '__main__':
    # TODO: Get server and port from settings
    debug=django_settings.get('debug_app')
    factory = WebSocketClientFactory("ws://localhost:9000", debug=debug)
    factory.protocol = APIClientProtocol
    connectWS(factory)
    reactor.run()
