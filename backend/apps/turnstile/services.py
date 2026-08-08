from datetime import timedelta

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

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


def generate_riders_count_report():
    past_hour_scans = ScanLog.objects.filter(scanned_at__gte=timezone.now() - timedelta(hours=1))

    totals = past_hour_scans.aggregate(
        total_scans=Count('id'),
        successful_scans=Count('id', filter=Q(success=True)),
        failed_scans=Count('id', filter=Q(success=False))
    )

    # TODO: how does values work?
    # TODO: What is Q?
    per_attraction = past_hour_scans.values('attraction_id', 'attraction__name').annotate(
        total_scans=Count('id'),
        successful_scans=Count('id', filter=Q(success=True)),
        failed_scans=Count('id', filter=Q(success=False)),
    )

    attractions = [
        {
            'id': row['attraction_id'],
            'name': row['attraction__name'],
            'total_scans': row['total_scans'],
            'successful_scans': row['successful_scans'],
            'failed_scans': row['failed_scans'],
        }
        for row in per_attraction
    ]

    return { **totals, 'attractions': attractions }


type ScanResult = tuple[Attraction, None] | tuple[None, Exception]

def scan_ticket_at_attraction(data) -> ScanResult:
    attraction = get_object_or_404(Attraction, pk=data.get('attraction_id'))
    ticket = get_object_or_404(Ticket, pk=data.get('ticket_id'))

    try:
        check_attraction_status(attraction)
        check_ticket_valid_today(ticket)
        check_no_recent_scan(ticket, attraction)
        check_guest_requirements(ticket.guest, attraction)
    except (TicketScanError, RideClosedError, GuestAccessError) as err:
        ScanLog.objects.create(
            ticket=ticket,
            attraction=attraction,
            success=False,
            message=err.message
        )

        return None, err

    ScanLog.objects.create(
        ticket=ticket,
        attraction=attraction,
        success=True
    )

    return attraction, None