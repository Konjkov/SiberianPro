import os
import json
from twisted.python import usage
from twisted.internet import task
from twisted.application import internet
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory
from twisted.python import log


class WatchClientProtocol(Protocol):

    def __init__(self, timeout):
        self.lc = task.LoopingCall(self.sendData)
        self.lc.start(timeout)
        self.data = {}

    def connectionMade(self):
        """Запоминаем начальное состояние директории.
        :return: None
        """
        log.msg('watching directory', self.factory.directory)
        self.data = self.directoryList(self.factory.directory)

    def directoryList(self, directory):
        """Возвращает список файлов в директории.
        :param directory:
        :return:
        """
        return {
            os.path.join(directory, f):
                self.fileProperty(os.path.join(directory, f))
            for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))
        }

    def fileProperty(self, file):
        """Свойство файла по которому определяется, что он изменился.
        Поскольку операция просмотра директории и последующего получения
        размера файла в целом не атомарна может возникнуть исключительная
        ситуация, когда файл был удален в промежутке между этими двумя
        операциями.
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
            'change': change_file
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
        # log.msg('sendData')
        if self.transport:
            self.transport.write(self.jsonResponce().encode('utf-8'))


class WatchClientFactory(ClientFactory):

    def __init__(self, source, directory, timeout):
        self.source = source
        self.directory = os.path.abspath(directory)
        self.timeout = timeout

    def buildProtocol(self, addr):
        protocol = WatchClientProtocol(self.timeout)
        protocol.factory = self
        return protocol

    def clientConnectionFailed(self, connector, reason):
        """Переподключится если соединение не установилось."""
        connector.connect()

    def clientConnectionLost(self, connector, reason):
        """Переподключится если соединение оборвалось."""
        connector.connect()


class Options(usage.Options):
    synopsis = "[options]"
    longdesc = "Create client watching file changes."
    optParameters = [
        ["directory", "d", '.', "Directory to watching on."],
        ["port", "p", 9000, "The port number to send to."],
        ["host", "h", "localhost", "Server hostname"],
        ["source", "s", "client", "Client name"],
        ["timeout", "t", 2, "Polling timeout"],
    ]


def makeService(options):
    return internet.TCPClient(
        options['host'],
        int(options['port']),
        WatchClientFactory(
            options['source'],
            options['directory'],
            int(options['timeout'])
        )
    )
