from django.utils import timezone

from apps.attractions.models import Attraction
from apps.tickets.models import Ticket

from .exceptions import RideClosedError, TicketScanError


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
        is_valid = ticket.valid_from.date() <= timezone.now().date()
    else:
        is_valid = ticket.valid_from.date() <= timezone.now().date() <= ticket.valid_to.date()
        
    if not is_valid:
        raise TicketScanError(message=TicketScanError.WRONG_TICKET_DATE_MESSAGE)


