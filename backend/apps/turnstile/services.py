from django.utils import timezone

from apps.attractions.models import Attraction
from apps.tickets.models import Ticket


class RideClosedError(Exception):
    DEFAULT_ERROR_MESSAGE = "Sorry, the ride is closed at this moment"
    DOWN_MECHANICAL_ERROR_MESSAGE = "Sorry, the ride broke down"
    DOWN_WEATHER_ERROR_MESSAGE = "Sorry, the ride is down for poor weather conditions"
    CLOSED_FOR_TODAY_ERROR_MESSAGE = "Sorry, the ride is closed for today"

    def __init__(self, message: str = DEFAULT_ERROR_MESSAGE):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f"[RideClosedError] {self.message}"

def check_attraction_status(attraction: Attraction) -> bool:
    match attraction.operation_status:
        case Attraction.OperationStatus.RUNNING:
            return True

        case Attraction.OperationStatus.DOWN_MECHANICAL:
            raise RideClosedError(RideClosedError.DOWN_MECHANICAL_ERROR_MESSAGE)

        case Attraction.OperationStatus.DOWN_WEATHER:
            raise RideClosedError(RideClosedError.DOWN_WEATHER_ERROR_MESSAGE)

        case Attraction.OperationStatus.CLOSED:
            raise RideClosedError(RideClosedError.CLOSED_FOR_TODAY_ERROR_MESSAGE)

        case _:
            raise RideClosedError(RideClosedError.DEFAULT_ERROR_MESSAGE)


class TicketScanError(Exception):
    DEFAULT_ERROR_MESSAGE = 'Failed to scan the ticket, please try again'
    WRONG_TICKET_DATE_MESSAGE = 'The ticket date is invalid'

    def __init__(self, message: str = DEFAULT_ERROR_MESSAGE):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f'[TicketScanError] {self.message}'


def check_ticked_purchased_today(ticket: Ticket):
    if ticket.purchased_at.date() != timezone.now().date():
        raise TicketScanError(message=TicketScanError.WRONG_TICKET_DATE_MESSAGE)