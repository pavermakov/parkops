import pytest
from django.utils import timezone

from apps.guests.models import Guest

from ..services import DAILY_TICKET_PRICE, create_new_ticket


@pytest.mark.django_db
def test_passes_when_new_guest_buys_ticket():
    data = {
        'first_name': 'John',
        'last_name': 'Snow',
        'height_cm': 155,
        'valid_from': timezone.now().date(),
        'valid_to': timezone.now().date(),
        'price': DAILY_TICKET_PRICE
    }

    new_ticket = create_new_ticket(data)
    assert new_ticket.guest.first_name == data.get('first_name')
    assert new_ticket.guest.last_name == data.get('last_name')
    assert new_ticket.guest.height_cm == data.get('height_cm')
    assert new_ticket.valid_from == data.get('valid_from')
    assert new_ticket.valid_to == data.get('valid_to')
    assert new_ticket.price == data.get('price')


@pytest.mark.django_db
def test_passes_when_existing_guest_buys_ticket():
    guest = Guest.objects.create(
        first_name='John',
        last_name='Snow',
        height_cm=155
    )

    data = {
        'guest': guest,
        'valid_from': timezone.now().date(),
        'valid_to': timezone.now().date(),
        'price': DAILY_TICKET_PRICE
    }

    new_ticket = create_new_ticket(data)
    assert new_ticket.guest is guest
    assert new_ticket.valid_from == data.get('valid_from')
    assert new_ticket.valid_to == data.get('valid_to')
    assert new_ticket.price == data.get('price')

