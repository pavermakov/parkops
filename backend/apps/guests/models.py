from django.db import models


class Guest(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    height_cm = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.height_cm})'



