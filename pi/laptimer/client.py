from twisted.internet import reactor
from autobahn.websocket import WebSocketClientFactory, WebSocketClientProtocol
from autobahn.websocket import connectWS
 
 
class APIClientProtocol(WebSocketClientProtocol):
 
   def callAPI(self):
		self.sendMessage("get_all_data")
 
   def onOpen(self):
		self.callAPI()
 
   def onMessage(self, msg, binary):
		print "Result: " + msg
		reactor.callLater(1, self.callAPI)
 
 
if __name__ == '__main__':
	factory = WebSocketClientFactory("ws://localhost:9000", debug = False)
	factory.protocol = APIClientProtocol
	connectWS(factory)
	reactor.run()