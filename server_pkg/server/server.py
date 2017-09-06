#!/usr/bin/env python3

import json
from twisted.application import internet
from twisted.application import service
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.python import usage
from twisted.python import log


class WatchServerProtocol(Protocol):

    def printData(self, data):
        """Печать в лог информаци об изменении файлов.
        :param data: 
        :return: 
        """
        source = data['source']
        if data['diffs'] is None:
            log.msg('Наблюдаемая директория на сервере',
                    source, 'была удалена')
        else:
            for f, size in data['diffs']['add'].items():
                log.msg('На сервере', source, 'был создан файл', f,
                        'размером', size[1], 'байт')
            for f, size in data['diffs']['del'].items():
                log.msg('На сервере', source, 'был удален файл', f,
                        'размером', size[0], 'байт')
            for f, size in data['diffs']['change'].items():
                log.msg('На сервере', source, 'у файла', f,
                        'был изменен размер с ', size[0], 'до', size[1],
                        'байт')

    def dataReceived(self, data):
        # log.msg('dataReceived')
        self.printData(json.loads(data.decode('utf-8')))

    def clientConnectionLost(self, connector, reason):
        log.msg('Lost connection. Reason: {}'.format(reason))

    def clientConnectionFailed(self, connector, reason):
        log.msg('Lost failed. Reason: {}'.format(reason))


class WatchServerFactory(Factory):
    protocol = WatchServerProtocol


class Options(usage.Options):
    synopsis = "[options]"
    longdesc = "Create server collecting data from clients."
    optParameters = [
        ["port", "p", 9000, "The port number to listen on."],
    ]


def makeService(options):
    return internet.TCPServer(int(options['port']), WatchServerFactory())
