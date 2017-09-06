#!/usr/bin/env python3

from twisted.application import internet
from twisted.application import service
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.python import usage

port = 9000


class Options(usage.Options):
    optParameters = [
        ["port", "p", 9000, "The port number to listen on."],
    ]


class WatchServerProtocol(Protocol):

    def connectionMade(self):
        self.transport.write('hello world'.encode('latin-1'))

    def dataReceived(self, data):
        print(data)
        if data.startswith('quit'.encode('latin-1')):
            self.transport.loseConnection()

    def clientConnectionLost(self, connector, reason):
        print('Lost connection. Reason: {}'.format(reason))

    def clientConnectionFailed(self, connector, reason):
        print('Lost failed. Reason: {}'.format(reason))


class WatchServerFactory(Factory):
    protocol = WatchServerProtocol


def makeService(options={'port': port}):
    app = service.Application("server")
    tcp = internet.TCPServer(options['port'], WatchServerFactory())
    tcp.setServiceParent(app)
    return app

application = makeService()
