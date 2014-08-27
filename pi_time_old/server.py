from twisted.application import internet, \
                                service
from twisted.internet import defer, \
                             reactor
from twisted.python import threadpool
from twisted.web import client, \
                        resource, \
                        server, \
                        static, \
                        wsgi
import os
import sys

PORT = 80
sys.path.append('pi_time')
os.environ['DJANGO_SETTINGS_MODULE'] = 'pi_time.settings'
from django.core.handlers.wsgi import WSGIHandler

def wsgi_resource():
    pool = threadpool.ThreadPool()
    pool.start()
    reactor.addSystemEventTrigger('after', 'shutdown', pool.stop)
    wsgi_resource = wsgi.WSGIResource(reactor, pool, WSGIHandler())
    return wsgi_resource

class Root(resource.Resource):
    def __init__(self, wsgi_resource):
        resource.Resource.__init__(self)
        self.wsgi_resource = wsgi_resource

    def getChild(self, path, request):
        path0 = request.prepath.pop(0)
        request.postpath.insert(0, path0)
        return self.wsgi_resource

application = service.Application('twisted-django')
wsgi_root = wsgi_resource()
root = Root(wsgi_root)
#staticrsrc = static.File(os.path.join(os.path.abspath('.'), 'pi_time/media'))
#root.putChild('media', staticrsrc)
main_site = server.Site(root)
internet.TCPServer(PORT, main_site).setServiceParent(application)