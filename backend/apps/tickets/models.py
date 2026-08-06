from django.db import models


class Ticket(models.Model):
    purchased_at = models.DateTimeField(auto_now_add=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField(null=True, blank=True)

