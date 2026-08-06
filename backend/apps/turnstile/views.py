from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.attractions.models import Attraction
from apps.tickets.models import Ticket
from apps.turnstile.services import (
    GuestAccessError,
    RideClosedError,
    TicketScanError,
    check_attraction_status,
    check_guest_requirements,
    check_no_recent_scan,
    check_ticket_valid_today,
)

from .models import ScanLog
from .serializers import ScanTicketSerializer


class ScanTicketView(APIView):
    def post(self, request):
        serializer = ScanTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        attraction = get_object_or_404(Attraction, pk=serializer.validated_data['attraction_id'])
        ticket = get_object_or_404(Ticket, pk=serializer.validated_data['ticket_id'])
        
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
            
            return Response({"error": err.message}, status=status.HTTP_409_CONFLICT)

        ScanLog.objects.create(
            ticket=ticket,
            attraction=attraction,
            success=True
        )

        return Response(
            {"success": f"Enjoy your ride on {attraction.name}!"},
            status=status.HTTP_200_OK,
        )
