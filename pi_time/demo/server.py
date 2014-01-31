from autobahn.twisted.websocket import listenWS
from laptimer.server import APIServerFactory
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File
import django_settings
import logging


logger = logging.getLogger('laptimer')

if __name__ == '__main__':
    # TODO: Get server and port from settings
    debug=django_settings.get('debug_app')
    factory = APIServerFactory('ws://localhost:9000', debug=debug, debugCodePaths=debug)
    listenWS(factory)
    webdir = File('.')
    web = Site(webdir)
    reactor.run()
