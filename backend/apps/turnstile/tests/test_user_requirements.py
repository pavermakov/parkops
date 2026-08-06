import pytest

from apps.attractions.models import Attraction
from apps.guests.models import Guest

from ..services import check_guest_requirements
from ..exceptions import GuestAccessError


def test_pass_when_guest_is_tall_enough():
    guest = Guest(first_name="FN", last_name="LN", height_cm=185)
    attraction = Attraction(
        name="Ride",
        operation_status=Attraction.OperationStatus.RUNNING,
        min_height_cm=132
    )

    check_guest_requirements(guest, attraction)


def test_raises_when_guest_not_tall_enough():
    guest = Guest(first_name="FN", last_name="LN", height_cm=120)
    attraction = Attraction(
        name="Ride",
        operation_status=Attraction.OperationStatus.RUNNING,
        min_height_cm=132
    )

    with pytest.raises(GuestAccessError, match=GuestAccessError.MIN_HEIGHT_ERROR_MESSAGE):
        check_guest_requirements(guest, attraction)