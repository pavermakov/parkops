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


class TicketScanError(Exception):
    DEFAULT_ERROR_MESSAGE = 'Failed to scan the ticket, please try again'
    WRONG_TICKET_DATE_MESSAGE = 'The ticket date is invalid'
    RECENTLY_SCANNED_MESSAGE = 'You have already scanned your ticket. Try again later'

    def __init__(self, message: str = DEFAULT_ERROR_MESSAGE):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f'[TicketScanError] {self.message}'


class GuestAccessError(Exception):
    DEFAULT_ERROR_MESSAGE = 'Sorry, you are not allowed to ride this attraction'
    MIN_HEIGHT_ERROR_MESSAGE = 'Sorry, you are not tall enough for this ride'

    def __init__(self, message: str = DEFAULT_ERROR_MESSAGE):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f'[GuestAccessError] {self.message}'