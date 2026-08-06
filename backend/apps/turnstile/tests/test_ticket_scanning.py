from datetime import timedelta

import pytest
from django.utils import timezone

from apps.attractions.models import Attraction
from apps.tickets.models import Ticket

from ..exceptions import TicketScanError
from ..models import ScanLog
from ..services import MINUTES_TILL_NEXT_SCAN, check_no_recent_scan


@pytest.mark.django_db
def test_passes_when_no_recent_scan():
    ticket = Ticket.objects.create(valid_from=timezone.now())
    attraction = Attraction.objects.create(name="Coaster", operation_status="running")
    check_no_recent_scan(ticket, attraction)


@pytest.mark.django_db
def test_raises_when_recently_scanned():
    ticket = Ticket.objects.create(valid_from=timezone.now())
    attraction = Attraction.objects.create(name="Coaster", operation_status=Attraction.OperationStatus.RUNNING)
    ScanLog.objects.create(ticket=ticket, attraction=attraction, success=True)

    with pytest.raises(TicketScanError, match=TicketScanError.RECENTLY_SCANNED_MESSAGE):
        check_no_recent_scan(ticket, attraction)


@pytest.mark.django_db
def test_passes_when_scanned_after_interval():
    ticket = Ticket.objects.create(valid_from=timezone.now())
    attraction = Attraction.objects.create(name="Coaster", operation_status=Attraction.OperationStatus.RUNNING)

    log = ScanLog.objects.create(ticket=ticket, attraction=attraction, success=True)
    log.scanned_at = timezone.now() - timedelta(minutes=MINUTES_TILL_NEXT_SCAN)
    log.save()

    check_no_recent_scan(ticket, attraction)


@pytest.mark.django_db
def test_passes_when_last_scan_failed():
    ticket = Ticket.objects.create(valid_from=timezone.now())
    attraction = Attraction.objects.create(name="Coaster", operation_status=Attraction.OperationStatus.RUNNING)
    ScanLog.objects.create(ticket=ticket, attraction=attraction, success=False)

    check_no_recent_scan(ticket, attraction)
