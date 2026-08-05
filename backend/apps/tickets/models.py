from django.db import models

class Ticket(models.Model):
    purchased_at = models.DateTimeField(auto_now_add=True)
