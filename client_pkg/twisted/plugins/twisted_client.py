from twisted.application.service import ServiceMaker

TwistedClient = ServiceMaker(
    'Client.',
    'client.client',
    'File watcher client.',
    'client'
)

