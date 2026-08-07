from datetime import timedelta

from django.utils import timezone

from apps.attractions.models import Attraction
from apps.guests.models import Guest
from apps.tickets.models import Ticket

from .exceptions import GuestAccessError, RideClosedError, TicketScanError
from .models import ScanLog

MINUTES_TILL_NEXT_SCAN = 5


def check_attraction_status(attraction: Attraction):
    match attraction.operation_status:
        case Attraction.OperationStatus.RUNNING:
            return

        case Attraction.OperationStatus.DOWN_MECHANICAL:
            raise RideClosedError(RideClosedError.DOWN_MECHANICAL_ERROR_MESSAGE)

        case Attraction.OperationStatus.DOWN_WEATHER:
            raise RideClosedError(RideClosedError.DOWN_WEATHER_ERROR_MESSAGE)

        case Attraction.OperationStatus.CLOSED:
            raise RideClosedError(RideClosedError.CLOSED_FOR_TODAY_ERROR_MESSAGE)

        case _:
            raise RideClosedError(RideClosedError.DEFAULT_ERROR_MESSAGE)


def check_ticket_valid_today(ticket: Ticket):
    if ticket.valid_to is None:
        is_valid = ticket.valid_from <= timezone.now().date()
    else:
        is_valid = ticket.valid_from <= timezone.now().date() <= ticket.valid_to
        
    if not is_valid:
        raise TicketScanError(message=TicketScanError.WRONG_TICKET_DATE_MESSAGE)


def check_no_recent_scan(ticket: Ticket, attraction: Attraction):
    if (
        ScanLog.objects.filter(
            ticket=ticket,
            attraction=attraction,
            success=True,
            scanned_at__gte=timezone.now() - timedelta(minutes=MINUTES_TILL_NEXT_SCAN)
        ).exists()
    ):
        raise TicketScanError(message=TicketScanError.RECENTLY_SCANNED_MESSAGE)


def check_guest_requirements(guest: Guest, attraction: Attraction):
    if not attraction.min_height_cm:
        return

    if guest.height_cm < attraction.min_height_cm:
        raise GuestAccessError(GuestAccessError.MIN_HEIGHT_ERROR_MESSAGE)