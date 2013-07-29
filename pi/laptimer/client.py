import django_settings
import json
from twisted.internet import reactor
from autobahn.websocket import WebSocketClientFactory, WebSocketClientProtocol
from autobahn.websocket import connectWS
 
 
class APIClientProtocol(WebSocketClientProtocol):
 
   def callAPI(self):
		self.sendMessage('{"call":"get_all_data"}')
		self.sendMessage('{"call":"add_rider","args":{"rider_name":"Test API Rider"}}')
		self.sendMessage('{"call":"change_rider","args":{"old_rider_name":"Test API Rider","new_rider_name":"API Rider"}}')
		self.sendMessage('{"call":"remove_rider","args":{"rider_name":"API Rider"}}')

   def onOpen(self):
		self.callAPI()
 
   def onMessage(self, msg, binary):
		print "Result: " + msg
		#reactor.callLater(1, self.callAPI)
 
 
if __name__ == '__main__':
	# TODO: Get server and port from settings
	factory = WebSocketClientFactory("ws://localhost:9000", 
		debug=django_settings.get('debug_app'))
	factory.protocol = APIClientProtocol
	connectWS(factory)
	reactor.run()