import pytest

from apps.attractions.models import Attraction

from ..services import RideClosedError, check_attraction_status


def test_attraction_status_running():
    attraction = Attraction(operation_status=Attraction.OperationStatus.RUNNING)
    check_attraction_status(attraction)


def test_attraction_status_down_mechanical():
    attraction = Attraction(operation_status=Attraction.OperationStatus.DOWN_MECHANICAL)

    with pytest.raises(RideClosedError, match=RideClosedError.DOWN_MECHANICAL_ERROR_MESSAGE):
        check_attraction_status(attraction)

    
def test_attraction_status_down_weather():
    attraction = Attraction(operation_status=Attraction.OperationStatus.DOWN_WEATHER)

    with pytest.raises(RideClosedError, match=RideClosedError.DOWN_WEATHER_ERROR_MESSAGE):
        check_attraction_status(attraction)


def test_attraction_status_closed():
    attraction = Attraction(operation_status=Attraction.OperationStatus.CLOSED)
    with pytest.raises(RideClosedError, match=RideClosedError.CLOSED_FOR_TODAY_ERROR_MESSAGE):
        check_attraction_status(attraction)


def test_attraction_status_unknown():
    attraction = Attraction(operation_status="unknown")
    
    with pytest.raises(RideClosedError, match=RideClosedError.DEFAULT_ERROR_MESSAGE):
        check_attraction_status(attraction)

