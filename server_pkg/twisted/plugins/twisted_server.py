from twisted.application.service import ServiceMaker

serviceMaker = ServiceMaker(
    'Server.',
    'server.server',
    'Data collector server.',
    'server'
)
