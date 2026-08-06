from django.db import models

from apps.guests.models import Guest


class Ticket(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='tickets')
    purchased_at = models.DateTimeField(auto_now_add=True)
    valid_from = models.DateField()
    valid_to = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        full_name = f'{self.guest.first_name} {self.guest.last_name}'
        date_range = self.valid_from.strftime('%B %-d')

        if self.valid_to:
            date_range += f' - {self.valid_to.strftime('%B %-d')}'

        return f'{full_name} ({date_range})'

