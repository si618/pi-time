# WebSocket server courtesy of Autobahn goes here.
# TODO: Add/inject port and debug to/from settings
from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol
from autobahn.websocket import listenWS
from laptimer import services
from laptimer import models
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File


class APIServerProtocol(WebSocketServerProtocol):
	def onMessage(self, msg, binary):
		api_method = 'get_all_data' # TODO : Parse from msg
		api = API()
		method = getattr(api, api_method)
		if not method:
			raise Exception("Method %s not implemented" % method_name)
		result = method()
		self.sendMessage(result, binary)


if __name__ == '__main__':
	factory = WebSocketServerFactory("ws://localhost:9000", 
		debug=django_settings.get('debug_app', settings.DEBUG))
	factory.protocol = APIServerProtocol
	listenWS(factory)
	webdir = File(".")
	web = Site(webdir)
	reactor.run()
