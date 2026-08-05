from django.db import models


class Attraction(models.Model):
    class OperationStatus(models.TextChoices):
        RUNNING = 'running'
        DOWN_WEATHER = 'down_weather'
        DOWN_MECHANICAL = 'down_mechanical'
        CLOSED = 'closed'

    name = models.CharField(max_length=255)
    operation_status = models.CharField(choices=OperationStatus, max_length=20)