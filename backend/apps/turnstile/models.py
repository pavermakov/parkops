from django.db import models

from apps.attractions.models import Attraction
from apps.tickets.models import Ticket


class ScanLog(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)
    success = models.BooleanField()
    message = models.CharField(max_length=255, null=True, blank=True)
    scanned_at = models.DateTimeField(auto_now_add=True)