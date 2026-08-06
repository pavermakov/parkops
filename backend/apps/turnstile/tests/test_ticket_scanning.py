from datetime import timedelta

import pytest
from django.utils import timezone

from apps.attractions.models import Attraction
from apps.tickets.models import Ticket
from apps.guests.models import Guest

from ..exceptions import TicketScanError
from ..models import ScanLog
from ..services import MINUTES_TILL_NEXT_SCAN, check_no_recent_scan


@pytest.mark.django_db
def test_passes_when_no_recent_scan():
    guest = Guest.objects.create(first_name="Alice", last_name="Smith", height_cm=150)
    ticket = Ticket.objects.create(guest=guest, valid_from=timezone.now())
    attraction = Attraction.objects.create(name="Coaster", operation_status="running")
    check_no_recent_scan(ticket, attraction)


@pytest.mark.django_db
def test_raises_when_recently_scanned():
    guest = Guest.objects.create(first_name="Alice", last_name="Smith", height_cm=150)
    ticket = Ticket.objects.create(guest=guest, valid_from=timezone.now())
    attraction = Attraction.objects.create(name="Coaster", operation_status=Attraction.OperationStatus.RUNNING)
    ScanLog.objects.create(ticket=ticket, attraction=attraction, success=True)

    with pytest.raises(TicketScanError, match=TicketScanError.RECENTLY_SCANNED_MESSAGE):
        check_no_recent_scan(ticket, attraction)


@pytest.mark.django_db
def test_passes_when_scanned_after_interval():
    guest = Guest.objects.create(first_name="Alice", last_name="Smith", height_cm=150)
    ticket = Ticket.objects.create(guest=guest, valid_from=timezone.now())
    attraction = Attraction.objects.create(name="Coaster", operation_status=Attraction.OperationStatus.RUNNING)

    log = ScanLog.objects.create(ticket=ticket, attraction=attraction, success=True)
    log.scanned_at = timezone.now() - timedelta(minutes=MINUTES_TILL_NEXT_SCAN)
    log.save()

    check_no_recent_scan(ticket, attraction)


@pytest.mark.django_db
def test_passes_when_last_scan_failed():
    guest = Guest.objects.create(first_name="Alice", last_name="Smith", height_cm=150)
    ticket = Ticket.objects.create(guest=guest, valid_from=timezone.now())
    attraction = Attraction.objects.create(name="Coaster", operation_status=Attraction.OperationStatus.RUNNING)
    ScanLog.objects.create(ticket=ticket, attraction=attraction, success=False)

    check_no_recent_scan(ticket, attraction)
