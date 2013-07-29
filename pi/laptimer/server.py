import django_settings
import json
from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol
from autobahn.websocket import listenWS
from laptimer import services
from laptimer import models
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File


class APIServerProtocol(WebSocketServerProtocol):
	def onMessage(self, msg, binary):
		print 'msg: %s' % (msg)
		data = json.loads(msg)
		if data['call'] is None:
			raise Exception('Missing "call"')
		if 'args' not in msg:
			data['args'] = {}
		call = data['call']
		args = data['args']
		print 'call: %s args: %s' % (call, args)
		method = getattr(services.API(), call)
		if not method:
			raise Exception('Method not implemented: %s' % method)
		result = method(*args)
		self.sendMessage(json.dumps(call), binary)


if __name__ == '__main__':
	# TODO: Get server and port from settings
	factory = WebSocketServerFactory('ws://localhost:9000', 
		debug=django_settings.get('debug_app'))
	factory.protocol = APIServerProtocol
	listenWS(factory)
	webdir = File('.')
	web = Site(webdir)
	print 'Server is running...'
	reactor.run()
