from apps.attractions.models import Attraction


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