from decimal import Decimal
from typing import Any

from django.utils import timezone

from apps.guests.models import Guest
from apps.tickets.models import Ticket

DAILY_TICKET_PRICE = Decimal('59.99')


def calculate_ticket_price(data: dict[str, Any]) -> Decimal:
    date_from = data.get('date_from')
    date_to = data.get('date_to', timezone.now().date())
    discount = data.get('discount')

    duration_days = max((date_to - date_from).days, 1)
    price = DAILY_TICKET_PRICE * duration_days

    if discount:
        price *= (1 - Decimal(discount.discount_percent) / 100)


    return price


def create_new_ticket(data) -> Ticket:
    guest = data.get('guest')

    # TODO: good place to wrap into transaction?
    if not guest:
        guest = Guest.objects.create(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            height_cm=data.get('height_cm'),
        )

    return Ticket.objects.create(
        guest=guest,
        valid_from=data.get('valid_from'),
        valid_to=data.get('valid_to'),
        price=data.get('price')
    )