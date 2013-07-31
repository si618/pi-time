from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol
from autobahn.websocket import listenWS
from laptimer.models import APIResult
from laptimer.services import API
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File
import django_settings
import json
import logging


logger = logging.getLogger(__name__)

class APIServerProtocol(WebSocketServerProtocol):
	
	def onMessage(self, msg, binary):
		'''Processes an API call, returning an APIResult in JSON format.'''
		data = json.loads(msg)
		if data['call'] is None:
			error = "Message missing 'call': %s" % msg
			logger.error(error)
			return APIResult(result=False, data=error)
		if 'args' not in msg:
			data['args'] = {}
		call = data['call']
		kwargs = data['args']
		
		method = getattr(API(), call)
		if not method:
			error = "Method not implemented in API: %s" % call
			logger.error(error)
			return APIResult(result=False, data=error)
		logger.debug('%s(%s)' % (call, ', '.join(['%s=%s' % (key, value)
			for key, value in kwargs.iteritems()])))
		# http://xkcd.com/353/ applies above and below :)
		result = method(**kwargs)
		if (isinstance(result, APIResult) == False):
			error = "Method must return APIResult, error in: %s" % call
			logger.error(error)
			result = APIResult(result=False, data=error)
		self.sendMessage(result.toJSON(), binary)


if __name__ == '__main__':
	# TODO: Get server and port from settings
	factory = WebSocketServerFactory('ws://localhost:9000',
		debug=django_settings.get('debug_app'))
	factory.protocol = APIServerProtocol
	listenWS(factory)
	webdir = File('.')
	web = Site(webdir)
	logger.debug('Running server...')
	reactor.run()
