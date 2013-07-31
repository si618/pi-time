from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS
from twisted.internet import reactor
from twisted.python import log
from laptimer.models import APIResult
from laptimer.services import API
import django_settings
import json
import logging
import sys


logger = logging.getLogger(__name__)

class BroadcastServerProtocol(WebSocketServerProtocol):

   def onOpen(self):
      self.factory.register(self)

   def onMessage(self, msg, binary):
      if not binary:
         self.factory.broadcast("received message '%s' from %s" % (msg, self.peerstr))

   def connectionLost(self, reason):
      WebSocketServerProtocol.connectionLost(self, reason)
      self.factory.unregister(self)


class BroadcastServerFactory(WebSocketServerFactory):
   protocol = BroadcastServerProtocol

   def __init__(self, url):
      WebSocketServerFactory.__init__(self, url)
      self.clients = []
      self.tickcount = 0
      self.tick()

   def tick(self):
      self.tickcount += 1
      self.broadcast("tick %d" % self.tickcount)
      reactor.callLater(1, self.tick)

   def register(self, client):
      if not client in self.clients:
         logger.info("registered client " + client.peerstr)
         self.clients.append(client)

   def unregister(self, client):
      if client in self.clients:
         logger.info("unregistered client " + client.peerstr)
         self.clients.remove(client)

   def broadcast(self, msg):
      logger.info("broadcasting message '%s' .." % msg)
      for c in self.clients:
         logger.info("send to " + c.peerstr)
         c.sendMessage(msg)


if __name__ == '__main__':
   log.startLogging(sys.stdout)
   factory = BroadcastServerFactory("ws://localhost:9000")
   listenWS(factory)
   reactor.run()
