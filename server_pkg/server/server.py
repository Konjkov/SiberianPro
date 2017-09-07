#!/usr/bin/env python3

import json
from datetime import datetime
from psycopg2 import OperationalError
from psycopg2 import IntegrityError
from twisted.application import internet
from twisted.enterprise import adbapi
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.python import usage
from twisted.python import log


class ReconnectingConnectionPool(adbapi.ConnectionPool):
    """Действия в случае ошибки дравера psycopg2.
    """
    def _runInteraction(self, interaction, *args, **kw):
        try:
            return adbapi.ConnectionPool._runInteraction(
                self, interaction, *args, **kw)
        except OperationalError as e:
            log.msg("psycopg2: got error %s" % e)
            conn = self.connections.get(self.threadID())
            self.disconnect(conn)
        except IntegrityError as e:
            log.msg("psycopg2: got error %s" % e)
            conn = self.connections.get(self.threadID())
            self.disconnect(conn)


class WatchServerProtocol(Protocol):

    def __init__(self):
        self.dbpool = ReconnectingConnectionPool(
            'psycopg2',
            host='localhost',
            port='5432',
            database='watcher',
            user='watcher',
            password='watcher'
        )
        self.query = ('INSERT INTO "watcher_logrecord" '
                      '(source, status, file_name, prev_size, next_size, log_time) '
                      'VALUES (%s, %s, %s, %s, %s, %s)')

    def insertIntoDB(self, source, status, file_name, prev_size, next_size):
        return self.dbpool.runOperation(
            self.query, (source, status, file_name, prev_size, next_size, datetime.now())
        ).addErrback(log.err)

    def loadData(self, data):
        source = data['source']
        if data['diffs']:
            for f, size in data['diffs']['add'].items():
                self.insertIntoDB(source, 1, f, size[0], size[1])
            for f, size in data['diffs']['del'].items():
                self.insertIntoDB(source, 2, f, size[0], size[1])
            for f, size in data['diffs']['change'].items():
                self.insertIntoDB(source, 3, f, size[0], size[1])

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
        self.loadData(json.loads(data.decode('utf-8')))

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
