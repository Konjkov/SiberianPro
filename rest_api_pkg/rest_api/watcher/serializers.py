from rest_framework import serializers
from .models import LogRecord


class LogRecordSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = LogRecord
        fields = ['pk', 'source', 'status', 'file_name',
                  'prev_size', 'next_size', 'log_time']
