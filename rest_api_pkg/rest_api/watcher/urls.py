from rest_framework import routers

from .views import LogRecordViewSet

router = routers.SimpleRouter()

router.register(r'logrecord', LogRecordViewSet, base_name='logrecord')

urlpatterns = router.urls
