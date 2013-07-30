from twisted.internet import reactor
from autobahn.websocket import WebSocketClientFactory, WebSocketClientProtocol
from autobahn.websocket import connectWS
import django_settings
import json
import logging


logger = logging.getLogger(__name__)

class APIClientProtocol(WebSocketClientProtocol):

	def callAPI(self):
		self.sendMessage('{"call":"add_rider","args":{"rider_name":"Test API Rider"}}')
		self.sendMessage('{"call":"change_rider","args":{"rider_name":"Test API Rider","new_rider_name":"API Rider"}}')
		self.sendMessage('{"call":"remove_rider","args":{"rider_name":"API Rider"}}')
		self.sendMessage('{"call":"get_all_data"}')
		
	def onOpen(self):
		self.callAPI()

	def onClose(self, wasClean, code, reason):
		logger.debug('Closing connection')

	def onMessage(self, msg, binary):
		logger.debug(msg)


if __name__ == '__main__':
	# TODO: Get server and port from settings
	factory = WebSocketClientFactory("ws://localhost:9000",
		debug=django_settings.get('debug_app'))
	factory.protocol = APIClientProtocol
	connectWS(factory)
	reactor.run()
