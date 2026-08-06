import pytest
from django.utils import timezone

from apps.guests.models import Guest
from apps.tickets.models import Ticket


@pytest.fixture
def make_ticket():
    def _make_ticket(**overrides):
        guest = overrides.pop('guest', None) or Guest.objects.create(
            first_name="Alice", last_name="Smith", height_cm=150
        )

        defaults = {
            'guest': guest,
            'valid_from': timezone.now(),
            'price': 19.99,
        }

        defaults.update(overrides)
        return Ticket.objects.create(**defaults)

    return _make_ticket