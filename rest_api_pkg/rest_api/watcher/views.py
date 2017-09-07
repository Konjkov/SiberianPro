from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet
from django_filters import DateTimeFilter
from .serializers import LogRecordSerializer
from .models import LogRecord

class LogRecordFilter(FilterSet):
    dateStart = DateTimeFilter(name='log_time', lookup_expr='gte')
    dateEnd = DateTimeFilter(name='log_time', lookup_expr='lte')

    class Meta:
        model = LogRecord
        fields = ('source', 'dateStart', 'dateEnd')


class LogRecordViewSet(ReadOnlyModelViewSet):
    """Return LogRecord (metadata)."""

    serializer_class = LogRecordSerializer
    # permission_classes = (IsAuthenticated,)
    queryset = LogRecord.objects.order_by('pk')
    filter_backends = (DjangoFilterBackend,)
    filter_class = LogRecordFilter
