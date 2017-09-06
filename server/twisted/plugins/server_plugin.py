from twisted.application.service import ServiceMaker

serviceMaker = ServiceMaker(
    'server', 'server.server', 'data collector plugin', 'collector'
)
