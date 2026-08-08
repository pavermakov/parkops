from datetime import datetime, timedelta

import pytest
from django.utils import timezone

from apps.tickets.models import Ticket

from ..exceptions import TicketScanError
from ..services import check_ticket_valid_today


def test_single_day_ticket_purchased_today():
    purchased_at = timezone.now()

    ticket = Ticket(
        purchased_at=purchased_at,
        valid_from=purchased_at.date(),
        valid_to = None
    )

    check_ticket_valid_today(ticket)


def test_single_ticket_purchased_for_tomorrow():
    purchased_at = datetime(2026, 8, 6, tzinfo=timezone.get_current_timezone())
    valid_from = (timezone.now() + timedelta(days=1)).date()

    ticket = Ticket(
        purchased_at=purchased_at,
        valid_from=valid_from,
        valid_to=None
    )

    with pytest.raises(TicketScanError, match=TicketScanError.WRONG_TICKET_DATE_MESSAGE):
        check_ticket_valid_today(ticket)


def test_multiday_ticket_for_today():
    purchased_at = datetime(2026, 8, 1, tzinfo=timezone.get_current_timezone())
    valid_from = (timezone.now() - timedelta(days=1)).date()
    valid_to = (timezone.now() + timedelta(days=1)).date()

    ticket = Ticket(
        purchased_at=purchased_at,
        valid_from=valid_from,
        valid_to=valid_to
    )

    check_ticket_valid_today(ticket)


def test_multiday_ticket_for_future():
    purchased_at = datetime(2026, 8, 1, tzinfo=timezone.get_current_timezone())
    valid_from = (timezone.now() + timedelta(days=1)).date()
    valid_to = (timezone.now() + timedelta(days=2)).date()

    ticket = Ticket(
        purchased_at=purchased_at,
        valid_from=valid_from,
        valid_to=valid_to
    )

    with pytest.raises(TicketScanError, match=TicketScanError.WRONG_TICKET_DATE_MESSAGE):
        check_ticket_valid_today(ticket)

