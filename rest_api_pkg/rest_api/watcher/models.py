from django.db import models


class LogRecord(models.Model):

    CREATED = 1
    DELETED = 2
    CHANGED = 3

    STATUS_CHOICES = (
        (CREATED, 'Created'),
        (DELETED, 'Deleted'),
        (CHANGED, 'Changed'),
    )

    source = models.TextField()
    status = models.IntegerField(choices=STATUS_CHOICES)
    file_name = models.TextField()
    prev_size = models.IntegerField(null=True)
    next_size = models.IntegerField(null=True)
    log_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u'log records'
