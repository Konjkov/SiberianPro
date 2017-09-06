#!/usr/bin/env python3

import os
import json
from twisted.application import service
from twisted.application import internet
from twisted.internet import task
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory
from twisted.python import usage

timeout = 2.0

host = '127.0.0.1'
port = 9000
source = 'first'


class Options(usage.Options):
    optParameters = [
        ["dir", "d", '.', "Directory to watching on."],
        ["port", "p", 9000, "The port number to send to."],
        ["host", "h", "localhost", "Server hostname"],
        ["src", "s", "first", "Server source name"],
    ]


class WatchClientProtocol(Protocol):

    def __init__(self):
        self.lc = task.LoopingCall(self.sendData)
        self.lc.start(2)
        self.data = {}

    def connectionMade(self):
        print('connectionMade')
        self.data = self.directoryList(self.factory.directory)

    def directoryList(self, directory):
        return {
            f: self.fileProperty(f) for f in os.listdir(directory)
            if os.path.isfile(f)
        }

    def fileProperty(self, file):
        """Свойство файла по которому определяется, что он изменился.
        Поскольку операция просмотра директории и последующего получения
        размера файла в целом не атомарна может возникнуть исключительная
        ситуация.
        :param file: 
        :return: filesize or None
        """
        try:
            return os.path.getsize(file)
        except FileNotFoundError:
            return None

    def directoryDiff(self, directory):
        """Создает списки, созданныйх, удаленных и измененных файлов.
        :param directory: 
        :return: словарь списков 
        """
        old_data, new_data = self.data, self.directoryList(directory)
        del_files = {
            f: (old_data[f], 0) for f in old_data.keys() - new_data.keys()
        }
        add_files = {
            f: (0, new_data[f]) for f in new_data.keys() - old_data.keys()
        }
        change_file = {
            f: (old_data[f], new_data[f]) for f in new_data
            if f in old_data.keys() & new_data.keys()
               and old_data[f] != new_data[f]
        }
        self.data = new_data
        return {
            'del': del_files,
            'add': add_files,
            'change_files': change_file
        }

    def jsonResponce(self):
        """Возвращает информацию об изменения файлов в директориии.
        Возвращает информацию об изменения файлов в директориии 
        в json формате с указанием имени источника.
        В случае если директория была удалена в процессе мониторинга
        вместо инвормации об изменениях возвращается None.
        :return: JSON-object 
        """
        diffs = (
            self.directoryDiff(self.factory.directory)
            if os.path.isdir(self.factory.directory)
            else None
        )

        result = {
            'source': self.factory.source,
            'diffs': diffs
        }
        return json.dumps(result)

    def sendData(self):
        """Посылает информацию об изменениях файлов на сервер.
        :return: None 
        """
        if self.transport:
            self.transport.write(self.jsonResponce().encode('latin-1'))


class WatchClientFactory(ClientFactory):

    def __init__(self, source, directory):
        self.source = source
        self.directory = directory

    def buildProtocol(self, addr):
        protocol = WatchClientProtocol()
        protocol.factory = self
        return protocol

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()


def makeService(options={'host': host, 'port': port, 'source': source, 'directory': '.'}):
    app = service.Application("client")
    tcp = internet.TCPClient(
        options['host'],
        options['port'],
        WatchClientFactory(options['source'], options['directory'])
    )
    tcp.setServiceParent(app)
    return app


application = makeService()
