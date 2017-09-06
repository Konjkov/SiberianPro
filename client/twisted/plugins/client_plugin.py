from twisted.application.service import ServiceMaker

serviceMaker = ServiceMaker(
    'client', 'client.client', 'file watcher plugin', 'watcher'
)
